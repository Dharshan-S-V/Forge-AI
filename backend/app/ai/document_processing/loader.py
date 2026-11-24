"""
ForgeAI Document Loader.

Extracts plain text from various file formats (PDF, DOCX, TXT, XLSX).
"""

import io
from typing import BinaryIO

import docx
import fitz  # PyMuPDF
import openpyxl

from app.core.logging import get_logger

logger = get_logger(__name__)


class DocumentLoader:
    """Extracts text from supported file types."""

    @classmethod
    def load(cls, file_bytes: bytes, file_type: str) -> str:
        """Extract text from file bytes based on file type.

        Args:
            file_bytes: Raw bytes of the file.
            file_type: Extension (pdf, docx, txt, xlsx).

        Returns:
            Extracted plain text.
        """
        logger.info(f"Extracting text from {file_type} document")
        
        file_stream = io.BytesIO(file_bytes)

        if file_type == "pdf":
            return cls._load_pdf(file_bytes)
        elif file_type == "docx":
            return cls._load_docx(file_stream)
        elif file_type == "xlsx":
            return cls._load_xlsx(file_stream)
        elif file_type == "txt":
            return cls._load_txt(file_bytes)
        else:
            raise ValueError(f"Unsupported file type for extraction: {file_type}")

    @staticmethod
    def _load_pdf(file_bytes: bytes) -> str:
        """Extract text from a PDF file using PyMuPDF."""
        text = []
        try:
            # Open the PDF from memory
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                if page_text.strip():
                    text.append(page_text)
            return "\n\n".join(text)
        except Exception as e:
            logger.error("Failed to extract text from PDF", error=str(e))
            raise ValueError("Failed to read PDF file") from e

    @staticmethod
    def _load_docx(file_stream: BinaryIO) -> str:
        """Extract text from a DOCX file."""
        text = []
        try:
            doc = docx.Document(file_stream)
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text)
            return "\n".join(text)
        except Exception as e:
            logger.error("Failed to extract text from DOCX", error=str(e))
            raise ValueError("Failed to read DOCX file") from e

    @staticmethod
    def _load_xlsx(file_stream: BinaryIO) -> str:
        """Extract text from an XLSX file."""
        text = []
        try:
            wb = openpyxl.load_workbook(file_stream, data_only=True)
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                text.append(f"--- Sheet: {sheet_name} ---")
                for row in sheet.iter_rows(values_only=True):
                    # Filter out None values and convert to strings
                    row_values = [str(cell).strip() for cell in row if cell is not None and str(cell).strip()]
                    if row_values:
                        text.append(" | ".join(row_values))
                text.append("\n")
            return "\n".join(text)
        except Exception as e:
            logger.error("Failed to extract text from XLSX", error=str(e))
            raise ValueError("Failed to read XLSX file") from e

    @staticmethod
    def _load_txt(file_bytes: bytes) -> str:
        """Extract text from a TXT file."""
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1 if utf-8 fails
                return file_bytes.decode("latin-1")
            except Exception as e:
                logger.error("Failed to extract text from TXT", error=str(e))
                raise ValueError("Failed to read TXT file") from e
