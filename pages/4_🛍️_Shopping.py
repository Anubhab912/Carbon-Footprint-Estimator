"""Shopping & consumption input form — Streamlit page."""

import streamlit as st
from pydantic import ValidationError

from app.calculator import calculate_shopping_emissions
from app.validators import ShoppingInput

st.set_page_config(page_title="Shopping", page_icon="🛍️")
st.title("🛍️ Shopping & Consumption")
st.markdown("Tell us about your spending habits.")

if st.button("🔄 Reset", key="reset_shopping"):
    st.session_state["shopping"] = {}
    st.rerun()

with st.form("shopping_form"):
    spend = st.number_input(
        "Average monthly spending (EUR)", min_value=0.0, value=200.0, step=10.0
    )
    category = st.selectbox(
        "Main spending category",
        ["general", "clothing", "electronics", "furniture"],
    )
    submitted = st.form_submit_button("Calculate")

if submitted:
    try:
        data = ShoppingInput(monthly_spend_eur=spend, category=category)
    except ValidationError as e:
        st.error(f"Validation error: {e}")
        st.stop()

    emissions = calculate_shopping_emissions(data.monthly_spend_eur, data.category)
    total_tco2e = emissions / 1000
    st.session_state["shopping"] = {
        "shopping_tco2e": round(total_tco2e, 2),
        "total_tco2e": round(total_tco2e, 2),
    }

    st.success(f"Shopping & consumption: **{total_tco2e:.2f} tCO₂e/year**")
    st.json(st.session_state["shopping"])
