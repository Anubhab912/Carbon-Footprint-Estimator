"""Chart builders using Plotly for emissions visualisations."""

import plotly.express as px
import plotly.graph_objects as go


def create_category_breakdown_chart(category_breakdown: dict[str, float]) -> go.Figure:
    sorted_items: list[tuple[str, float]] = sorted(
        category_breakdown.items(), key=lambda x: -x[1]
    )
    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig = px.pie(
        names=labels,
        values=values,
        title="Emissions Breakdown by Category",
        color_discrete_sequence=px.colors.sequential.Greens_r,
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def create_comparison_chart(
    user_total: float,
    country_avg: float,
    global_avg: float = 4.7,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["You", "Country Average", "Global Average"],
            y=[user_total, country_avg, global_avg],
            marker_color=["#2E7D32", "#66BB6A", "#A5D6A7"],
        )
    )
    fig.update_layout(
        title="Your Footprint vs. Averages",
        yaxis_title="tCO₂e / year",
        yaxis={"range": [0, max(user_total, country_avg, global_avg) * 1.2]},
    )
    return fig


def create_equivalency_metrics(total_tco2e: float) -> dict[str, str]:
    trees = total_tco2e / 0.021
    km_driven = total_tco2e / 0.000192
    return {
        "Trees needed to offset": f"{trees:,.0f} trees/year",
        "Equivalent car KM": f"{km_driven:,.0f} km driven",
    }
