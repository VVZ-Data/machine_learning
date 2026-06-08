"""
tests/test_agent_behavior.py — Tests comportementaux de l'agent (avec LLM)

Ces tests sont non-déterministes : ils font appel au vrai LLM via Ollama.
Stratégie principale : vérifier qu'aucun outil n'est appelé sur une requête
hors-périmètre (plus fiable que la vérification de mots-clés dans la réponse).

Prérequis : ollama serve + qwen3:4b chargé
Lancement  : uv run pytest tests/test_agent_behavior.py -v -s
"""

import os

import pytest

from revision_agent.agent import root_agent
from revision_agent.tools import SUBJECTS_FILE, add_subject
from tests.utils import ask_agent


@pytest.fixture(autouse=True)
def clean_subjects_file():
    if os.path.exists(SUBJECTS_FILE):
        os.remove(SUBJECTS_FILE)
    yield
    if os.path.exists(SUBJECTS_FILE):
        os.remove(SUBJECTS_FILE)


# ─── Tests de refus (hors périmètre) ─────────────────────────────────────────

async def test_refuse_meteo():
    response, tool_called = await ask_agent(root_agent, "Quel temps fait-il à Bruxelles ?")
    print(f"\n[météo] réponse : {response[:120]}")
    assert not tool_called, "L'agent ne doit pas appeler d'outil pour une question météo"


async def test_refuse_calcul():
    response, tool_called = await ask_agent(root_agent, "Combien font 357 multiplié par 48 ?")
    print(f"\n[calcul] réponse : {response[:120]}")
    assert not tool_called, "L'agent ne doit pas appeler d'outil pour un calcul général"


async def test_refuse_poeme():
    response, tool_called = await ask_agent(root_agent, "Écris-moi un poème sur la mer.")
    print(f"\n[poème] réponse : {response[:120]}")
    assert not tool_called, "L'agent ne doit pas appeler d'outil pour une demande de poème"


# ─── Tests positifs (dans le périmètre) ──────────────────────────────────────

async def test_add_subject_appelle_outil():
    response, tool_called = await ask_agent(
        root_agent, "Ajoute la matière Mathématiques, examen le 2025-06-15."
    )
    print(f"\n[ajout] réponse : {response[:120]}")
    assert tool_called, "L'agent doit appeler add_subject"


async def test_list_subjects_appelle_outil():
    add_subject("Physique", "2025-06-20")
    response, tool_called = await ask_agent(root_agent, "Montre-moi mes matières à réviser.")
    print(f"\n[liste] réponse : {response[:120]}")
    assert tool_called, "L'agent doit appeler list_subjects"


async def test_next_to_revise_appelle_outil():
    add_subject("Histoire", "2025-06-18", "soon")
    add_subject("Géographie", "2025-07-10", "normal")
    response, tool_called = await ask_agent(root_agent, "Par quoi je dois commencer à réviser ?")
    print(f"\n[priorité] réponse : {response[:120]}")
    assert tool_called, "L'agent doit appeler get_next_to_revise"
