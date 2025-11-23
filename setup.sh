#!/bin/bash

set -e

echo "🗣️  PARLE - Installation"
echo "========================"
echo ""

# Vérifier les prérequis
echo "📋 Vérification des prérequis..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL n'est pas installé"
    echo "   Installez-le avec: sudo apt install postgresql postgresql-contrib"
fi

echo "✅ Prérequis vérifiés"
echo ""

# Setup Backend
echo "🐍 Configuration du backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "   Création de l'environnement virtuel..."
    python3 -m venv venv
fi

echo "   Activation de l'environnement virtuel..."
source venv/bin/activate

echo "   Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "   Copie du fichier .env.example vers .env..."
    cp .env.example .env
    echo "   ⚠️  N'oubliez pas de configurer .env avec vos paramètres!"
fi

echo "✅ Backend configuré"
cd ..

# Setup Frontend
echo ""
echo "⚛️  Configuration du frontend..."
cd frontend

echo "   Installation des dépendances npm..."
npm install

if [ ! -f ".env" ]; then
    echo "   Création du fichier .env..."
    echo "VITE_API_BASE_URL=http://localhost:8000" > .env
    echo "VITE_APP_NAME=Parle" >> .env
fi

echo "✅ Frontend configuré"
cd ..

# Instructions finales
echo ""
echo "🎉 Installation terminée!"
echo ""
echo "📝 Prochaines étapes:"
echo ""
echo "1. Configurez PostgreSQL:"
echo "   sudo -u postgres psql"
echo "   CREATE DATABASE parle;"
echo "   CREATE USER parle_user WITH PASSWORD 'parle_password';"
echo "   GRANT ALL PRIVILEGES ON DATABASE parle TO parle_user;"
echo ""
echo "2. Configurez le fichier backend/.env"
echo ""
echo "3. Créez les tables de la base de données:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   alembic upgrade head"
echo ""
echo "4. Lancez l'application:"
echo "   ./start-app.sh"
echo ""
