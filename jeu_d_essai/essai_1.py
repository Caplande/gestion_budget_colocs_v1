from db.db import fetch_one, execute_sql, get_cursor


# 1️⃣ Créer une OI
oi = fetch_one(
    """
    INSERT INTO operation_individualisee (code_oi, libelle, description)
    VALUES (%s, %s, %s)
    RETURNING id_oi
    """,
    ("VOYAGE_ROME", "Voyage à Rome", "Voyage de 5 jours"),
)
id_oi = oi["id_oi"]

# 2️⃣ Créer des personnes
alice = fetch_one(
    """
    INSERT INTO personne (nom, prenom)
    VALUES (%s, %s)
    RETURNING id_personne
    """,
    ("Dupont", "Alice"),
)

bob = fetch_one(
    """
    INSERT INTO personne (nom, prenom)
    VALUES (%s, %s)
    RETURNING id_personne
    """,
    ("Martin", "Bob"),
)

# 3️⃣ Créer un événement
evt = fetch_one(
    """
    INSERT INTO evenement (type_evenement, date_evenement, libelle, id_oi)
    VALUES (%s, %s, %s, %s)
    RETURNING id_evenement
    """,
    ("depense", "2025-05-02", "Billet avion Rome", id_oi),
)
id_evt = evt["id_evenement"]

# 4️⃣ Ajouter les payeurs
execute_sql(
    """
    INSERT INTO evenement_payeur (id_evenement, id_personne, montant)
    VALUES (%s, %s, %s)
    """,
    (id_evt, alice["id_personne"], 200.00),
)

execute_sql(
    """
    INSERT INTO evenement_payeur (id_evenement, id_personne, montant)
    VALUES (%s, %s, %s)
    """,
    (id_evt, bob["id_personne"], 150.00),
)

# 5️⃣ Ajouter les bénéficiaires
execute_sql(
    """
    INSERT INTO evenement_beneficiaire (id_evenement, id_personne, pourcentage)
    VALUES (%s, %s, %s)
    """,
    (id_evt, alice["id_personne"], 50),
)

execute_sql(
    """
    INSERT INTO evenement_beneficiaire (id_evenement, id_personne, pourcentage)
    VALUES (%s, %s, %s)
    """,
    (id_evt, bob["id_personne"], 50),
)

# 6️⃣ Ajouter le montant total
execute_sql(
    """
    INSERT INTO evenement_montant (id_evenement, montant_total, nature)
    VALUES (%s, %s, %s)
    """,
    (id_evt, 350.00, "charge"),
)

print("✅ Test de bout en bout terminé avec succès")
