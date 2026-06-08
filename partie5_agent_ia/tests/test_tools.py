"""
tests/test_tools.py — Tests unitaires des outils (déterministes, sans LLM)
"""

import json
import os

import pytest

from revision_agent.tools import (
    SUBJECTS_FILE,
    add_subject,
    get_next_to_revise,
    get_stats,
    list_subjects,
    remove_subject,
    update_status,
)


@pytest.fixture(autouse=True)
def clean_subjects_file():
    if os.path.exists(SUBJECTS_FILE):
        os.remove(SUBJECTS_FILE)
    yield
    if os.path.exists(SUBJECTS_FILE):
        os.remove(SUBJECTS_FILE)


def test_add_subject():
    result = add_subject("Mathématiques", "2025-06-15", "normal")
    assert "id: 1" in result
    assert "Mathématiques" in result

    with open(SUBJECTS_FILE) as f:
        subjects = json.load(f)
    assert len(subjects) == 1
    assert subjects[0]["title"] == "Mathématiques"
    assert subjects[0]["exam_date"] == "2025-06-15"
    assert subjects[0]["priority"] == "normal"
    assert subjects[0]["status"] == "not_started"


def test_add_subject_invalid_priority():
    result = add_subject("Physique", "2025-06-20", "critique")
    assert "Erreur" in result


def test_list_subjects_empty():
    result = list_subjects()
    assert "Aucune" in result


def test_list_subjects_filter_by_status():
    add_subject("Mathématiques", "2025-06-15")
    add_subject("Histoire", "2025-06-20")
    update_status(2, "in_progress")

    result_in_progress = list_subjects("in_progress")
    assert "Histoire" in result_in_progress
    assert "Mathématiques" not in result_in_progress

    result_not_started = list_subjects("not_started")
    assert "Mathématiques" in result_not_started
    assert "Histoire" not in result_not_started


def test_update_status():
    add_subject("Chimie", "2025-07-01")
    result = update_status(1, "in_progress")
    assert "in_progress" in result

    with open(SUBJECTS_FILE) as f:
        subjects = json.load(f)
    assert subjects[0]["status"] == "in_progress"


def test_update_status_invalid():
    add_subject("Biologie", "2025-07-10")
    result = update_status(1, "terminée")
    assert "Erreur" in result


def test_remove_subject():
    add_subject("Géographie", "2025-06-25")
    result = remove_subject(1)
    assert "supprimée" in result
    assert "Aucune" in list_subjects()


def test_remove_subject_not_found():
    result = remove_subject(999)
    assert "Erreur" in result


def test_get_next_to_revise_priority_order():
    add_subject("Normal non commencé", "2025-08-01", "normal")
    add_subject("Soon en cours", "2025-06-10", "soon")
    add_subject("Soon non commencé", "2025-06-05", "soon")
    update_status(2, "in_progress")

    result = get_next_to_revise()
    assert "Soon non commencé" in result


def test_get_next_to_revise_ignores_mastered():
    add_subject("Maîtrisée", "2025-06-01", "soon")
    update_status(1, "mastered")

    result = get_next_to_revise()
    assert "Félicitations" in result
    assert "Maîtrisée" not in result


def test_get_stats():
    add_subject("Maths", "2025-06-15")
    add_subject("Physique", "2025-06-20")
    add_subject("Chimie", "2025-06-25")
    update_status(1, "mastered")
    update_status(2, "in_progress")

    result = get_stats()
    assert "33.3%" in result
    assert "1" in result  # mastered count
    assert "1" in result  # in_progress count
    assert "1" in result  # not_started count
