import json
import os

SUBJECTS_FILE = "subjects.json"
VALID_PRIORITIES = ["soon", "normal"]
VALID_STATUSES = ["not_started", "in_progress", "mastered"]


def _load_subjects() -> list[dict]:
    if not os.path.exists(SUBJECTS_FILE):
        return []
    with open(SUBJECTS_FILE, "r") as f:
        return json.load(f)


def _save_subjects(subjects: list[dict]) -> None:
    with open(SUBJECTS_FILE, "w") as f:
        json.dump(subjects, f, indent=2, ensure_ascii=False)


def _next_id(subjects: list[dict]) -> int:
    if not subjects:
        return 1
    return max(s["id"] for s in subjects) + 1


def add_subject(title: str, exam_date: str, priority: str = "normal") -> str:
    """Ajoute une matière à réviser avec sa date d'examen et sa priorité.

    Args:
        title: Le nom de la matière (ex. "Mathématiques", "Histoire").
        exam_date: La date de l'examen au format YYYY-MM-DD (ex. "2025-06-15").
        priority: L'urgence de la matière. Valeurs acceptées : "soon" (examen
                  proche, dans les jours/semaines à venir) ou "normal".
                  Par défaut : "normal".

    Returns:
        Un message de confirmation avec l'id créé, ou un message d'erreur
        si la priorité est invalide.
    """
    if priority not in VALID_PRIORITIES:
        return f"Erreur : priorité '{priority}' invalide. Valeurs acceptées : {', '.join(VALID_PRIORITIES)}."
    subjects = _load_subjects()
    new_subject = {
        "id": _next_id(subjects),
        "title": title,
        "exam_date": exam_date,
        "priority": priority,
        "status": "not_started",
    }
    subjects.append(new_subject)
    _save_subjects(subjects)
    return f"Matière ajoutée : '{title}' [examen : {exam_date}, priorité : {priority}] (id: {new_subject['id']})"


def remove_subject(subject_id: int) -> str:
    """Supprime définitivement une matière par son identifiant.

    Cette opération est irréversible. Une confirmation explicite de
    l'utilisateur doit être obtenue avant d'appeler cet outil.

    Args:
        subject_id: L'identifiant numérique de la matière à supprimer.

    Returns:
        Un message de confirmation, ou un message d'erreur si l'id est
        introuvable.
    """
    subjects = _load_subjects()
    for i, s in enumerate(subjects):
        if s["id"] == subject_id:
            removed = subjects.pop(i)
            _save_subjects(subjects)
            return f"Matière '{removed['title']}' (id: {subject_id}) supprimée."
    return f"Erreur : aucune matière trouvée avec l'id {subject_id}."


def list_subjects(status: str = "all") -> str:
    """Liste les matières enregistrées avec un filtre optionnel par statut.

    Args:
        status: Filtre par statut. Valeurs acceptées : "all" (toutes),
                "not_started" (non commencées), "in_progress" (en cours),
                "mastered" (maîtrisées). Par défaut : "all".

    Returns:
        La liste des matières formatée, ou un message si aucune matière
        ne correspond au filtre.
    """
    subjects = _load_subjects()
    if not subjects:
        return "Aucune matière enregistrée."

    if status != "all":
        subjects = [s for s in subjects if s["status"] == status]

    if not subjects:
        return f"Aucune matière avec le statut '{status}'."

    lines = []
    for s in subjects:
        lines.append(
            f"[{s['id']}] {s['title']} | examen : {s['exam_date']} | priorité : {s['priority']} | statut : {s['status']}"
        )
    return "\n".join(lines)


def update_status(subject_id: int, status: str) -> str:
    """Met à jour le statut de révision d'une matière.

    Args:
        subject_id: L'identifiant numérique de la matière à mettre à jour.
        status: Le nouveau statut. Valeurs acceptées : "not_started"
                (non commencée), "in_progress" (en cours), "mastered"
                (maîtrisée).

    Returns:
        Un message de confirmation, ou un message d'erreur si l'id est
        introuvable ou le statut invalide.
    """
    if status not in VALID_STATUSES:
        return f"Erreur : statut '{status}' invalide. Valeurs acceptées : {', '.join(VALID_STATUSES)}."
    subjects = _load_subjects()
    for s in subjects:
        if s["id"] == subject_id:
            s["status"] = status
            _save_subjects(subjects)
            return f"Statut de '{s['title']}' (id: {subject_id}) mis à jour : {status}."
    return f"Erreur : aucune matière trouvée avec l'id {subject_id}."


def get_next_to_revise() -> str:
    """Retourne la prochaine matière à réviser selon la priorité et le statut.

    La logique de sélection, par ordre décroissant d'urgence :
      1. priority="soon"   + status="not_started"
      2. priority="soon"   + status="in_progress"
      3. priority="normal" + status="not_started"
      4. priority="normal" + status="in_progress"

    Les matières avec status="mastered" sont ignorées.

    Returns:
        Un message décrivant la matière à attaquer en priorité, un message
        de félicitations si tout est maîtrisé, ou un message si aucune
        matière n'est enregistrée.
    """
    subjects = _load_subjects()
    if not subjects:
        return "Aucune matière enregistrée. Commence par en ajouter une !"

    candidates = [s for s in subjects if s["status"] != "mastered"]
    if not candidates:
        return "Félicitations ! Tu as maîtrisé toutes tes matières."

    priority_order = [
        ("soon", "not_started"),
        ("soon", "in_progress"),
        ("normal", "not_started"),
        ("normal", "in_progress"),
    ]
    for priority, status in priority_order:
        for s in candidates:
            if s["priority"] == priority and s["status"] == status:
                return (
                    f"Prochaine matière à réviser : '{s['title']}' "
                    f"[examen : {s['exam_date']}, priorité : {s['priority']}, statut : {s['status']}] (id: {s['id']})"
                )

    return "Aucune matière à réviser trouvée."


def get_stats() -> str:
    """Retourne un résumé statistique de la progression des révisions.

    Affiche le nombre total de matières, le décompte par statut et le
    pourcentage de progression globale (matières maîtrisées / total).

    Returns:
        Un résumé textuel des statistiques, ou un message si aucune
        matière n'est enregistrée.
    """
    subjects = _load_subjects()
    if not subjects:
        return "Aucune matière enregistrée."

    total = len(subjects)
    counts = {s: 0 for s in VALID_STATUSES}
    for s in subjects:
        counts[s["status"]] += 1

    progress = (counts["mastered"] / total) * 100
    return (
        f"Progression globale : {progress:.1f}% ({counts['mastered']}/{total} matières maîtrisées)\n"
        f"  - Non commencées : {counts['not_started']}\n"
        f"  - En cours       : {counts['in_progress']}\n"
        f"  - Maîtrisées     : {counts['mastered']}"
    )
