import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from sqlalchemy import create_engine, inspect, text
from db.modeles import Base

engine = create_engine(
    "postgresql+psycopg2://postgres:PO1357po@localhost:5432/coloc_db",  # echo=True
)  # True pour voir les requêtes SQL exécutées


def get_connection():
    return psycopg2.connect(
        dbname="coloc_db",
        user="postgres",
        password="PO1357po",
        host="localhost",
        port=5432,
    )


@contextmanager
def get_cursor():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def execute_sql(sql: str):
    """Exécute une requête SQL simple"""
    cur = get_cursor()
    with get_cursor() as cur:
        cur.execute(text(sql))


def execute_sql_file(sql, params=None):
    with get_cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return rows


def execute_sql_sa(sql):
    with engine.connect() as conn:
        return conn.execute(text(sql))


def fetch_one(sql, params=None):
    with get_cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
    return row


def vider_table(nom_table: str):
    with get_cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {nom_table} CASCADE;")
        print(f"Table {nom_table} vidée.")


def print_schema_bdd():

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\n=== Schéma ER textuel de la base ===\n")

    for table in tables:
        print(f"Table: {table}")

        # Colonnes
        cols = inspector.get_columns(table)
        for col in cols:
            name = col["name"]
            typ = col["type"]
            nullable = "YES" if col["nullable"] else "NO"
            print(f"  {name:<20} {str(typ):<15} nullable={nullable}")

        # Clés primaires
        pk = inspector.get_pk_constraint(table).get("constrained_columns", [])
        print(f"  Primary key: {', '.join(pk) if pk else 'None'}")

        # Clés étrangères
        fks = inspector.get_foreign_keys(table)
        if fks:
            print("  Foreign keys:")
            for fk in fks:
                cols = ", ".join(fk["constrained_columns"])
                ref = f"{fk['referred_table']}({', '.join(fk['referred_columns'])})"
                print(f"    {cols} -> {ref}")
        print("-" * 60)


def redefinir_bdd():
    sql = text(
        """
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    """
    )
    with engine.begin() as conn:  # begin = commit auto
        conn.execute(sql)

    print("✅ Création des tables selon les modèles")
    Base.metadata.create_all(engine)


def fermer_sessions_postgres(engine):
    """
    Ferme toutes les sessions PostgreSQL sur la base courante,
    sauf la session appelante.
    """
    sql = """
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = current_database()
      AND pid <> pg_backend_pid();
    """

    with engine.begin() as conn:
        conn.execute(text(sql))


def voir_sessions_ouvertes(engine):
    """
    Affiche les sessions PostgreSQL ouvertes sur la base courante.
    """
    sql = """
    SELECT pid, usename, application_name, client_addr, state, query
    FROM pg_stat_activity
    WHERE datname = current_database();
    """

    with engine.begin() as conn:
        result = conn.execute(text(sql))
        for row in result:
            print(row)


if __name__ == "__main__":
    voir_sessions_ouvertes
    # print_schema_bdd()
