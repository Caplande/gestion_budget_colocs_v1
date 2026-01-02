from src.utils.reinit_bdd_vide import vider_bdd, creer_tables
from db.db_bbc import print_schema_bdd

if __name__ == "__main__":
    vider_bdd()
    print("Recréation des tables…")
    creer_tables()
    print("✅ Base prête à l’emploi")
    print_schema_bdd()
