"""Tests for the tariff module."""

from datetime import time

from source.tariff import (
    Tariff,
    TariffElement,
    TariffElements,
    PriceComponent,
    TariffRestrictions,
    DayOfWeek,
)
from source.utils import Price, TariffDimensionType

'''def test_tariff():
    """Test the Tariff class."""
    price_component = PriceComponent(type="ENERGY", price=0.30)
    tariff_element = TariffElement(type="FLAT", price_components=[price_component])
    tariff_restrictions = TariffRestrictions(start_date_time="2024-01-01T00:00:00Z", end_date_time="2024-12-31T23:59:59Z")
    tariff = Tariff(id="tariff1", currency="EUR", elements=[tariff_element], last_updated="2024-06-01T12:00:00Z")
    
    assert tariff.id == "tariff1"
    assert tariff.currency == "EUR"
    assert len(tariff.elements) == 1
    assert tariff.elements[0].type == "FLAT"
    assert len(tariff.elements[0].price_components) == 1
    assert tariff.elements[0].price_components[0].type == "ENERGY"
    assert tariff.elements[0].price_components[0].price == 0.30
    assert tariff.last_updated == "2024-06-01T12:00:00Z"
'''


def test_price():
    """Test the Price class."""
    price = Price(amount=1.20)

    assert price.amount == 1.20
    assert price.excl_vat == 1.00
    assert price.vat == 0.20
    assert price.incl_vat == 1.20


def test_pricecomponent():
    """Test the PriceComponent class."""
    price = Price(amount=0.30)
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=price)

    assert price_component.type.value == "ENERGY"
    assert price_component.price.amount == 0.30


def test_pricecomponent_tax_included():
    """Test the PriceComponent class with tax included."""
    price = Price(amount=0.30)
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=price)
    tax_included = True
    assert price_component.to_json(tax_included=tax_included) == {
        "type": "ENERGY",
        "price": 0.3,
    }
    assert (
        PriceComponent.from_json(
            price_component.to_json(tax_included=tax_included),
            tax_included=tax_included,
        )
        == price_component
    )


def test_pricecomponent_tax_excluded():
    """Test the PriceComponent class with tax excluded."""
    price = Price(amount=0.30)
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=price)
    tax_included = False
    assert price_component.to_json(tax_included=tax_included) == {
        "type": "ENERGY",
        "price": 0.25,
    }
    assert (
        PriceComponent.from_json(
            price_component.to_json(tax_included=tax_included),
            tax_included=tax_included,
        )
        == price_component
    )


def test_tariffrestrictions():
    """Test the TariffRestrictions class."""
    restrictions = TariffRestrictions()

    assert restrictions.days_of_week is None
    assert restrictions.start_date is None
    assert restrictions.end_date is None
    assert restrictions.start_time is None
    assert restrictions.end_time is None
    assert restrictions.min_current is None
    assert restrictions.max_current is None
    assert restrictions.min_duration is None
    assert restrictions.max_duration is None
    assert restrictions.min_kwh is None
    assert restrictions.max_kwh is None
    assert restrictions.min_power is None
    assert restrictions.max_power is None


def test_tariffrestrictions_from_json():
    """Test the TariffRestrictions class from JSON."""
    json_data = {
        "days_of_week": ["MONDAY", "TUESDAY"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "start_time": "13:10",
        "end_time": "23:59",
        "min_current": 10.0,
        "max_current": 100.0,
        "min_duration": 30,
        "max_duration": 120,
        "min_kwh": 1.0,
        "max_kwh": 50.0,
        "min_power": 5.0,
        "max_power": 20.0,
    }
    # print(
    #    time.fromisoformat(json_data["start_time"] + ":00").isoformat(
    #        timespec="minutes"
    #    )
    # )
    restrictions = TariffRestrictions.from_json(json_data)
    # print(restrictions.start_time.isoformat())
    assert restrictions.days_of_week == [DayOfWeek.MONDAY, DayOfWeek.TUESDAY]
    assert restrictions.start_date.isoformat() == "2024-01-01"
    assert restrictions.end_date.isoformat() == "2024-12-31"
    assert restrictions.start_time.isoformat() == "13:10:00"
    assert restrictions.end_time.isoformat() == "23:59:00"
    assert restrictions.min_current == 10.0
    assert restrictions.max_current == 100.0
    assert restrictions.min_duration == 30
    assert restrictions.max_duration == 120
    assert restrictions.min_kwh == 1.0
    assert restrictions.max_kwh == 50.0
    assert restrictions.min_power == 5.0
    assert restrictions.max_power == 20.0
    assert restrictions.to_json() == json_data


def test_tariffelement():
    """Test the TariffElement class."""
    price_component = PriceComponent(
        type=TariffDimensionType.ENERGY, price=Price(amount=0.30)
    )
    restrictions = TariffRestrictions.from_json(
        {
            "days_of_week": ["MONDAY", "TUESDAY"],
            "start_date_time": "2024-01-01T00:00:00+00:00",
        }
    )
    tariff_element = TariffElement(
        price_components=[price_component], restrictions=restrictions
    )

    assert len(tariff_element.price_components) == 1
    assert tariff_element.price_components[0].type.value == "ENERGY"
    assert tariff_element.price_components[0].price.amount == 0.30


def test_tariffelement_from_json():
    """Test the TariffElement class from JSON."""
    json_data = {
        "price_components": [
            {
                "type": "ENERGY",
                "price": 0.31,
            }
        ],
        "restrictions": {
            "days_of_week": ["MONDAY", "TUESDAY"],
            "start_date": "2024-01-01",
            "start_time": "13:10",
        },
    }
    tariff_element = TariffElement.from_json(json_data)
    # print(tariff_element.to_json())
    assert len(tariff_element.price_components) == 1
    assert tariff_element.price_components[0].type.value == "ENERGY"
    assert tariff_element.price_components[0].price.amount == 0.31
    assert tariff_element.to_json() == json_data


def test_tariff():
    """Test the Tariff class."""
    price_component = PriceComponent(
        type=TariffDimensionType.ENERGY, price=Price(amount=0.30)
    )
    tariff_element = TariffElement(price_components=[price_component])
    tariff = Tariff(id="tariff1", elements=[tariff_element])

    assert tariff.id == "tariff1"
    assert len(tariff.elements) == 1
    assert len(tariff.elements[0].price_components) == 1
    assert tariff.elements[0].price_components[0].type == TariffDimensionType.ENERGY
    assert tariff.elements[0].price_components[0].price.amount == 0.30


def test_tariff_from_json():
    """Test the Tariff class from JSON."""
    json_data = {
        "id": "tariff1",
        "type": "AD_HOC_PAYMENT",
        "elements": [
            {
                "price_components": [
                    {
                        "type": "ENERGY",
                        "price": 0.30,
                    }
                ],
            }
        ],
        "last_updated": "2024-06-01T12:00:00+00:00",
        "tax_included": "YES",
    }
    tariff = Tariff.from_json(json_data)
    # print(tariff.to_json())
    assert tariff.id == "tariff1"
    assert len(tariff.elements) == 1
    assert len(tariff.elements[0].price_components) == 1
    assert tariff.elements[0].price_components[0].type.value == "ENERGY"
    assert tariff.elements[0].price_components[0].price.amount == 0.30
    assert tariff.last_updated.isoformat() == "2024-06-01T12:00:00+00:00"
    assert tariff.to_json() == json_data
    assert tariff.to_json(simple=True) == {
        "id": "tariff1",
        "elements": [{"price_components": {"ENERGY": 0.3}}],
    }
    assert (
        Tariff.from_json(tariff.to_json(simple=True)).to_json()["elements"]
        == json_data["elements"]
    )


def test_tariff_to_string():
    price_component1 = PriceComponent(
        type=TariffDimensionType.ENERGY, price=Price(amount=0.30)
    )
    price_component2 = PriceComponent(
        type=TariffDimensionType.FLAT, price=Price(amount=1.20)
    )
    price_component3 = PriceComponent(
        type=TariffDimensionType.ENERGY, price=Price(amount=0.10)
    )
    price_component4 = PriceComponent(
        type=TariffDimensionType.FLAT, price=Price(amount=1.50)
    )
    tariff_element1 = TariffElement(
        price_components=[price_component1, price_component2],
        restrictions=TariffRestrictions.from_json(
            {
                "days_of_week": ["MONDAY", "TUESDAY"],
                "start_date": "2024-01-01",
                "end_date": "2024-01-02",
                "start_time": "13:10",
                "end_time": "23:59",
            }
        ),
    )
    tariff_element2 = TariffElement(
        price_components=[price_component3, price_component4]
    )
    tariff_elements = TariffElements([tariff_element1, tariff_element2])
    tariff = Tariff(id="tariff1", elements=tariff_elements)

    assert tariff.to_string() == tariff_elements.to_string()
    assert (
        tariff.to_string()
        == "EN30+FL120+J=LuMa+D>2024-01-01+D<2024-01-02+T>13:10+T<23:59|EN10+FL150"
    )
    assert (
        TariffElements.from_string(tariff.to_string()).to_string() == tariff.to_string()
    )
    # print(TariffElements.from_string(tariff.to_string()).to_json(simple=True))


test_price()
test_pricecomponent()
test_pricecomponent_tax_included()
test_pricecomponent_tax_excluded()
test_tariffrestrictions()
test_tariffrestrictions_from_json()
test_tariffelement()
test_tariffelement_from_json()
test_tariff()
test_tariff_from_json()
test_tariff_to_string()

# option complete pour json
