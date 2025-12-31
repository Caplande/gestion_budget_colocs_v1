from src.core.variables_metier import get_connection


def lister_contenu_tables(l_noms_tables):
    # Exemple de liste le contenu des tables passées en paramètre
    conn = get_connection()
    cur = conn.cursor()

    for nom_table in l_noms_tables:
        cur.execute(f"SELECT * FROM {nom_table};")
        rows = cur.fetchall()
        print(f"Contenu de la table {nom_table}:")
        for row in rows:
            print(row)
        print("\n")

    cur.close()
    conn.close()


def supprimer_tables(l_tables):

    # Exemple de suppression des tables passées en paramètre
    conn = get_connection()
    cur = conn.cursor()

    for nom_table in l_tables:
        cur.execute(f"DROP TABLE IF EXISTS {nom_table} CASCADE;")
        print(f"Table {nom_table} supprimée.")

    conn.commit()
    cur.close()
    conn.close()


def creer_table_evenement():
    conn = get_connection()
    cur = conn.cursor()

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

    # Exécution
    cur.execute(sql)
    conn.commit()

    # Nettoyage
    cur.close()
    conn.close()

    print("Table operation_individualisee créée avec succès.")
