
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "processed" / "telco_clean.csv"
FIGURES_DIR = ROOT / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Graphique 1 : churn selon le contrat
churn_contract = (
    pd.crosstab(df["Contract"], df["Churn"], normalize="index")["Yes"] * 100
).sort_values()

churn_contract.plot(kind="bar", title="Churn rate by contract type")
plt.ylabel("Churn rate (%)")
plt.xlabel("Contract type")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "churn_by_contract.png", dpi=150)
plt.close()

# Graphique 2 : churn selon l'ancienneté
df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=["0-12 months", "13-24 months", "25-48 months", "49-72 months"]
)

churn_tenure = (
    pd.crosstab(df["TenureGroup"], df["Churn"], normalize="index")["Yes"] * 100
)

churn_tenure.plot(
    kind="bar",
    title="Churn rate by customer tenure"
)
plt.ylabel("Churn rate (%)")
plt.xlabel("Customer tenure")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "churn_by_tenure.png", dpi=150)
plt.close()

print("Graphiques enregistrés dans :", FIGURES_DIR)
