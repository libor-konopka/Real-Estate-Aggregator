from enum import StrEnum
import datetime as dt

from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class SourceType(StrEnum):
    """Výčtový typ definující podporované zdroje datových importů."""
    SREALITY = "sreality"
    IDNES = "idnes"
    BEZREALITKY = "bezrealitky"


class EstateType(StrEnum):
    """Výčtový typ definující podporované typy nemovitostí."""
    POZEMEK = "pozemek"
    STAVBA = "stavba"

class TransactionType(StrEnum):
    """Výčtový typ definující podporované typy transakcí."""
    PRODEJ = "prodej"
    PRONAJEM = "pronajem"
    DRAZBA = "drazba"

class Currency(StrEnum):
    """Výčtový typ definující podporované měny."""
    CZK = "czk"
    EUR = "eur"
    USD = "usd"

class RealEstateItem(BaseModel):
    """Základní datové schéma."""

    model_config = ConfigDict(extra="forbid")

    # === MANDATORY FIELDS ===
    source_id: str = Field(..., min_length=1, description="Unikátní ID z portálu")
    source_type: SourceType = Field(...,description="Zdroj dat")
    source_url: HttpUrl = Field(..., description="Odkaz na inzerát")
    active : bool = Field(..., description="Stav inzerátu")
    estate_type: EstateType = Field(..., description="Typ nemovitosti")
    transaction_type: TransactionType = Field(..., description="Typ transakce")
    region: str = Field(..., min_length=1, description="Kraj")
    district: str = Field(..., min_length=1, description="Okres")
    municipality: str = Field(..., min_length=1, description="Obec")
    latitude: float = Field(..., description="Zeměpisná šířka")
    longitude: float = Field(..., description="Zeměpisná délka")
    price: int | None = Field(..., ge=0, description="Cena nemovitosti")
    currency: Currency = Field(..., description="Měna")
    land_area: int | None = Field(..., ge=0, description="Rozloha pozemku")
    usable_area: int | None = Field(..., ge=0, description="Podlahová plocha")
    description: str = Field(..., min_length=1, description="Textový popis nemovitosti")
    timestamp: dt.datetime = Field(..., description="Čas extrakce")

    # === OPTIONAL FIELDS ===
    # === --- Infrastructure --- ===
    water_source: str | None = Field(None, description="Zdroj vody")
    electricity_connection: str | None = Field(None, description="Napojení na elektrickou síť")
    sewage_system: str | None = Field(None, description="Likvidace odpadních vod")
    heating_source: str | None = Field(None, description="Zdroj tepla / vytápění")
    gas_connection: str | None = Field(None, description="Dostupnost plynu")

    # === --- Building Specific --- ===
    built_up_area: int | None = Field(None, ge=0, description="Zastavěná plocha")
    construction_material: str | None = Field(None, description="Materiál stavby")
    building_condition: str | None = Field(None, description="Stav objektu")
    energy_efficiency_rating: str | None = Field(None, description="Energetická náročnost")

    # === --- Land Specific --- ===
    land_category: str | None = Field(None, description="Kategorie půdy")
    location_character: str | None = Field(None, description="Charakter lokality")
    access_road: str | None = Field(None, description="Přístupová cesta")
    transport_accessibility: str | None = Field(None, description="Dopravní obslužnost")

    # === --- Legal and business context --- ===
    ownership_type: str | None = Field(None, description="Typ vlastnictví")
    availability_date: dt.date | None = Field(None, description="Datum uvolnění")
    price_note: str | None = Field(None, description="Poznámka k ceně")