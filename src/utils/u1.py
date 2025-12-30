from src.core.variables_metier import conn

def exe_sql(path_sql_file):
    # Exemple d'exécution de fichier .sql
    # Connexion à la base
    cur = conn.cursor()

    # Lire le fichier SQL
    with open(path_sql_file, 'r', encoding='utf-8') as f:
        sql = f.read()

    # Exécuter tout le contenu
    cur.execute(sql)

    # Valider les changements
    conn.commit()

    # Fermer la connexion
    cur.close()
    # conn.close()
    
def lister_contenu_tables(l_noms_tables):
    # Exemple de liste le contenu des tables passées en paramètre
    cur = conn.cursor()

    for nom_table in l_noms_tables:
        cur.execute(f"SELECT * FROM {nom_table};")
        rows = cur.fetchall()
        print(f"Contenu de la table {nom_table}:")
        for row in rows:
            print(row)
        print("\n")

    cur.close()
    # 
    
def supprimer_tables(l_tables):
    
    # Exemple de suppression des tables passées en paramètre

    cur = conn.cursor()

    for nom_table in l_tables:
        cur.execute(f"DROP TABLE IF EXISTS {nom_table} CASCADE;")
        print(f"Table {nom_table} supprimée.")

    conn.commit()
    cur.close()
    # conn.close()
    
def creer_table_evenement():
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
    # conn.close()

    print("Table operation_individualisee créée avec succès.")
