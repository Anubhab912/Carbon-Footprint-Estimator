"""Centralised prompt templates for LLM calls."""


def build_summary_messages(
    category_breakdown: dict[str, float],
    total_tco2e: float,
    country: str,
) -> list[dict[str, str]]:
    categories = "\n".join(
        f"- {name}: {value:.2f} tCO₂e/year"
        for name, value in sorted(category_breakdown.items(), key=lambda x: -x[1])
    )
    return [
        {
            "role": "system",
            "content": (
                "You are a carbon footprint analyst. Given a user's annual emissions "
                "breakdown, write a concise plain-language summary (3-4 sentences). "
                "Mention the total, the largest contributor, and compare "
                f"the total to the approximate per-capita average for {country} "
                "(~4.7 tCO₂e global average unless you know the specific figure)."
            ),
        },
        {
            "role": "user",
            "content": f"Annual carbon footprint breakdown for a user in {country}:\n\n"
            f"{categories}\n\n"
            f"Total: {total_tco2e:.2f} tCO₂e/year",
        },
    ]


def build_recommendations_messages(
    category_breakdown: dict[str, float],
    total_tco2e: float,
) -> list[dict[str, str]]:
    categories = "\n".join(
        f"- {name}: {value:.2f} tCO₂e/year"
        for name, value in sorted(category_breakdown.items(), key=lambda x: -x[1])
    )
    return [
        {
            "role": "system",
            "content": (
                "You are a sustainability coach. Based on the user's emissions "
                "breakdown, suggest 3-4 personalised, actionable reduction tips. "
                "Focus on the highest-impact categories. Be specific and realistic."
            ),
        },
        {
            "role": "user",
            "content": f"My annual carbon footprint breakdown:\n\n"
            f"{categories}\n\n"
            f"Total: {total_tco2e:.2f} tCO₂e/year\n\n"
            f"What are my top reduction opportunities?",
        },
    ]
