
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "processed" / "telco_clean.csv"

df = pd.read_csv(DATA_PATH)

# 1. Taux de départ des clients
print("=== TAUX DE CHURN ===")
print(df["Churn"].value_counts(normalize=True).mul(100).round(2))

# 2. Statistiques principales
print("\n=== STATISTIQUES ===")
print(df[["tenure", "MonthlyCharges", "TotalCharges"]].describe().round(2))

# 3. Départs selon le type de contrat
print("\n=== CHURN SELON LE CONTRAT (%) ===")
print(pd.crosstab(df["Contract"], df["Churn"], normalize="index").mul(100).round(2))

# 4. Départs selon l'ancienneté
df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=["0-12 mois", "13-24 mois", "25-48 mois", "49-72 mois"]
)

print("\n=== CHURN SELON L'ANCIENNETÉ (%) ===")
print(pd.crosstab(df["TenureGroup"], df["Churn"], normalize="index").mul(100).round(2))
