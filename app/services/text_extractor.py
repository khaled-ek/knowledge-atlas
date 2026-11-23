from pathlib import Path

import pymupdf

from app.core.config import settings
from app.models.source import Source

class TextExtractor:

    @staticmethod
    def extract_text(source: Source) -> list[str]:

        file_path = settings.UPLOAD_DIRECTORY / source.storage_key

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Document not found: {source.storage_key}"
            )

        extracted_pages = []

        try:
            with pymupdf.open(file_path) as document:

                if document.is_encrypted:
                    raise ValueError(
                        "Encrypted PDF files are not supported."
                    )
                for page_number, page in enumerate(document, start=1):
                    text = page.get_text("text").strip()

                    if text:
                        extracted_pages.append({
                            "page_number": page_number,
                            "text": text
                        })

        except (pymupdf.FileDataError, RuntimeError) as error:
            raise ValueError(
                "The uploaded file could not be read as a valid PDF."
            ) from error

        if not extracted_pages:
            raise ValueError(
                "No extractable text was found in this PDF file."
            )

        return extracted_pages