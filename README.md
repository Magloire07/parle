# Parle - Application d'Entraînement à l'Oral

## 🎯 Description

Parle est une application web qui aide les utilisateurs à améliorer leur expression orale en lisant des textes à voix haute. L'application analyse la prononciation, l'intonation et le rythme pour fournir un feedback détaillé et des suggestions d'amélioration.

## ✨ Fonctionnalités

### 🔍 OCR (Reconnaissance Optique de Caractères)
- Scan de pages de livre avec Tesseract OCR
- Extraction de texte structuré en paragraphes
- Support multilingue (français, anglais)

### 🎤 Analyse Vocale
- Transcription en temps réel avec Whisper
- Détection des erreurs de prononciation
- Analyse prosodique (intonation, rythme, pauses)
- Alignement avec le texte attendu

### 🔊 Synthèse Vocale
- Génération de modèles audio corrects
- Support de différentes langues
- Contrôle de la vitesse de lecture

### 📝 Évaluation des Résumés
- Analyse de résumés oraux
- Évaluation de la pertinence et de la qualité
- Suggestions d'amélioration
- Détection des erreurs de transition

## 🏗️ Architecture

### Frontend (Vue.js 3)
- Interface utilisateur moderne et responsive
- Composants réutilisables
- Gestion d'état avec Pinia
- Intégration avec Element Plus

### Backend (FastAPI)
- API REST performante
- Traitement asynchrone
- Intégration des services IA
- Gestion des fichiers audio

### Base de Données (PostgreSQL)
- Stockage des utilisateurs et textes
- Historique des lectures
- Statistiques de progression
- Données de feedback

### Services IA
- **Tesseract OCR** : Extraction de texte
- **Whisper** : Reconnaissance vocale
- **gTTS/Coqui** : Synthèse vocale
- **Parselmouth** : Analyse prosodique
- **Transformers** : Évaluation des résumés

## 🚀 Installation

### Prérequis
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Docker (optionnel)

### Installation avec Docker

```bash
# Cloner le repository
git clone <repository-url>
cd parle

# Démarrer les services
cd docker
docker-compose up -d

# L'application sera disponible sur :
# - Frontend: http://localhost:3000
# - Backend: http://localhost:5000
# - Base de données: localhost:5432
```

### Installation manuelle

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Base de données
```bash
# Créer la base de données
createdb parle

# Exécuter les migrations
psql -d parle -f database/init.sql
```

## 📖 Utilisation

### 1. Scanner un Document
1. Accédez à la page d'upload
2. Glissez-déposez une image de page de livre
3. L'application extrait le texte avec OCR

### 2. Lire à Voix Haute
1. Le texte est affiché paragraphe par paragraphe
2. Lisez à voix haute en cliquant sur "Enregistrer"
3. Recevez un feedback en temps réel

### 3. Analyser les Erreurs
1. Les mots mal prononcés sont surlignés
2. Écoutez le modèle correct
3. Répétez jusqu'à la correction

### 4. Résumer Oralement
1. Tous les 2 paragraphes, passez en mode résumé
2. Enregistrez votre résumé
3. Recevez des suggestions d'amélioration

## 🔧 Configuration

### Variables d'environnement
```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/parle
SECRET_KEY=your-secret-key
TESSERACT_CMD=/usr/bin/tesseract
WHISPER_MODEL=base
TTS_LANG=fr

# Frontend
VITE_API_URL=http://localhost:5000
```

### Configuration OCR
- Langues supportées : `fra+eng`
- Modèle Tesseract : `--oem 3 --psm 6`
- Formats d'image : JPG, PNG, GIF

### Configuration Whisper
- Modèle : `base` (équilibre performance/précision)
- Device : `cpu` (ou `cuda` si disponible)
- Langues : français, anglais

## 📊 API Endpoints

### OCR
- `POST /ocr/upload` - Upload et traitement d'image
- `POST /ocr/analyze` - Analyse de texte existant

### Speech
- `POST /speech/analyze` - Analyse d'enregistrement vocal
- `POST /speech/prosody` - Analyse prosodique

### TTS
- `POST /tts/read` - Génération de parole
- `GET /tts/audio/{filename}` - Récupération de fichier audio

### Summary
- `POST /summary/evaluate` - Évaluation de résumé
- `POST /summary/generate` - Génération de suggestions

### Health
- `GET /health/` - Vérification de l'état de l'API

## 🧪 Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 📈 Monitoring

### Logs
- Backend : `/var/log/parle/`
- Frontend : Console du navigateur
- Base de données : Logs PostgreSQL

### Métriques
- Santé de l'API : `GET /health/`
- Performance : Temps de réponse des endpoints
- Utilisation : Nombre de requêtes par minute

## 🔒 Sécurité

- Authentification JWT
- Validation des fichiers uploadés
- Limitation de la taille des fichiers
- CORS configuré
- Sanitisation des entrées utilisateur

## 🚀 Déploiement

### Production
```bash
# Build des images Docker
docker-compose -f docker-compose.prod.yml build

# Déploiement
docker-compose -f docker-compose.prod.yml up -d
```

### Variables d'environnement de production
```bash
DEBUG=False
DATABASE_URL=postgresql://user:password@db:5432/parle
SECRET_KEY=your-production-secret-key
ALLOWED_ORIGINS=https://yourdomain.com
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

- **Email** : support@parle-app.com
- **Documentation** : [Lien vers docs]
- **Issues** : [Lien vers GitHub Issues]

## 🙏 Remerciements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Whisper](https://github.com/openai/whisper)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)

---

*Développé avec ❤️ pour améliorer l'expression orale*