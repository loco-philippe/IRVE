"""Tests for the tariff module."""

from datetime import datetime
import json

from OCPI.source.tariff2 import (
    TariffObject,
    TariffElement,
    TariffElements,
    PriceComponent,
    TariffRestrictions,
    DayOfWeekEnum,
)
from OCPI.source.utils import Format, TariffDimensionType


def test_pricecomponent():
    """Test the PriceComponent class."""
    price = 0.30
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=price)

    assert price_component.type.value == "ENERGY"
    assert price_component.price == 0.30


def test_pricecomponent_tax_included():
    """Test the PriceComponent class with tax included."""
    price = 0.30
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=price)
    tax_included = True
    assert price_component.to_json(tax_included=tax_included, incl_vat=True) == {
        "type": "ENERGY",
        "price": 0.3,
    }
    assert (
        PriceComponent.model_validate(
            price_component.to_json(tax_included=tax_included, incl_vat=True)
        )
        == price_component
    )
    tax_included = False
    assert price_component.to_json(tax_included=tax_included, incl_vat=True) == {
        "type": "ENERGY",
        "price": 0.36,
    }


def test_pricecomponent_tax_excluded():
    """Test the PriceComponent class with tax excluded."""
    price = 0.30
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=price)
    tax_included = False
    assert price_component.to_json(tax_included=tax_included, incl_vat=True) == {
        "type": "ENERGY",
        "price": 0.36,
    }
    assert (
        PriceComponent.model_validate(
            price_component.to_json(tax_included=tax_included, incl_vat=False)
        )
        == price_component
    )


def test_tariffrestrictions():
    """Test the TariffRestrictions class."""
    restrictions = TariffRestrictions()

    assert restrictions.day_of_week is None
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
        "day_of_week": ["MONDAY", "TUESDAY"],
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
    restrictions = TariffRestrictions.model_validate(json_data)
    assert restrictions.day_of_week == [DayOfWeekEnum.MONDAY, DayOfWeekEnum.TUESDAY]
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
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=0.30)
    restrictions = TariffRestrictions.model_validate(
        {
            "day_of_week": ["MONDAY", "TUESDAY"],
            "start_date_time": "2024-01-01T00:00:00+00:00",
        }
    )
    tariff_element = TariffElement(
        price_components=[price_component], restrictions=restrictions
    )

    assert len(tariff_element.price_components) == 1
    assert tariff_element.price_components[0].type.value == "ENERGY"
    assert tariff_element.price_components[0].price == 0.30


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
            "day_of_week": ["MONDAY", "TUESDAY"],
            "start_date": "2024-01-01",
            "start_time": "13:10",
        },
    }
    tariff_element = TariffElement.model_validate(json_data)
    assert len(tariff_element.price_components) == 1
    assert tariff_element.price_components[0].type.value == "ENERGY"
    assert tariff_element.price_components[0].price == 0.31
    assert (
        tariff_element.to_json(simple=False, tax_included=False, incl_vat=False)
        == json_data
    )


def test_tariff():
    """Test the Tariff class."""
    price_component = PriceComponent(type=TariffDimensionType.ENERGY, price=0.30)
    tariff_elements = TariffElements(
        root=[TariffElement(price_components=[price_component])]
    )
    tariff = TariffObject(
        country_code="FR",
        party_id="QUA",
        id="tariff1",
        elements=tariff_elements,
        last_updated="2024-06-01T12:00:00Z",
    )

    assert tariff.tariff_id == "FRQUAtariff1"
    assert len(tariff.elements.root) == 1
    assert len(tariff.elements.root[0].price_components) == 1
    assert (
        tariff.elements.root[0].price_components[0].type
        == TariffDimensionType.ENERGY.value
    )
    assert tariff.elements.root[0].price_components[0].price == 0.30
    assert tariff.last_updated == datetime.fromisoformat("2024-06-01T12:00:00Z")


def test_tariff_json():
    """Test the Tariff class from JSON."""
    json_data = {
        "country_code": "FR",
        "party_id": "QUA",
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
    tariff = TariffObject.model_validate(json_data)
    # print(tariff.to_json())
    assert tariff.tariff_id == "FRQUAtariff1"
    assert len(tariff.elements.root) == 1
    assert len(tariff.elements.root[0].price_components) == 1
    assert tariff.elements.root[0].price_components[0].type.value == "ENERGY"
    assert tariff.elements.root[0].price_components[0].price == 0.30
    assert tariff.last_updated.isoformat() == "2024-06-01T12:00:00+00:00"
    assert tariff.to_json() == json_data
    assert tariff.to_json(ocpi=False, simple=True) == {
        "country_code": "FR",
        "party_id": "QUA",
        "id": "tariff1",
        "elements": [{"price_components": {"ENERGY": 0.3}}],
        "last_updated": "2024-06-01T12:00:00+00:00",
    }
    assert (
        TariffObject.model_validate(tariff.to_json(incl_vat=True)).to_json(
            incl_vat=True
        )["elements"]
        == json_data["elements"]
    )
    """assert json.dumps(
        TariffObject.convert(json.dumps(tariff.to_json()), Format.JSON_OCPI)
    ) == json.dumps(tariff.to_json())
    assert json.dumps(
        TariffObject.convert(json.dumps(tariff.to_json(simple=True)), Format.JSON_LIGHT)
    ) == json.dumps(tariff.to_json(ocpi=False, simple=False))
    """


'''def test_tariff_string():
    """Test the Tariff class from string and to string."""
    price_component1 = PriceComponent(type=TariffDimensionType.ENERGY, price=0.30)
    price_component2 = PriceComponent(type=TariffDimensionType.FLAT, price=1.20)
    price_component3 = PriceComponent(type=TariffDimensionType.ENERGY, price=0.10)
    price_component4 = PriceComponent(type=TariffDimensionType.FLAT, price=1.50)
    tariff_element1 = TariffElement(
        price_components=[price_component1, price_component2],
        restrictions=TariffRestrictions.from_json(
            {
                "day_of_week": ["MONDAY", "TUESDAY"],
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
    tariff = TariffObject(id="tariff1", elements=tariff_elements)

    assert tariff.to_string() == tariff_elements.to_string()
    assert (
        tariff.to_string()
        == "EN30+FL120+J=LuMa+D>2024-01-01+D<2024-01-02+T>13:10+T<23:59+P>20|EN10+FL150"
    )
    assert (
        TariffElements.from_string(tariff.to_string()).to_string() == tariff.to_string()
    )
    assert (
        TariffObject.convert(tariff.to_string(), Format.TEXT_LIGHT)
        == tariff.to_string()
    )


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
        assert TariffObject.is_valid_string(tst)
    for tst in test_ko:
        assert not TariffObject.is_valid_string(tst)
'''


def test_json_validation():
    """Test the JSON schema for the Tariff class."""
    json_data = {
        "country_code": "FR",
        "party_id": "QUA",
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
    assert TariffObject.is_valid_json(json_data)

    with open("OCPI/examples/examples.json") as f:
        examples_data = json.load(f)
    for example in examples_data:
        assert TariffObject.is_valid_json(example, verbose=False)


def test_to_text():
    """Test the to_text method of the Tariff class."""

    with open("OCPI/examples/examples.json") as f:
        examples_data = json.load(f)
    text = "# tarifs au format texte des exemples du fichier examples.json\n\n"
    for example in examples_data:
        example["country_code"] = example.get("country_code", "NO")
        example["party_id"] = example.get("party_id", "NOP")
        tariff = TariffObject.model_validate(example)
        text += tariff.to_text() + "\n"
    with open("OCPI/examples/examples2.md", "w", encoding="utf-8") as f:
        f.write(text[:-1])


# test_price()
test_pricecomponent()
test_pricecomponent_tax_included()
test_pricecomponent_tax_excluded()
test_tariffrestrictions()
test_tariffrestrictions_from_json()
test_tariffelement()
test_tariffelement_from_json()
test_tariff()
test_tariff_json()
# test_tariff_string()
# test_string_validation()
test_json_validation()
test_to_text()
