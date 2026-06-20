"""Edge-case tests for Pydantic input validators."""

import pytest
from pydantic import ValidationError

from app.validators import (
    FoodInput,
    HouseholdEnergyInput,
    ShoppingInput,
    TransportInput,
)


class TestHouseholdEnergyInput:
    def test_valid(self):
        data = HouseholdEnergyInput(
            country="GB",
            electricity_kwh_per_month=280.0,
            natural_gas_m3_per_month=90.0,
        )
        assert data.country == "GB"

    def test_country_auto_uppercase(self):
        data = HouseholdEnergyInput(country="gb")
        assert data.country == "GB"

    def test_negative_electricity(self):
        with pytest.raises(ValidationError):
            HouseholdEnergyInput(electricity_kwh_per_month=-10.0)

    def test_excessive_electricity(self):
        with pytest.raises(ValidationError):
            HouseholdEnergyInput(electricity_kwh_per_month=200000.0)


class TestTransportInput:
    def test_valid(self):
        data = TransportInput(car_km_per_year=10000.0)
        assert data.car_fuel_type == "petrol"

    def test_invalid_fuel(self):
        with pytest.raises(ValidationError):
            TransportInput(car_fuel_type="hydrogen")

    def test_negative_km(self):
        with pytest.raises(ValidationError):
            TransportInput(car_km_per_year=-1.0)


class TestFoodInput:
    def test_valid_diets(self):
        for diet in ("omnivore", "pescatarian", "vegetarian", "vegan"):
            FoodInput(diet_type=diet)

    def test_invalid_diet(self):
        with pytest.raises(ValidationError):
            FoodInput(diet_type="carnivore")

    def test_min_household_size(self):
        with pytest.raises(ValidationError):
            FoodInput(household_size=0)


class TestShoppingInput:
    def test_valid(self):
        data = ShoppingInput(monthly_spend_eur=150.0, category="clothing")
        assert data.category == "clothing"

    def test_invalid_category(self):
        with pytest.raises(ValidationError):
            ShoppingInput(category="toys")

    def test_negative_spend(self):
        with pytest.raises(ValidationError):
            ShoppingInput(monthly_spend_eur=-50.0)
