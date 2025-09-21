-- Script d'initialisation de la base de données Parle
-- Création des tables et données de base

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des textes
CREATE TABLE IF NOT EXISTS texts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    paragraphs TEXT, -- JSON string des paragraphes
    language VARCHAR(10) DEFAULT 'fr',
    confidence FLOAT DEFAULT 0.0,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des lectures
CREATE TABLE IF NOT EXISTS readings (
    id SERIAL PRIMARY KEY,
    text_id INTEGER REFERENCES texts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    audio_file VARCHAR(255) NOT NULL,
    transcription TEXT,
    confidence FLOAT DEFAULT 0.0,
    errors TEXT, -- JSON string des erreurs
    prosody TEXT, -- JSON string des données prosodiques
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des résumés
CREATE TABLE IF NOT EXISTS summaries (
    id SERIAL PRIMARY KEY,
    text_id INTEGER REFERENCES texts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    audio_file VARCHAR(255) NOT NULL,
    transcription TEXT,
    relevance_score FLOAT DEFAULT 0.0,
    quality_score FLOAT DEFAULT 0.0,
    suggestions TEXT, -- JSON string des suggestions
    errors TEXT, -- JSON string des erreurs
    transitions TEXT, -- JSON string des transitions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des statistiques
CREATE TABLE IF NOT EXISTS stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    total_readings INTEGER DEFAULT 0,
    total_summaries INTEGER DEFAULT 0,
    average_confidence FLOAT DEFAULT 0.0,
    common_errors TEXT, -- JSON string des erreurs fréquentes
    improvement_areas TEXT, -- JSON string des domaines d'amélioration
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_texts_user_id ON texts(user_id);
CREATE INDEX IF NOT EXISTS idx_readings_user_id ON readings(user_id);
CREATE INDEX IF NOT EXISTS idx_readings_text_id ON readings(text_id);
CREATE INDEX IF NOT EXISTS idx_summaries_user_id ON summaries(user_id);
CREATE INDEX IF NOT EXISTS idx_summaries_text_id ON summaries(text_id);
CREATE INDEX IF NOT EXISTS idx_stats_user_id ON stats(user_id);
CREATE INDEX IF NOT EXISTS idx_stats_date ON stats(date);

-- Fonction pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insertion d'un utilisateur de test
INSERT INTO users (email, username, hashed_password, is_active) 
VALUES (
    'test@parle.com', 
    'test_user', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8.8.8.8', -- mot de passe: test123
    TRUE
) ON CONFLICT (email) DO NOTHING;

-- Insertion d'un texte de test
INSERT INTO texts (title, content, paragraphs, language, confidence, user_id)
VALUES (
    'Texte de test',
    'Ceci est un texte de test pour l''application Parle. Il contient plusieurs paragraphes pour permettre de tester les fonctionnalités de lecture et de résumé.',
    '["Ceci est un texte de test pour l''application Parle.", "Il contient plusieurs paragraphes pour permettre de tester les fonctionnalités de lecture et de résumé."]',
    'fr',
    95.0,
    1
) ON CONFLICT DO NOTHING;
