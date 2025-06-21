"""PDF processor for extracting text from PDF documents."""

import asyncio
import tempfile
from pathlib import Path
from typing import Optional

import httpx
from pypdf import PdfReader
from pdfminer.high_level import extract_text

from ..utils.logger import LoggerMixin
from ..utils.helpers import clean_text


class PDFProcessor(LoggerMixin):
    """Processor for extracting text from PDF documents."""

    def __init__(self):
        """Initialize the PDF processor."""
        self.logger.info("Initialized PDF processor")

    async def extract_text_from_url(self, pdf_url: str) -> Optional[str]:
        """
        Extract text from a PDF at the given URL.

        Args:
            pdf_url: URL to the PDF file

        Returns:
            Extracted text or None if extraction fails
        """
        try:
            self.logger.info(f"Downloading PDF from: {pdf_url}")

            # Download the PDF asynchronously
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(pdf_url)
                response.raise_for_status()

            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name

            try:
                # Extract text from the temporary file
                text = await self.extract_text_from_file(temp_path)
                return text
            finally:
                # Clean up temporary file
                Path(temp_path).unlink(missing_ok=True)

        except Exception as e:
            self.logger.error(
                f"Error extracting text from PDF URL {pdf_url}: {e}")
            return None

    async def extract_text_from_file(self, file_path: str) -> Optional[str]:
        """
        Extract text from a local PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text or None if extraction fails
        """
        try:
            self.logger.info(f"Extracting text from PDF file: {file_path}")

            # Try pdfminer first (usually more accurate) - run in executor for async
            try:
                loop = asyncio.get_event_loop()
                text = await loop.run_in_executor(None, extract_text, file_path)
                if text and text.strip():
                    cleaned_text = clean_text(text)
                    self.logger.info(
                        f"Extracted {len(cleaned_text)} characters using pdfminer"
                    )
                    return cleaned_text
            except Exception as e:
                self.logger.warning(
                    f"pdfminer extraction failed: {e}, trying pypdf")

            # Fallback to pypdf - also run in executor for async
            try:

                def _extract_with_pypdf2(file_path):
                    with open(file_path, "rb") as file:
                        reader = PdfReader(file)
                        text = ""

                        for page in reader.pages:
                            try:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n"
                            except Exception:
                                # Log but continue with other pages
                                pass
                        return text

                loop = asyncio.get_event_loop()
                text = await loop.run_in_executor(None, _extract_with_pypdf2, file_path)

                if text and text.strip():
                    cleaned_text = clean_text(text)
                    self.logger.info(
                        f"Extracted {len(cleaned_text)} characters using pypdf"
                    )
                    return cleaned_text

            except Exception as e:
                self.logger.error(f"pypdf extraction failed: {e}")

            self.logger.error(
                f"All PDF extraction methods failed for: {file_path}")
            return None

        except Exception as e:
            self.logger.error(
                f"Error extracting text from PDF file {file_path}: {e}")
            return None

    async def extract_text_from_bytes(self, pdf_bytes: bytes) -> Optional[str]:
        """
        Extract text from PDF bytes.

        Args:
            pdf_bytes: PDF content as bytes

        Returns:
            Extracted text or None if extraction fails
        """
        try:
            # Save bytes to temporary file and extract
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(pdf_bytes)
                temp_path = temp_file.name

            try:
                text = await self.extract_text_from_file(temp_path)
                return text
            finally:
                # Clean up temporary file
                Path(temp_path).unlink(missing_ok=True)

        except Exception as e:
            self.logger.error(f"Error extracting text from PDF bytes: {e}")
            return None

    def is_valid_pdf_url(self, url: str) -> bool:
        """
        Check if a URL appears to point to a PDF.

        Args:
            url: URL to check

        Returns:
            True if URL appears to be a PDF
        """
        if not url:
            return False

        # Simple heuristics
        url_lower = url.lower()
        return (
            url_lower.endswith(".pdf")
            or "pdf" in url_lower
            or "arxiv.org/pdf" in url_lower
        )
