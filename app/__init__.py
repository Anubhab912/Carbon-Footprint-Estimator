"""Carbon Footprint Estimator - Core Application Package."""

from app.calculator import (
    calculate_car_emissions,
    calculate_electricity_emissions,
    calculate_flight_emissions,
    calculate_food_emissions,
    calculate_gas_emissions,
    calculate_shopping_emissions,
)
from app.llm_client import LLMClient
from app.validators import (
    FoodInput,
    HouseholdEnergyInput,
    ShoppingInput,
    TransportInput,
)
from app.visualisations import (
    create_category_breakdown_chart,
    create_comparison_chart,
    create_equivalency_metrics,
)

__all__ = [
    "calculate_electricity_emissions",
    "calculate_gas_emissions",
    "calculate_car_emissions",
    "calculate_flight_emissions",
    "calculate_food_emissions",
    "calculate_shopping_emissions",
    "HouseholdEnergyInput",
    "TransportInput",
    "FoodInput",
    "ShoppingInput",
    "LLMClient",
    "create_category_breakdown_chart",
    "create_comparison_chart",
    "create_equivalency_metrics",
]
