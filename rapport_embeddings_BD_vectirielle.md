# Rapport — Embeddings & Bases de données vectorielles

**Projet Machine Learning — 2INTAR**  
**Devoir 4**

---

## 1. Utilisation de l'IA générative

L'outil utilisé tout au long de ce travail est **Claude (Anthropic)**. Notre approche a été de ne jamais déléguer la réflexion à l'IA, mais de l'utiliser comme un exécutant capable et critique. Concrètement, nous dictitions nos idées par vocal en étant aussi précis que possible dans nos instructions, ce qui nous permettait de minimiser les allers-retours et donc le coût en tokens — l'utilisation de l'IA représentant une ressource non négligeable qu'il faut gérer avec soin.

### Tokenisation sans ponctuation

La consigne demandait explicitement de s'appuyer sur une IA pour cette partie. Nous avons demandé à Claude de proposer une fonction Python de tokenisation ignorant la ponctuation tout en conservant les caractères accentués. La première suggestion était `re.sub(r"[^\w\s]", " ", texte, flags=re.UNICODE)` combinée à un filtre `not t.isdigit()`. Nous avons identifié une limite : le métacaractère `\w` inclut chiffres et underscores, ce qui laissait passer des tokens mixtes comme `'90km'` ou `'1er'`. Nous avons soumis ce constat à l'IA, qui a confirmé le problème et proposé plusieurs alternatives. Nous avons retenu `re.findall(r'[a-zA-ZÀ-ÿ]+', texte.lower())`, qui ne conserve que des séquences de lettres pures. Cette itération illustre qu'il faut toujours tester et comprendre le code suggéré avant de l'intégrer.

### Génération des fichiers Word de test

Les trois articles `.docx` utilisés comme données de test ont été générés par Claude, avec des contenus réalistes pour les catégories **sport** et **cuisine**, ainsi qu'un article volontairement ambigu (Tour de France + nutrition sportive) pour tester les cas limites du système.

---

## 2. Analyse réflexive

Notre posture vis-à-vis de l'IA a été constante : **nous pensions, l'IA exécutait**. Nous ne lui avons pas demandé de concevoir l'architecture du projet ni de choisir nos outils — ces décisions nous appartenaient. L'IA intervenait sur des points précis où son aide avait une vraie valeur ajoutée technique (regex Unicode, génération de données de test) sans valeur pédagogique directe pour nous.

Un aspect important de notre méthode : nous soumettons régulièrement nos idées à la critique de l'IA avant de les implémenter. Nous lui présentions un choix ou une approche envisagée, et elle nous en exposait les points forts et les points faibles. Cela nous a permis soit de confirmer nos intuitions, soit de les remettre en question et de rebondir sur de nouvelles pistes — mais toujours dans le cadre d'une réflexion qui restait la nôtre. L'IA n'a jamais été une source de décision, plutôt un interlocuteur technique permettant d'affiner notre jugement.

La limite principale du système construit reste sa fragilité : avec seulement 2 articles de référence dans FAISS, un article ambigu peut facilement être mal classifié. En production, il faudrait alimenter la base vectorielle avec plusieurs dizaines d'articles par catégorie pour obtenir une classification robuste.

---

## 3. Organisation des tests

Quatre tests ont été réalisés pour valider le système de bout en bout.

**Test unitaire — tokenisation** : exécuté inline dans le notebook, il valide que la fonction `tokeniser()` retourne bien des tokens sans ponctuation, sans chiffres isolés et en minuscules.

**Classification sport** (`article_sport.docx`) : article clairement sportif, résultat attendu `sport`. Sert à valider le chemin nominal de détection.

**Classification cuisine** (`article_cuisine.docx`) : article clairement culinaire, résultat attendu `cuisine`. Symétrique du test précédent.

**Cas limite** (`article_test.docx`) : article volontairement ambigu mêlant cyclisme (Tour de France) et nutrition. Le résultat n'est pas prédéfini — ce test explore le comportement du système aux frontières et met en évidence ses limites avec une base FAISS de taille minimale.
