import os
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

try:
    from google import genai
except Exception:  # pragma: no cover
    genai = None


class GeminiDocumentGenerator:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        if load_dotenv is not None:
            load_dotenv(Path(__file__).resolve().parents[2] / ".env")

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def _fallback_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        return (
            f"{document_type.title()}\n\n"
            f"This {document_type.lower()} is entered into by and between {parties}.\n"
            f"The parties agree to the following terms: {terms}.\n"
            f"The effective date and relevant schedule are set as follows: {dates}.\n\n"
            "This draft is a basic legal template generated for review by qualified counsel. "
            "Please confirm jurisdiction, governing law, risk allocation, and final legal language before use."
        )

    def _build_prompt(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        return (
            f"Draft a concise but professional {document_type} for the following parties: {parties}.\n"
            f"Include important legal terms and obligations: {terms}.\n"
            f"Include effective dates and schedule details: {dates}.\n"
            "Keep the output clear, formal, and suitable for a business legal document."
        )

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = self._build_prompt(document_type, parties, terms, dates)

        if not self.api_key or genai is None:
            return self._fallback_document(document_type, parties, terms, dates)

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            text = getattr(response, "text", None)
            if text:
                return text

            if isinstance(response, dict):
                return response.get("text") or str(response)

            return str(response)
        except Exception:
            return self._fallback_document(document_type, parties, terms, dates)
