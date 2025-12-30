import psycopg2

conn = psycopg2.connect(
        dbname="coloc_db",
        user="postgres",
        password="PO1357po",
        host="localhost",
        port=5432
    )

tables_metier = ['evenement','evenement_beneficiaire','evenement_montant','evenement_payeur','operation_individualisee','personne']