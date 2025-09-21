# 🚀 Guide de Démarrage Rapide - Parle

## 📋 Prérequis

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+ (optionnel pour le développement)
- Tesseract OCR

## ⚡ Démarrage Ultra-Rapide

### 1. Backend (Port 5000)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

pip install -r requirements-minimal.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

### 2. Frontend (Port 3000)

```bash
cd frontend
npm install
npm run dev
```

### 3. Accès

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Documentation API**: http://localhost:5000/docs

## 🎯 Fonctionnalités Disponibles

### ✅ Déjà Fonctionnel
- [x] Upload d'images
- [x] OCR basique avec Tesseract
- [x] Interface de lecture
- [x] Simulation d'analyse vocale
- [x] Page de résumé
- [x] Tableau de bord

### 🔄 En Développement
- [ ] Intégration Whisper réelle
- [ ] Analyse prosodique avancée
- [ ] Base de données PostgreSQL
- [ ] Authentification utilisateur
- [ ] Export des progrès

## 🧪 Test Rapide

1. **Ouvrir** http://localhost:3000
2. **Cliquer** sur "Commencer"
3. **Uploader** une image de texte
4. **Voir** le texte extrait
5. **Cliquer** "Commencer la Lecture"
6. **Tester** l'enregistrement audio

## 🐛 Dépannage

### Backend ne démarre pas
```bash
# Vérifier Python
python3 --version

# Réinstaller les dépendances
pip install --upgrade pip
pip install -r requirements-minimal.txt
```

### Frontend ne démarre pas
```bash
# Vérifier Node.js
node --version

# Nettoyer et réinstaller
rm -rf node_modules package-lock.json
npm install
```

### OCR ne fonctionne pas
```bash
# Installer Tesseract
sudo apt-get install tesseract-ocr tesseract-ocr-fra  # Ubuntu/Debian
brew install tesseract  # macOS
```

## 📁 Structure du Projet

```
parle/
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── api/      # Endpoints
│   │   ├── services/ # Logique métier
│   │   └── models/   # Modèles de données
│   └── requirements-minimal.txt
├── frontend/          # Interface Vue.js
│   ├── src/
│   │   ├── views/    # Pages
│   │   ├── components/ # Composants
│   │   └── services/ # Services API
│   └── package.json
└── docs/             # Documentation
```

## 🔧 Configuration

### Variables d'environnement
```bash
# backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/parle
SECRET_KEY=your-secret-key
TESSERACT_CMD=/usr/bin/tesseract
DEBUG=true
```

### Ports
- Backend: 5000
- Frontend: 3000
- PostgreSQL: 5432 (si utilisé)

## 🚀 Prochaines Étapes

1. **Tester l'upload d'images** avec différents formats
2. **Améliorer l'OCR** avec des paramètres optimisés
3. **Intégrer Whisper** pour la reconnaissance vocale
4. **Configurer PostgreSQL** pour la persistance
5. **Ajouter l'authentification** utilisateur

## 📞 Support

- **Documentation complète**: README.md
- **Maintenance**: MAINTENANCE.md
- **Issues**: Créer une issue sur le repository

---

*Développé avec ❤️ pour améliorer l'expression orale*
