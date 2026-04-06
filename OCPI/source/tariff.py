"""Tariff module for handling tariff-related operations."""

from datetime import datetime, date, time

from .utils import (
    DayOfWeek,
    DayOfWeekCode,
    OCPIBaseModel,
    Price,
    TariffDimensionCode,
    TariffRestrictionsCode,
    TariffDimensionType,
    TariffType,
    TaxIncluded,
)


class PriceComponent(OCPIBaseModel):
    """Represents a price component within a tariff element."""

    def __init__(self, type: TariffDimensionType, price: Price):
        self.type = type
        self.price = price

    def __str__(self):
        return f"PriceComponent(type={self.type}, price={self.price})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        return self.type == other.type and self.price == other.price

    def __hash__(self):
        return hash((self.type, self.price))

    def __lt__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        return self.price.amount < other.price.amount

    def __le__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        return self.price.amount <= other.price.amount

    def __gt__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        return self.price.amount > other.price.amount

    def __ge__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        return self.price.amount >= other.price.amount

    def __ne__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        return self.price.amount != other.price.amount

    def __add__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        if self.type != other.type:
            raise ValueError("Cannot add PriceComponents of different types")
        return PriceComponent(
            type=self.type, price=Price(amount=self.price.amount + other.price.amount)
        )

    def __sub__(self, other):
        if not isinstance(other, PriceComponent):
            return NotImplemented
        if self.type != other.type:
            raise ValueError("Cannot subtract PriceComponents of different types")
        return PriceComponent(
            type=self.type, price=Price(amount=self.price.amount - other.price.amount)
        )

    @staticmethod
    def from_price(type: TariffDimensionType, price: Price):
        """Create a PriceComponent from a Price."""
        return PriceComponent(type=type, price=price)

    @staticmethod
    def from_amount(
        type: TariffDimensionType, amount: float, tax_included: bool = True
    ):
        """Create a PriceComponent from an amount."""
        return PriceComponent(
            type=type, price=Price(amount=amount, tax_included=tax_included)
        )

    @staticmethod
    def from_excl_vat(type: TariffDimensionType, excl_vat: float):
        """Create a PriceComponent from an excl_vat amount."""
        price = Price(amount=excl_vat * 1.20)
        return PriceComponent(type=type, price=price)

    @staticmethod
    def from_incl_vat(type: TariffDimensionType, incl_vat: float):
        """Create a PriceComponent from an incl_vat amount."""
        price = Price(amount=incl_vat)
        return PriceComponent(type=type, price=price)

    @classmethod
    def from_price_component(cls, price_component: "PriceComponent"):
        """Create a PriceComponent from another PriceComponent."""
        return cls(type=price_component.type, price=price_component.price)

    @staticmethod
    def from_json(data: dict, tax_included: bool = True):
        """Create a PriceComponent from a JSON dictionary."""
        type = TariffDimensionType(data["type"])
        amount = data["price"]
        price = Price(amount=amount, tax_included=tax_included)
        return PriceComponent(type=type, price=price)

    def to_json(self, tax_included: bool = True) -> dict:
        """Convert the PriceComponent to a JSON dictionary."""
        return {
            "type": self.type.value,
            "price": self.price.incl_vat if tax_included else self.price.excl_vat,
        }

    @staticmethod
    def from_string(data: str):
        """Create a PriceComponent from a string representation."""
        parts = data.split("+")
        price_components = []
        for part in parts:
            code = part[:2]
            if code in [cod.value for cod in TariffDimensionCode]:
                type = TariffDimensionType[TariffDimensionCode(code).name]
                price = Price(amount=float(part[2:]) / 100)
                price_components.append(PriceComponent(type=type, price=price))
        return price_components

    def to_string(self):
        """Convert the PriceComponent to a string representation."""
        return f"{self.type.code}{int(self.price.incl_vat * 100)}"


class TariffRestrictions(OCPIBaseModel):
    """Represents restrictions that may apply to a tariff."""

    def __init__(self):
        self.days_of_week: list[DayOfWeek] = None
        self.start_date: date = None
        self.end_date: date = None
        self.start_time: time = None
        self.end_time: time = None
        self.min_current: float = None
        self.max_current: float = None
        self.min_duration: int = None
        self.max_duration: int = None
        self.min_kwh: float = None
        self.max_kwh: float = None
        self.min_power: float = None
        self.max_power: float = None

    def __str__(self):
        return "TariffRestrictions(truc)"

    def __len__(self):
        return len(self.to_json())

    @staticmethod
    def from_json(data: dict):
        """Create a TariffRestrictions object from a JSON dictionary."""
        # print(data)
        restrictions = TariffRestrictions()
        if "days_of_week" in data:
            restrictions.days_of_week = [DayOfWeek(day) for day in data["days_of_week"]]
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
        """Convert the TariffRestrictions object to a JSON dictionary."""
        data = {}
        if self.days_of_week is not None:
            data["days_of_week"] = [day.value for day in self.days_of_week]
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

    def to_string(self) -> str:
        """Convert the TariffRestrictions object to a string representation."""
        parts = []
        if self.days_of_week is not None:
            parts.append("J=" + "".join(day.code for day in self.days_of_week))
        if self.start_date is not None:
            parts.append(f"D>{self.start_date.isoformat()}")
        if self.end_date is not None:
            parts.append(f"D<{self.end_date.isoformat()}")
        if self.start_time is not None:
            parts.append(f"T>{self.start_time.isoformat(timespec='minutes')}")
        if self.end_time is not None:
            parts.append(f"T<{self.end_time.isoformat(timespec='minutes')}")
        if self.min_current is not None:
            parts.append(f"A>{int(self.min_current)}")
        if self.max_current is not None:
            parts.append(f"A<{int(self.max_current)}")
        if self.min_duration is not None:
            parts.append(f"I<{int(self.min_duration)}")
        if self.max_duration is not None:
            parts.append(f"I>{int(self.max_duration)}")
        if self.min_kwh is not None:
            parts.append(f"K>{int(self.min_kwh)}")
        if self.max_kwh is not None:
            parts.append(f"K<{int(self.max_kwh)}")
        if self.min_power is not None:
            parts.append(f"P>{int(self.min_power)}")
        if self.max_power is not None:
            parts.append(f"P<{int(self.max_power)}")
        return "+".join(parts)

    @staticmethod
    def from_string(data: str):
        """Create a TariffRestrictions from a string representation."""
        parts = data.split("+")
        restrictions = TariffRestrictions()
        for part in parts:
            code = part[:2]
            value = part[2:]
            if code == "J=":
                day_codes = [value[i : i + 2] for i in range(0, len(value), 2)]
                restrictions.days_of_week = [
                    DayOfWeek[DayOfWeekCode(day).name] for day in day_codes
                ]
            elif code == "D>":
                restrictions.start_date = date.fromisoformat(value)
            elif code == "D<":
                restrictions.end_date = date.fromisoformat(value)
            elif code == "T>":
                restrictions.start_time = time.fromisoformat(value + ":00")
            elif code == "T<":
                restrictions.end_time = time.fromisoformat(value + ":00")
            elif code == "A>":
                restrictions.min_current = float(value)
            elif code == "A<":
                restrictions.max_current = float(value)
            elif code == "I>":
                restrictions.min_duration = int(value)
            elif code == "I<":
                restrictions.max_duration = int(value)
            elif code == "K>":
                restrictions.min_kwh = float(value)
            elif code == "K<":
                restrictions.max_kwh = float(value)
            elif code == "P>":
                restrictions.min_power = float(value)
            elif code == "P<":
                restrictions.max_power = float(value)
        return restrictions


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

    @staticmethod
    def from_json(data: dict, tax_included: bool = True):
        """Create a TariffElement from a JSON dictionary."""
        if isinstance(data["price_components"], dict):
            price_components = [
                PriceComponent.from_json(
                    {
                        "type": type,
                        "price": amount,
                    }
                )
                for type, amount in data["price_components"].items()
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

    def to_json(self, simple: bool = False, tax_included: bool = True) -> dict:
        """Convert the TariffElement to a JSON dictionary."""
        if simple:
            data = {
                "price_components": {
                    pc.type.value: pc.price.incl_vat for pc in self.price_components
                }
            }
        else:
            data = {
                "price_components": [
                    pc.to_json(tax_included=tax_included)
                    for pc in self.price_components
                ]
            }
        if self.restrictions is not None:
            data["restrictions"] = self.restrictions.to_json()
        return data

    def to_string(self):
        """Convert the TariffElement to a string representation."""
        text = "+".join(pc.to_string() for pc in self.price_components)
        if self.restrictions is not None and len(self.restrictions) > 0:
            text += "+" + self.restrictions.to_string()
        return text

    @staticmethod
    def from_string(data: str):
        """Create a TariffElement from a string representation."""
        price_components = PriceComponent.from_string(data)
        restrictions = TariffRestrictions.from_string(data)
        restrictions = None if len(restrictions) == 0 else restrictions
        return TariffElement(
            price_components=price_components, restrictions=restrictions
        )


class TariffElements(OCPIBaseModel):
    """Represents a list of tariff elements."""

    def __init__(self, elements: list[TariffElement]):
        self.elements = elements

    def __str__(self):
        return f"TariffElements(elements={self.elements})"

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def to_json(self, simple=False, tax=True) -> list[dict]:
        """Convert the TariffElements to a JSON list."""
        return [element.to_json(simple, tax) for element in self.elements]

    @staticmethod
    def from_json(data: list[dict], tax_included: bool = True):
        """Create TariffElements from a JSON list."""
        return TariffElements(
            elements=[
                TariffElement.from_json(element, tax_included=tax_included)
                for element in data
            ]
        )

    def to_string(self, mono_line: bool = True):
        """Convert the TariffElements to a string representation."""
        if mono_line:
            return "|".join(elt.to_string() for elt in self.elements)
        else:
            return "\n".join(elt.to_string() for elt in self.elements)

    @staticmethod
    def from_string(data: str):
        """Create TariffElements from a string representation."""
        data_line = data.replace("\n", "|").replace(" ", "")
        return TariffElements(
            [
                TariffElement.from_string(elt)
                for elt in data_line.split("|")
                if elt != ""
            ]
        )


class Tariff(OCPIBaseModel):
    """Represents a tariff in the OCPI protocol."""

    def __init__(
        self,
        id: str,
        elements: TariffElements,
        type: TariffType = TariffType.AD_HOC_PAYMENT,
        tariff_alt_text: str = None,
        min_price: Price = None,
        max_price: Price = None,
        start_date_time: datetime = None,
        end_date_time: datetime = None,
        last_updated: datetime = None,
        tax_included: TaxIncluded = TaxIncluded.YES,
    ):
        self.id = id
        self.elements = elements
        self.type = type
        self.tariff_alt_text = tariff_alt_text
        self.min_price = min_price
        self.max_price = max_price
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.last_updated = last_updated
        self.tax_included = tax_included

    def __str__(self):
        return f"Tariff(id={self.id}, type={self.type}, elements={self.elements}, tariff_alt_text={self.tariff_alt_text}, start_date_time={self.start_date_time}, end_date_time={self.end_date_time})"

    @staticmethod
    def from_json(data: dict):
        """Create a Tariff from a JSON dictionary."""
        id = data["id"]
        tax_included = (
            TaxIncluded(data["tax_included"])
            if "tax_included" in data
            else TaxIncluded.YES
        )
        tax = True if tax_included != TaxIncluded.NO else False
        elements = TariffElements.from_json(data["elements"], tax_included=tax)
        type = TariffType(data["type"]) if "type" in data else TariffType.AD_HOC_PAYMENT
        tariff_alt_text = data.get("tariff_alt_text")
        min_price = (
            Price(amount=data["min_price"], tax_included=tax)
            if "min_price" in data
            else None
        )
        max_price = (
            Price(amount=data["max_price"], tax_included=tax)
            if "max_price" in data
            else None
        )
        start_date_time = (
            datetime.fromisoformat(data["start_date_time"])
            if "start_date_time" in data
            else None
        )
        end_date_time = (
            datetime.fromisoformat(data["end_date_time"])
            if "end_date_time" in data
            else None
        )
        last_updated = (
            datetime.fromisoformat(data["last_updated"])
            if "last_updated" in data
            else None
        )
        return Tariff(
            id=id,
            elements=elements,
            type=type,
            tariff_alt_text=tariff_alt_text,
            min_price=min_price,
            max_price=max_price,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            tax_included=tax_included,
            last_updated=last_updated,
        )

    def to_json(self, simple=False) -> dict:
        """Convert the Tariff to a JSON dictionary."""
        if simple and self.type != TariffType.AD_HOC_PAYMENT:
            return NotImplemented
        tax = True if simple else self.tax_included != TaxIncluded.NO
        data = {
            "id": self.id,
            "elements": self.elements.to_json(simple, tax),
        }
        if self.type is not None and not simple:
            data["type"] = self.type.value
        if self.tariff_alt_text is not None:
            data["tariff_alt_text"] = self.tariff_alt_text
        if self.min_price is not None and not simple:
            data["min_price"] = self.min_price.amount
        if self.max_price is not None and not simple:
            data["max_price"] = self.max_price.amount
        if self.start_date_time is not None:
            data["start_date_time"] = self.start_date_time.isoformat()
        if self.end_date_time is not None:
            data["end_date_time"] = self.end_date_time.isoformat()
        if self.last_updated is not None and not simple:
            data["last_updated"] = self.last_updated.isoformat()
        if self.tax_included is not None and not simple:
            data["tax_included"] = self.tax_included.value
        return data

    def to_string(self):
        """Convert the Tariff to a string representation."""
        return self.elements.to_string()

    @staticmethod
    def from_string(
        data: str,
        id: str,
        tariff_alt_text: str = None,
        min_price: Price = None,
        max_price: Price = None,
        start_date_time: datetime = None,
        end_date_time: datetime = None,
        last_updated: datetime = None,
    ):
        """Create a Tariff from a string representation."""
        elements = TariffElements.from_string(data)
        return Tariff(
            id=id,
            elements=elements,
            tariff_alt_text=tariff_alt_text,
            min_price=min_price,
            max_price=max_price,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            last_updated=last_updated,
        )
