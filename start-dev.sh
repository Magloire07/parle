#!/bin/bash

# Script de démarrage pour l'environnement de développement
# Usage: ./start-dev.sh

echo "🚀 Démarrage de l'application Parle en mode développement"
echo "=================================================="

# Vérification des prérequis
echo "📋 Vérification des prérequis..."

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérification de Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    exit 1
fi

# Vérification de PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL n'est pas installé"
    exit 1
fi

# Vérification de Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "❌ Tesseract OCR n'est pas installé"
    echo "💡 Installation: sudo apt-get install tesseract-ocr tesseract-ocr-fra"
    exit 1
fi

echo "✅ Tous les prérequis sont installés"

# Création des répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p backend/uploads
mkdir -p backend/static
mkdir -p frontend/dist

# Configuration de l'environnement
echo "⚙️ Configuration de l'environnement..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "📝 Fichier .env créé à partir de env.example"
fi

# Installation des dépendances backend
echo "🐍 Installation des dépendances Python..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Installation des dépendances frontend
echo "📦 Installation des dépendances Node.js..."
cd frontend
npm install
cd ..

# Démarrage de la base de données
echo "🗄️ Démarrage de la base de données..."
if ! pg_isready -q; then
    echo "❌ PostgreSQL n'est pas démarré"
    echo "💡 Démarrez PostgreSQL avec: sudo systemctl start postgresql"
    exit 1
fi

# Création de la base de données si elle n'existe pas
createdb parle 2>/dev/null || echo "Base de données 'parle' existe déjà"

# Exécution des migrations
echo "🔄 Exécution des migrations..."
psql -d parle -f database/init.sql

echo "✅ Configuration terminée"
echo ""
echo "🎯 Pour démarrer l'application:"
echo "1. Backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "🌐 URLs:"
echo "- Frontend: http://localhost:3000"
echo "- Backend: http://localhost:8000"
echo "- Documentation API: http://localhost:8000/docs"
echo ""
echo "📚 Documentation complète dans README.md"
