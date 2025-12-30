import psycopg2

def exe_sql(path_sql_file):
# Connexion à la base
    conn = psycopg2.connect(
        dbname="coloc_db",
        user="postgres",
        password="PO1357po",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    # Lire le fichier SQL
    with open('init_coloc.sql', 'r', encoding='utf-8') as f:
        sql = f.read()

    # Exécuter tout le contenu
    cur.execute(sql)

    # Valider les changements
    conn.commit()

    # Fermer la connexion
    cur.close()
    conn.close()
