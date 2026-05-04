import unittest

from tomador_apuntes.presentation import parse_multipart_file, safe_filename


class PresentationTest(unittest.TestCase):
    def test_safe_filename_removes_paths_and_unsafe_chars(self) -> None:
        self.assertEqual(safe_filename("../mi clase final.pdf"), "mi_clase_final.pdf")

    def test_parse_multipart_file_reads_pdf_payload(self) -> None:
        boundary = "----test-boundary"
        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="file"; filename="clase.pdf"\r\n'
            "Content-Type: application/pdf\r\n"
            "\r\n"
        ).encode("utf-8") + b"%PDF-1.4 fake" + f"\r\n--{boundary}--\r\n".encode("utf-8")

        upload = parse_multipart_file(f"multipart/form-data; boundary={boundary}", body)

        self.assertEqual(upload.filename, "clase.pdf")
        self.assertEqual(upload.content, b"%PDF-1.4 fake")


if __name__ == "__main__":
    unittest.main()

