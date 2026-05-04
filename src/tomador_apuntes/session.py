from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any
import json
import uuid


class SessionStatus(StrEnum):
    CREATED = "creada"
    RUNNING = "en_vivo"
    PAUSED = "pausada"
    STOPPED = "detenida"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def format_dt(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


@dataclass
class SessionEvent:
    type: str
    timestamp: datetime
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "timestamp": format_dt(self.timestamp),
            "detail": self.detail,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionEvent":
        timestamp = parse_dt(data.get("timestamp")) or utc_now()
        return cls(
            type=str(data.get("type", "")),
            timestamp=timestamp,
            detail=str(data.get("detail", "")),
        )


@dataclass
class Session:
    id: str
    title: str
    status: SessionStatus
    created_at: datetime
    started_at: datetime | None = None
    stopped_at: datetime | None = None
    accumulated_seconds: float = 0
    last_started_at: datetime | None = None
    presentation_name: str | None = None
    current_slide: int | None = None
    transcription_state: str = "pendiente"
    events: list[SessionEvent] = field(default_factory=list)

    @classmethod
    def create(cls, title: str | None = None, now: datetime | None = None) -> "Session":
        timestamp = now or utc_now()
        clean_title = (title or "Sesion sin titulo").strip() or "Sesion sin titulo"
        session = cls(
            id=str(uuid.uuid4()),
            title=clean_title,
            status=SessionStatus.CREATED,
            created_at=timestamp,
        )
        session.add_event("sesion_creada", timestamp, clean_title)
        return session

    def add_event(self, event_type: str, timestamp: datetime | None = None, detail: str = "") -> None:
        self.events.append(SessionEvent(event_type, timestamp or utc_now(), detail))

    def start(self, now: datetime | None = None) -> None:
        timestamp = now or utc_now()
        if self.status == SessionStatus.STOPPED:
            raise ValueError("No se puede iniciar una sesion detenida.")
        if self.status == SessionStatus.RUNNING:
            return
        if self.started_at is None:
            self.started_at = timestamp
        self.last_started_at = timestamp
        self.status = SessionStatus.RUNNING
        self.transcription_state = "lista_para_capturar"
        self.add_event("sesion_iniciada", timestamp)

    def pause(self, now: datetime | None = None) -> None:
        timestamp = now or utc_now()
        if self.status != SessionStatus.RUNNING:
            return
        self._close_running_interval(timestamp)
        self.status = SessionStatus.PAUSED
        self.transcription_state = "pausada"
        self.add_event("sesion_pausada", timestamp)

    def resume(self, now: datetime | None = None) -> None:
        timestamp = now or utc_now()
        if self.status != SessionStatus.PAUSED:
            return
        self.last_started_at = timestamp
        self.status = SessionStatus.RUNNING
        self.transcription_state = "lista_para_capturar"
        self.add_event("sesion_reanudada", timestamp)

    def stop(self, now: datetime | None = None) -> None:
        timestamp = now or utc_now()
        if self.status == SessionStatus.STOPPED:
            return
        if self.status == SessionStatus.RUNNING:
            self._close_running_interval(timestamp)
        self.status = SessionStatus.STOPPED
        self.stopped_at = timestamp
        self.last_started_at = None
        self.transcription_state = "detenida"
        self.add_event("sesion_detenida", timestamp)

    def elapsed_seconds(self, now: datetime | None = None) -> int:
        total = self.accumulated_seconds
        if self.status == SessionStatus.RUNNING and self.last_started_at is not None:
            total += ((now or utc_now()) - self.last_started_at).total_seconds()
        return max(0, int(total))

    def set_presentation(self, name: str | None, now: datetime | None = None) -> None:
        clean_name = (name or "").strip() or None
        self.presentation_name = clean_name
        self.current_slide = 1 if clean_name else None
        detail = clean_name or "sin presentacion"
        self.add_event("presentacion_actualizada", now or utc_now(), detail)

    def set_current_slide(self, slide: int, now: datetime | None = None) -> None:
        if slide < 1:
            raise ValueError("La diapositiva debe ser mayor o igual a 1.")
        self.current_slide = slide
        self.add_event("diapositiva_actualizada", now or utc_now(), str(slide))

    def to_dict(self, now: datetime | None = None) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "created_at": format_dt(self.created_at),
            "started_at": format_dt(self.started_at),
            "stopped_at": format_dt(self.stopped_at),
            "accumulated_seconds": self.accumulated_seconds,
            "last_started_at": format_dt(self.last_started_at),
            "elapsed_seconds": self.elapsed_seconds(now),
            "presentation_name": self.presentation_name,
            "current_slide": self.current_slide,
            "transcription_state": self.transcription_state,
            "events": [event.to_dict() for event in self.events],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Session":
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            status=SessionStatus(str(data["status"])),
            created_at=parse_dt(data.get("created_at")) or utc_now(),
            started_at=parse_dt(data.get("started_at")),
            stopped_at=parse_dt(data.get("stopped_at")),
            accumulated_seconds=float(data.get("accumulated_seconds", 0)),
            last_started_at=parse_dt(data.get("last_started_at")),
            presentation_name=data.get("presentation_name"),
            current_slide=data.get("current_slide"),
            transcription_state=str(data.get("transcription_state", "pendiente")),
            events=[SessionEvent.from_dict(item) for item in data.get("events", [])],
        )

    def _close_running_interval(self, timestamp: datetime) -> None:
        if self.last_started_at is None:
            return
        self.accumulated_seconds += max(0, (timestamp - self.last_started_at).total_seconds())
        self.last_started_at = None


class SessionStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def list_sessions(self) -> list[Session]:
        data = self._read()
        sessions = [Session.from_dict(item) for item in data.get("sessions", [])]
        return sorted(sessions, key=lambda item: item.created_at, reverse=True)

    def create_session(self, title: str | None = None) -> Session:
        session = Session.create(title)
        sessions = self.list_sessions()
        sessions.append(session)
        self._write_sessions(sessions)
        return session

    def get(self, session_id: str) -> Session:
        for session in self.list_sessions():
            if session.id == session_id:
                return session
        raise KeyError(f"Sesion no encontrada: {session_id}")

    def save(self, session: Session) -> None:
        sessions = self.list_sessions()
        replaced = False
        for index, existing in enumerate(sessions):
            if existing.id == session.id:
                sessions[index] = session
                replaced = True
                break
        if not replaced:
            sessions.append(session)
        self._write_sessions(sessions)

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"sessions": []}
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write_sessions(self, sessions: list[Session]) -> None:
        payload = {"sessions": [session.to_dict() for session in sessions]}
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
            file.write("\n")

