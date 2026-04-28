"""Utility classes and functions for the OCPI protocol."""

# from pydantic import BaseModel
from enum import Enum
import re

TARIFF_REGEX = re.compile(
    r"""
  ^(\d+\.?\d*)$  # float
  |
  ^(
      (
        ( ((EN|FL|PT|TI|A<|A>|P<|P>|I<|I>)\d+) # energy, flat, time, parking_time, min/max_current/kwh/power/duration, 
          |((D>|D<)\d{4}-\d{2}-\d{2}) # start_date, end_date
          |((T>|T<)\d{2}:\d{2}) # start_time, end_time
          |(J=(?!$)(Lu)?(Ma)?(Me)?(Je)?(Ve)?(Sa)?(Di)?) #day_of_week
        )
      \+?)+  
    \|?)+
  $""",
    re.VERBOSE,
)


class Format(Enum):
    """Enumeration for format string."""

    TEXT_LIGHT = "text_light"
    JSON_LIGHT = "json_light"
    JSON_LIGHT_PLUS = "json_light+"
    JSON_OCPI = "json_ocpi"


class TaxIncluded(Enum):
    """Enumeration for tax inclusion."""

    YES = "YES"
    NO = "NO"
    NA = "N/A"


class DayOfWeek(Enum):
    """Enumeration for days of the week."""

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    @property
    def code(self):
        """text code of the day."""
        return DayOfWeekCode[self.name].value


class DayOfWeekCode(Enum):
    """Enumeration for days of the week."""

    MONDAY = "Lu"
    TUESDAY = "Ma"
    WEDNESDAY = "Me"
    THURSDAY = "Je"
    FRIDAY = "Ve"
    SATURDAY = "Sa"
    SUNDAY = "Di"


class TariffRestrictionsCode(Enum):
    """Enumeration for tariff restrictions codes."""

    DAYS_OF_WEEK = "J="
    START_DATE = "D>"
    END_DATE = "D<"
    START_TIME = "T>"
    END_TIME = "T<"
    MAX_POWER = "P<"
    MIN_POWER = "P>"
    MAX_KWH = "K<"
    MIN_KWH = "K>"
    MAX_DURATION = "I<"
    MIN_DURATION = "I>"
    MAX_CURRENT = "A<"
    MIN_CURRENT = "A>"


class TariffRestrictionsText(Enum):
    """Enumeration for tariff restrictions texts."""

    DAYS_OF_WEEK = "les"
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


class TariffRestrictionsUnite(Enum):
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


class TariffType(Enum):
    """Enumeration for tariff types."""

    AD_HOC_PAYMENT = "AD_HOC_PAYMENT"
    PROFILE_CHEAP = "PROFILE_CHEAP"
    PROFILE_FAST = "PROFILE_FAST"
    PROFILE_GREEN = "PROFILE_GREEN"
    REGULAR = "REGULAR"


class TariffDimensionType(Enum):
    """Enumeration for tariff dimension types."""

    ENERGY = "ENERGY"
    TIME = "TIME"
    FLAT = "FLAT"
    PARKING_TIME = "PARKING_TIME"
    CONGESTION_TIME = "CONGESTION_TIME"

    @property
    def code(self):
        """code of the dimension."""
        return TariffDimensionCode[self.name].value

    @property
    def text(self):
        """text of the dimension."""
        return TariffDimensionText[self.name].value


class TariffDimensionCode(Enum):
    """Enumeration for tariff dimension types."""

    ENERGY = "EN"
    TIME = "TI"
    FLAT = "FL"
    PARKING_TIME = "PT"
    CONGESTION_TIME = "CT"


class TariffDimensionText(Enum):
    """Enumeration for tariff dimension types."""

    ENERGY = "énergie"
    TIME = "durée de recharge"
    FLAT = "forfait"
    PARKING_TIME = "durée de parking"
    CONGESTION_TIME = "durée de congestion"


class TariffDimensionUnit(Enum):
    """Enumeration for tariff dimension units."""

    ENERGY = "€/kWh"
    TIME = "€/h"
    FLAT = "€"
    PARKING_TIME = "€/h"
    CONGESTION_TIME = "€/h"


class OCPIBaseModel:
    """Base model for OCPI data structures."""

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


class Price(OCPIBaseModel):
    """Represents a price in the OCPI protocol."""

    def __init__(self, amount: float, tax_included: bool = True):
        self.amount = round(amount, 2) if tax_included else round(amount * 1.20, 2)

    def __str__(self):
        return f"Price(amount={self.amount})"

    def __eq__(self, other):
        if not isinstance(other, Price):
            return NotImplemented
        return self.amount == other.amount

    @property
    def excl_vat(self):
        return round(self.amount / 1.20, 2)

    @property
    def vat(self):
        return round(self.amount - self.excl_vat, 2)

    @property
    def incl_vat(self):
        return self.amount


class OCPIError(OCPIBaseModel):
    """Represents an error in the OCPI protocol."""

    code: int
    message: str

    def __str__(self):
        return f"OCPIError(code={self.code}, message={self.message})"


class OCPIResponse(OCPIBaseModel):
    """Represents a response in the OCPI protocol."""

    status_code: int
    status_message: str
    data: dict = None

    def __str__(self):
        return f"OCPIResponse(status_code={self.status_code}, status_message={self.status_message}, data={self.data})"
