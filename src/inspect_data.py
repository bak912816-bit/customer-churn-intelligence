from pathlib import Path
import pandas as pd

# Chemin vers le fichier CSV
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

# Charger les données
df = pd.read_csv(DATA_PATH)

# Examiner le dataset
print("Dimensions :", df.shape)
print("\nPremières lignes :")
print(df.head())

print("\nColonnes :")
print(df.columns.tolist())

print("\nTypes de données :")
print(df.dtypes)