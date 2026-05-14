"""Pydantic tariff models for the OCPI source package."""

from __future__ import annotations

import json
from datetime import date, datetime, time
from enum import StrEnum
from typing import Annotated, List, Optional, Union

from annotated_types import Ge
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pydantic import BaseModel, Field, StringConstraints, model_validator
from pydantic.types import AwareDatetime
from typing_extensions import Self

from .utils import (
    DayOfWeekCode,
    Format,
    TariffDimensionCode,
    TariffDimensionUnit,
    TariffRestrictionsCode,
    TariffRestrictionsText,
    TariffRestrictionsUnite,
    TariffDimensionType,
    TARIFF_REGEX,
    VAT,
)


class PriceComponentTypeEnum(StrEnum):
    """Tariff price component dimensions."""

    ENERGY = "ENERGY"
    FLAT = "FLAT"
    PARKING_TIME = "PARKING_TIME"
    TIME = "TIME"
    CONGESTION_TIME = "CONGESTION_TIME"

    @property
    def code(self) -> str:
        return TariffDimensionCode[self.name].value


class ReservationRestrictionEnum(StrEnum):
    """OCPI reservation restriction."""

    RESERVATION = "RESERVATION"
    RESERVATION_EXPIRES = "RESERVATION_EXPIRES"


class DayOfWeekEnum(StrEnum):
    """OCPI days of week."""

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    @property
    def code(self) -> str:
        return DayOfWeekCode[self.name].value


class TaxIncludedEnum(StrEnum):
    """Whether tariff prices include taxes."""

    YES = "YES"
    NO = "NO"
    NA = "N/A"


class TariffAltText(BaseModel):
    """Localized tariff display text."""

    language: str
    text: str


class DisplayPrice(BaseModel):
    """OCPI 2.3 display price."""

    before_taxes: float
    after_taxes: Optional[float] = None


class Price(BaseModel):
    """OCPI 2.2 price with VAT split."""

    excl_vat: float
    incl_vat: Optional[float] = None


class PriceComponent(BaseModel):
    """A tariff price component."""

    type: PriceComponentTypeEnum
    price: Annotated[float, Ge(0.0)]
    vat: Optional[float] = None
    step_size: Optional[Annotated[int, Ge(1)]] = None

    def __str__(self) -> str:
        return f"PriceComponent(type={self.type}, price={self.price})"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def from_json(
        data: dict,
        tax_included: bool = True,
        incl_vat: bool = True,
        vat_rate: float = VAT,
    ) -> PriceComponent:
        type_value = PriceComponentTypeEnum(data["type"])
        price_incl_vat = (
            data["price"] if tax_included else round(data["price"] * (1 + vat_rate), 2)
        )
        price_excl_vat = (
            data["price"]
            if not tax_included
            else round(data["price"] / (1 + vat_rate), 2)
        )
        return PriceComponent(
            type=type_value, price=price_incl_vat if incl_vat else price_excl_vat
        )

    def to_json(
        self, tax_included: bool = True, incl_vat: bool = True, vat_rate: float = VAT
    ) -> dict:
        return {
            "type": self.type.value,
            "price": (
                self.price_incl_vat(tax_included=tax_included, vat_rate=vat_rate)
                if incl_vat
                else self.price_excl_vat(tax_included=tax_included, vat_rate=vat_rate)
            ),
        }

    def price_excl_vat(self, tax_included: bool = True, vat_rate: float = VAT) -> float:
        if not tax_included:
            return self.price
        return round(self.price / (1 + vat_rate), 2)

    def price_incl_vat(self, tax_included: bool = True, vat_rate: float = VAT) -> float:
        if tax_included:
            return self.price
        return round(self.price * (1 + vat_rate), 2)

    @staticmethod
    def from_string(data: str) -> list["PriceComponent"]:
        parts = data.split("+")
        price_components: list[PriceComponent] = []
        for part in parts:
            code = part[:2]
            if code in [cod.value for cod in TariffDimensionCode]:
                type_value = PriceComponentTypeEnum[TariffDimensionCode(code).name]
                price = float(part[2:]) / 100
                price_components.append(PriceComponent(type=type_value, price=price))
        return price_components

    def to_string(self) -> str:
        return f"{self.type.code}{int(self.price * 100)}"


class TariffRestrictions(BaseModel):
    """Restrictions that control when a tariff element applies."""

    start_time: Optional[time] = None
    end_time: Optional[time] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    min_kwh: Optional[Annotated[float, Ge(0.0)]] = None
    max_kwh: Optional[Annotated[float, Ge(0.0)]] = None
    min_current: Optional[Annotated[float, Ge(0.0)]] = None
    max_current: Optional[Annotated[float, Ge(0.0)]] = None
    min_power: Optional[Annotated[float, Ge(0.0)]] = None
    max_power: Optional[Annotated[float, Ge(0.0)]] = None
    min_duration: Optional[Annotated[int, Ge(0)]] = None
    max_duration: Optional[Annotated[int, Ge(0)]] = None
    day_of_week: Optional[List[DayOfWeekEnum]] = None
    reservation: Optional[ReservationRestrictionEnum] = None
    min_vehicle_soc: Optional[Annotated[int, Ge(0)]] = None
    min_congestion_threshold: Optional[Annotated[int, Ge(0)]] = None

    def __str__(self) -> str:
        return "TariffRestrictions(truc)"

    def __len__(self) -> int:
        return len(self.to_json())

    @staticmethod
    def from_json(data: dict) -> "TariffRestrictions":
        restrictions = TariffRestrictions()
        if "day_of_week" in data:
            restrictions.day_of_week = [
                DayOfWeekEnum(day) for day in data["day_of_week"]
            ]
        if "start_date" in data:
            restrictions.start_date = date.fromisoformat(data["start_date"])
        if "end_date" in data:
            restrictions.end_date = date.fromisoformat(data["end_date"])
        if "start_time" in data:
            restrictions.start_time = time.fromisoformat(data["start_time"] + ":00")
        if "end_time" in data:
            restrictions.end_time = time.fromisoformat(data["end_time"] + ":00")
        if "min_current" in data:
            restrictions.min_current = data["min_current"]
        if "max_current" in data:
            restrictions.max_current = data["max_current"]
        if "min_duration" in data:
            restrictions.min_duration = data["min_duration"]
        if "max_duration" in data:
            restrictions.max_duration = data["max_duration"]
        if "min_kwh" in data:
            restrictions.min_kwh = data["min_kwh"]
        if "max_kwh" in data:
            restrictions.max_kwh = data["max_kwh"]
        if "min_power" in data:
            restrictions.min_power = data["min_power"]
        if "max_power" in data:
            restrictions.max_power = data["max_power"]
        return restrictions

    def to_json(self) -> dict:
        data: dict = {}
        if self.day_of_week is not None:
            data["day_of_week"] = [day.value for day in self.day_of_week]
        if self.start_date is not None:
            data["start_date"] = self.start_date.isoformat()
        if self.end_date is not None:
            data["end_date"] = self.end_date.isoformat()
        if self.start_time is not None:
            data["start_time"] = self.start_time.isoformat(timespec="minutes")
        if self.end_time is not None:
            data["end_time"] = self.end_time.isoformat(timespec="minutes")
        if self.min_current is not None:
            data["min_current"] = self.min_current
        if self.max_current is not None:
            data["max_current"] = self.max_current
        if self.min_duration is not None:
            data["min_duration"] = self.min_duration
        if self.max_duration is not None:
            data["max_duration"] = self.max_duration
        if self.min_kwh is not None:
            data["min_kwh"] = self.min_kwh
        if self.max_kwh is not None:
            data["max_kwh"] = self.max_kwh
        if self.min_power is not None:
            data["min_power"] = self.min_power
        if self.max_power is not None:
            data["max_power"] = self.max_power
        return data

    def to_text(self) -> str:
        parts: list[str] = []
        if self.day_of_week is not None:
            parts.append(
                TariffRestrictionsText.DAYS_OF_WEEK.value
                + " ".join(day.code for day in self.day_of_week)
                + TariffRestrictionsUnite.DAYS_OF_WEEK.value
            )
        if self.start_date is not None and self.end_date is not None:
            parts.append(
                "du " + self.start_date.isoformat() + "au " + self.end_date.isoformat()
            )
        elif self.start_date is not None:
            parts.append(
                TariffRestrictionsText.START_DATE.value
                + " "
                + self.start_date.isoformat()
                + TariffRestrictionsUnite.START_DATE.value
            )
        elif self.end_date is not None:
            parts.append(
                TariffRestrictionsText.END_DATE.value
                + " "
                + self.end_date.isoformat()
                + TariffRestrictionsUnite.END_DATE.value
            )
        if self.start_time is not None and self.end_time is not None:
            parts.append(
                "entre "
                + self.start_time.isoformat(timespec="minutes")
                + " et "
                + self.end_time.isoformat(timespec="minutes")
            )
        elif self.start_time is not None:
            parts.append(
                TariffRestrictionsText.START_TIME.value
                + " "
                + self.start_time.isoformat(timespec="minutes")
                + TariffRestrictionsUnite.START_TIME.value
            )
        elif self.end_time is not None:
            parts.append(
                TariffRestrictionsText.END_TIME.value
                + " "
                + self.end_time.isoformat(timespec="minutes")
                + TariffRestrictionsUnite.END_TIME.value
            )
        if self.min_current is not None and self.min_current > 0:
            parts.append(
                TariffRestrictionsText.MIN_CURRENT.value
                + " "
                + str(int(self.min_current))
                + TariffRestrictionsUnite.MIN_CURRENT.value
            )
        if self.max_current is not None:
            parts.append(
                TariffRestrictionsText.MAX_CURRENT.value
                + " "
                + str(int(self.max_current))
                + TariffRestrictionsUnite.MAX_CURRENT.value
            )
        if (
            self.min_duration is not None
            and self.min_duration > 0
            and self.max_duration is not None
        ):
            parts.append(
                "si la durée est comprise entre "
                + str(int(self.min_duration / 60))
                + TariffRestrictionsUnite.MAX_DURATION.value
                + " et "
                + str(int(self.max_duration / 60))
                + TariffRestrictionsUnite.MAX_DURATION.value
            )
        elif self.min_duration is not None and self.min_duration > 0:
            parts.append(
                TariffRestrictionsText.MIN_DURATION.value
                + " "
                + str(int(self.min_duration / 60))
                + TariffRestrictionsUnite.MIN_DURATION.value
            )
        elif self.max_duration is not None:
            parts.append(
                TariffRestrictionsText.MAX_DURATION.value
                + " "
                + str(int(self.max_duration / 60))
                + TariffRestrictionsUnite.MAX_DURATION.value
            )
        if self.min_kwh is not None and self.min_kwh > 0 and self.max_kwh is not None:
            parts.append(
                "si l'énergie est comprise entre "
                + str(int(self.min_kwh))
                + TariffRestrictionsUnite.MIN_KWH.value
                + " et "
                + str(int(self.max_kwh))
                + TariffRestrictionsUnite.MAX_KWH.value
            )
        elif self.min_kwh is not None and self.min_kwh > 0:
            parts.append(
                TariffRestrictionsText.MIN_KWH.value
                + " "
                + str(int(self.min_kwh))
                + TariffRestrictionsUnite.MIN_KWH.value
            )
        elif self.max_kwh is not None:
            parts.append(
                TariffRestrictionsText.MAX_KWH.value
                + " "
                + str(int(self.max_kwh))
                + TariffRestrictionsUnite.MAX_KWH.value
            )
        if (
            self.min_power is not None
            and self.min_power > 0
            and self.max_power is not None
        ):
            parts.append(
                "si la puissance est comprise entre "
                + str(int(self.min_power))
                + TariffRestrictionsUnite.MIN_POWER.value
                + " et "
                + str(int(self.max_power))
                + TariffRestrictionsUnite.MAX_POWER.value
            )
        elif self.min_power is not None and self.min_power > 0:
            parts.append(
                TariffRestrictionsText.MIN_POWER.value
                + " "
                + str(int(self.min_power))
                + TariffRestrictionsUnite.MIN_POWER.value
            )
        elif self.max_power is not None:
            parts.append(
                TariffRestrictionsText.MAX_POWER.value
                + " "
                + str(int(self.max_power))
                + TariffRestrictionsUnite.MAX_POWER.value
            )
        return "" if not parts else " et ".join(parts)

    def to_string(self) -> str:
        parts: list[str] = []
        if self.days_of_week is not None:
            parts.append(
                TariffRestrictionsCode.DAYS_OF_WEEK.value
                + "".join(day.code for day in self.days_of_week)
            )
        if self.start_date is not None:
            parts.append(
                TariffRestrictionsCode.START_DATE.value + self.start_date.isoformat()
            )
        if self.end_date is not None:
            parts.append(
                TariffRestrictionsCode.END_DATE.value + self.end_date.isoformat()
            )
        if self.start_time is not None:
            parts.append(
                TariffRestrictionsCode.START_TIME.value
                + self.start_time.isoformat(timespec="minutes")
            )
        if self.end_time is not None:
            parts.append(
                TariffRestrictionsCode.END_TIME.value
                + self.end_time.isoformat(timespec="minutes")
            )
        if self.min_current is not None:
            parts.append(
                TariffRestrictionsCode.MIN_CURRENT.value + str(int(self.min_current))
            )
        if self.max_current is not None:
            parts.append(
                TariffRestrictionsCode.MAX_CURRENT.value + str(int(self.max_current))
            )
        if self.min_duration is not None:
            parts.append(
                TariffRestrictionsCode.MIN_DURATION.value + str(int(self.min_duration))
            )
        if self.max_duration is not None:
            parts.append(
                TariffRestrictionsCode.MAX_DURATION.value + str(int(self.max_duration))
            )
        if self.min_kwh is not None:
            parts.append(TariffRestrictionsCode.MIN_KWH.value + str(int(self.min_kwh)))
        if self.max_kwh is not None:
            parts.append(TariffRestrictionsCode.MAX_KWH.value + str(int(self.max_kwh)))
        if self.min_power is not None:
            parts.append(
                TariffRestrictionsCode.MIN_POWER.value + str(int(self.min_power))
            )
        if self.max_power is not None:
            parts.append(
                TariffRestrictionsCode.MAX_POWER.value + str(int(self.max_power))
            )
        return "+".join(parts)

    @staticmethod
    def from_string(data: str) -> "TariffRestrictions":
        parts = data.split("+")
        restrictions = TariffRestrictions()
        for part in parts:
            code = part[:2]
            value = part[2:]
            if code == TariffRestrictionsCode.DAYS_OF_WEEK.value:
                day_codes = [value[i : i + 2] for i in range(0, len(value), 2)]
                restrictions.days_of_week = [
                    DayOfWeekEnum[DayOfWeekCode(day).name] for day in day_codes
                ]
            elif code == TariffRestrictionsCode.START_DATE.value:
                restrictions.start_date = date.fromisoformat(value)
            elif code == TariffRestrictionsCode.END_DATE.value:
                restrictions.end_date = date.fromisoformat(value)
            elif code == TariffRestrictionsCode.START_TIME.value:
                restrictions.start_time = time.fromisoformat(value + ":00")
            elif code == TariffRestrictionsCode.END_TIME.value:
                restrictions.end_time = time.fromisoformat(value + ":00")
            elif code == TariffRestrictionsCode.MIN_CURRENT.value:
                restrictions.min_current = float(value)
            elif code == TariffRestrictionsCode.MAX_CURRENT.value:
                restrictions.max_current = float(value)
            elif code == TariffRestrictionsCode.MIN_DURATION.value:
                restrictions.min_duration = int(value)
            elif code == TariffRestrictionsCode.MAX_DURATION.value:
                restrictions.max_duration = int(value)
            elif code == TariffRestrictionsCode.MIN_KWH.value:
                restrictions.min_kwh = float(value)
            elif code == TariffRestrictionsCode.MAX_KWH.value:
                restrictions.max_kwh = float(value)
            elif code == TariffRestrictionsCode.MIN_POWER.value:
                restrictions.min_power = float(value)
            elif code == TariffRestrictionsCode.MAX_POWER.value:
                restrictions.max_power = float(value)
        return restrictions


class TariffElement(BaseModel):
    """A tariff element, composed of prices and optional restrictions."""

    price_components: List[PriceComponent] = Field(min_length=1)
    restrictions: Optional[TariffRestrictions] = None

    def __str__(self) -> str:
        return f"TariffElement(price_components={self.price_components})"

    @staticmethod
    def from_json(data: dict, tax_included: bool = True) -> "TariffElement":
        if isinstance(data["price_components"], dict):
            price_components = [
                PriceComponent.from_json(
                    {"type": type_, "price": amount}, tax_included=tax_included
                )
                for type_, amount in data["price_components"].items()
            ]
        else:
            price_components = [
                PriceComponent.from_json(pc, tax_included=tax_included)
                for pc in data["price_components"]
            ]
        restrictions = (
            TariffRestrictions.from_json(data["restrictions"])
            if "restrictions" in data
            else None
        )
        return TariffElement(
            price_components=price_components, restrictions=restrictions
        )

    def to_json(self, simple: bool = False) -> dict:
        if simple:
            data = {
                "price_components": {
                    pc.type.value: pc.price for pc in self.price_components
                }
            }
        else:
            data = {"price_components": [pc.to_json() for pc in self.price_components]}
        if self.restrictions is not None:
            data["restrictions"] = self.restrictions.to_json()
        return data

    def to_string(self) -> str:
        text = "+".join(pc.to_string() for pc in self.price_components)
        if self.restrictions is not None and len(self.restrictions) > 0:
            text += "+" + self.restrictions.to_string()
        return text

    @staticmethod
    def from_string(data: str) -> "TariffElement":
        price_components = PriceComponent.from_string(data)
        restrictions = TariffRestrictions.from_string(data)
        restrictions = None if len(restrictions) == 0 else restrictions
        return TariffElement(
            price_components=price_components, restrictions=restrictions
        )


class TariffElements(BaseModel):
    """Represents a list of tariff elements."""

    elements: List[TariffElement]

    def __str__(self) -> str:
        return f"TariffElements(elements={self.elements})"

    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self, index: int) -> TariffElement:
        return self.elements[index]

    def to_json(self, simple: bool = False) -> list[dict]:
        return [element.to_json(simple) for element in self.elements]

    @staticmethod
    def from_json(data: list[dict], tax_included: bool = True) -> "TariffElements":
        return TariffElements(
            elements=[
                TariffElement.from_json(element, tax_included=tax_included)
                for element in data
            ]
        )

    def to_string(self, mono_line: bool = True) -> str:
        if mono_line:
            return "|".join(elt.to_string() for elt in self.elements)
        return "\n".join(elt.to_string() for elt in self.elements)

    def to_text(self) -> str:
        text = ""
        for dimension in TariffDimensionType:
            text_elements = []
            for element in self.elements:
                for pc in element.price_components:
                    if pc.type == PriceComponentTypeEnum[dimension.name]:
                        text_elements.append(
                            [
                                pc.price,
                                TariffDimensionUnit[dimension.name].value,
                                element.restrictions,
                            ]
                        )
            if len(text_elements) == 0:
                continue
            if [te[0] for te in text_elements] == [
                text_elements[0][0] for _ in text_elements
            ]:
                text += f"- {dimension.name.lower()} :\n"
                te_text = f"  - {text_elements[0][0]} {text_elements[0][1]}"
                text += te_text.rstrip() + "\n"
            else:
                text += f"- {dimension.name.lower()} :\n"
                valid_text_elements = [
                    te for te in text_elements if te[0] is not None and te[0] > 0
                ]
                for te in valid_text_elements:
                    restrictions = (
                        te[2].to_text()
                        if te[2] is not None and len(te[2].to_text()) > 0
                        else "sinon"
                    )
                    last = te == valid_text_elements[-1] or restrictions == "sinon"
                    te_text = f"  - {te[0]} {te[1]} {restrictions}"
                    text += te_text.rstrip() + "\n"
                    if last:
                        break
        return text

    @staticmethod
    def from_string(data: str) -> "TariffElements":
        data_line = data.replace("\n", "|").replace(" ", "")
        return TariffElements(
            elements=[
                TariffElement.from_string(elt)
                for elt in data_line.split("|")
                if elt != ""
            ]
        )


class TariffObject(BaseModel):
    """Internal tariff object compatible with a subset of OCPI."""

    country_code: Optional[
        Annotated[str, StringConstraints(min_length=2, max_length=2)]
    ] = None
    party_id: Optional[
        Annotated[str, StringConstraints(min_length=3, max_length=3)]
    ] = None
    tariff_id: str = Field(alias="id", max_length=36)
    currency: Optional[
        Annotated[str, StringConstraints(min_length=3, max_length=3)]
    ] = None
    elements: List[TariffElement] = Field(min_length=1)
    tariff_alt_text: Optional[List[TariffAltText]] = None
    start_date_time: Optional[AwareDatetime] = None
    end_date_time: Optional[AwareDatetime] = None
    last_updated: AwareDatetime
    tax_included: Optional[TaxIncludedEnum] = None
    min_price: Optional[Union[Price, DisplayPrice]] = None
    max_price: Optional[Union[Price, DisplayPrice]] = None

    @model_validator(mode="after")
    def check_application_dates(self) -> Self:
        if (
            self.start_date_time is not None
            and self.end_date_time is not None
            and self.start_date_time > self.end_date_time
        ):
            raise ValueError("A tariff cannot start after it has ended.")
        return self

    def __str__(self) -> str:
        return (
            f"Tariff(id={self.tariff_id}, elements={self.elements}, tariff_alt_text={self.tariff_alt_text}, "
            f"start_date_time={self.start_date_time}, end_date_time={self.end_date_time})"
        )

    @staticmethod
    def from_json(data: dict) -> "TariffObject":
        tax_included = (
            TaxIncludedEnum(data["tax_included"])
            if "tax_included" in data
            else TaxIncludedEnum.YES
        )
        tax = tax_included != TaxIncludedEnum.NO
        elements = TariffElements.from_json(data["elements"], tax_included=tax)
        kwargs = {
            "id": data["id"],
            "elements": elements,
            "tax_included": tax_included,
            "last_updated": (
                datetime.fromisoformat(data["last_updated"])
                if "last_updated" in data
                else datetime.now()
            ),
        }
        if "country_code" in data:
            kwargs["country_code"] = data["country_code"]
        if "party_id" in data:
            kwargs["party_id"] = data["party_id"]
        if "currency" in data:
            kwargs["currency"] = data["currency"]
        if "tariff_alt_text" in data:
            kwargs["tariff_alt_text"] = data["tariff_alt_text"]
        if "start_date_time" in data:
            kwargs["start_date_time"] = datetime.fromisoformat(data["start_date_time"])
        if "end_date_time" in data:
            kwargs["end_date_time"] = datetime.fromisoformat(data["end_date_time"])
        return TariffObject(**kwargs)

    def to_json(self, ocpi: bool = True, simple: bool = False) -> dict:
        if not ocpi:
            return self.model_dump(by_alias=True, exclude_none=True)
        data = {
            "id": self.tariff_id,
            "elements": self.elements.to_json(simple),
        }
        if self.currency is not None:
            data["currency"] = self.currency
        if self.tariff_alt_text is not None:
            data["tariff_alt_text"] = [
                item.model_dump() for item in self.tariff_alt_text
            ]
        if self.start_date_time is not None:
            data["start_date_time"] = self.start_date_time.isoformat()
        if self.end_date_time is not None:
            data["end_date_time"] = self.end_date_time.isoformat()
        if self.last_updated is not None:
            data["last_updated"] = self.last_updated.isoformat()
        if self.tax_included is not None:
            data["tax_included"] = self.tax_included.value
        if self.min_price is not None:
            data["min_price"] = (
                self.min_price
                if isinstance(self.min_price, float)
                else self.min_price.model_dump()
            )
        if self.max_price is not None:
            data["max_price"] = (
                self.max_price
                if isinstance(self.max_price, float)
                else self.max_price.model_dump()
            )
        return data

    def to_string(self) -> str:
        return self.elements.to_string()

    def to_text(self) -> str:
        text = f'Tariff : "{self.tariff_id}" version du {self.last_updated.strftime("%d/%m/%Y")}\n\n'
        if self.start_date_time is not None and self.end_date_time is not None:
            text += f"- applicable du {self.start_date_time.strftime('%d/%m/%Y')} au {self.end_date_time.strftime('%d/%m/%Y')}\n"
        elif self.start_date_time is not None:
            text += f"- applicable à partir du {self.start_date_time.strftime('%d/%m/%Y')}\n"
        elif self.end_date_time is not None:
            text += f"- applicable jusqu'au {self.end_date_time.strftime('%d/%m/%Y')}\n"
        text += self.elements.to_text()
        return text

    @staticmethod
    def from_string(
        data: str,
        id: str = "undefined",
        tariff_alt_text: Optional[List[TariffAltText]] = None,
        min_price: Optional[Price] = None,
        max_price: Optional[Price] = None,
        start_date_time: Optional[datetime] = None,
        end_date_time: Optional[datetime] = None,
        last_updated: Optional[datetime] = None,
    ) -> "TariffObject":
        elements = TariffElements.from_string(data)
        return TariffObject(
            id=id,
            elements=elements,
            tariff_alt_text=tariff_alt_text,
            min_price=min_price,
            max_price=max_price,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            last_updated=last_updated or datetime.now(),
        )

    @staticmethod
    def convert(data: str, format: Format) -> Union[str, dict]:
        if not isinstance(data, str):
            return {}
        if data[0].isdigit():
            tarif = TariffObject.from_json(
                {
                    "id": "undefined",
                    "elements": [
                        {
                            "price_components": [
                                {"type": "ENERGY", "price": float(data)}
                            ],
                        }
                    ],
                    "last_updated": datetime.now().isoformat(),
                }
            )
        elif data[0] == "{":
            tarif = TariffObject.from_json(json.loads(data))
        else:
            tarif = TariffObject.from_string(data)
        if format == Format.TEXT_LIGHT:
            return tarif.to_string()
        if format == Format.JSON_LIGHT:
            return tarif.to_json(ocpi=False, simple=False)
        if format == Format.JSON_LIGHT_PLUS:
            return tarif.to_json(ocpi=False, simple=True)
        return tarif.to_json(ocpi=True, simple=False)

    @staticmethod
    def is_valid_string(data: str) -> bool:
        return TARIFF_REGEX.match(data) is not None

    @staticmethod
    def is_valid_json(data: dict, verbose: bool = False) -> bool:
        with open("source/schema.json") as f:
            schema = json.load(f)
        try:
            validate(instance=data, schema=schema)
            if verbose:
                print(f"Validation réussie pour : {data.get('id', 'inconnu')}")
        except ValidationError as e:
            if verbose:
                print(f"Erreur de validation sur {data.get('id', 'Inconnu')} :")
                print(f"Message : {e.message}")
                print(f"Emplacement : {list(e.path)}")
            return False
        return True
