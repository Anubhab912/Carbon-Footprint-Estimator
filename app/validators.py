"""Input schema & validation using Pydantic models."""

from pydantic import BaseModel, Field, field_validator


class HouseholdEnergyInput(BaseModel):
    country: str = Field(default="IN", min_length=1, max_length=10)
    electricity_kwh_per_month: float = Field(default=0.0, ge=0.0, le=100000.0)
    natural_gas_m3_per_month: float = Field(default=0.0, ge=0.0, le=100000.0)
    renewable_tariff: bool = False

    @field_validator("country")
    @classmethod
    def country_upper(cls, v: str) -> str:
        return v.strip().upper()


class TransportInput(BaseModel):
    car_km_per_year: float = Field(default=0.0, ge=0.0, le=1000000.0)
    car_fuel_type: str = Field(
        default="petrol", pattern=r"^(petrol|diesel|electric|hybrid)$"
    )
    car_size: str = Field(default="medium", pattern=r"^(small|medium|large)$")
    short_haul_flights: int = Field(default=0, ge=0, le=365)
    long_haul_flights: int = Field(default=0, ge=0, le=365)
    short_flight_distance_km: float = Field(default=1000.0, ge=0.0, le=5000.0)
    long_flight_distance_km: float = Field(default=8000.0, ge=3000.0, le=20000.0)


class FoodInput(BaseModel):
    diet_type: str = Field(
        default="omnivore", pattern=r"^(omnivore|pescatarian|vegetarian|vegan)$"
    )
    household_size: int = Field(default=1, ge=1, le=20)


class ShoppingInput(BaseModel):
    monthly_spend_eur: float = Field(default=0.0, ge=0.0, le=100000.0)
    category: str = Field(
        default="general", pattern=r"^(general|clothing|electronics|furniture)$"
    )
