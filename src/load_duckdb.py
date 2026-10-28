
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "processed" / "telco_clean.csv"
DB_PATH = ROOT / "data" / "processed" / "churn.duckdb"

# Connexion à la base DuckDB
con = duckdb.connect(str(DB_PATH))

# Charger le CSV et créer une table
con.execute("""
    CREATE OR REPLACE TABLE customers AS
    SELECT *
    FROM read_csv_auto(?)
""", [str(CSV_PATH)])

# Vérifier le chargement
print("Nombre de clients :",
      con.execute("SELECT COUNT(*) FROM customers").fetchone()[0])

print("\nRépartition du churn :")
print(con.execute("""
    SELECT
        Churn,
        COUNT(*) AS nombre_clients,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pourcentage
    FROM customers
    GROUP BY Churn
    ORDER BY Churn
""").df())

con.close()
print("\nBase créée :", DB_PATH)
