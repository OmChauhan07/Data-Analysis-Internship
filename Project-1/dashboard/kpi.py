"""KPI calculations and display components."""

import pandas as pd

import streamlit as st

from dashboard.helpers import (
    format_currency,
    format_number,
    format_rating,
    render_kpi_card,
)


def calculate_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Calculate the dashboard KPIs without changing source logic."""
    if df.empty:
        return {
            "total_apps": 0,
            "average_rating": 0,
            "total_installs": 0,
            "total_revenue": 0,
            "average_reviews": 0,
        }

    return {
        "total_apps": df["App"].nunique(),
        "average_rating": df["Rating"].mean(),
        "total_installs": df["Installs"].sum(),
        "total_revenue": df["Revenue"].sum(),
        "average_reviews": df["Reviews"].mean(),
    }


def show_kpis(df: pd.DataFrame) -> None:
    """Render dashboard KPI cards."""
    kpis = calculate_kpis(df)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card(
            "",
            "Total Apps",
            format_number(kpis["total_apps"]),
            "Apps currently analyzed",
        )
    with col2:
        render_kpi_card(
            "",
            "Average Rating",
            format_rating(kpis["average_rating"]),
            "Mean rating across filtered apps",
        )
    with col3:
        render_kpi_card(
            "",
            "Total Installs",
            format_number(kpis["total_installs"]),
            "Install volume in selected data",
        )
    with col4:
        render_kpi_card(
            "",
            "Total Revenue",
            format_currency(kpis["total_revenue"]),
            "Estimated revenue from paid apps",
        )
    with col5:
        render_kpi_card(
            "",
            "Average Reviews",
            format_number(kpis["average_reviews"]),
            "Average review count",
        )


def show_dataset_summary(df: pd.DataFrame) -> None:
    """Render dataset summary metrics."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("", "Rows", format_number(len(df)), "Filtered records")
    with col2:
        render_kpi_card("", "Columns", format_number(len(df.columns)), "Available fields")
    with col3:
        render_kpi_card(
            "",
            "Categories",
            format_number(df["Category"].nunique()),
            "Unique app categories",
        )
    with col4:
        render_kpi_card(
            "",
            "App Types",
            format_number(df["Type"].nunique()),
            "Free and paid segments",
        )
