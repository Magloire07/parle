"""
Application principale FastAPI pour Parle
Plateforme d'apprentissage linguistique (Anglais/Français)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, flashcards, recordings, journal, schedule, progress

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Parle API",
    description="API pour la plateforme d'apprentissage linguistique Parle",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter le répertoire audio pour servir les fichiers
audio_dir = Path(settings.AUDIO_DIR) if not settings.DEBUG else Path("audio")
audio_dir.mkdir(exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")

# Inclusion des routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(flashcards.router, prefix="/flashcards", tags=["Flashcards"])
app.include_router(recordings.router, prefix="/recordings", tags=["Recordings"])
app.include_router(journal.router, prefix="/journal", tags=["Journal"])
app.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'application"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
