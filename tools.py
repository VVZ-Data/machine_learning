"""
tools.py — Outils de l'agent todo_agent
Atelier C. Suire — Devoir 5 Henallux
"""

import json
import os

# ─── Configuration ────────────────────────────────────────────────────────────
TODO_FILE = "todos.json"
VALID_TAGS = ["perso", "travail", "urgent"]
PRIORITY_ORDER = {"urgent": 0, "travail": 1, "perso": 2}


# ─── Persistance ──────────────────────────────────────────────────────────────

def _load_todos() -> list[dict]:
    """Charge la liste des tâches depuis le fichier JSON."""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)


def _save_todos(todos: list[dict]) -> None:
    """Sauvegarde la liste des tâches dans le fichier JSON."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)


def _next_id(todos: list[dict]) -> int:
    """Retourne le prochain ID disponible."""
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1


# ─── Outils CRUD ──────────────────────────────────────────────────────────────

def add_todo(title: str, tag: str = "perso") -> str:
    """Ajoute une nouvelle tâche à la liste.

    Args:
        title: Le titre ou la description de la tâche à ajouter.
        tag: La catégorie de la tâche. Valeurs possibles : "perso", "travail", "urgent".
             Par défaut : "perso".

    Returns:
        Un message de confirmation avec l'ID de la tâche créée,
        ou une erreur si le tag est invalide.
    """
    if tag not in VALID_TAGS:
        return f"Erreur : tag '{tag}' invalide. Valeurs acceptées : {', '.join(VALID_TAGS)}."
    todos = _load_todos()
    new_todo = {
        "id": _next_id(todos),
        "title": title,
        "tag": tag,
        "done": False,
    }
    todos.append(new_todo)
    _save_todos(todos)
    return f"Tâche ajoutée : '{title}' [tag: {tag}] (id: {new_todo['id']})"


def list_todos(tag: str = "all") -> str:
    """Liste les tâches existantes, avec filtre optionnel par tag.

    Args:
        tag: Tag de filtrage. Valeurs possibles : "all" (toutes),
             "perso", "travail", "urgent", "pending" (non terminées), "done" (terminées).

    Returns:
        La liste des tâches formatée en texte lisible, ou un message si aucune tâche.
    """
    todos = _load_todos()
    if not todos:
        return "Aucune tâche enregistrée."

    if tag == "pending":
        todos = [t for t in todos if not t["done"]]
    elif tag == "done":
        todos = [t for t in todos if t["done"]]
    elif tag in VALID_TAGS:
        todos = [t for t in todos if t["tag"] == tag]

    if not todos:
        return f"Aucune tâche pour le filtre '{tag}'."

    lines = []
    for t in todos:
        state = "✅" if t["done"] else "⬜"
        lines.append(f"{state} [{t['id']}] {t['title']} (tag: {t['tag']})")
    return "\n".join(lines)


def complete_todo(todo_id: int) -> str:
    """Marque une tâche comme terminée.

    Args:
        todo_id: L'identifiant numérique de la tâche à terminer.

    Returns:
        Un message de confirmation ou d'erreur si la tâche n'existe pas.
    """
    todos = _load_todos()
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            _save_todos(todos)
            return f"Tâche '{t['title']}' (id: {todo_id}) marquée comme terminée."
    return f"Erreur : aucune tâche trouvée avec l'id {todo_id}."


def delete_todo(todo_id: int) -> str:
    """Supprime définitivement une tâche.

    Args:
        todo_id: L'identifiant numérique de la tâche à supprimer.

    Returns:
        Un message de confirmation ou d'erreur si la tâche n'existe pas.
    """
    todos = _load_todos()
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            removed = todos.pop(i)
            _save_todos(todos)
            return f"Tâche '{removed['title']}' (id: {todo_id}) supprimée."
    return f"Erreur : aucune tâche trouvée avec l'id {todo_id}."


# ─── Outils d'analyse (déterministes) ────────────────────────────────────────

def list_todos_by_priority() -> str:
    """Retourne toutes les tâches non terminées, triées par priorité décroissante.

    L'ordre de priorité est : urgent > travail > perso.

    Returns:
        La liste triée des tâches en attente, ou un message si aucune tâche.
    """
    todos = _load_todos()
    pending = [t for t in todos if not t["done"]]
    if not pending:
        return "Aucune tâche en attente."

    sorted_todos = sorted(pending, key=lambda t: PRIORITY_ORDER.get(t["tag"], 99))
    lines = []
    for t in sorted_todos:
        lines.append(f"[{t['tag'].upper()}] [{t['id']}] {t['title']}")
    return "\n".join(lines)


def group_todos_by_tag() -> str:
    """Retourne toutes les tâches non terminées, regroupées par tag.

    Returns:
        Les tâches organisées par catégorie (urgent, travail, perso),
        ou un message si aucune tâche.
    """
    todos = _load_todos()
    pending = [t for t in todos if not t["done"]]
    if not pending:
        return "Aucune tâche en attente."

    groups: dict[str, list[str]] = {tag: [] for tag in VALID_TAGS}
    for t in pending:
        tag = t.get("tag", "perso")
        if tag in groups:
            groups[tag].append(f"  [{t['id']}] {t['title']}")

    lines = []
    for tag in sorted(VALID_TAGS, key=lambda t: PRIORITY_ORDER[t]):
        if groups[tag]:
            lines.append(f"### {tag.capitalize()}")
            lines.extend(groups[tag])
    return "\n".join(lines) if lines else "Aucune tâche en attente."
