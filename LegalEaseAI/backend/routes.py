from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.schemas import (
    DocumentRequest,
    DocumentResponse,
)


router = APIRouter()

_generator = None


def get_generator():

    global _generator

    if _generator is None:

        _generator = (
            GeminiDocumentGenerator()
        )

    return _generator


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest,
):

    try:

        generator = get_generator()

        content = (
            generator.generate_document(
                document_type=request.document_type,
                parties=request.parties,
                terms=request.terms,
                dates=request.dates,
            )
        )

        return DocumentResponse(
            success=True,
            document_type=(
                request.document_type
            ),
            content=content,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error