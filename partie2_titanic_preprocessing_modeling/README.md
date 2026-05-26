# Partie 2 — Prétraitement & Modélisation Titanic

## Contenu

### Notebooks
| Fichier | Rôle |
|---------|------|
| `Titanic_preprocessing.ipynb` | Nettoyage, imputation, encodage, export des X/y train/test |
| `Titanic_select.ipynb` | Sélection de features, split par groupe (KB / P / VT) |
| `Titanic_model_*_KNN.ipynb` | Modèles KNN (par groupe) |
| `Titanic_model_*_DecisionTree.ipynb` | Modèles Decision Tree (par groupe) |
| `Titanic_model_*_RandomForest.ipynb` | Modèles Random Forest (par groupe) |
| `Titanic_summary.xlsx` | Comparaison des performances des modèles |

### Données
- `Titanic Dataset.csv` — dataset source
- `X_train.csv`, `X_test.csv`, `X_train_brut.csv`, `X_test_brut.csv` — features train/test
- `y_train.csv`, `y_test.csv` — variable cible
- `xtrain_KB.csv`, `xtest_KB.csv` — split groupe KB
- `xtrain_P.csv`, `xtest_P.csv` — split groupe P
- `xtrain_VT.csv`, `xtest_VT.csv` — split groupe VT

## Dépendances
Tous les notebooks utilisent des chemins relatifs — tous les CSV doivent rester dans ce dossier.
