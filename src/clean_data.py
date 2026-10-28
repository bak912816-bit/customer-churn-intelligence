
from pathlib import Path
import pandas as pd

# 1. Définir les chemins
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "telco_clean.csv"

# 2. Charger les données brutes
df = pd.read_csv(DATA_PATH)

# 3. Nettoyer TotalCharges
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"].str.strip(),
    errors="coerce"
)

# 4. Vérifier le nettoyage
print("=== APRÈS NETTOYAGE ===")
print("Dimensions :", df.shape)
print("\nValeurs manquantes :")
print(df.isna().sum()[df.isna().sum() > 0])

# 5. Enregistrer les données nettoyées
df.to_csv(OUTPUT_PATH, index=False)

print("\nFichier enregistré :", OUTPUT_PATH)
