
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "processed" / "churn.duckdb"
SQL_PATH = ROOT / "sql" / "churn_analysis.sql"

# Connexion à la base de données
con = duckdb.connect(str(DB_PATH))

# Lecture du fichier SQL
sql = SQL_PATH.read_text(encoding="utf-8")

# Suppression des lignes de commentaires
lignes = [
    ligne for ligne in sql.splitlines()
    if not ligne.strip().startswith("--")
]

sql_sans_commentaires = "\n".join(lignes)

# Séparation des requêtes SQL
requetes = sql_sans_commentaires.split(";")

# Exécution de chaque requête
for i, query in enumerate(requetes, start=1):
    query = query.strip()

    if query:
        print(f"\n=== RÉSULTAT {i} ===")
        resultat = con.execute(query).df()
        print(resultat.to_string(index=False))

# Fermeture de la connexion
con.close()
