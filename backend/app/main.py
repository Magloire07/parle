"""
Application principale FastAPI pour Parle
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.core.config import settings
from app.api.routes import ocr, speech, tts, summary, health

app = FastAPI(
    title="Parle API",
    description="API pour l'application d'entraînement à l'oral Parle",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage des routes statiques pour les fichiers audio
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclusion des routes
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
app.include_router(speech.router, prefix="/speech", tags=["speech"])
app.include_router(tts.router, prefix="/tts", tags=["tts"])
app.include_router(summary.router, prefix="/summary", tags=["summary"])

@app.get("/")
async def root():
    """Point d'entrée principal de l'API"""
    return {
        "message": "Bienvenue sur l'API Parle",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )
