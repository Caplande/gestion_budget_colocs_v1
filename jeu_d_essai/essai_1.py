from datetime import date
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.db_bbc import engine, fetch_one, execute_sql_sa
from db.modeles import (
    CompteComptable,
    Personne,
    Evenement,
    Ecriture,
    Journal,
    OperationIndividualisee,
)


def vider_toutes_les_tables(engine):
    sql = """
    DO
    $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
        )
        LOOP
            EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END
    $$;
    """

    with engine.begin() as conn:
        conn.execute(text(sql))


# 🧱 Étape 1 — Création des comptes comptables
def creer_donnees_exemple():
    vider_toutes_les_tables(engine)
    with Session(engine) as session:

        # ======================
        # Comptes comptables
        # ======================
        c_6061 = CompteComptable(
            numero="6061", libelle="Achats alimentaires", nature="CHARGE"
        )
        c_467A = CompteComptable(numero="467A", libelle="Compte Alice", nature="PASSIF")
        c_467B = CompteComptable(numero="467B", libelle="Compte Bob", nature="PASSIF")
        c_467C = CompteComptable(
            numero="467C", libelle="Compte Claire", nature="PASSIF"
        )

        session.add_all([c_6061, c_467A, c_467B, c_467C])
        session.flush()

        # 👤 Étape 2 — Personnes
        alice = Personne(nom="Dupont", prenom="Alice", compte_tiers=c_467A)
        bob = Personne(nom="Martin", prenom="Bob", compte_tiers=c_467B)
        claire = Personne(nom="Durand", prenom="Claire", compte_tiers=c_467C)

        session.add_all([alice, bob, claire])

        # 📒 Étape 3 — Journal
        journal_od = Journal(code="OD", libelle="Opérations diverses")
        session.add(journal_od)

        # 🧭 Étape 4 — OI (axe analytique)
        oi = OperationIndividualisee(
            code="VOYAGE_ESPAGNE",
            libelle="Voyage Espagne été",
            date_debut=date(2025, 6, 1),
        )
        session.add(oi)

        # 📄 Étape 5 — Événement métier
        evenement = Evenement(
            code="EVT_001",
            libelle="Courses supermarché",
            description="Achat commun hebdomadaire",
            date_evenement=date.today(),
        )
        session.add(evenement)
        session.flush()

        # ✍️ Étape 6 — Écritures comptables générées
        # 6.1 Débit charge
        e1 = Ecriture(
            date_ecriture=date.today(),
            libelle="Courses alimentaires",
            debit=Decimal("90.00"),
            credit=None,
            compte=c_6061,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )
        # 6.2 Crédit tiers (répartition)
        e2 = Ecriture(
            date_ecriture=date.today(),
            libelle="Part Alice",
            debit=None,
            credit=Decimal("30.00"),
            compte=c_467A,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )

        e3 = Ecriture(
            date_ecriture=date.today(),
            libelle="Part Bob",
            debit=None,
            credit=Decimal("30.00"),
            compte=c_467B,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )

        e4 = Ecriture(
            date_ecriture=date.today(),
            libelle="Part Claire",
            debit=None,
            credit=Decimal("30.00"),
            compte=c_467C,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )

        session.add_all([e1, e2, e3, e4])

        # ✅ Étape 7 — Commit
        session.commit()

        # 🔎 Vérifications possibles
        # Journal comptable
        sql = """
        SELECT
        e.date_ecriture,
        c.numero,
        c.libelle,
        e.debit,
        e.credit
        FROM ecriture e
        JOIN compte_comptable c ON c.id = e.compte_id
        ORDER BY e.date_ecriture;
        """
        # Exécuter la requête et afficher les résultats
        result = execute_sql_sa(sql)
        for row in result:
            print(row)

        # Solde par personne
        sql = """
            SELECT
            c.numero,
            SUM(COALESCE(e.credit,0)) - SUM(COALESCE(e.debit,0)) AS solde
            FROM ecriture e
            JOIN compte_comptable c ON c.id = e.compte_id
            WHERE c.numero LIKE '467%'
            GROUP BY c.numero;
        """
        # Exécuter la requête et afficher les résultats
        result = execute_sql_sa(sql)
        for row in result:
            print(row)


if __name__ == "__main__":
    creer_donnees_exemple()
