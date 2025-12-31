import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import String, Date, ForeignKey, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# ============================================================
# Base
# ============================================================


class Base(DeclarativeBase):
    pass


# ============================================================
# 1. Personne
# ============================================================


class Personne(Base):
    __tablename__ = "personne"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str | None] = mapped_column(String(100))
    date_naissance: Mapped[date | None] = mapped_column(Date)

    occupations = relationship("OccupationPersonne", back_populates="personne")
    repartitions = relationship("RepartitionOperation", back_populates="personne")


# ============================================================
# 2. Nomenclature des comptes
# ============================================================


class NomenclatureCompte(Base):
    __tablename__ = "nomenclature_comptes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    type_compte: Mapped[str] = mapped_column(String(50), nullable=False)

    ecritures = relationship("Ecriture", back_populates="compte")


# ============================================================
# 3. Evenement
# ============================================================


class Evenement(Base):
    __tablename__ = "evenement"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    date_evenement: Mapped[date | None] = mapped_column(Date)

    operations = relationship("Operation", back_populates="evenement")
    ecritures = relationship("Ecriture", back_populates="evenement")


# ============================================================
# 4. Operation individualisée (facultative)
# ============================================================


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    date_debut: Mapped[date | None] = mapped_column(Date)
    date_fin: Mapped[date | None] = mapped_column(Date)

    evenement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evenement.id")
    )

    evenement = relationship("Evenement", back_populates="operations")
    ecritures = relationship("Ecriture", back_populates="operation")
    repartitions = relationship("RepartitionOperation", back_populates="operation")


# ============================================================
# 5. Ecriture comptable
# ============================================================


class Ecriture(Base):
    __tablename__ = "ecriture"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    date_ecriture: Mapped[date] = mapped_column(Date, nullable=False)
    montant: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    compte_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("nomenclature_comptes.id"), nullable=False
    )
    operation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("operation.id")
    )
    evenement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evenement.id")
    )

    compte = relationship("NomenclatureCompte", back_populates="ecritures")
    operation = relationship("Operation", back_populates="ecritures")
    evenement = relationship("Evenement", back_populates="ecritures")


# ============================================================
# 6. Repartition d'une opération
# ============================================================


class RepartitionOperation(Base):
    __tablename__ = "repartition_operation"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    operation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("operation.id"), nullable=False
    )
    personne_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("personne.id"), nullable=False
    )
    pourcentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)

    operation = relationship("Operation", back_populates="repartitions")
    personne = relationship("Personne", back_populates="repartitions")


# ============================================================
# 7. OccupationPersonne
# ============================================================


class OccupationPersonne(Base):
    __tablename__ = "occupation_personne"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    personne_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("personne.id"), nullable=False
    )
    date_debut: Mapped[date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[date | None] = mapped_column(Date)
    actif: Mapped[bool] = mapped_column(Boolean, default=True)

    personne = relationship("Personne", back_populates="occupations")


# ============================================================
# 8. Charge récurrente
# ============================================================


class ChargeRecurrente(Base):
    __tablename__ = "charge_recurrente"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    montant: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    periodicite: Mapped[str] = mapped_column(String(20), nullable=False)
    date_debut: Mapped[date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[date | None] = mapped_column(Date)
