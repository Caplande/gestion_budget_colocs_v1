from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.db_bbc import engine, execute_sql_sa, fermer_sessions_postgres
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


def creer_donnees_exemple():
    # Fermer toutes les sessions ouvertes et vider les tables pour dev
    fermer_sessions_postgres(engine)
    # Ici, tu peux appeler ta fonction de vidage de tables si besoin
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
        c_512 = CompteComptable(numero="512", libelle="Banque", nature="ACTIF")

        session.add_all([c_6061, c_467A, c_467B, c_467C, c_512])
        session.flush()

        # 👤 Personnes
        alice = Personne(nom="Dupont", prenom="Alice", compte_tiers=c_467A)
        bob = Personne(nom="Martin", prenom="Bob", compte_tiers=c_467B)
        claire = Personne(nom="Durand", prenom="Claire", compte_tiers=c_467C)

        session.add_all([alice, bob, claire])

        # 📒 Journal
        journal_od = Journal(code="OD", libelle="Opérations diverses")
        session.add(journal_od)

        # 🧭 OI (facultative)
        oi = OperationIndividualisee(
            code="VOYAGE_ESPAGNE",
            libelle="Voyage Espagne été",
            date_debut=date(2025, 6, 1),
        )
        session.add(oi)

        # 📄 Événement métier
        evenement = Evenement(
            code="EVT_001",
            libelle="Courses supermarché",
            description="Achat commun hebdomadaire",
            date_evenement=date.today(),
        )
        session.add(evenement)
        session.flush()

        # ✍️ Écritures comptables
        montant_total = Decimal("90.00")
        nb_colocs = 3
        part_coloc = montant_total / nb_colocs  # 30 € chacun

        # 1️⃣ Débit charge 6061
        e_charge = Ecriture(
            date_ecriture=date.today(),
            libelle="Courses alimentaires",
            debit=montant_total,
            credit=None,
            compte=c_6061,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )

        # 2️⃣ Crédit comptes colocataires (répartition)
        e_alice = Ecriture(
            date_ecriture=date.today(),
            libelle="Part Alice",
            debit=None,
            credit=part_coloc,
            compte=c_467A,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )
        e_bob = Ecriture(
            date_ecriture=date.today(),
            libelle="Part Bob",
            debit=None,
            credit=part_coloc,
            compte=c_467B,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )
        e_claire = Ecriture(
            date_ecriture=date.today(),
            libelle="Part Claire",
            debit=None,
            credit=part_coloc,
            compte=c_467C,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )

        # 3️⃣ Paiement réel par Alice : banque 512 diminue, dette Alice diminue
        e_paiement_alice = Ecriture(
            date_ecriture=date.today(),
            libelle="Paiement Alice",
            debit=part_coloc,
            credit=part_coloc,
            compte=c_512,  # banque
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )
        # Ajuster la dette d'Alice
        e_dette_alice = Ecriture(
            date_ecriture=date.today(),
            libelle="Règlement Alice",
            debit=part_coloc,
            credit=None,
            compte=c_467A,
            evenement=evenement,
            journal=journal_od,
            oi=oi,
        )

        session.add_all(
            [e_charge, e_alice, e_bob, e_claire, e_paiement_alice, e_dette_alice]
        )

        session.commit()

    # 🔎 Vérifications : Journal comptable
    print(
        "******************************** JOURNAL *******************************************"
    )
    sql_journal = """
    SELECT
        e.date_ecriture,
        c.numero,
        c.libelle,
        e.debit,
        e.credit
    FROM ecriture e
    JOIN compte_comptable c ON c.id = e.compte_id
    ORDER BY e.date_ecriture, c.numero;
    """
    for row in execute_sql_sa(sql_journal):
        print(row)

    # 🔎 Solde par personne
    print(
        "********************************* SOLDE PAR PERSONNE *****************************************"
    )
    sql_solde = """
    SELECT
        c.numero,
        SUM(COALESCE(e.credit,0)) - SUM(COALESCE(e.debit,0)) AS solde
    FROM ecriture e
    JOIN compte_comptable c ON c.id = e.compte_id
    WHERE c.numero LIKE '467%'
    GROUP BY c.numero
    ORDER BY c.numero;
    """
    for row in execute_sql_sa(sql_solde):
        print(row)


if __name__ == "__main__":
    creer_donnees_exemple()
