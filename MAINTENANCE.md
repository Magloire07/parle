# Documentation de Maintenance - Projet Parle

## 📋 Vue d'ensemble du projet

**Parle** est une application d'entraînement à l'oral qui aide les utilisateurs à améliorer leur prononciation, intonation et rythme en lisant des textes à voix haute.

### Objectif principal
L'application permet de :
- Scanner des pages de livre et les convertir en texte
- Suivre en temps réel la lecture orale de l'utilisateur
- Détecter les erreurs (prononciation, rythme, intonation, mots sautés)
- Fournir un feedback visuel et audio
- Évaluer les résumés oraux tous les 2 paragraphes

## 🏗️ Architecture technique

### Stack technologique
- **Frontend**: Vue.js 3 + TypeScript
- **Backend**: FastAPI (Python)
- **Base de données**: PostgreSQL
- **OCR**: Tesseract OCR (pytesseract)
- **Reconnaissance vocale**: OpenAI Whisper
- **Synthèse vocale**: gTTS ou Coqui TTS
- **Analyse prosodique**: parselmouth (Praat) ou librosa

### Structure du projet
```
parle/
├── frontend/                 # Application Vue.js
│   ├── src/
│   │   ├── components/      # Composants Vue
│   │   ├── views/          # Pages de l'application
│   │   ├── services/       # Services API
│   │   └── utils/          # Utilitaires
│   └── package.json
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints API
│   │   ├── core/           # Configuration
│   │   ├── models/         # Modèles de données
│   │   ├── services/       # Logique métier
│   │   └── utils/          # Utilitaires
│   └── requirements.txt
├── database/               # Scripts de base de données
│   ├── migrations/         # Migrations
│   └── seeds/             # Données de test
├── docs/                  # Documentation
│   ├── api/               # Documentation API
│   └── diagrams/          # Diagrammes SVG
└── docker/                # Configuration Docker
    ├── docker-compose.yml
    └── Dockerfile
```

## 🔄 Flux de données

### 1. Processus OCR
1. Utilisateur upload une image
2. Backend traite l'image avec Tesseract OCR
3. Texte extrait structuré en paragraphes
4. Stockage en base de données

### 2. Processus de lecture
1. Affichage du texte paragraphe par paragraphe
2. Enregistrement audio de l'utilisateur
3. Transcription avec Whisper
4. Alignement avec le texte attendu
5. Analyse prosodique (pitch, rythme, pauses)
6. Génération du feedback visuel

### 3. Processus de résumé
1. Tous les 2 paragraphes, passage en mode résumé
2. Enregistrement audio du résumé
3. Transcription avec Whisper
4. Analyse avec modèle de langage
5. Génération de suggestions

## 🛠️ APIs principales

### OCR
- `POST /ocr/upload` - Upload et traitement d'image

### Reconnaissance vocale
- `POST /speech/analyze` - Analyse de l'enregistrement vocal

### Synthèse vocale
- `POST /tts/read` - Génération audio du modèle correct

### Résumé
- `POST /summary/evaluate` - Évaluation du résumé oral

## 📊 Base de données

### Tables principales
- `users` - Informations utilisateur
- `texts` - Textes extraits des livres
- `readings` - Enregistrements + résultats d'analyse
- `summaries` - Résumés oraux + feedback
- `stats` - Scores de progression

## 🚀 Déploiement

### Prérequis
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Docker (optionnel)

### Installation
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Base de données
# Voir scripts dans database/
```

## 🔧 Maintenance

### Logs importants
- Logs OCR : `/var/log/parle/ocr.log`
- Logs API : `/var/log/parle/api.log`
- Logs Whisper : `/var/log/parle/whisper.log`

### Monitoring
- Santé de l'API : `GET /health`
- Métriques : `GET /metrics`
- Status de la base : `GET /db/status`

### Sauvegarde
- Base de données : Scripts dans `database/backup/`
- Fichiers audio : Sauvegarde quotidienne
- Logs : Rotation hebdomadaire

## 🐛 Dépannage courant

### Problèmes OCR
- Vérifier la qualité de l'image
- Ajuster les paramètres Tesseract
- Vérifier les langues supportées

### Problèmes Whisper
- Vérifier l'espace disque (modèles volumineux)
- Ajuster la qualité audio d'entrée
- Vérifier les langues supportées

### Problèmes de performance
- Optimiser les requêtes base de données
- Mise en cache des modèles IA
- Compression des fichiers audio

## 📈 Évolutions prévues

### Version 2
- Mode conversation improvisée
- Système de gamification
- Analyse du langage corporel

### Améliorations techniques
- Mise en cache Redis
- CDN pour les fichiers audio
- Monitoring avancé avec Prometheus

## 👥 Équipe de développement

- **Développeur principal**: [Nom]
- **DevOps**: [Nom]
- **UI/UX**: [Nom]

## 📞 Support

- **Email**: support@parle-app.com
- **Documentation**: [Lien vers docs]
- **Issues**: [Lien vers GitHub Issues]

---
*Dernière mise à jour: [Date]*
*Version: 1.0.0*
