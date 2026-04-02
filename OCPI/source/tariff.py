"""Tariff module for handling tariff-related operations."""

import datetime

from .utils import DayOfWeek, OCPIBaseModel, Price, TariffDimensionType


class PriceComponent(OCPIBaseModel):
    """Represents a price component within a tariff element."""

    def __init__(self, type: TariffDimensionType, price: Price):
        self.type = type
        self.price = price

    def __str__(self):
        return f"PriceComponent(type={self.type}, price={self.price})"


class TariffRestrictions(OCPIBaseModel):
    """Represents restrictions that may apply to a tariff."""

    def __init__(self):
        self.days_of_week: list[DayOfWeek] = None
        self.start_date_time: datetime = None
        self.end_date_time: datetime = None
        self.min_current: float = None
        self.max_current: float = None
        self.min_duration: int = None
        self.max_duration: int = None
        self.min_kwh: float = None
        self.max_kwh: float = None
        self.min_power: float = None
        self.max_power: float = None

    def __str__(self):
        return "TariffRestrictions()"


class TariffElement(OCPIBaseModel):
    """Represents an element of a tariff."""

    def __init__(
        self,
        price_components: list[PriceComponent],
        restrictions: TariffRestrictions = None,
    ):
        self.price_components = price_components
        self.restrictions = restrictions

    def __str__(self):
        return (
            f"TariffElement(type={self.type}, price_components={self.price_components})"
        )


class Tariff(OCPIBaseModel):
    """Represents a tariff in the OCPI protocol."""

    def __init__(
        self,
        id: str,
        elements: list[TariffElement],
        min_price: Price = None,
        max_price: Price = None,
        start_date_time: datetime = None,
        end_date_time: datetime = None,
    ):
        self.id = id
        self.elements = elements
        self.min_price = min_price
        self.max_price = max_price
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.last_updated = datetime.datetime.now()

    def __str__(self):
        return f"Tariff(id={self.id}, min_price={self.min_price}, max_price={self.max_price}, elements={self.elements}, last_updated={self.last_updated})"
