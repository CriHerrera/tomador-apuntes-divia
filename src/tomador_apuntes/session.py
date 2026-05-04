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
class TranscriptSegment:
    id: str
    text: str
    started_at_seconds: float
    ended_at_seconds: float
    recorded_at: datetime
    slide: int | None = None
    speaker_name: str | None = None

    @classmethod
    def create(
        cls,
        text: str,
        started_at_seconds: float,
        ended_at_seconds: float,
        slide: int | None = None,
        speaker_name: str | None = None,
        recorded_at: datetime | None = None,
    ) -> "TranscriptSegment":
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("El segmento de transcripcion no puede estar vacio.")
        if ended_at_seconds < started_at_seconds:
            raise ValueError("El fin del segmento no puede ser anterior al inicio.")
        return cls(
            id=str(uuid.uuid4()),
            text=clean_text,
            started_at_seconds=max(0, started_at_seconds),
            ended_at_seconds=max(0, ended_at_seconds),
            recorded_at=recorded_at or utc_now(),
            slide=slide,
            speaker_name=(speaker_name or "").strip() or None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "started_at_seconds": self.started_at_seconds,
            "ended_at_seconds": self.ended_at_seconds,
            "recorded_at": format_dt(self.recorded_at),
            "slide": self.slide,
            "speaker_name": self.speaker_name,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TranscriptSegment":
        return cls(
            id=str(data["id"]),
            text=str(data["text"]),
            started_at_seconds=float(data.get("started_at_seconds", 0)),
            ended_at_seconds=float(data.get("ended_at_seconds", 0)),
            recorded_at=parse_dt(data.get("recorded_at")) or utc_now(),
            slide=data.get("slide"),
            speaker_name=data.get("speaker_name"),
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
    presentation_file: str | None = None
    presentation_text: str = ""
    presentation_text_status: str = "sin_presentacion"
    current_slide: int | None = None
    speakers: list[str] = field(default_factory=list)
    active_speaker: str | None = None
    transcription_state: str = "pendiente"
    events: list[SessionEvent] = field(default_factory=list)
    transcript_segments: list[TranscriptSegment] = field(default_factory=list)

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

    def set_presentation_file(
        self,
        filename: str,
        extracted_text: str,
        extraction_status: str,
        now: datetime | None = None,
    ) -> None:
        clean_name = filename.strip()
        if not clean_name:
            raise ValueError("El nombre del archivo de presentacion no puede estar vacio.")
        self.presentation_name = clean_name
        self.presentation_file = clean_name
        self.presentation_text = extracted_text
        self.presentation_text_status = extraction_status
        self.current_slide = 1
        self.add_event("presentacion_pdf_cargada", now or utc_now(), extraction_status)

    def set_current_slide(self, slide: int, now: datetime | None = None) -> None:
        if slide < 1:
            raise ValueError("La diapositiva debe ser mayor o igual a 1.")
        self.current_slide = slide
        self.add_event("diapositiva_actualizada", now or utc_now(), str(slide))

    def add_speaker(self, name: str, now: datetime | None = None) -> str:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("El nombre del presentador no puede estar vacio.")
        existing = {speaker.lower(): speaker for speaker in self.speakers}
        speaker = existing.get(clean_name.lower(), clean_name)
        if speaker not in self.speakers:
            self.speakers.append(speaker)
            self.add_event("presentador_agregado", now or utc_now(), speaker)
        self.active_speaker = speaker
        self.add_event("presentador_activo", now or utc_now(), speaker)
        return speaker

    def set_active_speaker(self, name: str | None, now: datetime | None = None) -> None:
        clean_name = (name or "").strip()
        if not clean_name:
            self.active_speaker = None
            self.add_event("presentador_activo", now or utc_now(), "sin presentador")
            return
        if clean_name not in self.speakers:
            self.speakers.append(clean_name)
        self.active_speaker = clean_name
        self.add_event("presentador_activo", now or utc_now(), clean_name)

    def add_transcript_segment(
        self,
        text: str,
        started_at_seconds: float,
        ended_at_seconds: float,
        now: datetime | None = None,
    ) -> TranscriptSegment:
        segment = TranscriptSegment.create(
            text=text,
            started_at_seconds=started_at_seconds,
            ended_at_seconds=ended_at_seconds,
            slide=self.current_slide,
            speaker_name=self.active_speaker,
            recorded_at=now or utc_now(),
        )
        self.transcript_segments.append(segment)
        self.transcription_state = "capturando"
        detail = f"diapositiva {segment.slide}" if segment.slide else "sin presentacion"
        self.add_event("transcripcion_guardada", segment.recorded_at, detail)
        return segment

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
            "presentation_file": self.presentation_file,
            "presentation_text": self.presentation_text,
            "presentation_text_status": self.presentation_text_status,
            "current_slide": self.current_slide,
            "speakers": self.speakers,
            "active_speaker": self.active_speaker,
            "transcription_state": self.transcription_state,
            "events": [event.to_dict() for event in self.events],
            "transcript_segments": [segment.to_dict() for segment in self.transcript_segments],
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
            presentation_file=data.get("presentation_file"),
            presentation_text=str(data.get("presentation_text", "")),
            presentation_text_status=str(data.get("presentation_text_status", "sin_presentacion")),
            current_slide=data.get("current_slide"),
            speakers=[str(item) for item in data.get("speakers", [])],
            active_speaker=data.get("active_speaker"),
            transcription_state=str(data.get("transcription_state", "pendiente")),
            events=[SessionEvent.from_dict(item) for item in data.get("events", [])],
            transcript_segments=[
                TranscriptSegment.from_dict(item) for item in data.get("transcript_segments", [])
            ],
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
