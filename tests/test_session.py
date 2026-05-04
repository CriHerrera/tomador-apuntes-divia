from datetime import datetime, timedelta, timezone
import unittest

from tomador_apuntes.session import Session, SessionStatus


class SessionTest(unittest.TestCase):
    def test_session_lifecycle_accumulates_elapsed_time(self) -> None:
        start = datetime(2026, 5, 4, 12, 0, tzinfo=timezone.utc)
        session = Session.create("Consejo semanal", now=start)

        session.start(start)
        self.assertEqual(session.status, SessionStatus.RUNNING)
        self.assertEqual(session.elapsed_seconds(start + timedelta(seconds=30)), 30)

        session.pause(start + timedelta(seconds=30))
        self.assertEqual(session.status, SessionStatus.PAUSED)
        self.assertEqual(session.elapsed_seconds(start + timedelta(seconds=90)), 30)

        session.resume(start + timedelta(seconds=90))
        session.stop(start + timedelta(seconds=120))

        self.assertEqual(session.status, SessionStatus.STOPPED)
        self.assertEqual(session.elapsed_seconds(start + timedelta(seconds=300)), 60)

    def test_session_can_work_without_presentation(self) -> None:
        session = Session.create("Reunion simple")
        session.start()

        self.assertIsNone(session.presentation_name)
        self.assertIsNone(session.current_slide)
        self.assertEqual(session.transcription_state, "lista_para_capturar")

    def test_session_tracks_presentation_and_slide_changes(self) -> None:
        session = Session.create("Clase con diapositivas")

        session.set_presentation("clase.pdf")
        session.set_current_slide(4)

        self.assertEqual(session.presentation_name, "clase.pdf")
        self.assertEqual(session.current_slide, 4)
        self.assertEqual(session.events[-1].type, "diapositiva_actualizada")
        self.assertEqual(session.events[-1].detail, "4")

    def test_session_rejects_invalid_slide_number(self) -> None:
        session = Session.create("Clase")

        with self.assertRaisesRegex(ValueError, "diapositiva"):
            session.set_current_slide(0)

    def test_session_stores_transcript_segments_with_current_slide(self) -> None:
        session = Session.create("Clase")
        session.set_presentation("clase.pdf")
        session.set_current_slide(2)
        session.add_speaker("Marcela")

        segment = session.add_transcript_segment(
            text="este es un punto importante",
            started_at_seconds=4,
            ended_at_seconds=9,
        )

        self.assertEqual(segment.slide, 2)
        self.assertEqual(segment.speaker_name, "Marcela")
        self.assertEqual(segment.text, "este es un punto importante")
        self.assertEqual(session.transcription_state, "capturando")
        self.assertEqual(session.transcript_segments[0].id, segment.id)

    def test_session_rejects_empty_transcript_segment(self) -> None:
        session = Session.create("Clase")

        with self.assertRaisesRegex(ValueError, "transcripcion"):
            session.add_transcript_segment("", 0, 1)

    def test_session_tracks_active_speaker(self) -> None:
        session = Session.create("Panel")

        session.add_speaker("Marcela")
        session.add_speaker("Cristian")
        session.set_active_speaker("Marcela")

        self.assertEqual(session.speakers, ["Marcela", "Cristian"])
        self.assertEqual(session.active_speaker, "Marcela")

    def test_session_stores_presentation_text(self) -> None:
        session = Session.create("Clase")

        session.set_presentation_file("clase.pdf", "[Pagina 1]\nTexto", "texto_extraido")

        self.assertEqual(session.presentation_name, "clase.pdf")
        self.assertEqual(session.presentation_file, "clase.pdf")
        self.assertEqual(session.presentation_text, "[Pagina 1]\nTexto")
        self.assertEqual(session.presentation_text_status, "texto_extraido")
        self.assertEqual(session.current_slide, 1)


if __name__ == "__main__":
    unittest.main()
