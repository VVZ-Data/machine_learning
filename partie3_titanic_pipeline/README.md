# Partie 3 — Pipeline sklearn Titanic

## Contenu
- `Titanic_pipeline_final.ipynb` : pipeline end-to-end utilisant `sklearn.pipeline.Pipeline` et `ColumnTransformer`.
- `Titanic Dataset.csv` : dataset source (doit rester dans ce dossier).

## Architecture du pipeline

```
Pipeline([
  ('preprocessor', ColumnTransformer([
      ('num', Pipeline([SimpleImputer(median), StandardScaler]), NUM_COLS),
      ('cat', Pipeline([SimpleImputer(mode), OneHotEncoder]),    CAT_COLS)
  ])),
  ('classifier', RandomForestClassifier)
])
```

Le feature engineering (Title, FamilySize, IsAlone, HasCabin) est réalisé en pandas avant le split.  
Toute imputation et encodage est encapsulé dans le Pipeline — pas de data leakage possible.

## Étapes du notebook

1. Importation des bibliothèques
2. Chargement et exploration des données
3. Ingénierie des features (pandas, sur données brutes)
4. Séparation train/test sur données brutes (avec NaN)
5. Construction du Pipeline + ColumnTransformer
6. Optimisation par GridSearchCV (CV 5-fold, scoring F1)
7. Évaluation : métriques, matrice de confusion, importances de features
8. Courbe d'apprentissage et analyse du surapprentissage
9. Conclusion

## Dépendances
```
pandas, numpy, scikit-learn, matplotlib, seaborn
```
