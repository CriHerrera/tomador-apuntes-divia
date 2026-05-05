from __future__ import annotations

from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import mimetypes

from tomador_apuntes.export import (
    download_filename,
    presentation_text_as_text,
    transcript_as_json,
    transcript_as_text,
)
from tomador_apuntes.presentation import parse_multipart_file, save_and_extract_pdf
from tomador_apuntes.session import SessionStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = Path(__file__).resolve().parent / "static"
DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = PROJECT_ROOT / "uploads"
SESSION_STORE_PATH = DATA_DIR / "sessions.json"


class AppHandler(SimpleHTTPRequestHandler):
    store = SessionStore(SESSION_STORE_PATH)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_static("index.html")
            return
        if parsed.path == "/api/sessions":
            sessions = [session.to_dict() for session in self.store.list_sessions()]
            self._send_json({"sessions": sessions})
            return
        if parsed.path.startswith("/api/sessions/") and parsed.path.endswith("/transcript.txt"):
            self._handle_json_text_download(parsed.path, "transcript")
            return
        if parsed.path.startswith("/api/sessions/") and parsed.path.endswith("/transcript.json"):
            self._handle_json_download(parsed.path, "transcript")
            return
        if parsed.path.startswith("/api/sessions/") and parsed.path.endswith("/presentation-text.txt"):
            self._handle_text_download(parsed.path, "presentation")
            return
        if parsed.path.startswith("/static/"):
            self._send_static(parsed.path.removeprefix("/static/"))
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/sessions/") and parsed.path.endswith("/presentation-file"):
            self._handle_presentation_upload(parsed.path)
            return

        try:
            payload = self._read_json()
        except json.JSONDecodeError:
            self._send_json({"error": "JSON invalido"}, HTTPStatus.BAD_REQUEST)
            return

        if parsed.path == "/api/sessions":
            session = self.store.create_session(payload.get("title"))
            self._send_json({"session": session.to_dict()}, HTTPStatus.CREATED)
            return
        if parsed.path.startswith("/api/sessions/"):
            self._handle_session_action(parsed.path, payload)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")

    def _handle_session_action(self, path: str, payload: dict) -> None:
        parts = path.strip("/").split("/")
        if len(parts) != 4 or parts[0] != "api" or parts[1] != "sessions":
            self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")
            return

        session_id = parts[2]
        action = parts[3]

        try:
            session = self.store.get(session_id)
            if action == "start":
                session.start()
            elif action == "pause":
                session.pause()
            elif action == "resume":
                session.resume()
            elif action == "stop":
                session.stop()
            elif action == "presentation":
                session.set_presentation(payload.get("presentation_name"))
            elif action == "slide":
                session.set_current_slide(int(payload.get("slide", 1)))
            elif action == "speakers":
                session.add_speaker(str(payload.get("name", "")))
            elif action == "active-speaker":
                session.set_active_speaker(payload.get("name"))
            elif action == "transcript":
                session.add_transcript_segment(
                    text=str(payload.get("text", "")),
                    started_at_seconds=float(payload.get("started_at_seconds", 0)),
                    ended_at_seconds=float(payload.get("ended_at_seconds", 0)),
                )
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "Accion no encontrada")
                return
            self.store.save(session)
        except KeyError:
            self.send_error(HTTPStatus.NOT_FOUND, "Sesion no encontrada")
            return
        except (TypeError, ValueError) as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return

        self._send_json({"session": session.to_dict()})

    def _handle_text_download(self, path: str, export_type: str) -> None:
        parts = path.strip("/").split("/")
        if len(parts) != 4 or parts[0] != "api" or parts[1] != "sessions":
            self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")
            return

        try:
            session = self.store.get(parts[2])
        except KeyError:
            self.send_error(HTTPStatus.NOT_FOUND, "Sesion no encontrada")
            return

        if export_type == "transcript":
            filename = download_filename(session.title, "transcripcion")
            body = transcript_as_text(session)
        else:
            filename = download_filename(session.title, "texto-presentacion")
            body = presentation_text_as_text(session)
        self._send_text_download(body, filename)

    def _handle_json_text_download(self, path: str, export_type: str) -> None:
        parts = path.strip("/").split("/")
        if len(parts) != 4 or parts[0] != "api" or parts[1] != "sessions":
            self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")
            return

        try:
            session = self.store.get(parts[2])
        except KeyError:
            self.send_error(HTTPStatus.NOT_FOUND, "Sesion no encontrada")
            return

        if export_type != "transcript":
            self.send_error(HTTPStatus.NOT_FOUND, "Exportacion no encontrada")
            return

        filename = download_filename(session.title, "transcripcion-json")
        body = json.dumps(transcript_as_json(session), ensure_ascii=False, indent=2)
        self._send_text_download(body + "\n", filename)

    def _handle_json_download(self, path: str, export_type: str) -> None:
        parts = path.strip("/").split("/")
        if len(parts) != 4 or parts[0] != "api" or parts[1] != "sessions":
            self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")
            return

        try:
            session = self.store.get(parts[2])
        except KeyError:
            self.send_error(HTTPStatus.NOT_FOUND, "Sesion no encontrada")
            return

        if export_type != "transcript":
            self.send_error(HTTPStatus.NOT_FOUND, "Exportacion no encontrada")
            return

        filename = download_filename(session.title, "transcripcion", "json")
        self._send_json_download(transcript_as_json(session), filename)

    def _handle_presentation_upload(self, path: str) -> None:
        parts = path.strip("/").split("/")
        if len(parts) != 4 or parts[0] != "api" or parts[1] != "sessions":
            self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")
            return
        content_type = self.headers.get("Content-Type", "")
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(content_length)

        try:
            session = self.store.get(parts[2])
            upload = parse_multipart_file(content_type, body)
            extracted = save_and_extract_pdf(upload, UPLOAD_DIR / session.id)
            session.set_presentation_file(
                filename=extracted.filename,
                extracted_text=extracted.text,
                extraction_status=extracted.status,
            )
            self.store.save(session)
        except KeyError:
            self.send_error(HTTPStatus.NOT_FOUND, "Sesion no encontrada")
            return
        except ValueError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return

        self._send_json({"session": session.to_dict()})

    def _read_json(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length)
        return json.loads(raw.decode("utf-8"))

    def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text_download(self, content: str, filename: str) -> None:
        body = content.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json_download(self, payload: dict, filename: str) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, relative_path: str) -> None:
        target = (STATIC_DIR / relative_path).resolve()
        try:
            target.relative_to(STATIC_DIR.resolve())
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN, "Ruta invalida")
            return
        if not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Archivo no encontrado")
            return

        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def build_server(host: str, port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), AppHandler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor local de Tomador Apuntes Divia")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()

    server = build_server(args.host, args.port)
    print(f"Tomador Apuntes Divia disponible en http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
