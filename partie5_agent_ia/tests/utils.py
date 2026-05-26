"""
tests/utils.py — Utilitaire pour les tests comportementaux de l'agent
Atelier C. Suire — Devoir 5 Henallux
"""

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def ask_agent(agent, message: str) -> tuple[str, bool]:
    """Envoie un message à l'agent et retourne (réponse, outil_appelé).

    Args:
        agent       : L'instance Agent ADK à interroger.
        message     : Le message en langage naturel à envoyer.

    Returns:
        response_text  : Le texte de la réponse finale de l'agent.
        tool_was_called: True si au moins un outil a été invoqué.
    """
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name="test_behavioral",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_behavioral",
        user_id="test_user",
    )
    content = types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )

    response_text = ""
    tool_was_called = False

    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=content,
    ):
        if event.content:
            for part in event.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_was_called = True
                if hasattr(part, "text") and part.text:
                    response_text += part.text

    return response_text, tool_was_called
