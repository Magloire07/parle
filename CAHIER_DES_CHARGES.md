# Cahier des Charges - Plateforme d'Apprentissage Linguistique "Parle"

## 1. Vue d'ensemble du projet

### 1.1 Objectif
Créer une plateforme web centralisée pour l'apprentissage intensif de l'anglais et du français, niveau avancé (B2 → C2), avec suivi personnalisé et outils d'entraînement intégrés.

### 1.2 Public cible
- Apprenants autodidactes motivés
- Niveau actuel : B2 minimum
- Objectif : C2 (éloquence, persuasion, maîtrise)
- Engagement : 20-30h/semaine

### 1.3 Langues supportées
- Interface principale : Français
- Deux modules d'apprentissage : Anglais et Français

---

## 2. Architecture technique

### 2.1 Stack technologique recommandée

#### Frontend
- **Framework** : Vue.js 3 (Composition API)
- **Langage** : TypeScript
- **Build Tool** : Vite
- **Router** : Vue Router 4
- **UI/Styling** : 
  - Tailwind CSS (thème sombre par défaut)
  - Headless UI Vue (composants accessibles)
  - Heroicons (icônes)
- **State Management** : Pinia
- **Animations** : GSAP ou Vue Transitions
- **HTTP Client** : Axios

#### Backend
- **Framework** : FastAPI (Python 3.10+)
- **Base de données** : PostgreSQL
- **ORM** : SQLAlchemy 2.0
- **Migrations** : Alembic
- **Authentification** : JWT (python-jose) + OAuth2

#### Stockage & Médias
- **Fichiers audio** : Cloudflare R2 ou AWS S3
- **CDN** : Cloudflare ou AWS CloudFront
- **Enregistrements** : API Web Audio (MediaRecorder)

#### Outils de développement
- **Linting Frontend** : ESLint + Prettier
- **Linting Backend** : Ruff + Black
- **Tests Frontend** : Vitest + Vue Test Utils
- **Tests Backend** : Pytest + pytest-asyncio
- **CI/CD** : GitHub Actions
- **Déploiement** : Self-hosted (machine locale avec port 443 exposé)
- **Reverse Proxy** : Nginx ou Caddy (gestion HTTPS/SSL)
- **Process Manager** : Systemd ou PM2

---

## 3. Fonctionnalités principales

### 3.1 Système de cartes flash (type Anki)

#### Fonctionnalités
- **Création de cartes** : Front/Back avec audio optionnel
- **Algorithme SRS** : Répétition espacée (SM-2 ou FSRS)
- **Catégories** : Grammaire, Vocabulaire, Expressions, Phrases complètes
- **Import/Export** : Format JSON ou CSV
- **Tags et filtres** : Organisation par thème/niveau
- **Statistiques** : Taux de réussite, intervalle de révision

#### Priorités techniques
- Algorithme de répétition espacée robuste
- Audio intégré (lecture et enregistrement)
- Interface rapide (< 100ms par carte)

---

### 3.2 Enregistreur audio intégré

#### Fonctionnalités
- **Enregistrement** : Mono, qualité moyenne (32kbps)
- **Lecture** : Contrôles standard (play/pause/vitesse)
- **Sauvegarde** : Cloud + metadata (date, durée, exercice)
- **Analyse** : Visualisation forme d'onde
- **Comparaison** : Écoute modèle vs enregistrement utilisateur

#### Priorités techniques
- API MediaRecorder (WebRTC)
- Compression audio côté client
- Stockage optimisé (max 5MB par fichier)

---

### 3.3 Planificateur hebdomadaire

#### Fonctionnalités
- **Vue calendrier** : Lundi → Dimanche
- **Blocs de 30 min** : Glisser-déposer pour planifier
- **Templates** : Plans prédéfinis (français et anglais)
- **Rappels** : Notifications push (optionnel)
- **Suivi** : Cocher activités complétées
- **Statistiques** : Heures par semaine/mois

#### Priorités techniques
- Calendrier interactif (react-big-calendar ou FullCalendar)
- Persistance locale (localStorage) + sync cloud
- Export PDF/iCal

---

### 3.4 Journal de progression

#### Fonctionnalités
- **Entrées quotidiennes** : 150-300 mots
- **Champs structurés** :
  - Ce qui a été pratiqué
  - Difficultés rencontrées
  - 3 améliorations pour demain
  - Nouvelles tournures apprises (10 max)
- **Recherche** : Filtres par date/mot-clé
- **Export** : Markdown, PDF

#### Priorités techniques
- Éditeur de texte riche (TipTap ou Lexical)
- Auto-save toutes les 30s
- Recherche full-text (PostgreSQL)

---

### 3.5 Bibliothèque de ressources

#### Fonctionnalités
- **Catégories** :
  - Articles (lecture active)
  - Podcasts/Vidéos (écoute)
  - Discours/TED Talks (analyse)
  - Exercices de prononciation
  - Templates de structures (PREP, S-P-A-R)
- **Annotations** : Surligner et commenter
- **Extraction** : Sélectionner texte → créer carte Anki
- **Recherche** : Par niveau, durée, thème

#### Priorités techniques
- Player vidéo/audio intégré (Plyr.js)
- Annotation de texte (Hypothesis ou custom)
- API externe (YouTube, Spotify embed)

---

### 3.6 Exercices interactifs

#### Types d'exercices
1. **Monologue guidé** (PREP/S-P-A-R)
   - Timer 5-10 min
   - Enregistrement automatique
   - Grille d'auto-évaluation (5 critères)

2. **Shadowing**
   - Audio modèle
   - Enregistrement synchronisé
   - Comparaison visuelle (waveform)

3. **Dictée**
   - Audio + champ texte
   - Correction automatique (Levenshtein distance)

4. **Paraphrase**
   - Texte source
   - Trois champs : formel/neutre/familier

5. **Débat solo**
   - Sujet aléatoire
   - 10 min préparation + 6 min enregistrement

#### Priorités techniques
- Timer configurable
- Sauvegarde automatique des enregistrements
- Algorithme de correction orthographique

---

### 3.7 Tableau de bord (Dashboard)

#### Widgets
- **Statistiques hebdomadaires** : Heures pratiquées, exercices complétés
- **Cartes Anki** : Dues aujourd'hui
- **Prochaine session** : Calendrier
- **Streak** : Jours consécutifs
- **Objectifs** : Barre de progression (hebdo/mensuel)
- **Derniers enregistrements** : Accès rapide

#### Graphiques
- Heures par compétence (Speaking/Listening/Reading/Writing)
- Courbe de progression (nombre de cartes maîtrisées)
- Heatmap d'activité (GitHub style)

#### Priorités techniques
- Graphiques avec Recharts ou Chart.js
- Mise à jour en temps réel
- Responsive design (mobile-first)

---

### 3.8 Tests et simulations

#### Fonctionnalités
- **Tests blancs** : Format Cambridge C2 / IELTS Advanced
- **Sections** : Listening, Reading, Writing, Speaking
- **Timer** : Chronomètre par section
- **Correction** : Semi-automatique (QCM auto, écriture manuelle)
- **Historique** : Résultats archivés avec détails

#### Priorités techniques
- Interface exam-like (full screen, timer visible)
- Sauvegarde auto toutes les 2 min
- Export PDF des résultats

---

## 4. Design et UX

### 4.1 Thème visuel

#### Palette de couleurs (sombre)
- **Fond principal** : `#0a0a0a` (noir profond)
- **Fond secondaire** : `#1a1a1a` (gris très foncé)
- **Fond cards** : `#252525` (gris foncé)
- **Texte principal** : `#e5e5e5` (blanc cassé)
- **Texte secondaire** : `#a3a3a3` (gris clair)
- **Accent primaire** : `#3b82f6` (bleu)
- **Accent secondaire** : `#8b5cf6` (violet)
- **Succès** : `#10b981` (vert)
- **Erreur** : `#ef4444` (rouge)

#### Typographie
- **Titres** : Inter ou Geist (bold)
- **Corps** : Inter ou system-ui (regular/medium)
- **Code/mono** : JetBrains Mono

### 4.2 Composants UI

#### Obligatoires
- Cards avec hover effects
- Boutons avec états (hover/active/disabled)
- Inputs avec validation visuelle
- Modals (dialogs) fluides
- Toast notifications
- Loading spinners/skeletons
- Navigation sidebar (collapsible)

#### Animations
- Transitions douces (150-300ms)
- Micro-interactions (boutons, cartes)
- Page transitions (Framer Motion)

### 4.3 Responsive
- **Desktop-first** : Optimisé pour écrans ≥ 1280px
- **Tablet** : Adaptatif 768-1279px
- **Mobile** : Fonctionnel 320-767px (version simplifiée)

---

## 5. Modèle de données

### 5.1 Schéma SQLAlchemy (simplifié)

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    flashcards = relationship("Flashcard", back_populates="user")
    recordings = relationship("Recording", back_populates="user")
    journal_entries = relationship("JournalEntry", back_populates="user")
    progress = relationship("Progress", back_populates="user")
    schedule = relationship("ScheduleBlock", back_populates="user")

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    language = Column(String, nullable=False)  # "en" | "fr"
    front = Column(String, nullable=False)
    back = Column(String, nullable=False)
    audio_url = Column(String, nullable=True)
    tags = Column(ARRAY(String), default=[])  # Array de tags
    category = Column(String, nullable=False)  # "vocabulary" | "grammar" | "expression"
    
    next_review = Column(DateTime, nullable=False)
    interval = Column(Integer, default=1)  # Jours
    ease_factor = Column(Float, default=2.5)
    review_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="flashcards")

class Recording(Base):
    __tablename__ = "recordings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    language = Column(String, nullable=False)
    exercise_type = Column(String, nullable=False)  # "monologue" | "shadowing" | "debate"
    audio_url = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # Secondes
    transcript = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="recordings")

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)  # Markdown
    practiced = Column(ARRAY(String), default=[])  # Activités
    difficulties = Column(ARRAY(String), default=[])
    improvements = Column(ARRAY(String), default=[])
    new_phrases = Column(ARRAY(String), default=[])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="journal_entries")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    language = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    
    hours_studied = Column(Float, default=0.0)
    cards_reviewed = Column(Integer, default=0)
    exercises_completed = Column(Integer, default=0)
    
    user = relationship("User", back_populates="progress")

class ScheduleBlock(Base):
    __tablename__ = "schedule_blocks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0-6 (lundi=0)
    start_time = Column(String, nullable=False)  # "09:00"
    duration = Column(Integer, nullable=False)  # Minutes
    activity_type = Column(String, nullable=False)
    activity_name = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="schedule")
```

---

## 6. Pages et navigation

### 6.1 Structure des routes

```
/                          → Page d'accueil/Landing
/auth/login                → Connexion
/auth/register             → Inscription

/dashboard                 → Tableau de bord principal

/english                   → Hub anglais
/english/flashcards        → Cartes Anki anglais
/english/practice/speaking → Exercices oral
/english/practice/listening→ Exercices écoute
/english/practice/reading  → Exercices lecture
/english/practice/writing  → Exercices écriture
/english/resources         → Bibliothèque ressources
/english/tests             → Tests blancs

/french                    → Hub français (même structure)
/french/flashcards
/french/practice/speaking
/french/practice/listening
/french/practice/reading
/french/practice/writing
/french/resources
/french/tests

/schedule                  → Planificateur hebdomadaire
/journal                   → Journal de progression
/progress                  → Statistiques et graphiques
/settings                  → Paramètres utilisateur
```

### 6.2 Navigation

#### Sidebar (toujours visible)
- Dashboard
- English
  - Practice
  - Flashcards
  - Resources
  - Tests
- Français
  - Practice
  - Flashcards
  - Resources
  - Tests
- Schedule
- Journal
- Progress
- Settings

---

## 7. Priorités de développement (MVP)

### Phase 1 - Core (2-3 semaines)
1. ✅ Setup projet (Vue.js + Vite + FastAPI + SQLAlchemy)
2. ✅ Configuration Tailwind CSS + Headless UI (thème sombre)
3. ✅ Authentification JWT (login/register)
4. ✅ Dashboard de base
5. ✅ Système flashcards (sans audio)
6. ✅ Journal simple

### Phase 2 - Practice (2-3 semaines)
7. ✅ Enregistreur audio (MediaRecorder API)
8. ✅ Exercices de base (monologue, shadowing)
9. ✅ Planificateur hebdomadaire
10. ✅ Intégration audio dans flashcards

### Phase 3 - Content (2 semaines)
11. ✅ Bibliothèque de ressources
12. ✅ Templates de structures
13. ✅ Import de contenu prédéfini

### Phase 4 - Analytics (1-2 semaines)
14. ✅ Tracking de progression (Chart.js)
15. ✅ Graphiques et statistiques
16. ✅ Tests blancs

### Phase 5 - Polish (1 semaine)
17. ✅ Optimisations performances
18. ✅ Responsive mobile
19. ✅ Tests et corrections bugs

---

## 8. Contraintes et exigences

### 8.1 Performance
- **Temps de chargement** : < 2s (LCP)
- **Interactivité** : < 100ms (FID)
- **Stabilité visuelle** : CLS < 0.1

### 8.2 Sécurité
- Authentification sécurisée (JWT + refresh tokens)
- Validation côté serveur (Zod)
- Protection CSRF
- Rate limiting API
- Sanitization des inputs

### 8.3 Accessibilité
- WCAG 2.1 Level AA minimum
- Navigation clavier
- Lecteurs d'écran compatibles
- Contraste suffisant (4.5:1)

### 8.4 SEO
- Métadonnées optimisées
- Sitemap.xml
- Robots.txt
- Open Graph tags

---

## 9. Fichiers de configuration nécessaires

### 9.1 Dépendances principales

#### Frontend (package.json)
```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.3.0",
    "pinia": "^2.1.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.4.0",
    "@headlessui/vue": "^1.7.0",
    "@heroicons/vue": "^2.1.0",
    "chart.js": "^4.4.0",
    "vue-chartjs": "^5.3.0",
    "v-calendar": "^3.1.0",
    "@tiptap/vue-3": "^2.2.0",
    "@tiptap/starter-kit": "^2.2.0",
    "date-fns": "^3.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.4.0",
    "vite": "^5.1.0",
    "vitest": "^1.3.0",
    "@vue/test-utils": "^2.4.0",
    "eslint": "^8.57.0",
    "prettier": "^3.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

#### Backend (requirements.txt)
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
alembic==1.13.0
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pytest==7.4.0
pytest-asyncio==0.21.0
httpx==0.26.0
ruff==0.1.0
black==23.12.0
boto3==1.34.0  # Pour S3/R2
python-dotenv==1.0.0
```

### 9.2 Variables d'environnement

#### Frontend (.env.production)
```env
VITE_API_BASE_URL=https://votre-domaine.com/api
VITE_APP_NAME=Parle
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/parle
SECRET_KEY=your-secret-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Storage (Local ou S3/R2)
UPLOAD_DIR=/var/www/parle/uploads
AUDIO_DIR=/var/www/parle/audio
MAX_UPLOAD_SIZE=10485760  # 10MB

# CORS (ajoutez votre domaine/IP)
CORS_ORIGINS=https://votre-domaine.com,https://votre-ip-publique

# Server
HOST=0.0.0.0
PORT=8000
```

---

## 10. Livrables attendus

### Code source
- ✅ Repository Git (GitHub/GitLab)
- ✅ Documentation README.md
- ✅ Architecture bien structurée
- ✅ Code commenté (fonctions complexes)

### Documentation
- ✅ Guide d'installation
- ✅ Guide utilisateur
- ✅ Documentation API (si applicable)

### Déploiement
- ✅ Instance de production (Self-hosted)
- ✅ Base de données PostgreSQL configurée
- ✅ Nginx/Caddy reverse proxy avec SSL
- ✅ Port 443 exposé sur routeur + redirection
- ✅ Systemd services (auto-restart)
- ✅ Script de backup automatique

---

## 11. Configuration de l'hébergement local

### 11.1 Architecture réseau

```
Internet (Port 443)
    ↓
Routeur (Port Forwarding 443 → Machine locale)
    ↓
Machine locale (Ubuntu Server)
    ↓
Nginx/Caddy (Reverse Proxy HTTPS)
    ├─→ Frontend Vue.js (Port 3000)
    └─→ Backend FastAPI (Port 8000)
         ↓
    PostgreSQL (Port 5432)
```

### 11.2 Configuration Nginx (exemple)

```nginx
# /etc/nginx/sites-available/parle

server {
    listen 443 ssl http2;
    server_name votre-domaine.com;  # ou votre IP publique

    # SSL avec Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Frontend Vue.js
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        rewrite ^/api(/.*)$ $1 break;
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (si nécessaire)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Uploads/Audio (fichiers statiques)
    location /uploads {
        alias /var/www/parle/uploads;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # Sécurité
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Max body size (pour uploads audio)
    client_max_body_size 10M;
}

# Redirection HTTP → HTTPS
server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}
```

### 11.3 Configuration Systemd

#### Service Backend FastAPI
```ini
# /etc/systemd/system/parle-backend.service

[Unit]
Description=Parle Backend FastAPI
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/parle/backend
Environment="PATH=/var/www/parle/backend/venv/bin"
ExecStart=/var/www/parle/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Service Frontend Vue.js (si servi par Node)
```ini
# /etc/systemd/system/parle-frontend.service

[Unit]
Description=Parle Frontend Vue.js
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/parle/frontend
Environment="NODE_ENV=production"
ExecStart=/usr/bin/npm run preview -- --port 3000 --host 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 11.4 Configuration routeur

#### Port Forwarding (exemple)
- **Port externe** : 443 (HTTPS)
- **Port interne** : 443
- **IP locale** : 192.168.x.x (IP fixe de votre machine)
- **Protocole** : TCP

#### IP statique locale (recommandé)
Configurez une IP fixe pour votre machine dans le DHCP du routeur ou directement sur la machine :

```bash
# /etc/netplan/01-netcfg.yaml (Ubuntu)
network:
  version: 2
  ethernets:
    eth0:
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

### 11.5 Obtenir un certificat SSL

#### Option 1 : Avec nom de domaine (recommandé)
```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir certificat (Nginx doit être configuré)
sudo certbot --nginx -d votre-domaine.com

# Auto-renouvellement (Certbot l'active automatiquement)
sudo certbot renew --dry-run
```

#### Option 2 : Sans nom de domaine (IP publique uniquement)
Utilisez un certificat auto-signé (attention : navigateur affichera un avertissement)
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/parle-selfsigned.key \
  -out /etc/ssl/certs/parle-selfsigned.crt
```

### 11.6 Script de déploiement automatique

```bash
#!/bin/bash
# /var/www/parle/deploy.sh

set -e

echo "🚀 Déploiement Parle..."

# Backend
cd /var/www/parle/backend
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart parle-backend

# Frontend
cd /var/www/parle/frontend
git pull origin main
npm install
npm run build
sudo systemctl restart parle-frontend

# Nginx
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Déploiement terminé!"
```

### 11.7 Backup automatique

```bash
#!/bin/bash
# /var/www/parle/backup.sh

BACKUP_DIR="/var/backups/parle"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup PostgreSQL
pg_dump -U parle_user parle > "$BACKUP_DIR/db_$DATE.sql"

# Backup fichiers audio
tar -czf "$BACKUP_DIR/audio_$DATE.tar.gz" /var/www/parle/uploads

# Garder seulement les 7 derniers backups
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "audio_*.tar.gz" -mtime +7 -delete

echo "✅ Backup créé: $DATE"
```

Ajoutez dans crontab (`sudo crontab -e`) :
```cron
# Backup quotidien à 3h du matin
0 3 * * * /var/www/parle/backup.sh >> /var/log/parle-backup.log 2>&1
```

### 11.8 Monitoring et logs

```bash
# Logs backend
sudo journalctl -u parle-backend -f

# Logs frontend
sudo journalctl -u parle-frontend -f

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Status des services
sudo systemctl status parle-backend
sudo systemctl status parle-frontend
sudo systemctl status nginx
sudo systemctl status postgresql
```

### 11.9 Sécurité supplémentaire

#### Fail2ban (protection contre brute force)
```bash
sudo apt install fail2ban

# /etc/fail2ban/jail.local
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 5
findtime = 600
bantime = 3600
```

#### Firewall (UFW)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP (redirection)
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
```

---

## 12. Budget et timeline

### Estimation développement
- **MVP complet** : 8-12 semaines (solo developer)
- **Version polished** : +2-4 semaines

### Coûts récurrents (estimés)
- Électricité (machine locale 24/7) : ~5-15$/mois (selon consommation)
- Nom de domaine (optionnel) : ~10-15$/an
- Certificat SSL : Gratuit (Let's Encrypt)
- Internet (bande passante) : Inclus dans abonnement existant
- **Total** : ~5-15$/mois + 10$/an (domaine optionnel)

### Hébergement local - Configuration requise

#### Matériel recommandé
- **CPU** : 4 cores minimum (8+ recommandé)
- **RAM** : 8 GB minimum (16 GB recommandé)
- **Stockage** : 50 GB minimum (SSD recommandé)
- **Connexion** : Upload ≥ 10 Mbps (pour accès mobile fluide)

#### Logiciels système
- **OS** : Ubuntu Server 22.04 LTS ou Debian 12
- **PostgreSQL** : 15+
- **Python** : 3.10+
- **Node.js** : 20 LTS
- **Nginx** ou **Caddy** : Reverse proxy + SSL
- **Certbot** : Certificats SSL automatiques (Let's Encrypt)

---

## 12. Évolutions futures (post-MVP)

### Features avancées
- IA pour correction automatique (OpenAI/Claude)
- Reconnaissance vocale (Web Speech API)
- Community features (partage de decks)
- Mode hors-ligne (PWA)
- Application mobile (React Native)
- Intégration calendrier externe (Google/Outlook)
- Gamification (badges, streaks, leaderboard)

---

**Document créé le** : 24 novembre 2025  
**Version** : 1.0  
**Auteur** : GitHub Copilot (Claude Sonnet 4.5)