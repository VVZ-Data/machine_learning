# Rapport — Agent IA (Todo-agent)

**Projet Machine Learning — 2INTAR**  
**Devoir 5**

---

## 1. Contexte

Ce travail s'appuie intégralement sur l'atelier animé par **Cyrille Suire (IUT de La Rochelle)** lors de sa venue à Henallux en avril 2026. Nous avons reproduit à l'identique le **todo-agent** décrit dans sa fiche de laboratoire : un agent de gestion de tâches construit avec **Google ADK**, tournant sur un modèle local via **Ollama** (`qwen3.5:4b`), avec des outils CRUD complets et une persistance JSON. L'objectif n'était pas d'innover sur l'architecture mais de comprendre et maîtriser chaque composant — environnement `uv`, boucle agentique ReAct, function calling, system prompt — avant d'envisager des extensions.

---

## 2. Utilisation de l'IA générative

L'outil utilisé est **Claude (Anthropic)**. Notre approche a été identique à celle adoptée pour le devoir 4 : nous ne délégions pas la réflexion à l'IA, nous lui dictitions nos intentions par vocal en étant aussi précis et détaillés que possible dans nos instructions, de façon à minimiser les allers-retours et donc le coût en tokens — ressource coûteuse qu'il faut gérer consciencieusement.

### Rôle de l'IA sur le code

Le labo de M. Suire fournissait une structure claire et des extraits de code. L'IA intervenait sur des points précis où nous avions un doute ou un blocage : formulation d'une docstring correcte pour qu'ADK l'expose bien au LLM, gestion des cas d'erreur dans les fonctions de persistance JSON, ou encore compréhension du comportement du `Runner` ADK dans les tests. Dans ces cas, nous décrivions précisément le comportement attendu et l'IA produisait le code correspondant, que nous relisions, comprenions et intégrions.

### Rôle de l'IA sur le system prompt

La rédaction du system prompt a été un exercice de prompt engineering à part entière. Nous soumettions une version à l'IA en lui demandant d'en identifier les faiblesses — par exemple : est-ce que cette formulation suffit pour empêcher l'agent de répondre à des questions hors-périmètre ? Elle nous listait les points forts et les points faibles, ce qui nous permettait soit de valider notre approche, soit de l'affiner. La décision finale restait toujours la nôtre.

### Rôle de l'IA sur les tests

Les tests comportementaux (partie adversariale) requièrent une certaine créativité dans les requêtes de refus. Nous avons demandé à l'IA de proposer des cas limites pertinents, puis nous avons sélectionné et reformulé ceux qui nous semblaient les plus révélateurs du comportement de notre agent.

---

## 3. Analyse réflexive

Travailler sur un agent IA en s'appuyant sur une IA pour le construire crée une mise en abyme intéressante. Il était d'autant plus important de rester rigoureux sur notre posture : **nous concevions, l'IA exécutait**. Pourquoi le function calling échoue sur certains modèles de petite taille, pourquoi un system prompt trop permissif laisse passer des requêtes hors-périmètre — tout cela ne pouvait pas être délégué. Ce sont précisément ces mécanismes qui font l'objet de l'évaluation.

L'IA nous a été utile comme **interlocuteur critique** : nous lui présentions une approche, elle en évaluait la solidité. Cela nous a parfois évité des impasses techniques (mauvaise signature de fonction, mauvais placement des `async`) et nous a conduits à reconsidérer certains choix de formulation dans le system prompt. Mais dans tous les cas, le raisonnement et la décision finale étaient les nôtres.

Un point de vigilance notable : les tests comportementaux sur LLM sont **non-déterministes par nature**. Un test de refus peut passer dix fois puis échouer sur la onzième requête sans que le code ait changé. L'IA ne nous a pas alertés spontanément sur cette propriété — c'est le labo de M. Suire qui en faisait explicitement un point pédagogique. Cela illustre qu'une IA générative n'est pas un bon juge de ses propres limites : la supervision humaine et le recours aux ressources pédagogiques primaires restent indispensables.

Nous n'avons malheureusement pas pu faire tourner l'agent en conditions réelles : nos machines ne disposaient pas de la puissance nécessaire pour exécuter le modèle local de façon stable. C'est un regret, car les observations sur le comportement de qwen3.5:4b évoquées dans le labo auraient été particulièrement instructives à constater par nous-mêmes. Nous restons néanmoins satisfaits du travail de réflexion mené autour du system prompt et de la conception des tests comportementaux, qui constituent selon nous la part la plus structurante de cet exercice.

---

## 4. Organisation des tests

Deux niveaux de tests ont été mis en place, conformément à la structure du labo.

**Tests unitaires des outils** (`tests/test_tools.py`) : ces tests vérifient le comportement des fonctions Python de façon déterministe et sans appel au LLM. Ils couvrent l'ajout d'une tâche (`add_todo`), la liste des tâches (`list_todos`), le marquage comme terminé (`complete_todo`) et la suppression (`delete_todo`). Ils sont rapides, reproductibles, et ne dépendent pas de la disponibilité du modèle.

**Tests comportementaux de l'agent** (`tests/test_agent_behavior.py`) : ces tests envoient de vraies requêtes au LLM via le `Runner` ADK. Deux catégories sont couvertes. Les tests de **refus** vérifient qu'aucun outil n'est appelé pour des requêtes hors-périmètre (météo, calcul mathématique, poème, question sportive) — le check sur l'absence d'appel d'outil est retenu car il est plus robuste qu'un check sur la formulation textuelle du refus. Les tests **positifs** vérifient que l'agent appelle bien un outil pour une demande d'ajout ou de liste de tâches. Ces tests sont lents (5 à 15 secondes par test) et occasionnellement non-déterministes : un échec ponctuel est informatif, pas nécessairement bloquant.
