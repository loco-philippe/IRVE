"""Tests for the tariff module."""

from datetime import date, datetime, time
import json

from OCPI.source.tariff import (
    TariffObject,
    TariffDimensionTypeEnum,
    TariffElement,
    TariffElements,
    PriceComponent,
    TariffRestrictions,
    DayOfWeekEnum,
)

VALUES = {
    "ENERGY": None,
    "TIME": None,
    "FLAT": None,
    "PARKING_TIME": None,
    "CONGESTION_TIME": None,
}
SESSION = {
    "time": time.fromisoformat("15:00"),
    "date": date.fromisoformat("2026-05-01"),
    "day_of_week": "MONDAY",
    "duration": 30,
    "kwh": 51.0,
}
PDC = {"power": 100.0}
OTHER = {
    "current": 1.0,
    "vehicle_soc": 50.0,
    "congestion": 10.0,
    "reservation": False,
}


def test_pricecomponent():
    """Test the PriceComponent class."""
    price = 0.30
    price_component = PriceComponent(type=TariffDimensionTypeEnum.ENERGY, price=price)

    assert price_component.type.value == "ENERGY"
    assert price_component.price == 0.30


def test_pricecomponent_tax_included():
    """Test the PriceComponent class with tax included."""
    price = 0.30
    price_component = PriceComponent(type=TariffDimensionTypeEnum.ENERGY, price=price)
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
    price_component = PriceComponent(type=TariffDimensionTypeEnum.ENERGY, price=price)
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
    json_data_simple = {
        "day_of_week": ["MONDAY", "TUESDAY"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "start_time": "13:10",
        "end_time": "23:59",
        "min_duration": 30,
        "max_duration": 120,
        "min_kwh": 1.0,
        "max_kwh": 50.0,
        "min_power": 5.0,
        "max_power": 20.0,
    }
    json_data = json_data_simple | {
        "min_current": 10.0,
    }
    restrictions = TariffRestrictions.model_validate(json_data)
    assert restrictions.day_of_week == [DayOfWeekEnum.MONDAY, DayOfWeekEnum.TUESDAY]
    assert restrictions.start_date.isoformat() == "2024-01-01"
    assert restrictions.end_date.isoformat() == "2024-12-31"
    assert restrictions.start_time.isoformat() == "13:10:00"
    assert restrictions.end_time.isoformat() == "23:59:00"
    assert restrictions.min_current == 10.0
    assert restrictions.min_duration == 30
    assert restrictions.max_duration == 120
    assert restrictions.min_kwh == 1.0
    assert restrictions.max_kwh == 50.0
    assert restrictions.min_power == 5.0
    assert restrictions.max_power == 20.0
    assert restrictions.to_json() == json_data

    param_other = {}
    param_session = {
        "day_of_week": "MONDAY",
        "time": time.fromisoformat("15:00"),
        "date": date.fromisoformat("2024-02-01"),
        "duration": 60,
        "kwh": 10.0,
    }
    param_pdc = {"power": 10.0}
    restrictions_simple = TariffRestrictions.model_validate(json_data_simple)
    assert restrictions_simple.is_met(param_session, param_pdc, param_other)
    assert restrictions.is_met(param_session, param_pdc, param_other) is None
    param_other_ok = {"current": 15.0}
    assert restrictions.is_met(param_session, param_pdc, param_other_ok)
    param_other_ko = {"current": 5.0}
    assert not restrictions.is_met(param_session, param_pdc, param_other_ko)
    param_session_ko = param_session | {"day_of_week": "WEDNESDAY"}
    assert not restrictions_simple.is_met(param_session_ko, param_pdc, param_other)
    param_pdc_ko = param_pdc | {"power": 30.0}
    assert not restrictions_simple.is_met(param_session, param_pdc_ko, param_other)


def test_tariffelement():
    """Test the TariffElement class."""
    price_component = PriceComponent(type=TariffDimensionTypeEnum.ENERGY, price=0.30)
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


def test_tariffelements():
    """Test the TariffElements class."""
    json_data = [
        {
            "price_components": [
                {
                    "type": "ENERGY",
                    "price": 0.30,
                }
            ],
            "restrictions": {
                "end_time": "13:00",
            },
        },
        {
            "price_components": [
                {
                    "type": "ENERGY",
                    "price": 0.50,
                },
                {
                    "type": "FLAT",
                    "price": 4.0,
                },
            ],
            "restrictions": {
                "end_time": "20:00",
            },
        },
    ]

    tariff_elements = TariffElements.model_validate(json_data)
    assert len(tariff_elements.root) == 2
    assert len(tariff_elements.root[0].price_components) == 1
    assert tariff_elements.root[0].price_components[0].type.value == "ENERGY"
    assert tariff_elements.root[0].price_components[0].price == 0.30
    param_session = {"time": time.fromisoformat("14:00")}
    expected = VALUES | {"ENERGY": 0.5, "FLAT": 4.0}
    assert tariff_elements.dimensions_values(True, param_session, {}, {}) == expected
    param_session = {"time": time.fromisoformat("10:00")}
    expected = VALUES | {"ENERGY": 0.3, "FLAT": 4.0}
    assert tariff_elements.dimensions_values(True, param_session, {}, {}) == expected


def test_dimensions_values():
    """Test the dimensions_values method of the TariffElements class."""
    json_data = [
        {
            "price_components": [
                {"type": "CONGESTION_TIME", "price": 0.00, "step_size": 60}
            ],
            "restrictions": {
                "min_duration": 0,
                "max_duration": 300,
                "min_vehicle_soc": 80,
                "min_congestion_threshold": 90,
            },
        },
        {
            "price_components": [
                {"type": "CONGESTION_TIME", "price": 30.00, "step_size": 60}
            ],
            "restrictions": {"min_vehicle_soc": 80, "min_congestion_threshold": 90},
        },
        {
            "price_components": [{"type": "ENERGY", "price": 0.28, "step_size": 1}],
            "restrictions": {
                "start_time": "00:00",
                "end_time": "04:00",
                "day_of_week": [
                    "MONDAY",
                    "TUESDAY",
                    "WEDNESDAY",
                    "THURSDAY",
                    "FRIDAY",
                    "SATURDAY",
                    "SUNDAY",
                ],
            },
        },
        {
            "price_components": [{"type": "ENERGY", "price": 0.35, "step_size": 1}],
            "restrictions": {
                "start_time": "04:00",
                "end_time": "09:00",
                "day_of_week": [
                    "MONDAY",
                    "TUESDAY",
                    "WEDNESDAY",
                    "THURSDAY",
                    "FRIDAY",
                    "SATURDAY",
                    "SUNDAY",
                ],
            },
        },
        {
            "price_components": [{"type": "ENERGY", "price": 0.64, "step_size": 1}],
            "restrictions": {
                "start_time": "09:00",
                "end_time": "20:00",
                "day_of_week": [
                    "MONDAY",
                    "TUESDAY",
                    "WEDNESDAY",
                    "THURSDAY",
                    "FRIDAY",
                    "SATURDAY",
                    "SUNDAY",
                ],
            },
        },
        {
            "price_components": [{"type": "ENERGY", "price": 0.35, "step_size": 1}],
            "restrictions": {
                "start_time": "20:00",
                "end_time": "00:00",
                "day_of_week": [
                    "MONDAY",
                    "TUESDAY",
                    "WEDNESDAY",
                    "THURSDAY",
                    "FRIDAY",
                    "SATURDAY",
                    "SUNDAY",
                ],
            },
        },
        {"price_components": [{"type": "ENERGY", "price": 0.46, "step_size": 1}]},
    ]
    tariff_elements = TariffElements.model_validate(json_data)
    expected = VALUES | {"ENERGY": 0.64}
    assert tariff_elements.dimensions_values(True, SESSION, PDC, OTHER) == expected


def test_tariff():
    """Test the Tariff class."""
    price_component = PriceComponent(type=TariffDimensionTypeEnum.ENERGY, price=0.30)
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
        == TariffDimensionTypeEnum.ENERGY.value
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
    assert tariff.current_price({}, {}, {}) == {"type": "ENERGY", "price": 0.3}


def test_json_validation():
    """Test the JSON schema for the Tariff class."""
    json_data = {
        "country_code": "FR",
        "party_id": "QUA",
        "id": "tariff1",
        "type": "AD_HOC_PAYMENT",
        "elements": [
            {
                "price_components": [{"type": "ENERGY", "price": 0.30, "step_size": 1}],
            }
        ],
        "last_updated": "2024-06-01T12:00:00+00:00",
        "tax_included": "YES",
    }
    assert TariffObject.is_valid_json(json_data)

    with open("OCPI/examples/examples.json") as f:
        examples_data = json.load(f)
    for example in examples_data:
        example["country_code"] = example.get("country_code", "NO")
        example["party_id"] = example.get("party_id", "NOP")
        assert TariffObject.is_valid_json(example, verbose=False)
    with open("OCPI/examples/model_schema.json", "w", encoding="utf-8") as f:
        json.dump(TariffObject.model_json_schema(), f, indent=4)


def test_to_text():
    """Test the to_text method of the Tariff class."""

    with open("OCPI/examples/examples.json") as f:
        examples_data = json.load(f)
    text = "# tarifs au format texte des exemples du fichier examples.json\n\n"
    for example in examples_data:
        example["country_code"] = example.get("country_code", "NO")
        example["party_id"] = example.get("party_id", "NOP")
        # print(example["id"])
        tariff = TariffObject.model_validate(example)
        text += tariff.to_text() + "\n"
        text += (
            "pastille tarif : "
            + json.dumps(tariff.current_price(SESSION, PDC, OTHER))
            + "\n\n"
        )
    with open("OCPI/examples/examples.md", "w", encoding="utf-8") as f:
        f.write(text[:-1])


test_pricecomponent()
test_pricecomponent_tax_included()
test_pricecomponent_tax_excluded()
test_tariffrestrictions()
test_tariffrestrictions_from_json()
test_tariffelement()
test_tariffelement_from_json()
test_tariffelements()
test_dimensions_values()
test_tariff()
test_tariff_json()
test_json_validation()
test_to_text()
