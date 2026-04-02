"""Utility classes and functions for the OCPI protocol."""

# from pydantic import BaseModel
from enum import Enum

class DayOfWeek(Enum):
    """Enumeration for days of the week."""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class TariffDimensionType(Enum):
    """Enumeration for tariff dimension types."""
    ENERGY = "ENERGY"
    TIME = "TIME"
    FLAT = "FLAT"
    PARKING_TIME = "PARKING_TIME"

class OCPIBaseModel:
    """Base model for OCPI data structures."""

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class Price(OCPIBaseModel):
    """Represents a price in the OCPI protocol."""

    def __init__(self, amount: float):
        self.amount = round(amount, 2)

    def __str__(self):
        return f"Price(amount={self.amount})"

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
