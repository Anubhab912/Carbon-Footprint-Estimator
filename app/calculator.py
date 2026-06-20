"""Deterministic emissions calculation logic — all functions are pure."""

from functools import lru_cache

import yaml


class EmissionFactorError(ValueError):
    """Raised when an emission factor cannot be found."""


@lru_cache(maxsize=1)
def _load_factors() -> dict:
    with open("data/emission_factors.yaml") as f:
        return yaml.safe_load(f)


def _lookup_factor(category: str, subcategory: str, country: str = "default") -> float:
    factors = _load_factors()
    cat = factors.get(category)
    if cat is None:
        raise EmissionFactorError(
            f"Category '{category}' not found in emission factors"
        )

    entry = cat.get(subcategory)
    if entry is None:
        raise EmissionFactorError(
            f"Subcategory '{subcategory}' not found in category '{category}'"
        )

    if isinstance(entry, dict):
        if country in entry:
            return entry[country]
        if "default" in entry:
            return entry["default"]
        raise EmissionFactorError(
            f"No factor for country '{country}' and "
            f"no default in '{category}.{subcategory}'"
        )

    return float(entry)


def calculate_electricity_emissions(
    kwh_per_month: float, country: str, months: int = 12
) -> float:
    factor = _lookup_factor("electricity", "kgCO2e_per_kwh", country)
    return kwh_per_month * factor * months


def calculate_gas_emissions(
    m3_per_month: float, country: str, months: int = 12
) -> float:
    factor = _lookup_factor("natural_gas", "kgCO2e_per_m3", country)
    return m3_per_month * factor * months


def calculate_car_emissions(
    km_per_year: float,
    fuel_type: str = "petrol",
    vehicle_size: str = "medium",
) -> float:
    key = f"car_{fuel_type}_{vehicle_size}"
    factor = _lookup_factor("transport", key)
    return km_per_year * factor


def calculate_flight_emissions(
    flights_per_year: int,
    avg_distance_km: float,
    cabin_class: str = "economy",
) -> float:
    key = f"{cabin_class}_flight"
    factor = _lookup_factor("transport", key)
    return flights_per_year * avg_distance_km * factor


def calculate_food_emissions(
    diet_type: str = "omnivore",
    household_size: int = 1,
) -> float:
    factor = _lookup_factor("food", f"{diet_type}_per_person")
    return factor * household_size


def calculate_shopping_emissions(
    monthly_spend: float,
    category: str = "general",
) -> float:
    factor = _lookup_factor("shopping", f"{category}_per_eur")
    return monthly_spend * factor * 12
