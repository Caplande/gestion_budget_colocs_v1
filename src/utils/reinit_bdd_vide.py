# db_reset.py
from sqlalchemy import inspect, text
from sqlalchemy.orm import sessionmaker
from src.modeles.modeles import Base
from db.db import engine


Session = sessionmaker(bind=engine)
session = Session()


inspector = inspect(engine)

tables = inspector.get_table_names()
print("Tables existantes :", tables)


# 2️⃣ Vider toutes les tables (attention aux FK)
def vider_bdd():
    with engine.connect() as conn:
        for table in tables:
            try:
                conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
                print(f"✅ Table {table} vidée")
            except Exception as e:
                print(f"⚠ Impossible de vider {table} : {e}")


# 3️⃣ Créer toutes les tables définies dans modeles.py
def creer_tables():

    # 1️⃣ Créer toutes les tables (si elles n’existent pas)
    Base.metadata.create_all(engine)

    # 2️⃣ Vider toutes les tables existantes dynamiquement
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    with engine.connect() as conn:
        for table in tables:
            conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))


# 4️⃣ Exécution
if __name__ == "__main__":
    print("Vider la base…")
    vider_bdd()
    print("Recréation des tables…")
    creer_tables()
    print("✅ Base prête à l’emploi")
