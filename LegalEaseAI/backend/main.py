from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


# Create FastAPI application
app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator API",
    version="1.0.0",
)


# CORS configuration
# Allows the Streamlit frontend to communicate with the FastAPI backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(router)


@app.get("/")
def root():
    """
    Root endpoint used to verify that the LegalEase
    backend service is running.
    """
    return {
        "service": "LegalEase API",
        "status": "running",
        "message": "LegalEase backend is running successfully.",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """
    Health-check endpoint.
    """
    return {
        "status": "healthy"
    }