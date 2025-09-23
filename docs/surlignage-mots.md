# Fonctionnalité de Surlignage des Mots

## Vue d'ensemble

La nouvelle fonctionnalité de surlignage permet d'afficher directement dans le texte l'état de prononciation de chaque mot, remplaçant la section "Erreurs Détectées" séparée.

## Système de Couleurs

- 🟢 **Vert** (`word-correct`) : Mots correctement prononcés
- � **Jaune** (`word-similar`) : Mots presque corrects (similarité > 50%)
- �🔴 **Rouge** (`word-error`) : Mots mal prononcés ou avec erreurs importantes
- ⚫ **Normal** : Mots non prononcés (couleur de texte par défaut)

## Logique d'Implémentation

### 1. Identification des Mots

```javascript
// Mots avec erreurs importantes (API response)
errorWords = Set(['mot1', 'mot2'])

// Mots prononcés (transcription)
pronouncedWords = Set(['savons', 'mot3', 'mot4'])

// Mots similaires (presque corrects) - Exemple: "avons" attendu, "savons" prononcé
similarWords = Set(['avons']) // détecté via similarité > 50%

// Mots corrects = prononcés exactement - erreurs
correctWords = Set(['mot3', 'mot4'])
```

### 2. Affichage

```vue
<span :class="getWordClass(part)">{{ part.text }}</span>
```

### 3. Classes CSS

```css
.word-error {
  background-color: #fef0f0;
  color: #f56c6c;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 500;
}

.word-similar {
  background-color: #fefce8;
  color: #eab308;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 500;
}

.word-correct {
  background-color: #f0f9ff;
  color: #67c23a;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 500;
}
```

## Tooltip d'Information

Les mots avec erreurs affichent un tooltip au survol avec des détails :
- Type d'erreur (deletion, mispronunciation, substitution)
- Mot attendu vs mot prononcé
- Niveau de sévérité

## Avantages

1. **Feedback visuel immédiat** : L'utilisateur voit directement dans le texte les mots problématiques
2. **Interface épurée** : Suppression de la section séparée des erreurs
3. **Meilleure UX** : Correspondance directe entre le texte lu et le feedback
4. **Détection de similarité** : Reconnaissance des efforts même imparfaits ("avons" vs "savons")
5. **Conformité aux spécifications** : Implémentation selon `spec.txt`

## Fichiers Modifiés

- `frontend/src/views/Reading.vue` : Interface principale de lecture
- `frontend/src/components/AudioRecorder.vue` : Composant d'enregistrement
- Suppression de la section "Erreurs Détectées" dans l'interface de lecture
- Conservation de la liste d'erreurs dans `Summary.vue` (contexte différent)