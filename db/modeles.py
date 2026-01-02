import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    String,
    Date,
    Numeric,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class CompteComptable(Base):
    __tablename__ = "compte_comptable"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    numero: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    nature: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # ACTIF / PASSIF / CHARGE / PRODUIT

    ecritures = relationship("Ecriture", back_populates="compte")


class Personne(Base):
    __tablename__ = "personne"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str | None] = mapped_column(String(100))

    compte_tiers_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("compte_comptable.id"), nullable=False
    )

    compte_tiers = relationship("CompteComptable")


class OperationIndividualisee(Base):
    __tablename__ = "operation_individualisee"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String)

    date_debut: Mapped[date | None] = mapped_column(Date)
    date_fin: Mapped[date | None] = mapped_column(Date)
    statut: Mapped[str] = mapped_column(String(20), default="OUVERTE")

    ecritures = relationship("Ecriture", back_populates="oi")


class Evenement(Base):
    __tablename__ = "evenement"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    date_evenement: Mapped[date] = mapped_column(Date, nullable=False)

    ecritures = relationship("Ecriture", back_populates="evenement")


class Journal(Base):
    __tablename__ = "journal"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)

    ecritures = relationship("Ecriture", back_populates="journal")


class Ecriture(Base):
    __tablename__ = "ecriture"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    date_ecriture: Mapped[date] = mapped_column(Date, nullable=False)
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)

    debit: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    credit: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    compte_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("compte_comptable.id"), nullable=False
    )
    evenement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evenement.id"), nullable=False
    )
    journal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journal.id"), nullable=False
    )
    oi_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("operation_individualisee.id")
    )

    compte = relationship("CompteComptable", back_populates="ecritures")
    evenement = relationship("Evenement", back_populates="ecritures")
    journal = relationship("Journal", back_populates="ecritures")
    oi = relationship("OperationIndividualisee", back_populates="ecritures")
