"""Results dashboard — breakdown chart, comparison, equivalencies, and AI insights."""

import json
import os

import streamlit as st

from app.llm_client import LLMClient
from app.visualisations import (
    create_category_breakdown_chart,
    create_comparison_chart,
    create_equivalency_metrics,
)

st.set_page_config(page_title="Results Dashboard", page_icon="📊")
st.title("📊 Your Carbon Footprint Results")

categories = ["household", "travel", "food", "shopping"]
category_labels = {
    "household": "Household Energy",
    "travel": "Transport & Travel",
    "food": "Food & Diet",
    "shopping": "Shopping & Consumption",
}

breakdown = {}
total = 0.0
has_data = False

for cat in categories:
    data = st.session_state.get(cat, {})
    if data.get("total_tco2e"):
        label = category_labels[cat]
        val = data["total_tco2e"]
        breakdown[label] = val
        total += val
        has_data = True

if not has_data:
    st.warning("No data found. Please fill in at least one category page first.")
    st.page_link("pages/1_🏠_Household.py", label="Go to Household Energy")
    st.stop()

st.metric("Total Annual Footprint", f"{total:.2f} tCO₂e/year")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_category_breakdown_chart(breakdown), width="stretch"
    )

with col2:
    country = "default"
    if st.session_state.get("household", {}).get("country"):
        country = st.session_state["household"]["country"]
    country_averages_path = os.path.join("data", "country_averages.json")
    if os.path.exists(country_averages_path):
        with open(country_averages_path) as f:
            averages = json.load(f)
    else:
        averages = {}
    country_avg = averages.get(country, averages.get("default", 4.7))
    st.plotly_chart(
        create_comparison_chart(total, country_avg), width="stretch"
    )

st.subheader("🌱 Equivalency Metrics")
equiv = create_equivalency_metrics(total)
for label, value in equiv.items():
    st.metric(label, value)

st.divider()
st.subheader("🤖 AI-Powered Insights")

hf_token = os.getenv("HF_TOKEN", "")
if not hf_token or hf_token == "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
    st.info(
        "Set your HF_TOKEN in a .env file to enable AI insights."
    )

if st.button("Get AI Insights", type="primary"):
    with st.spinner("Generating insights..."):
        try:
            client = LLMClient()
            summary = client.generate_summary(breakdown, total, country)
            recommendations = client.generate_recommendations(breakdown, total)

            with st.expander("📝 Summary", expanded=True):
                st.write(summary)
            with st.expander("💡 Personalised Recommendations", expanded=True):
                st.write(recommendations)
        except Exception as e:
            st.error(f"Could not generate AI insights: {e}")
            st.info(
                "Make sure your HF_TOKEN is valid and you have internet access."
            )

st.divider()
st.caption(
    "All calculations are estimates based on average emission factors. "
    "See the methodology section in the README for details."
)
