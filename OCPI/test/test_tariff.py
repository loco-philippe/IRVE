"""Tests for the tariff module."""

import json

from source.tariff import (
    Tariff,
    TariffElement,
    TariffElements,
    PriceComponent,
    TariffRestrictions,
    DayOfWeek,
)
from source.utils import Format, Price, TariffDimensionType


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
    restrictions = TariffRestrictions.from_json(json_data)
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
    tariff = Tariff(
        id="tariff1", elements=[tariff_element], last_updated="2024-06-01T12:00:00Z"
    )

    assert tariff.id == "tariff1"
    assert len(tariff.elements) == 1
    assert len(tariff.elements[0].price_components) == 1
    assert tariff.elements[0].price_components[0].type == TariffDimensionType.ENERGY
    assert tariff.elements[0].price_components[0].price.amount == 0.30
    assert tariff.last_updated == "2024-06-01T12:00:00Z"


def test_tariff_json():
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
    assert tariff.to_json(ocpi=False, simple=True) == {
        "id": "tariff1",
        "elements": [{"price_components": {"ENERGY": 0.3}}],
        "last_updated": "2024-06-01T12:00:00+00:00",
    }
    assert (
        Tariff.from_json(tariff.to_json(simple=True)).to_json()["elements"]
        == json_data["elements"]
    )
    assert json.dumps(
        Tariff.convert(json.dumps(tariff.to_json()), Format.JSON_OCPI)
    ) == json.dumps(tariff.to_json())
    assert json.dumps(
        Tariff.convert(json.dumps(tariff.to_json(simple=True)), Format.JSON_LIGHT)
    ) == json.dumps(tariff.to_json(ocpi=False, simple=False))


def test_tariff_string():
    """Test the Tariff class from string and to string."""
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
                "min_power": 20,
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
        == "EN30+FL120+J=LuMa+D>2024-01-01+D<2024-01-02+T>13:10+T<23:59+P>20|EN10+FL150"
    )
    assert (
        TariffElements.from_string(tariff.to_string()).to_string() == tariff.to_string()
    )
    assert Tariff.convert(tariff.to_string(), Format.TEXT_LIGHT) == tariff.to_string()


def test_string_validation():
    """Test the regular expression for tariff strings."""
    test_ok = [
        "0.25",
        "EN30+FL120",
        "EN30+FL120+D>2024-01-01",
        "EN30+FL120+D>2024-01-01+T<10:45",
        "A<248",
        "J=SaDi",
        "EN30+FL120|EN15+J=LuMe",
    ]
    test_ko = ["EN30++FL120", "J=DiSa", "J=", "EN30+xx120", "EN30+D>2024", "|", "|EN40"]

    for tst in test_ok:
        assert Tariff.is_valid_string(tst)
    for tst in test_ko:
        assert not Tariff.is_valid_string(tst)


def test_json_validation():
    """Test the JSON schema for the Tariff class."""
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
    assert Tariff.is_valid_json(json_data)

    with open("examples/examples.json") as f:
        examples_data = json.load(f)
    for example in examples_data:
        assert Tariff.is_valid_json(example)


def test_to_text():
    """Test the to_text method of the Tariff class."""

    with open("examples/examples.json") as f:
        examples_data = json.load(f)
    text = "# tarifs au format texte des exemples du fichier examples.json\n\n"
    for example in examples_data:
        tariff = Tariff.from_json(example)
        text += tariff.to_text() + "\n"
    with open("examples/examples.md", "w", encoding="utf-8") as f:
        f.write(text[:-1])


test_price()
test_pricecomponent()
test_pricecomponent_tax_included()
test_pricecomponent_tax_excluded()
test_tariffrestrictions()
test_tariffrestrictions_from_json()
test_tariffelement()
test_tariffelement_from_json()
test_tariff()
test_tariff_json()
test_tariff_string()
test_string_validation()
test_json_validation()
test_to_text()
