"""
tests/test_tools.py — Tests unitaires des outils (déterministes, sans LLM)
Atelier C. Suire — Devoir 5 Henallux

Lancement : uv run pytest tests/ -v
"""

import os
import json
import pytest

from todo_agents.tools import (
    add_todo,
    list_todos,
    complete_todo,
    delete_todo,
    list_todos_by_priority,
    group_todos_by_tag,
    TODO_FILE,
)


# ─── Fixture : fichier propre avant/après chaque test ─────────────────────────

@pytest.fixture(autouse=True)
def clean_todo_file():
    """Supprime le fichier de tâches avant et après chaque test."""
    if os.path.exists(TODO_FILE):
        os.remove(TODO_FILE)
    yield
    if os.path.exists(TODO_FILE):
        os.remove(TODO_FILE)


# ─── Tests add_todo ───────────────────────────────────────────────────────────

def test_add_todo():
    result = add_todo("Acheter du lait", "perso")
    assert "id: 1" in result
    assert "Acheter du lait" in result

    with open(TODO_FILE) as f:
        todos = json.load(f)
    assert len(todos) == 1
    assert todos[0]["title"] == "Acheter du lait"
    assert todos[0]["tag"] == "perso"
    assert todos[0]["done"] is False


def test_add_todo_invalid_tag():
    result = add_todo("Tâche", "mauvais_tag")
    assert "Erreur" in result


def test_add_todo_default_tag():
    result = add_todo("Tâche sans tag explicite")
    assert "perso" in result


def test_add_todo_increments_id():
    add_todo("Première", "perso")
    result = add_todo("Deuxième", "travail")
    assert "id: 2" in result


# ─── Tests list_todos ─────────────────────────────────────────────────────────

def test_list_todos_empty():
    assert "Aucune" in list_todos()


def test_list_todos_filter_by_tag():
    add_todo("Tâche perso", "perso")
    add_todo("Tâche travail", "travail")

    result_perso = list_todos("perso")
    assert "Tâche perso" in result_perso
    assert "Tâche travail" not in result_perso

    result_all = list_todos("all")
    assert "Tâche perso" in result_all
    assert "Tâche travail" in result_all


def test_list_todos_pending_and_done():
    add_todo("À faire", "travail")
    add_todo("Faite", "perso")
    complete_todo(2)

    assert "À faire" in list_todos("pending")
    assert "Faite" not in list_todos("pending")
    assert "Faite" in list_todos("done")


# ─── Tests complete_todo ──────────────────────────────────────────────────────

def test_complete_todo():
    add_todo("À terminer", "travail")
    result = complete_todo(1)
    assert "terminée" in result
    assert "À terminer" in list_todos("done")


def test_complete_todo_not_found():
    assert "Erreur" in complete_todo(999)


# ─── Tests delete_todo ────────────────────────────────────────────────────────

def test_delete_todo():
    add_todo("À supprimer", "perso")
    result = delete_todo(1)
    assert "supprimée" in result
    assert "Aucune" in list_todos()


def test_delete_todo_not_found():
    assert "Erreur" in delete_todo(999)


# ─── Tests list_todos_by_priority ─────────────────────────────────────────────

def test_list_todos_by_priority():
    add_todo("Tâche perso", "perso")
    add_todo("Tâche urgente", "urgent")
    add_todo("Tâche travail", "travail")

    result = list_todos_by_priority()
    lines = result.splitlines()
    assert "URGENT" in lines[0]
    assert "PERSO" in lines[-1]


def test_list_todos_by_priority_excludes_done():
    add_todo("Tâche urgente terminée", "urgent")
    complete_todo(1)
    add_todo("Tâche perso", "perso")

    result = list_todos_by_priority()
    assert "urgente terminée" not in result
    assert "perso" in result.lower()


def test_list_todos_by_priority_empty():
    assert "Aucune" in list_todos_by_priority()


# ─── Tests group_todos_by_tag ─────────────────────────────────────────────────

def test_group_todos_by_tag():
    add_todo("Tâche perso", "perso")
    add_todo("Tâche travail", "travail")
    add_todo("Tâche urgente", "urgent")

    result = group_todos_by_tag()
    idx_urgent  = result.index("Urgent")
    idx_travail = result.index("Travail")
    idx_perso   = result.index("Perso")
    assert idx_urgent < idx_travail < idx_perso


def test_group_todos_by_tag_excludes_done():
    add_todo("Urgente terminée", "urgent")
    complete_todo(1)
    add_todo("Perso active", "perso")

    result = group_todos_by_tag()
    assert "Urgente terminée" not in result
    assert "Perso active" in result
