"""Narrative insight and recommendation panels."""

from collections.abc import Iterable

import pandas as pd
import streamlit as st

from dashboard.helpers import format_currency, format_number, format_rating


def show_panel(title: str, items: Iterable[str]) -> None:
    """Render a bordered narrative panel."""
    with st.container(border=True):
        st.markdown(f"**{title}**")
        for item in items:
            st.markdown(f"- {item}")


def show_insight_recommendation(
    insights: Iterable[str],
    recommendations: Iterable[str],
) -> None:
    """Render paired insight and recommendation panels."""
    left, right = st.columns(2)
    with left:
        show_panel("Key Insights", insights)
    with right:
        show_panel("Business Recommendations", recommendations)


def executive_summary_items(df: pd.DataFrame) -> list[dict[str, str]]:
    """Return executive summary card content from the filtered dataset."""
    category_installs = df.groupby("Category")["Installs"].sum()
    category_ratings = df.groupby("Category")["Rating"].mean()
    category_revenue = df.groupby("Category")["Revenue"].sum()

    top_category = category_installs.idxmax()
    highest_rated = category_ratings.idxmax()
    largest_revenue = category_revenue.idxmax()

    return [
        {
            "icon": "",
            "title": "Top Performing Category",
            "value": top_category,
            "subtitle": f"{format_number(category_installs.max())} installs",
        },
        {
            "icon": "",
            "title": "Highest Rated Category",
            "value": highest_rated,
            "subtitle": f"{format_rating(category_ratings.max())} average rating",
        },
        {
            "icon": "",
            "title": "Largest Revenue Category",
            "value": largest_revenue,
            "subtitle": format_currency(category_revenue.max()),
        },
        {
            "icon": "",
            "title": "Average Rating",
            "value": format_rating(df["Rating"].mean()),
            "subtitle": "Across selected records",
        },
        {
            "icon": "",
            "title": "Most Installed Category",
            "value": top_category,
            "subtitle": "Leader by install volume",
        },
    ]


def show_business_summary(df: pd.DataFrame) -> None:
    """Render a compact business summary from the filtered dataset."""
    if df.empty:
        st.info("No records match the current filters.")
        return

    summary = executive_summary_items(df)
    show_panel(
        "Key Insights",
        [
            f"{summary[0]['value']} leads install performance with {summary[0]['subtitle']}.",
            f"{summary[1]['value']} has the strongest average rating at {summary[1]['subtitle']}.",
            f"{summary[2]['value']} contributes the largest filtered revenue at {summary[2]['subtitle']}.",
        ],
    )
    show_panel(
        "Business Recommendations",
        [
            "Prioritize high-install categories for reach-focused campaigns.",
            "Study highly rated categories to identify product quality patterns.",
            "Use revenue-leading categories for monetization and pricing benchmarks.",
        ],
    )


def task1_story(task_df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return insights and recommendations for Task 1."""
    highest_reviews = task_df.loc[task_df["Reviews"].idxmax()]
    highest_rating = task_df.loc[task_df["Rating"].idxmax()]
    return (
        [
            f"{highest_reviews['Category']} has the highest review volume at "
            f"{format_number(highest_reviews['Reviews'])}.",
            f"{highest_rating['Category']} has the strongest average rating at "
            f"{format_rating(highest_rating['Rating'])}.",
            "The chart compares quality signals and engagement volume side by side.",
        ],
        [
            "Prioritize categories with both high ratings and high review volume.",
            "Use review-heavy categories for feedback mining and feature planning.",
            "Investigate low-rating, high-review categories for product improvement opportunities.",
        ],
    )


def task2_story(task_df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return insights and recommendations for Task 2."""
    leader = task_df.loc[task_df["Installs"].idxmax()]
    return (
        [
            f"{leader['Category']} leads the mapped install view with "
            f"{format_number(leader['Installs'])} installs.",
            "The choropleth turns category install volume into an executive geographic view.",
        ],
        [
            "Use leading categories as benchmarks for broader market expansion.",
            "Pair install-heavy categories with regional acquisition strategies.",
        ],
    )


def task3_story(task_df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return insights and recommendations for Task 3."""
    install_leader = task_df.loc[task_df["Installs"].idxmax()]
    revenue_leader = task_df.loc[task_df["Revenue"].idxmax()]
    return (
        [
            f"{install_leader['Category']} / {install_leader['Type']} leads installs at "
            f"{format_number(install_leader['Installs'])}.",
            f"{revenue_leader['Category']} / {revenue_leader['Type']} leads revenue at "
            f"{format_currency(revenue_leader['Revenue'])}.",
            "Free and paid segments show different growth and monetization behavior.",
        ],
        [
            "Use free apps for reach and audience building.",
            "Use paid-app performance to identify categories with stronger monetization potential.",
            "Balance acquisition goals against revenue goals when prioritizing categories.",
        ],
    )


def task4_story(task_df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return insights and recommendations for Task 4."""
    leader = task_df.groupby("Category")["Installs"].sum().idxmax()
    leader_value = task_df.groupby("Category")["Installs"].sum().max()
    growth_df = task_df.dropna(subset=["MoM_Growth"])
    growth_leader = growth_df.loc[growth_df["MoM_Growth"].idxmax()]
    return (
        [
            f"{leader} has the highest total installs in the trend dataset "
            f"with {format_number(leader_value)} installs.",
            f"{growth_leader['Category']} shows the strongest month-over-month growth signal.",
            "The logarithmic scale helps compare large and smaller install trajectories together.",
        ],
        [
            "Track categories with sustained install momentum for campaign timing.",
            "Investigate sudden growth spikes before committing long-term budget.",
            "Use trend leaders as inputs for release and update planning.",
        ],
    )


def task5_story(task_df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return insights and recommendations for Task 5."""
    installs_leader = task_df.loc[task_df["Installs"].idxmax()]
    rating_leader = task_df.loc[task_df["Rating"].idxmax()]
    return (
        [
            f"{installs_leader['App']} has the largest install footprint in this view.",
            f"{rating_leader['App']} has the highest rating at "
            f"{format_rating(rating_leader['Rating'])}.",
            "Bubble size highlights the relationship between installs, size, rating, and category.",
        ],
        [
            "Use high-install apps as competitive benchmarks.",
            "Monitor large apps with weaker ratings for usability or performance issues.",
            "Promote strong-rating apps where install scale still has room to grow.",
        ],
    )


def task6_story(task_df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return insights and recommendations for Task 6."""
    final_totals = task_df.groupby("Category")["Cumulative_Installs"].max()
    leader = final_totals.idxmax()
    return (
        [
            f"{leader} has the largest cumulative install base at "
            f"{format_number(final_totals.max())}.",
            "The stacked area view emphasizes cumulative contribution over time.",
        ],
        [
            "Invest in categories with durable cumulative growth.",
            "Watch flattening cumulative curves for signs of saturation.",
            "Use cumulative leaders for long-term portfolio planning.",
        ],
    )


def show_workflow() -> None:
    """Show the analytics workflow used in the project."""
    st.markdown(
        """
        1. Source Google Play Store app and user review datasets.
        2. Clean missing values, data types, installs, prices, and date fields.
        3. Merge app and review signals into dashboard-ready analytical datasets.
        4. Prepare task-wise datasets for focused BI views.
        5. Present KPIs, category views, trend views, sentiment views, and downloads.
        """
    )


def show_objective() -> None:
    """Show the project objective."""
    st.write(
        "Analyze Google Play Store apps and user reviews to identify category "
        "performance, installs, ratings, revenue patterns, sentiment signals, "
        "and trend behavior in a recruiter-ready BI dashboard."
    )
