"""Reusable Plotly chart utilities."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.config import DEFAULT_CHART_HEIGHT, GOOGLE_PALETTE, PLOTLY_TEMPLATE
from dashboard.helpers import to_csv_bytes


def apply_default_layout(
    fig: go.Figure,
    title: str,
    subtitle: str | None = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> go.Figure:
    """Apply the dashboard's standard Plotly layout."""
    title_text = title
    if subtitle:
        title_text = f"{title}<br><sup>{subtitle}</sup>"

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        title={
            "text": title_text,
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 20, "color": "#202124"},
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.04,
            "xanchor": "right",
            "x": 1,
            "font": {"size": 12},
        },
        margin={"l": 35, "r": 25, "t": 95, "b": 55},
        hovermode="closest",
        font={"family": "Arial, sans-serif", "size": 13, "color": "#202124"},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
    )
    return fig


def style_axes(
    fig: go.Figure,
    x_title: str = "",
    y_title: str = "",
) -> go.Figure:
    """Apply consistent axis titles and grid styling."""
    fig.update_xaxes(title=x_title, showgrid=False, zeroline=False)
    fig.update_yaxes(
        title=y_title,
        showgrid=True,
        gridcolor="#E8EAED",
        zeroline=False,
    )
    return fig


def render_chart(fig: go.Figure) -> None:
    """Render a Plotly chart in Streamlit."""
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)


def render_time_warning(task_name: str, available_window: str) -> None:
    """Show a consistent message for time-gated charts."""
    with st.container(border=True):
        st.warning(f"{task_name} chart is available only between {available_window}.")


def download_dataframe(df: pd.DataFrame, label: str, filename: str) -> None:
    """Render a CSV download button for a dataframe."""
    st.download_button(
        label=label,
        data=to_csv_bytes(df),
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )


def repeated_google_palette(length: int) -> list[str]:
    """Return a repeated Google palette long enough for a trace."""
    repeats = (length // len(GOOGLE_PALETTE)) + 1
    return (GOOGLE_PALETTE * repeats)[:length]
