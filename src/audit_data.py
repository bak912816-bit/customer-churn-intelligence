
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

df = pd.read_csv(DATA_PATH)

# 1. Valeurs manquantes
print("=== VALEURS MANQUANTES ===")
print(df.isna().sum())

# 2. Lignes dupliquées
print("\n=== DOUBLONS ===")
print("Nombre de lignes dupliquées :", df.duplicated().sum())

# 3. Vérifier TotalCharges
print("\n=== TOTALCHARGES ===")
print("Type actuel :", df["TotalCharges"].dtype)
print("Exemples de valeurs :")
print(df["TotalCharges"].head(10).tolist())

# 4. Répartition de la variable cible
print("\n=== CHURN ===")
print(df["Churn"].value_counts())
print("\nProportions :")
print(df["Churn"].value_counts(normalize=True).round(3))

# 5. Détecter les chaînes vides ou composées d'espaces
print("\n=== TOTALCHARGES : VALEURS VIDES ===")

vides = df["TotalCharges"].str.strip().eq("")

print("Nombre de chaînes vides :", vides.sum())
print("\nLignes concernées :")
print(df.loc[vides, ["customerID", "tenure", "MonthlyCharges", "TotalCharges"]])

# 6. Rechercher les chaînes vides et les espaces superflus
print("\n=== ESPACES ET CHAÎNES VIDES ===")

for col in df.select_dtypes(include=["object", "str"]).columns:
    valeurs = df[col].astype("string")

    nb_vides = valeurs.str.strip().eq("").sum()
    nb_espaces = (
        valeurs.notna()
        & valeurs.ne(valeurs.str.strip())
    ).sum()

    if nb_vides > 0 or nb_espaces > 0:
        print(
            f"{col} : {nb_vides} chaîne(s) vide(s), "
            f"{nb_espaces} valeur(s) avec espaces superflus"
        )

# 7. Examiner les valeurs distinctes des colonnes catégorielles
print("\n=== VALEURS DISTINCTES ===")

for col in df.select_dtypes(include=["object", "str"]).columns:
    print(f"\n{col} :")
    print(df[col].value_counts(dropna=False).to_string())

# 8. Rechercher les caractères suspects dans les colonnes numériques attendues
print("\n=== VALEURS NON NUMÉRIQUES SUSPECTES ===")

colonnes_numeriques = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

for col in colonnes_numeriques:
    valeurs = df[col].astype("string").str.strip()
    converties = pd.to_numeric(valeurs, errors="coerce")

    suspects = valeurs.notna() & valeurs.ne("") & converties.isna()

    print(f"\n{col} : {suspects.sum()} valeur(s) non numérique(s)")
    if suspects.any():
        print(df.loc[suspects, ["customerID", col]].to_string(index=False))
