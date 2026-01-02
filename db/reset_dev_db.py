from sqlalchemy import text
from db.db_bbc import engine
from db.modeles import Base


from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from db.db_bbc import engine, Base


DB_NAME = "coloc_db"


def ensure_database_exists():
    """Crée la base si elle n'existe pas (connexion via postgres)"""

    print("🔍 Vérification de l'existence de la base de données...")

    admin_url = URL.create(
        drivername="postgresql+psycopg2",
        username=engine.url.username,
        password=engine.url.password,
        host=engine.url.host,
        port=engine.url.port,
        database="postgres",
    )

    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
            {"dbname": DB_NAME},
        ).scalar()

        if not exists:
            print(f"🆕 Création de la base '{DB_NAME}'...")
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
        else:
            print(f"✅ Base '{DB_NAME}' déjà existante")

    admin_engine.dispose()


def reset_dev_database():
    print("⚠️  RÉINITIALISATION DE LA BASE DE DONNÉES (DEV)")
    print("------------------------------------------------")

    # 0️⃣ S'assurer que la base existe
    ensure_database_exists()

    # 1️⃣ Fermer les connexions SQLAlchemy
    print("🔌 Fermeture des connexions SQLAlchemy...")
    engine.dispose()

    with engine.begin() as conn:
        # 2️⃣ Tuer les autres sessions
        print("🧹 Fermeture des autres sessions PostgreSQL...")
        conn.execute(
            text(
                """
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = current_database()
              AND pid <> pg_backend_pid();
            """
            )
        )

        # 3️⃣ Reset du schéma
        print("🔥 Suppression du schéma public...")
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))

        print("🆕 Création du schéma public...")
        conn.execute(text("CREATE SCHEMA public"))

    # 4️⃣ Recréation des tables
    print("🏗️  Création des tables depuis les modèles...")
    Base.metadata.create_all(engine)

    print("✅ Base de données DEV réinitialisée avec succès")


if __name__ == "__main__":
    reset_dev_database()


if __name__ == "__main__":
    reset_dev_database()
