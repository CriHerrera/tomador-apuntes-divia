from __future__ import annotations

import re
import unicodedata

from typing import Any

from tomador_apuntes.session import Session


SAFE_DOWNLOAD_RE = re.compile(r"[^A-Za-z0-9._-]+")


def download_filename(title: str, suffix: str, extension: str = "txt") -> str:
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    clean_title = SAFE_DOWNLOAD_RE.sub("_", ascii_title.strip().lower()).strip("_")
    if not clean_title:
        clean_title = "sesion"
    clean_extension = SAFE_DOWNLOAD_RE.sub("", extension.strip().lower()) or "txt"
    return f"{clean_title}-{suffix}.{clean_extension}"


def transcript_as_json(session: Session) -> dict[str, Any]:
    return transcript_grouped_by_slide(session)


def transcript_grouped_by_slide(session: Session) -> dict[str, Any]:
    slide_texts = _presentation_text_by_page(session.presentation_text)
    grouped: dict[str, Any] = {}

    for page_number, page_text in slide_texts.items():
        grouped[f"diapositiva {page_number}"] = {
            "texto_plano": page_text,
            "interlocutores": [],
        }

    for segment in session.transcript_segments:
        key = f"diapositiva {segment.slide}" if segment.slide else "sin_presentacion"
        if key not in grouped:
            grouped[key] = {
                "texto_plano": slide_texts.get(segment.slide, session.presentation_text if segment.slide else ""),
                "interlocutores": [],
            }
        grouped[key]["interlocutores"].append(
            {
                "interlocutor": segment.speaker_name or "Sin presentador",
                "texto": segment.text,
                "inicio_segundos": segment.started_at_seconds,
                "fin_segundos": segment.ended_at_seconds,
            }
        )

    return grouped


def transcript_as_text(session: Session) -> str:
    lines = [
        f"Sesion: {session.title}",
        f"Estado: {session.status.value}",
        f"Presentacion: {session.presentation_name or 'Sin presentacion'}",
        "",
        "Transcripcion",
        "==============",
        "",
    ]

    if not session.transcript_segments:
        lines.append("No hay segmentos de transcripcion guardados.")
        return "\n".join(lines) + "\n"

    for segment in session.transcript_segments:
        slide = f"Diapositiva {segment.slide}" if segment.slide else "Sin presentacion"
        speaker = segment.speaker_name or "Sin presentador"
        lines.append(
            f"[{_format_seconds(segment.started_at_seconds)} - {_format_seconds(segment.ended_at_seconds)}] "
            f"{slide} | {speaker}"
        )
        lines.append(segment.text)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def presentation_text_as_text(session: Session) -> str:
    lines = [
        f"Sesion: {session.title}",
        f"Presentacion: {session.presentation_name or 'Sin presentacion'}",
        f"Estado de extraccion: {session.presentation_text_status}",
        "",
        "Texto plano de presentacion",
        "============================",
        "",
    ]
    lines.append(session.presentation_text or "No hay texto de presentacion extraido.")
    return "\n".join(lines).rstrip() + "\n"


def _format_seconds(total_seconds: float) -> str:
    seconds = max(0, int(total_seconds))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remainder = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remainder:02d}"


def _presentation_text_by_page(text: str) -> dict[int, str]:
    pages: dict[int, list[str]] = {}
    current_page: int | None = None

    for line in text.splitlines():
        match = re.fullmatch(r"\[Pagina (\d+)\]", line.strip())
        if match:
            current_page = int(match.group(1))
            pages.setdefault(current_page, [])
            continue
        if current_page is not None:
            pages[current_page].append(line)

    return {page: "\n".join(lines).strip() for page, lines in pages.items()}
