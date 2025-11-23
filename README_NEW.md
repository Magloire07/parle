# 🗣️ PARLE - Plateforme d'Apprentissage Linguistique

Plateforme web pour l'apprentissage intensif de l'anglais et du français (niveau B2 → C2).

## 🏗️ Architecture

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Vue.js 3 + Vite
- **Base de données**: PostgreSQL
- **Authentification**: JWT
- **Styling**: Tailwind CSS (thème sombre)

## 📋 Prérequis

- Python 3.10+
- Node.js 20 LTS
- PostgreSQL 15+
- Git

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone <repository-url>
cd parle
```

### 2. Configuration de la base de données

```bash
# Créer la base de données PostgreSQL
createdb parle

# Ou via psql
psql -U postgres
CREATE DATABASE parle;
CREATE USER parle_user WITH PASSWORD 'parle_password';
GRANT ALL PRIVILEGES ON DATABASE parle TO parle_user;
```

### 3. Backend (FastAPI)

```bash
cd backend

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer .env
cp .env.example .env
# Éditer .env avec vos paramètres

# Créer les tables (migrations Alembic)
alembic upgrade head

# Lancer le serveur de développement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur `http://localhost:8000`
Documentation interactive: `http://localhost:8000/docs`

### 4. Frontend (Vue.js)

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

## 📁 Structure du projet

```
parle/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # Routes API
│   │   ├── core/             # Configuration, DB, Auth
│   │   ├── models/           # Modèles SQLAlchemy
│   │   ├── schemas.py        # Schémas Pydantic
│   │   └── main.py           # Point d'entrée FastAPI
│   ├── alembic/              # Migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/       # Composants Vue
│   │   ├── views/            # Pages
│   │   ├── router/           # Configuration routes
│   │   ├── stores/           # Stores Pinia
│   │   ├── services/         # API clients
│   │   └── assets/           # CSS, images
│   ├── package.json
│   └── tailwind.config.js
└── CAHIER_DES_CHARGES.md
```

## 🔑 Fonctionnalités principales

### ✅ MVP (Phase 1-2)

- [x] Authentification JWT (login/register)
- [x] Système de cartes flash avec algorithme SRS (répétition espacée)
- [x] Enregistreur audio pour exercices
- [x] Journal de progression
- [x] Planificateur hebdomadaire
- [x] Suivi de progression avec statistiques

### 🚧 En cours de développement

- [ ] Interface Dashboard
- [ ] Pages de practice (Speaking, Listening, Reading, Writing)
- [ ] Bibliothèque de ressources
- [ ] Tests blancs (Cambridge C2 / IELTS)

## 🛠️ Développement

### Commandes utiles

#### Backend

```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head

# Tests
pytest

# Linting
ruff check .
black .
```

#### Frontend

```bash
# Build de production
npm run build

# Preview du build
npm run preview

# Linting
npm run lint

# Format code
npm run format
```

## 🌐 Déploiement en production

Voir le [Cahier des Charges](./CAHIER_DES_CHARGES.md) section 11 pour les instructions de déploiement sur machine locale avec:
- Nginx reverse proxy
- SSL/TLS (Let's Encrypt)
- Systemd services
- PostgreSQL en production

## 📝 Variables d'environnement

### Backend (.env)

```env
DATABASE_URL=postgresql://parle_user:parle_password@localhost:5432/parle
SECRET_KEY=your-secret-key-32-chars-min
DEBUG=True
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Parle
```

## 🎨 Thème sombre

Palette de couleurs:
- Fond principal: `#0a0a0a`
- Fond secondaire: `#1a1a1a`
- Cards: `#252525`
- Texte: `#e5e5e5`
- Accent bleu: `#3b82f6`
- Accent violet: `#8b5cf6`

## 📚 Documentation API

Une fois le backend lancé, accédez à:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contribution

1. Créer une branche feature
2. Commit les changements
3. Push vers la branche
4. Créer une Pull Request

## 📄 Licence

MIT

## 👤 Auteur

Développé avec ❤️ pour l'apprentissage linguistique intensif
