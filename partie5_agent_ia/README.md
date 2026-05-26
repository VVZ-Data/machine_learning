# Partie 5 — Agent IA (Todo List)

Agent de gestion de tâches construit avec **Google ADK** et **Ollama** (qwen3.5:4b),
dans le cadre de l'atelier de M. Suire (Henallux — Devoir 5).

---

## Structure du projet

```
partie5_agent_ia/
├── pyproject.toml                 # Dépendances et config pytest (méthode recommandée)
├── requirements.txt               # Alternative pip si uv n'est pas disponible
├── todo_agents/
│   ├── __init__.py
│   ├── agent.py                   # Définition de l'agent (modèle, system prompt, outils)
│   └── tools.py                   # Outils CRUD + priorisation + regroupement
└── tests/
    ├── __init__.py
    ├── utils.py                   # Utilitaire ask_agent() pour les tests comportementaux
    ├── test_tools.py              # Tests unitaires (sans LLM) — 16 tests
    └── test_agent_behavior.py     # Tests comportementaux (avec LLM) — 9 tests
```

---

## Prérequis

### 1. Python 3.13+

Vérifiez : `python --version`

### 2. uv (gestionnaire de paquets recommandé)

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Vérifiez : `uv --version`

### 3. Ollama + modèle qwen3.5:4b

Téléchargez Ollama sur [ollama.com](https://ollama.com), installez-le, puis :

```bash
ollama pull qwen3.5:4b
```

Vérifiez que le modèle est bien présent :

```bash
ollama list
```

---

## Installation

Placez-vous dans le dossier du projet :

```powershell
cd partie5_agent_ia
```

### Méthode recommandée — uv

```powershell
uv sync
```

### Méthode alternative — pip

```powershell
pip install -r requirements.txt
```

---

## Lancer l'agent

Ollama doit tourner en arrière-plan (vérifiez l'icône dans la barre des tâches,
ou lancez `ollama serve` dans un terminal séparé).

```powershell
uv run adk web
```

Puis ouvrez **http://localhost:8000** dans votre navigateur.
Sélectionnez `todo_agent` et commencez à converser.

Pour arrêter : `Ctrl+C` dans le terminal.

---

## Lancer les tests

### Tests unitaires (sans LLM — rapides et déterministes)

```powershell
uv run pytest tests/test_tools.py -v
```

Pour sauvegarder les résultats dans un fichier :

```powershell
uv run pytest tests/test_tools.py -v 2>&1 | Tee-Object test_results.txt
```

Résultat attendu : **16/16 PASSED**

### Tests comportementaux (avec LLM — nécessite Ollama)

```powershell
uv run pytest tests/test_agent_behavior.py -v
```

> Ces tests sont non-déterministes : ils appellent le vrai LLM et peuvent
> prendre 5 à 15 secondes par test. Ils peuvent occasionnellement échouer
> sur des requêtes ambiguës — c'est normal et attendu.

---

## Outils disponibles

| Outil | Type | Description |
|-------|------|-------------|
| `add_todo` | CRUD | Ajoute une tâche avec titre et tag |
| `list_todos` | CRUD | Liste les tâches, filtrables par tag ou statut |
| `complete_todo` | CRUD | Marque une tâche comme terminée |
| `delete_todo` | CRUD | Supprime une tâche (confirmation demandée) |
| `list_todos_by_priority` | Analyse | Trie les tâches : urgent > travail > perso |
| `group_todos_by_tag` | Analyse | Regroupe les tâches par catégorie |

---

## Exemples de conversations

```
"Ajoute une tâche : envoyer le rapport, tag travail"
"Qu'est-ce que j'ai à faire ?"
"Par quoi je dois commencer ?"
"Montre-moi mes tâches par catégorie"
"J'ai fini la tâche 1"
"Supprime toutes les tâches terminées"
```
