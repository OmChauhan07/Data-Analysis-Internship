"""Sidebar filter controls."""

import pandas as pd
import streamlit as st

from dashboard.config import DEFAULT_MIN_RATING
from dashboard.helpers import format_number


def create_sidebar(df: pd.DataFrame) -> dict[str, object]:
    """Create sidebar filters and return the selected values."""
    categories = sorted(df["Category"].dropna().unique())
    app_types = sorted(df["Type"].dropna().unique())
    min_rating = float(df["Rating"].dropna().min())
    max_rating = float(df["Rating"].dropna().max())
    min_installs = int(df["Installs"].min())
    max_installs = int(df["Installs"].max())
    default_rating = min(max(DEFAULT_MIN_RATING, min_rating), max_rating)

    st.sidebar.title("Dashboard Controls")
    st.sidebar.caption("Filter the aggregated dataset for focused analysis.")

    if st.sidebar.button("Reset Filters", use_container_width=True):
        st.session_state["category_filter"] = categories
        st.session_state["rating_filter"] = default_rating
        st.session_state["type_filter"] = app_types
        st.session_state["install_filter"] = (min_installs, max_installs)
        st.rerun()

    with st.sidebar.container(border=True):
        st.markdown("**Filter Section**")
        selected_categories = st.multiselect(
            "Select Categories",
            options=categories,
            default=categories,
            key="category_filter",
        )

        selected_rating = st.slider(
            "Minimum Rating",
            min_value=min_rating,
            max_value=max_rating,
            value=default_rating,
            step=0.1,
            key="rating_filter",
        )

        selected_types = st.multiselect(
            "App Type",
            options=app_types,
            default=app_types,
            key="type_filter",
        )

        install_range = st.slider(
            "Install Range",
            min_value=min_installs,
            max_value=max_installs,
            value=(min_installs, max_installs),
            key="install_filter",
        )

    with st.sidebar.container(border=True):
        st.markdown("**Quick Statistics**")
        st.write(f"Apps: {format_number(df['App'].nunique())}")
        st.write(f"Reviews: {format_number(df['Reviews'].sum())}")
        st.write(f"Categories: {format_number(df['Category'].nunique())}")
        st.write(f"Installs: {format_number(df['Installs'].sum())}")

    with st.sidebar.container(border=True):
        st.markdown("**Reviewer Options**")
        st.checkbox(
            "Bypass Time Locks",
            value=True,
            key="bypass_time_locks",
            help="Enable to view all charts regardless of the time of day.",
        )

    with st.sidebar.expander("About Dataset", expanded=False):
        st.write(
            "Aggregated app and review data prepared from the Google Play "
            "Store internship analysis workflow."
        )
        st.write(f"Rows: {format_number(len(df))}")
        st.write(f"Columns: {format_number(len(df.columns))}")

    return {
        "categories": selected_categories,
        "rating": selected_rating,
        "types": selected_types,
        "install_range": install_range,
    }


def apply_filters(
    df: pd.DataFrame,
    filters: dict[str, object],
) -> pd.DataFrame:
    """Apply sidebar filters and return the filtered dataframe."""
    install_min, install_max = filters["install_range"]

    filtered_df = df[
        (df["Category"].isin(filters["categories"]))
        & (df["Rating"] >= filters["rating"])
        & (df["Type"].isin(filters["types"]))
        & (df["Installs"] >= install_min)
        & (df["Installs"] <= install_max)
    ]

    return filtered_df.copy()


def show_filter_summary(filters: dict[str, object]) -> None:
    """Display a compact summary of active filters."""
    install_min, install_max = filters["install_range"]

    with st.sidebar.expander("Current Filters", expanded=True):
        st.write(f"Categories selected: {len(filters['categories'])}")
        st.write(f"Minimum rating: {filters['rating']}")
        st.write(f"App types: {', '.join(filters['types'])}")
        st.write(
            "Install range: "
            f"{format_number(install_min)} to {format_number(install_max)}"
        )
