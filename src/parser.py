from PyPDF2 import PdfReader


class PDFParser:
    """
    Responsável por extrair texto de arquivos PDF.
    """

    @staticmethod
    def extract_text(pdf_file):

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()