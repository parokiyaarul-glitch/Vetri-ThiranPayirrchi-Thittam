from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(..., description="Type of legal document to generate")
    parties: str = Field(..., description="Names or parties involved")
    terms: str = Field(..., description="Key legal terms and obligations")
    dates: str = Field(..., description="Relevant dates, deadlines, and timing")


class DocumentResponse(BaseModel):
    success: bool = True
    document_type: str
    content: str
