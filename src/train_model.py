
from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "processed" / "telco_clean.csv"

# 1. Charger les données nettoyées
df = pd.read_csv(DATA_PATH)

# 2. Séparer la cible des variables explicatives
X = df.drop(columns=["Churn", "customerID"])
y = df["Churn"].map({"No": 0, "Yes": 1})

# 3. Identifier les variables catégorielles
categorical_cols = X.select_dtypes(
    include=["object", "str", "category"]
).columns

# 4. Transformer les catégories en colonnes numériques
X = pd.get_dummies(X, columns=categorical_cols, dtype=int)

# 5. Traiter les valeurs manquantes restantes
X = X.fillna(X.median(numeric_only=True))

# 6. Séparer les données en entraînement et test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("=== PRÉPARATION DES DONNÉES ===")
print("Nombre total de clients :", len(df))
print("Variables après transformation :", X.shape[1])
print("Taille de l'entraînement :", X_train.shape)
print("Taille du test :", X_test.shape)
print("\nRépartition de la cible :")
print(y.value_counts())
print("\nValeurs manquantes dans X :", X.isna().sum().sum())



# 7. Entraîner le modèle équilibré
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    )
)

model.fit(X_train, y_train)

# 8. Obtenir les probabilités de départ
probabilites = model.predict_proba(X_test)[:, 1]

# 9. Comparer plusieurs seuils de décision
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

seuils = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]

print("\n=== OPTIMISATION DU SEUIL ===")

for seuil in seuils:
    y_pred = (probabilites >= seuil).astype(int)

    print(f"\n--- Seuil : {seuil:.2f} ---")
    print("Accuracy :", round(accuracy_score(y_test, y_pred), 4))
    print("Precision :", round(precision_score(y_test, y_pred, zero_division=0), 4))
    print("Recall :", round(recall_score(y_test, y_pred, zero_division=0), 4))
    print("F1-score :", round(f1_score(y_test, y_pred, zero_division=0), 4))
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))
# Seuil retenu provisoirement
seuil_optimal = 0.55

y_pred = (probabilites >= seuil_optimal).astype(int)

print("\n=== MODÈLE FINAL : SEUIL 0.55 ===")
print("Recall :", round(recall_score(y_test, y_pred), 4))
print("Precision :", round(precision_score(y_test, y_pred), 4))
print("F1-score :", round(f1_score(y_test, y_pred), 4))
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))


# Variables les plus associées au churn
logistic_model = model.named_steps["logisticregression"]

coefficients = pd.DataFrame({
    "variable": X.columns,
    "coefficient": logistic_model.coef_[0]
})

coefficients = coefficients.sort_values(
    by="coefficient",
    ascending=False
)

print("\n=== TOP 10 : ASSOCIATION POSITIVE AVEC LE CHURN ===")
print(coefficients.head(10).to_string(index=False))

print("\n=== TOP 10 : ASSOCIATION NÉGATIVE AVEC LE CHURN ===")
print(
    coefficients.tail(10)
    .sort_values("coefficient")
    .to_string(index=False)
)



