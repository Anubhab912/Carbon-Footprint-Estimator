"""Streamlit entry point — landing page and session state initialisation."""

import streamlit as st

st.set_page_config(
    page_title="Carbon Footprint Estimator",
    page_icon="🌍",
    layout="centered",
)

st.title("🌍 Carbon Footprint Estimator")
st.markdown(
    """
Estimate your household's annual carbon footprint with AI-powered insights.

**How it works:**
1. Fill in each category page (Household, Travel, Food, Shopping)
2. View your personalised results dashboard
3. Get AI-generated recommendations

👉 Use the sidebar to navigate between pages.
"""
)

for key in ["household", "travel", "food", "shopping"]:
    if key not in st.session_state:
        st.session_state[key] = {}

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 View My Results", type="primary", width="stretch"):
        st.switch_page("pages/5_📊_Results.py")

with col2:
    if st.button("🔄 Reset All Data", width="stretch"):
        for key in ["household", "travel", "food", "shopping"]:
            st.session_state[key] = {}
        st.rerun()

st.info("⏱ Estimated time to complete: ~3 minutes")

categories = ["household", "travel", "food", "shopping"]
totals = []
for cat in categories:
    data = st.session_state.get(cat, {})
    if data.get("total_tco2e"):
        totals.append(data["total_tco2e"])
if totals:
    total = sum(totals)
    st.success(f"Your estimated total: **{total:.2f} tCO₂e/year**")
elif any(st.session_state.get(cat, {}) for cat in categories):
    st.warning("Complete at least one category page first.")
