"""Shared helper functions."""

from datetime import datetime
from typing import Any

import pandas as pd
from zoneinfo import ZoneInfo
import streamlit as st

IST_TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_ist_time() -> datetime:
    """Return the current datetime in Indian Standard Time."""
    return datetime.now(IST_TIMEZONE)


def get_ist_hour() -> int:
    """Return the current hour in Indian Standard Time."""
    return get_ist_time().hour


def is_time_between(start_hour: int, end_hour: int) -> bool:
    """Return True when the current IST hour is in the half-open range."""
    if st.session_state.get("bypass_time_locks", False):
        return True
    current_hour = get_ist_hour()
    return start_hour <= current_hour < end_hour


def format_number(value: Any) -> str:
    """Format numbers with thousands separators."""
    if pd.isna(value):
        return "0"

    return f"{float(value):,.0f}"


def format_compact_number(value: Any) -> str:
    """Format large numbers using K, M, and B suffixes."""
    if pd.isna(value):
        return "0"

    number = float(value)
    for suffix, divisor in (("B", 1_000_000_000), ("M", 1_000_000), ("K", 1_000)):
        if abs(number) >= divisor:
            return f"{number / divisor:.2f}{suffix}"
    return f"{number:.0f}"


def format_currency(value: Any) -> str:
    """Format revenue values as USD."""
    if pd.isna(value):
        return "$0"
    return f"${float(value):,.0f}"


def format_rating(value: Any) -> str:
    """Format app ratings with two decimals."""
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.2f}"


def show_section(title: str, description: str | None = None) -> None:
    """Render a consistent section heading."""
    st.subheader(title)
    if description:
        st.caption(description)


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a dataframe to downloadable CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")


def apply_custom_css() -> None:
    """Apply light BI-style CSS on top of Streamlit defaults."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2.5rem;
            max-width: 1440px;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0.85rem;
        }
        section[data-testid="stSidebar"] {
            background: #F8F9FA;
            border-right: 1px solid #DADCE0;
        }
        .hero-card {
            border: 1px solid #DADCE0;
            border-radius: 14px;
            padding: 1.45rem 1.55rem;
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            box-shadow: 0 1px 4px rgba(60, 64, 67, 0.10);
            margin-bottom: 0.9rem;
        }
        .hero-title {
            color: #202124;
            font-size: 2.2rem;
            font-weight: 750;
            letter-spacing: 0;
            margin: 0 0 0.35rem 0;
        }
        .hero-subtitle {
            color: #5F6368;
            font-size: 1.02rem;
            margin: 0 0 0.85rem 0;
        }
        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.3rem;
        }
        .stack-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            background: #E8F0FE;
            color: #174EA6;
            border: 1px solid #D2E3FC;
            font-size: 0.82rem;
            font-weight: 650;
        }
        .kpi-card {
            border: 1px solid #DADCE0;
            border-radius: 12px;
            padding: 1rem;
            background: #FFFFFF;
            box-shadow: 0 1px 3px rgba(60, 64, 67, 0.10);
            min-height: 132px;
        }
        .kpi-icon {
            font-size: 1.35rem;
            line-height: 1;
            margin-bottom: 0.45rem;
        }
        .kpi-title {
            color: #5F6368;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            margin-bottom: 0.25rem;
        }
        .kpi-value {
            color: #202124;
            font-size: 1.65rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }
        .kpi-subtitle {
            color: #5F6368;
            font-size: 0.84rem;
        }
        .section-kicker {
            color: #4285F4;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.2rem;
        }
        .section-title {
            color: #202124;
            font-size: 1.35rem;
            font-weight: 760;
            margin-bottom: 0.2rem;
        }
        .section-description {
            color: #5F6368;
            font-size: 0.95rem;
            margin-bottom: 0.35rem;
        }
        .footer {
            border-top: 1px solid #DADCE0;
            color: #5F6368;
            font-size: 0.84rem;
            padding-top: 0.9rem;
            margin-top: 1.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_badges(items: list[str]) -> None:
    """Render pill badges."""
    badges = "".join(f"<span class='stack-badge'>{item}</span>" for item in items)
    st.markdown(f"<div class='badge-row'>{badges}</div>", unsafe_allow_html=True)


def render_kpi_card(
    icon: str,
    title: str,
    value: str,
    subtitle: str,
) -> None:
    """Render a custom KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, description: str) -> None:
    """Render a consistent page header."""
    st.markdown(
        f"""
        <div class="section-kicker">Business Intelligence View</div>
        <div class="section-title">{title}</div>
        <div class="section-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )
