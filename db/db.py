import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from sqlalchemy import create_engine, inspect, text

engine = create_engine(
    "postgresql+psycopg2://postgres:PO1357po@localhost:5432/coloc_db", echo=True
)  # True pour voir les requêtes SQL exécutées


def get_connection():
    return psycopg2.connect(
        dbname="coloc_db",
        user="ton_user",
        password="ton_mot_de_passe",
        host="localhost",
        port=5432,
    )


def execute_sql(sql: str):
    """Exécute une requête SQL simple"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


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


def execute_sql_file(sql, params=None):
    with get_cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return rows


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
