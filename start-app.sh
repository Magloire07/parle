#!/bin/bash

echo "🗣️  PARLE - Démarrage de l'application"
echo "======================================"
echo ""

# Démarrer le backend
echo "📡 Démarrage du backend FastAPI..."
cd backend
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Exécutez d'abord:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✅ Backend démarré (PID: $BACKEND_PID)"
cd ..

# Attendre que le backend soit prêt
sleep 3

# Démarrer le frontend
echo ""
echo "🎨 Démarrage du frontend Vue.js..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules non trouvé. Exécutez d'abord:"
    echo "   npm install"
    exit 1
fi

npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend démarré (PID: $FRONTEND_PID)"
cd ..

echo ""
echo "🚀 Application démarrée!"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Pour arrêter l'application, exécutez:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Attendre
wait
