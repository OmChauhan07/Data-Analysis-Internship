"""Plotly chart builders for all dashboard visualizations."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dashboard.chart_utils import (
    apply_default_layout,
    repeated_google_palette,
    style_axes,
)
from dashboard.config import DEFAULT_CHART_HEIGHT, GOOGLE_COLORS, GOOGLE_PALETTE


def create_rating_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create an overview histogram for app ratings."""
    fig = px.histogram(
        df,
        x="Rating",
        nbins=20,
        color_discrete_sequence=[GOOGLE_COLORS["blue"]],
        labels={"Rating": "Rating"},
    )
    fig.update_traces(
        hovertemplate="Rating bucket: %{x}<br>Apps: %{y:,}<extra></extra>"
    )
    apply_default_layout(
        fig,
        "Rating Distribution",
        "Distribution of app ratings in the current filtered dataset",
        height=420,
    )
    style_axes(fig, "Rating", "Number of Apps")
    return fig


def create_top_categories_chart(df: pd.DataFrame) -> go.Figure:
    """Create an overview bar chart for top categories by app count."""
    category_counts = (
        df["Category"]
        .value_counts()
        .head(10)
        .rename_axis("Category")
        .reset_index(name="Apps")
    )

    fig = px.bar(
        category_counts,
        x="Category",
        y="Apps",
        color="Category",
        color_discrete_sequence=repeated_google_palette(len(category_counts)),
        labels={"Apps": "Apps", "Category": "Category"},
    )
    fig.update_traces(
        hovertemplate="Category: %{x}<br>Apps: %{y:,}<extra></extra>"
    )
    apply_default_layout(
        fig,
        "Top Categories by App Count",
        "Highest-volume app categories by number of records",
        height=420,
    )
    style_axes(fig, "Category", "Number of Apps")
    fig.update_layout(showlegend=False)
    return fig


def create_task1_chart(task1_df: pd.DataFrame) -> go.Figure:
    """Task 1: Average rating and total reviews by category."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=task1_df["Category"],
            y=task1_df["Rating"],
            name="Average Rating",
            marker_color=GOOGLE_PALETTE * 3,
            width=0.35,
            offsetgroup=1,
            hovertemplate=(
                "Category: %{x}<br>Average Rating: %{y:.2f}<extra></extra>"
            ),
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(
            x=task1_df["Category"],
            y=task1_df["Reviews"],
            name="Total Reviews",
            marker_color=[
                GOOGLE_COLORS["red"],
                GOOGLE_COLORS["yellow"],
                GOOGLE_COLORS["blue"],
                GOOGLE_COLORS["green"],
            ]
            * 3,
            width=0.35,
            offsetgroup=2,
            hovertemplate=(
                "Category: %{x}<br>Total Reviews: %{y:,}<extra></extra>"
            ),
        ),
        secondary_y=True,
    )

    apply_default_layout(
        fig,
        "Top 10 App Categories: Average Rating vs Reviews",
        "Compares user quality signals with engagement volume",
        height=600,
    )
    fig.update_yaxes(title_text="Average Rating", secondary_y=False)
    fig.update_yaxes(title_text="Total Reviews", secondary_y=True)
    fig.update_xaxes(title_text="Category")
    return fig


def create_task2_chart(task2_df: pd.DataFrame) -> go.Figure:
    """Task 2: Global installs choropleth."""
    chart_df = task2_df.copy()
    chart_df["Country"] = [
        "India",
        "United States",
        "Brazil",
        "Germany",
        "South Africa",
    ]

    fig = px.choropleth(
        chart_df,
        locations="Country",
        locationmode="country names",
        color="Installs",
        hover_name="Category",
        color_continuous_scale=GOOGLE_PALETTE,
        labels={"Installs": "Installs"},
    )
    apply_default_layout(
        fig,
        "Global Installs by Category",
        "Mapped install intensity for the prepared category dataset",
        height=DEFAULT_CHART_HEIGHT,
    )
    return fig


def create_task3_chart(task3_df: pd.DataFrame) -> go.Figure:
    """Task 3: Free vs paid installs and revenue analysis."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for app_type, color in zip(
        ["Free", "Paid"],
        [GOOGLE_COLORS["blue"], GOOGLE_COLORS["green"]],
    ):
        temp_df = task3_df[task3_df["Type"] == app_type]
        fig.add_trace(
            go.Bar(
                x=temp_df["Category"],
                y=temp_df["Installs"],
                name=f"{app_type} Installs",
                marker_color=color,
                hovertemplate=(
                    "Category: %{x}<br>"
                    f"{app_type} Installs: "
                    "%{y:,}<extra></extra>"
                ),
            ),
            secondary_y=False,
        )

    for app_type, color in zip(
        ["Free", "Paid"],
        [GOOGLE_COLORS["yellow"], GOOGLE_COLORS["red"]],
    ):
        temp_df = task3_df[task3_df["Type"] == app_type]
        fig.add_trace(
            go.Scatter(
                x=temp_df["Category"],
                y=temp_df["Revenue"],
                mode="lines+markers",
                name=f"{app_type} Revenue",
                line={"color": color, "width": 4},
                hovertemplate=(
                    "Category: %{x}<br>"
                    f"{app_type} Revenue: "
                    "$%{y:,.0f}<extra></extra>"
                ),
            ),
            secondary_y=True,
        )

    apply_default_layout(
        fig,
        "Free vs Paid Apps: Installs and Revenue",
        "Highlights reach and monetization by app type",
        height=DEFAULT_CHART_HEIGHT,
    )
    fig.update_yaxes(title_text="Installs", secondary_y=False)
    fig.update_yaxes(title_text="Revenue", secondary_y=True)
    fig.update_xaxes(title_text="Category")
    return fig


def create_task4_chart(task4_df: pd.DataFrame) -> go.Figure:
    """Task 4: Installs trend analysis."""
    chart_df = task4_df.copy()
    chart_df["Category"] = chart_df["Category"].replace(
        {
            "Beauty": "सौंदर्य",
            "Business": "வணிகம்",
            "Dating": "Partnersuche",
        }
    )

    top_categories = (
        chart_df.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(4)
        .index
    )
    chart_df = chart_df[chart_df["Category"].isin(top_categories)]

    fig = go.Figure()
    for category, color in zip(chart_df["Category"].unique(), GOOGLE_PALETTE * 5):
        category_df = chart_df[chart_df["Category"] == category]
        fig.add_trace(
            go.Scatter(
                x=category_df["Year_Month"],
                y=category_df["Installs"],
                mode="lines",
                name=category,
                line={"color": color, "width": 3},
                hovertemplate="Month: %{x}<br>Installs: %{y:,}<extra></extra>",
            )
        )

    apply_default_layout(
        fig,
        "Installs Trend for Top Categories",
        "Monthly install movement for the highest-volume categories",
        height=700,
    )
    style_axes(fig, "Month", "Installs")
    fig.update_layout(yaxis_type="log")
    return fig


def create_task5_chart(task5_df: pd.DataFrame) -> go.Figure:
    """Task 5: Bubble chart analysis."""
    chart_df = task5_df.copy()
    chart_df["Category"] = chart_df["Category"].replace(
        {
            "BEAUTY": "सौंदर्य",
            "BUSINESS": "வணிகம்",
            "DATING": "Partnersuche",
        }
    )

    color_map = {
        "GAME": GOOGLE_COLORS["red"],
        "सौंदर्य": GOOGLE_COLORS["blue"],
        "வணிகம்": GOOGLE_COLORS["green"],
        "COMICS": GOOGLE_COLORS["yellow"],
        "COMMUNICATION": GOOGLE_COLORS["blue"],
    }

    fig = px.scatter(
        chart_df,
        x="Size",
        y="Rating",
        size="Installs",
        color="Category",
        color_discrete_map=color_map,
        hover_name="App",
        size_max=60,
        labels={"Size": "Size", "Rating": "Rating", "Installs": "Installs"},
    )
    fig.update_traces(
        hovertemplate=(
            "App: %{hovertext}<br>Size: %{x}<br>Rating: %{y:.2f}"
            "<br>Installs: %{marker.size:,}<extra></extra>"
        )
    )
    apply_default_layout(
        fig,
        "App Size, Rating, Installs, and Category",
        "Bubble size represents install scale for selected apps",
        height=700,
    )
    style_axes(fig, "Size", "Rating")
    return fig


def create_task6_chart(task6_df: pd.DataFrame) -> go.Figure:
    """Task 6: Stacked area chart for cumulative installs."""
    chart_df = task6_df.copy()
    chart_df["Category"] = chart_df["Category"].replace(
        {
            "TRAVEL_AND_LOCAL": "Voyage_Local",
            "PRODUCTIVITY": "Productividad",
            "PHOTOGRAPHY": "写真",
        }
    )

    fig = go.Figure()
    for category, color in zip(chart_df["Category"].unique(), GOOGLE_PALETTE * 5):
        category_df = chart_df[chart_df["Category"] == category]
        fig.add_trace(
            go.Scatter(
                x=category_df["Year_Month"],
                y=category_df["Cumulative_Installs"],
                mode="lines",
                stackgroup="one",
                name=category,
                line={"color": color, "width": 2},
                hovertemplate=(
                    "Month: %{x}<br>Cumulative Installs: %{y:,}<extra></extra>"
                ),
            )
        )

    apply_default_layout(
        fig,
        "Cumulative Installs Over Time",
        "Stacked cumulative install contribution by category",
        height=700,
    )
    style_axes(fig, "Month", "Cumulative Installs")
    return fig
