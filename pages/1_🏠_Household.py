"""Household energy input form — Streamlit page."""

import streamlit as st
from pydantic import ValidationError

from app.calculator import calculate_electricity_emissions, calculate_gas_emissions
from app.validators import HouseholdEnergyInput

st.set_page_config(page_title="Household Energy", page_icon="🏠")
st.title("🏠 Household Energy")
st.markdown("Tell us about your home energy usage.")

if st.button("🔄 Reset", key="reset_household"):
    st.session_state["household"] = {}
    st.rerun()

with st.form("household_form"):
    country = st.text_input(
        "Country code (ISO 3166-1 alpha-2)", value="IN", max_chars=2
    )
    electricity = st.number_input(
        "Monthly electricity consumption (kWh)", min_value=0.0, value=280.0, step=10.0
    )
    gas = st.number_input(
        "Monthly natural gas consumption (m³)", min_value=0.0, value=90.0, step=1.0
    )
    renewable = st.checkbox("I am on a 100 % renewable energy tariff")
    submitted = st.form_submit_button("Calculate")

if submitted:
    try:
        data = HouseholdEnergyInput(
            country=country,
            electricity_kwh_per_month=electricity,
            natural_gas_m3_per_month=gas,
            renewable_tariff=renewable,
        )
    except ValidationError as e:
        st.error(f"Validation error: {e}")
        st.stop()

    elec_emissions = calculate_electricity_emissions(
        data.electricity_kwh_per_month, data.country, months=12
    )
    gas_emissions = calculate_gas_emissions(
        data.natural_gas_m3_per_month, data.country, months=12
    )
    if data.renewable_tariff:
        elec_emissions = 0.0

    total = elec_emissions + gas_emissions
    st.session_state["household"] = {
        "country": data.country,
        "electricity_tco2e": round(elec_emissions / 1000, 2),
        "gas_tco2e": round(gas_emissions / 1000, 2),
        "total_tco2e": round(total / 1000, 2),
    }

    st.success(f"Household energy: **{total / 1000:.2f} tCO₂e/year**")
    st.json(st.session_state["household"])
