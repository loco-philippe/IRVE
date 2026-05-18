"""Utility classes and functions for the OCPI protocol."""

# from pydantic import BaseModel
from enum import Enum

VAT = 0.20


class DayOfWeekCode(Enum):
    """Enumeration for days of the week."""

    MONDAY = "Lu"
    TUESDAY = "Ma"
    WEDNESDAY = "Me"
    THURSDAY = "Je"
    FRIDAY = "Ve"
    SATURDAY = "Sa"
    SUNDAY = "Di"


class TariffRestrictionsText(Enum):
    """Enumeration for tariff restrictions texts."""

    DAYS_OF_WEEK = "les "
    START_DATE = "après le"
    END_DATE = "avant le"
    START_TIME = "après"
    END_TIME = "avant"
    MAX_POWER = "si la puissance est inférieure à"
    MIN_POWER = "si la puissance est supérieure à"
    MAX_KWH = "si l'énergie est inférieure à"
    MIN_KWH = "si l'énergie est supérieure à"
    MAX_DURATION = "si la durée est inférieure à"
    MIN_DURATION = "si la durée est supérieure à"
    MAX_CURRENT = "si le courant est inférieur à"
    MIN_CURRENT = "si le courant est supérieur à"


class TariffRestrictionsUnit(Enum):
    """Enumeration for tariff restrictions units."""

    DAYS_OF_WEEK = ""
    START_DATE = ""
    END_DATE = ""
    START_TIME = ""
    END_TIME = ""
    MAX_POWER = " kW"
    MIN_POWER = " kW"
    MAX_KWH = " kWh"
    MIN_KWH = " kWh"
    MAX_DURATION = " min"
    MIN_DURATION = " min"
    MAX_CURRENT = " A"
    MIN_CURRENT = " A"


class TariffDimensionText(Enum):
    """Enumeration for tariff dimension types."""

    ENERGY = "énergie"
    TIME = "durée de recharge"
    FLAT = "forfait"
    PARKING_TIME = "durée d'occupation hors charge"
    CONGESTION_TIME = "durée de congestion"


class TariffDimensionUnit(Enum):
    """Enumeration for tariff dimension units."""

    ENERGY = "€/kWh"
    TIME = "€/h"
    FLAT = "€"
    PARKING_TIME = "€/h"
    CONGESTION_TIME = "€/h"
