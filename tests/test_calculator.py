"""Unit tests for emissions calculation logic."""

import pytest

from app.calculator import (
    EmissionFactorError,
    calculate_car_emissions,
    calculate_electricity_emissions,
    calculate_flight_emissions,
    calculate_food_emissions,
    calculate_gas_emissions,
    calculate_shopping_emissions,
)


def test_electricity_uk_known_value():
    result = calculate_electricity_emissions(kwh_per_month=280, country="GB", months=12)
    assert abs(result - 782.88) < 1.0


def test_electricity_zero():
    result = calculate_electricity_emissions(kwh_per_month=0, country="GB", months=12)
    assert result == 0.0


def test_gas_uk_known_value():
    result = calculate_gas_emissions(m3_per_month=90, country="GB", months=12)
    assert abs(result - 2029.32) < 1.0


def test_car_petrol_medium():
    result = calculate_car_emissions(
        km_per_year=12000, fuel_type="petrol", vehicle_size="medium"
    )
    expected = 12000 * 0.192
    assert abs(result - expected) < 0.1


def test_car_electric():
    result = calculate_car_emissions(
        km_per_year=12000, fuel_type="electric", vehicle_size="medium"
    )
    expected = 12000 * 0.050
    assert abs(result - expected) < 0.1


def test_car_invalid_fuel_size():
    with pytest.raises(EmissionFactorError):
        calculate_car_emissions(
            km_per_year=10000, fuel_type="hydrogen", vehicle_size="medium"
        )


def test_flight_economy():
    result = calculate_flight_emissions(flights_per_year=2, avg_distance_km=1000)
    expected = 2 * 1000 * 0.255
    assert abs(result - expected) < 0.1


def test_flight_business():
    result = calculate_flight_emissions(
        flights_per_year=1, avg_distance_km=8000, cabin_class="business"
    )
    expected = 1 * 8000 * 0.510
    assert abs(result - expected) < 0.1


def test_flight_invalid_class():
    with pytest.raises(EmissionFactorError):
        calculate_flight_emissions(
            flights_per_year=1, avg_distance_km=1000, cabin_class="first"
        )


def test_food_omnivore():
    result = calculate_food_emissions(diet_type="omnivore", household_size=1)
    assert abs(result - 1800.0) < 1.0


def test_food_vegan():
    result = calculate_food_emissions(diet_type="vegan", household_size=2)
    assert abs(result - 1000.0) < 1.0


def test_food_invalid_diet():
    with pytest.raises(EmissionFactorError):
        calculate_food_emissions(diet_type="carnivore", household_size=1)


def test_shopping_general():
    result = calculate_shopping_emissions(monthly_spend=200, category="general")
    expected = 200 * 0.400 * 12
    assert abs(result - expected) < 0.1


def test_shopping_clothing():
    result = calculate_shopping_emissions(monthly_spend=100, category="clothing")
    expected = 100 * 0.600 * 12
    assert abs(result - expected) < 0.1


def test_shopping_invalid_category():
    with pytest.raises(EmissionFactorError):
        calculate_shopping_emissions(monthly_spend=100, category="toys")


def test_electricity_invalid_country_fallbacks_to_default():
    result = calculate_electricity_emissions(kwh_per_month=280, country="XX", months=12)
    expected = 280 * 0.500 * 12
    assert abs(result - expected) < 1.0


def test_gas_invalid_country_fallbacks_to_default():
    result = calculate_gas_emissions(m3_per_month=90, country="XX", months=12)
    expected = 90 * 1.850 * 12
    assert abs(result - expected) < 1.0


def test_electricity_no_default_raises_error():
    pass
