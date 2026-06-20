"""Transport & travel input form — Streamlit page."""

import streamlit as st
from pydantic import ValidationError

from app.calculator import calculate_car_emissions, calculate_flight_emissions
from app.validators import TransportInput

st.set_page_config(page_title="Travel", page_icon="✈️")
st.title("✈️ Transport & Travel")
st.markdown("Tell us about your travel habits.")

if st.button("🔄 Reset", key="reset_travel"):
    st.session_state["travel"] = {}
    st.rerun()

with st.form("travel_form"):
    car_km = st.number_input(
        "Annual car distance (km)", min_value=0.0, value=12000.0, step=100.0
    )
    fuel_type = st.selectbox("Fuel type", ["petrol", "diesel", "electric", "hybrid"])
    car_size = st.selectbox("Car size", ["small", "medium", "large"])
    short_flights = st.number_input(
        "Short-haul flights per year (< 3,500 km)", min_value=0, value=2, step=1
    )
    long_flights = st.number_input(
        "Long-haul flights per year (≥ 3,500 km)", min_value=0, value=1, step=1
    )
    short_flight_dist = st.number_input(
        "Average short-haul flight distance (km)",
        min_value=0.0, value=1000.0, step=100.0,
    )
    long_flight_dist = st.number_input(
        "Average long-haul flight distance (km)",
        min_value=0.0, value=8000.0, step=500.0,
    )
    submitted = st.form_submit_button("Calculate")

if submitted:
    try:
        data = TransportInput(
            car_km_per_year=car_km,
            car_fuel_type=fuel_type,
            car_size=car_size,
            short_haul_flights=short_flights,
            long_haul_flights=long_flights,
            short_flight_distance_km=short_flight_dist,
            long_flight_distance_km=long_flight_dist,
        )
    except ValidationError as e:
        st.error(f"Validation error: {e}")
        st.stop()

    car_emissions = calculate_car_emissions(
        data.car_km_per_year, data.car_fuel_type, data.car_size
    )

    short_flight_emissions = calculate_flight_emissions(
        data.short_haul_flights, data.short_flight_distance_km, "economy"
    )
    long_flight_emissions = calculate_flight_emissions(
        data.long_haul_flights, data.long_flight_distance_km, "economy"
    )
    flight_emissions = short_flight_emissions + long_flight_emissions

    total = car_emissions + flight_emissions
    st.session_state["travel"] = {
        "car_tco2e": round(car_emissions / 1000, 2),
        "short_flight_tco2e": round(short_flight_emissions / 1000, 2),
        "long_flight_tco2e": round(long_flight_emissions / 1000, 2),
        "flight_tco2e": round(flight_emissions / 1000, 2),
        "total_tco2e": round(total / 1000, 2),
    }

    st.success(f"Transport & travel: **{total / 1000:.2f} tCO₂e/year**")
    st.json(st.session_state["travel"])
