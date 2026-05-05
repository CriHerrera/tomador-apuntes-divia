import unittest

from tomador_apuntes.export import (
    download_filename,
    presentation_text_as_text,
    transcript_as_json,
    transcript_as_text,
)
from tomador_apuntes.session import Session


class ExportTest(unittest.TestCase):
    def test_transcript_as_text_includes_segments_with_context(self) -> None:
        session = Session.create("Clase final")
        session.set_presentation("clase.pdf")
        session.set_current_slide(2)
        session.add_speaker("Marcela")
        session.add_transcript_segment("Punto importante", 4, 9)

        text = transcript_as_text(session)

        self.assertIn("Sesion: Clase final", text)
        self.assertIn("Presentacion: clase.pdf", text)
        self.assertIn("[00:00:04 - 00:00:09] Diapositiva 2 | Marcela", text)
        self.assertIn("Punto importante", text)

    def test_transcript_as_text_handles_empty_transcript(self) -> None:
        session = Session.create("Reunion")

        text = transcript_as_text(session)

        self.assertIn("No hay segmentos de transcripcion guardados.", text)

    def test_transcript_as_json_includes_slide_speaker_and_slide_text(self) -> None:
        session = Session.create("Clase final")
        session.set_presentation_file(
            "clase.pdf",
            "[Pagina 1]\nContexto inicial\n\n[Pagina 2]\nTexto de la diapositiva dos",
            "texto_extraido",
        )
        session.set_current_slide(2)
        session.add_speaker("Marcela")
        session.add_transcript_segment("Esto dice la presentadora", 4, 9)

        payload = transcript_as_json(session)

        self.assertEqual(payload["diapositiva 1"]["texto_plano"], "Contexto inicial")
        self.assertEqual(payload["diapositiva 1"]["interlocutores"], [])
        self.assertEqual(payload["diapositiva 2"]["texto_plano"], "Texto de la diapositiva dos")
        self.assertEqual(payload["diapositiva 2"]["interlocutores"][0]["interlocutor"], "Marcela")
        self.assertEqual(payload["diapositiva 2"]["interlocutores"][0]["texto"], "Esto dice la presentadora")

    def test_presentation_text_as_text_exports_extracted_text(self) -> None:
        session = Session.create("Clase")
        session.set_presentation_file("clase.pdf", "[Pagina 1]\nContenido", "texto_extraido")

        text = presentation_text_as_text(session)

        self.assertIn("Presentacion: clase.pdf", text)
        self.assertIn("Estado de extraccion: texto_extraido", text)
        self.assertIn("[Pagina 1]\nContenido", text)

    def test_download_filename_is_safe(self) -> None:
        self.assertEqual(
            download_filename("Reunion / Final", "transcripcion"),
            "reunion_final-transcripcion.txt",
        )
        self.assertEqual(
            download_filename("Reunion / Final", "transcripcion", "json"),
            "reunion_final-transcripcion.json",
        )


if __name__ == "__main__":
    unittest.main()
