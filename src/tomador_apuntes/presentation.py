from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass
class UploadedFile:
    filename: str
    content: bytes


@dataclass
class ExtractedPresentation:
    filename: str
    path: Path
    text: str
    status: str


def safe_filename(filename: str) -> str:
    name = Path(filename).name.strip() or "presentacion.pdf"
    return SAFE_FILENAME_RE.sub("_", name)


def parse_multipart_file(content_type: str, body: bytes, field_name: str = "file") -> UploadedFile:
    boundary_token = "boundary="
    if boundary_token not in content_type:
        raise ValueError("La solicitud no incluye boundary multipart.")
    boundary = content_type.split(boundary_token, 1)[1].strip().strip('"')
    delimiter = f"--{boundary}".encode("utf-8")

    for part in body.split(delimiter):
        if not part or part in {b"--\r\n", b"--"}:
            continue
        header_blob, separator, content = part.partition(b"\r\n\r\n")
        if not separator:
            continue
        headers = header_blob.decode("utf-8", errors="replace")
        if f'name="{field_name}"' not in headers:
            continue
        filename = _header_value(headers, "filename") or "presentacion.pdf"
        clean_content = content.rstrip(b"\r\n")
        if clean_content.endswith(b"--"):
            clean_content = clean_content[:-2].rstrip(b"\r\n")
        return UploadedFile(filename=safe_filename(filename), content=clean_content)

    raise ValueError("No se encontro archivo en la solicitud.")


def save_and_extract_pdf(upload: UploadedFile, upload_dir: Path) -> ExtractedPresentation:
    if not upload.filename.lower().endswith(".pdf"):
        raise ValueError("Por ahora solo se soportan archivos PDF.")

    upload_dir.mkdir(parents=True, exist_ok=True)
    target = upload_dir / upload.filename
    target.write_bytes(upload.content)
    text, status = extract_pdf_text(target)
    return ExtractedPresentation(filename=upload.filename, path=target, text=text, status=status)


def extract_pdf_text(path: Path) -> tuple[str, str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return "", "pypdf_no_instalado"

    try:
        reader = PdfReader(str(path))
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            page_text = (page.extract_text() or "").strip()
            if page_text:
                pages.append(f"[Pagina {index}]\n{page_text}")
        if not pages:
            return "", "sin_texto_extraible"
        return "\n\n".join(pages), "texto_extraido"
    except Exception as exc:  # pypdf puede lanzar varias excepciones especificas.
        return "", f"error_extraccion: {exc}"


def _header_value(headers: str, key: str) -> str | None:
    match = re.search(rf'{key}="([^"]*)"', headers)
    if not match:
        return None
    return match.group(1)

