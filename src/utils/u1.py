from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session
from db.modeles import Base
from db.db_bbc import engine, get_cursor


def lister_contenu_tables(l_noms_tables):
    # Exemple de liste le contenu des tables passées en paramètre
    cur = get_cursor()
    with cur:
        for nom_table in l_noms_tables:
            cur.execute(f"SELECT * FROM {nom_table};")
            rows = cur.fetchall()
            print(f"Contenu de la table {nom_table}:")
            for row in rows:
                print(row)
            print("\n")


def supprimer_tables(l_tables):

    # Exemple de suppression des tables passées en paramètre
    cur = get_cursor()
    with cur:
        for nom_table in l_tables:
            cur.execute(f"DROP TABLE IF EXISTS {nom_table} CASCADE;")
            print(f"Table {nom_table} supprimée.")

    cur = get_cursor()

    # Requête SQL
    sql = """
    CREATE TABLE operation_individualisee (
    id_oi        SERIAL PRIMARY KEY,
    code_oi      TEXT UNIQUE NOT NULL,
    libelle      TEXT NOT NULL,
    description  TEXT,
    date_debut   DATE,
    date_fin     DATE,
    statut       TEXT NOT NULL DEFAULT 'OUVERTE'
        CHECK (statut IN ('OUVERTE','CLOTUREE'))
    );
    """
    with cur:
        # Exécution
        cur.execute(sql)

    print("Table operation_individualisee créée avec succès.")


if __name__ == "__main__":
    pass
