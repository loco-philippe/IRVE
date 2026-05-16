"""Pydantic tariff models for the OCPI source package."""

from __future__ import annotations

import json
from datetime import date, time
from enum import StrEnum
from typing import Annotated, List, Optional, Union

from annotated_types import Ge
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pydantic import BaseModel, Field, RootModel, StringConstraints, model_validator
from pydantic.types import AwareDatetime
from typing_extensions import Self

from .utils import (
    DayOfWeekCode,
    TariffDimensionText,
    TariffDimensionUnit,
    TariffRestrictionsText,
    TariffRestrictionsUnit,
    VAT,
)


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
    def code(self):
        """text code of the day."""
        return DayOfWeekCode[self.name].value


class TariffTypeEnum(StrEnum):
    """Enumeration for tariff types."""

    AD_HOC_PAYMENT = "AD_HOC_PAYMENT"
    PROFILE_CHEAP = "PROFILE_CHEAP"
    PROFILE_FAST = "PROFILE_FAST"
    PROFILE_GREEN = "PROFILE_GREEN"
    REGULAR = "REGULAR"


class TariffDimensionTypeEnum(StrEnum):
    """Enumeration for tariff dimension types."""

    ENERGY = "ENERGY"
    TIME = "TIME"
    FLAT = "FLAT"
    PARKING_TIME = "PARKING_TIME"
    CONGESTION_TIME = "CONGESTION_TIME"

    @property
    def text(self):
        """text of the dimension."""
        return TariffDimensionText[self.name].value

    @property
    def unit(self):
        """unit of the dimension."""
        return TariffDimensionUnit[self.name].value


class TaxIncludedEnum(StrEnum):
    """Whether tariff prices include taxes."""

    YES = "YES"
    NO = "NO"
    NA = "N/A"


class TariffAltText(BaseModel):
    """Localized tariff display text."""

    language: str
    text: str


class PriceLimit(BaseModel):
    """OCPI 2.3 price with taxes split."""

    before_taxes: float
    after_taxes: Optional[float] = None


class Price(BaseModel):
    """OCPI 2.2 price with VAT split."""

    excl_vat: float
    incl_vat: Optional[float] = None


class PriceComponent(BaseModel):
    """A tariff price component."""

    type: TariffDimensionTypeEnum
    price: Annotated[float, Ge(0.0)]
    vat: Optional[float] = None
    step_size: Optional[Annotated[int, Ge(1)]] = None

    def to_json(
        self, tax_included: bool, incl_vat: bool, vat_rate: float = VAT
    ) -> dict:
        return {
            "type": self.type.value,
            "price": (
                self.price_incl_vat(tax_included=tax_included, vat_rate=vat_rate)
                if incl_vat
                else self.price_excl_vat(tax_included=tax_included, vat_rate=vat_rate)
            ),
        }

    def price_excl_vat(self, tax_included: bool, vat_rate: float = VAT) -> float:
        if not tax_included:
            return self.price
        return round(self.price / (1 + vat_rate), 2)

    def price_incl_vat(self, tax_included: bool, vat_rate: float = VAT) -> float:
        if tax_included:
            return self.price
        return round(self.price * (1 + vat_rate), 2)


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

    @property
    def text(self):
        """text of the restriction."""
        return TariffRestrictionsText[self.name].value

    @property
    def unit(self):
        """unit of the restriction."""
        return TariffRestrictionsUnit[self.name].value

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
                + TariffRestrictionsUnit.DAYS_OF_WEEK.value
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
                + TariffRestrictionsUnit.START_DATE.value
            )
        elif self.end_date is not None:
            parts.append(
                TariffRestrictionsText.END_DATE.value
                + " "
                + self.end_date.isoformat()
                + TariffRestrictionsUnit.END_DATE.value
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
                + TariffRestrictionsUnit.START_TIME.value
            )
        elif self.end_time is not None:
            parts.append(
                TariffRestrictionsText.END_TIME.value
                + " "
                + self.end_time.isoformat(timespec="minutes")
                + TariffRestrictionsUnit.END_TIME.value
            )
        if self.min_current is not None and self.min_current > 0:
            parts.append(
                TariffRestrictionsText.MIN_CURRENT.value
                + " "
                + str(int(self.min_current))
                + TariffRestrictionsUnit.MIN_CURRENT.value
            )
        if self.max_current is not None:
            parts.append(
                TariffRestrictionsText.MAX_CURRENT.value
                + " "
                + str(int(self.max_current))
                + TariffRestrictionsUnit.MAX_CURRENT.value
            )
        if (
            self.min_duration is not None
            and self.min_duration > 0
            and self.max_duration is not None
        ):
            parts.append(
                "si la durée est comprise entre "
                + str(int(self.min_duration / 60))
                + TariffRestrictionsUnit.MAX_DURATION.value
                + " et "
                + str(int(self.max_duration / 60))
                + TariffRestrictionsUnit.MAX_DURATION.value
            )
        elif self.min_duration is not None and self.min_duration > 0:
            parts.append(
                TariffRestrictionsText.MIN_DURATION.value
                + " "
                + str(int(self.min_duration / 60))
                + TariffRestrictionsUnit.MIN_DURATION.value
            )
        elif self.max_duration is not None:
            parts.append(
                TariffRestrictionsText.MAX_DURATION.value
                + " "
                + str(int(self.max_duration / 60))
                + TariffRestrictionsUnit.MAX_DURATION.value
            )
        if self.min_kwh is not None and self.min_kwh > 0 and self.max_kwh is not None:
            parts.append(
                "si l'énergie est comprise entre "
                + str(int(self.min_kwh))
                + TariffRestrictionsUnit.MIN_KWH.value
                + " et "
                + str(int(self.max_kwh))
                + TariffRestrictionsUnit.MAX_KWH.value
            )
        elif self.min_kwh is not None and self.min_kwh > 0:
            parts.append(
                TariffRestrictionsText.MIN_KWH.value
                + " "
                + str(int(self.min_kwh))
                + TariffRestrictionsUnit.MIN_KWH.value
            )
        elif self.max_kwh is not None:
            parts.append(
                TariffRestrictionsText.MAX_KWH.value
                + " "
                + str(int(self.max_kwh))
                + TariffRestrictionsUnit.MAX_KWH.value
            )
        if (
            self.min_power is not None
            and self.min_power > 0
            and self.max_power is not None
        ):
            parts.append(
                "si la puissance est comprise entre "
                + str(int(self.min_power))
                + TariffRestrictionsUnit.MIN_POWER.value
                + " et "
                + str(int(self.max_power))
                + TariffRestrictionsUnit.MAX_POWER.value
            )
        elif self.min_power is not None and self.min_power > 0:
            parts.append(
                TariffRestrictionsText.MIN_POWER.value
                + " "
                + str(int(self.min_power))
                + TariffRestrictionsUnit.MIN_POWER.value
            )
        elif self.max_power is not None:
            parts.append(
                TariffRestrictionsText.MAX_POWER.value
                + " "
                + str(int(self.max_power))
                + TariffRestrictionsUnit.MAX_POWER.value
            )
        return "" if not parts else " et ".join(parts)


class TariffElement(BaseModel):
    """A tariff element, composed of prices and optional restrictions."""

    price_components: List[PriceComponent] = Field(min_length=1)
    restrictions: Optional[TariffRestrictions] = None

    def to_json(self, simple: bool, tax_included: bool, incl_vat: bool) -> dict:
        if simple:
            data = {
                "price_components": {
                    pc.type.value: pc.price for pc in self.price_components
                }
            }
        else:
            data = {
                "price_components": [
                    pc.to_json(tax_included=tax_included, incl_vat=incl_vat)
                    for pc in self.price_components
                ]
            }
        if self.restrictions is not None:
            data["restrictions"] = self.restrictions.to_json()
        return data


class TariffElements(RootModel[List[TariffElement]]):
    """Represents a list of tariff elements."""

    root: List[TariffElement] = Field(min_length=1)

    def to_json(self, simple: bool, tax_included: bool, incl_vat: bool) -> list[dict]:
        return [
            element.to_json(simple, tax_included=tax_included, incl_vat=incl_vat)
            for element in self.root
        ]

    def to_text(self, tax_included: bool) -> str:
        text = ""
        for dimension in TariffDimensionTypeEnum:
            text_elements = []
            for element in self.root:
                for pc in element.price_components:
                    if pc.type == TariffDimensionTypeEnum[dimension.name]:
                        text_elements.append(
                            {
                                "price": pc.price_incl_vat(tax_included=tax_included),
                                "unit": dimension.unit,
                                "restrictions": element.restrictions,
                            }
                        )
            if len(text_elements) == 0:
                continue
            if [te["price"] for te in text_elements] == [
                text_elements[0]["price"]
            ] * len(text_elements):
                text += f"- {dimension.text} :\n"
                te_text = f"  - {text_elements[0]['price']} {text_elements[0]['unit']}"
                text += te_text.rstrip() + "\n"
            else:
                text += f"- {dimension.text} :\n"
                valid_text_elements = [
                    te
                    for te in text_elements
                    if te["price"] is not None and te["price"] > 0
                ]
                for te in valid_text_elements:
                    restrictions = (
                        te["restrictions"].to_text()
                        if te["restrictions"] is not None
                        and len(te["restrictions"].to_text()) > 0
                        else "sinon"
                    )
                    last = te == valid_text_elements[-1] or restrictions == "sinon"
                    te_text = f"  - {te['price']} {te['unit']} {restrictions}"
                    text += te_text.rstrip() + "\n"
                    if last:
                        break
        return text


class TariffObject(BaseModel):
    """Internal tariff object compatible with a subset of OCPI."""

    country_code: Annotated[str, StringConstraints(min_length=2, max_length=2)]
    party_id: Annotated[str, StringConstraints(min_length=3, max_length=3)]
    id: Annotated[str, StringConstraints(max_length=36)]
    currency: Optional[
        Annotated[str, StringConstraints(min_length=3, max_length=3)]
    ] = None
    type: Optional[TariffTypeEnum] = None
    elements: TariffElements
    tariff_alt_text: Optional[List[TariffAltText]] = None
    start_date_time: Optional[AwareDatetime] = None
    end_date_time: Optional[AwareDatetime] = None
    last_updated: AwareDatetime
    tax_included: Optional[TaxIncludedEnum] = None
    min_price: Optional[Union[Price, PriceLimit]] = None
    max_price: Optional[Union[Price, PriceLimit]] = None

    @model_validator(mode="after")
    def check_application_dates(self) -> Self:
        if (
            self.start_date_time is not None
            and self.end_date_time is not None
            and self.start_date_time > self.end_date_time
        ):
            raise ValueError(
                f"Tariff {self.tariff_id} cannot start after it has ended."
            )
        if self.end_date_time is not None and self.last_updated > self.end_date_time:
            raise ValueError(
                f"Tariff {self.tariff_id} cannot end before his last updated time."
            )
        return self

    @model_validator(mode="after")
    def check_valid_enums(self) -> Self:
        if self.type is not None and self.type != TariffTypeEnum.AD_HOC_PAYMENT:
            # raise ValueError(f"Tariff {self.tariff_id} type must be 'AD_HOC_PAYMENT'.")
            print(f"Tariff {self.tariff_id} type must be 'AD_HOC_PAYMENT'.")
        # if self.country_code is not None and self.country_code != "FR":
        #    raise ValueError(f"Tariff {self.tariff_id} country_code must be 'FR'.")
        if self.currency is not None and self.currency != "EUR":
            print(f"Tariff {self.tariff_id} currency must be 'EUR'.")
        if self.tax_included is not None and self.tax_included == TaxIncludedEnum.NA:
            print(f"Tariff {self.tariff_id} tax_included must not be 'NA'.")
        return self

    @property
    def tariff_application_date(self) -> AwareDatetime:
        return max(self.start_date_time or self.last_updated, self.last_updated)

    @property
    def tariff_id(self) -> str:
        return self.country_code + self.party_id + self.id

    @property
    def is_ocpi_23(self) -> bool:
        return self.tax_included is not None

    @property
    def is_tax_included(self) -> bool:
        return (
            self.tax_included is not None and self.tax_included == TaxIncludedEnum.YES
        )

    def to_json(
        self, ocpi: bool = True, simple: bool = False, incl_vat: bool = True
    ) -> dict:
        data = {
            "country_code": self.country_code,
            "party_id": self.party_id,
            "id": self.id,
            "elements": self.elements.to_json(
                simple, tax_included=self.is_tax_included, incl_vat=incl_vat
            ),
        }
        if self.type is not None and ocpi:
            data["type"] = self.type.value
        if self.currency is not None and ocpi:
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
        if self.tax_included is not None and ocpi:
            data["tax_included"] = self.tax_included.value
        if self.min_price is not None and ocpi:
            data["min_price"] = (
                self.min_price
                if isinstance(self.min_price, float)
                else self.min_price.model_dump()
            )
        if self.max_price is not None and ocpi:
            data["max_price"] = (
                self.max_price
                if isinstance(self.max_price, float)
                else self.max_price.model_dump()
            )
        return data

    def to_text(self) -> str:
        text = f'Tariff : "{self.tariff_id}" version du {self.last_updated.strftime("%d/%m/%Y")}\n\n'
        if (
            self.tariff_application_date != self.last_updated
            and self.end_date_time is not None
        ):
            text += f"- applicable du {self.tariff_application_date.strftime('%d/%m/%Y')} au {self.end_date_time.strftime('%d/%m/%Y')}\n"
        elif self.tariff_application_date != self.last_updated:
            text += f"- applicable à partir du {self.tariff_application_date.strftime('%d/%m/%Y')}\n"
        elif self.end_date_time is not None:
            text += f"- applicable jusqu'au {self.end_date_time.strftime('%d/%m/%Y')}\n"
        text += self.elements.to_text(tax_included=self.is_tax_included)
        return text

    @staticmethod
    def is_valid_json(data: dict, verbose: bool = False) -> bool:
        with open("OCPI/source/schema.json") as f:
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
