-- 🔹 Vider les tables dépendantes en premier
TRUNCATE TABLE evenement_payeur RESTART IDENTITY CASCADE;
TRUNCATE TABLE evenement_beneficiaire RESTART IDENTITY CASCADE;
TRUNCATE TABLE evenement_montant RESTART IDENTITY CASCADE;

-- 🔹 Vider la table des événements
TRUNCATE TABLE evenement RESTART IDENTITY CASCADE;

-- 🔹 Vider la table des personnes
TRUNCATE TABLE personne RESTART IDENTITY CASCADE;

-- 🔹 Vider la table des OI
TRUNCATE TABLE operation_individualisee RESTART IDENTITY CASCADE;
