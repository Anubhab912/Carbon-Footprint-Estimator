"""Food & diet input form — Streamlit page."""

import streamlit as st
from pydantic import ValidationError

from app.calculator import calculate_food_emissions
from app.validators import FoodInput

st.set_page_config(page_title="Food & Diet", page_icon="🥗")
st.title("🥗 Food & Diet")
st.markdown("Tell us about your eating habits.")

if st.button("🔄 Reset", key="reset_food"):
    st.session_state["food"] = {}
    st.rerun()

with st.form("food_form"):
    diet_type = st.selectbox(
        "Diet type", ["omnivore", "pescatarian", "vegetarian", "vegan"]
    )
    household_size = st.number_input("Household size", min_value=1, value=1, step=1)
    submitted = st.form_submit_button("Calculate")

if submitted:
    try:
        data = FoodInput(diet_type=diet_type, household_size=household_size)
    except ValidationError as e:
        st.error(f"Validation error: {e}")
        st.stop()

    emissions = calculate_food_emissions(data.diet_type, data.household_size)
    total_tco2e = emissions / 1000
    st.session_state["food"] = {
        "food_tco2e": round(total_tco2e, 2),
        "total_tco2e": round(total_tco2e, 2),
    }

    st.success(f"Food & diet: **{total_tco2e:.2f} tCO₂e/year**")
    st.json(st.session_state["food"])
