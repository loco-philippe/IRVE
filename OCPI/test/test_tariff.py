"""Tests for the tariff module."""

from source.tariff import Tariff, TariffElement, PriceComponent, TariffRestrictions
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
    price_component = PriceComponent(type="ENERGY", price=price)

    assert price_component.type == "ENERGY"
    assert price_component.price.amount == 0.30


def test_tariffrestrictions():
    """Test the TariffRestrictions class."""
    restrictions = TariffRestrictions()
    print(restrictions)

    assert restrictions.days_of_week is None
    assert restrictions.start_date_time is None
    assert restrictions.end_date_time is None
    assert restrictions.min_current is None
    assert restrictions.max_current is None
    assert restrictions.min_duration is None
    assert restrictions.max_duration is None
    assert restrictions.min_kwh is None
    assert restrictions.max_kwh is None
    assert restrictions.min_power is None
    assert restrictions.max_power is None


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
    assert tariff.last_updated is not None


test_price()
test_pricecomponent()
test_tariffrestrictions()
test_tariff()
