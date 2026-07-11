"""Page and tab rendering for the Streamlit dashboard."""

from datetime import datetime
from typing import Callable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard import charts
from dashboard.chart_utils import (
    download_dataframe,
    render_chart,
    render_time_warning,
)
from dashboard.config import (
    AUTHOR,
    FOOTER_TEXT,
    HERO_BADGES,
    PAGE_TABS,
    TECH_STACK,
    TIME_WINDOWS,
)
from dashboard.data_loader import (
    dataset_summary,
    load_clean_dataset,
    load_review_dataset,
)
from dashboard.helpers import (
    format_number,
    is_time_between,
    render_badges,
    render_kpi_card,
    render_page_header,
)
from dashboard.insights import (
    executive_summary_items,
    show_business_summary,
    show_insight_recommendation,
    show_objective,
    show_workflow,
    task1_story,
    task2_story,
    task3_story,
    task4_story,
    task5_story,
    task6_story,
)
from dashboard.kpi import show_dataset_summary, show_kpis

TaskData = dict[str, pd.DataFrame]


def render_dashboard(
    main_df: pd.DataFrame,
    filtered_df: pd.DataFrame,
    task_datasets: TaskData,
) -> None:
    """Render the complete tabbed dashboard."""
    render_hero(main_df)

    tabs = st.tabs(PAGE_TABS)
    with tabs[0]:
        render_home_page(main_df)
    with tabs[1]:
        render_overview_page(filtered_df)
    with tabs[2]:
        render_category_page(task_datasets)
    with tabs[3]:
        render_trend_page(task_datasets)
    with tabs[4]:
        render_sentiment_page(task_datasets)
    with tabs[5]:
        render_downloads_page(main_df, task_datasets)
    with tabs[6]:
        render_about_page(main_df)

    render_footer()


def render_hero(main_df: pd.DataFrame) -> None:
    """Render the executive hero section."""
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">PlayStore Interlligence: App Analytics & Sentiment Mining Dashboard</div>
            <div class="hero-subtitle">
                Interactive Business Intelligence Dashboard for Google Play Store
                Apps &amp; User Reviews
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_badges(HERO_BADGES)

    st.write("")
    total_reviews = main_df["Reviews"].sum()
    hero_cols = st.columns(4)
    with hero_cols[0]:
        render_kpi_card(
            "",
            "Total Apps",
            format_number(main_df["App"].nunique()),
            "Apps currently analyzed",
        )
    with hero_cols[1]:
        render_kpi_card(
            "",
            "Total Reviews",
            format_number(total_reviews),
            "Review volume in app data",
        )
    with hero_cols[2]:
        render_kpi_card(
            "",
            "Categories",
            format_number(main_df["Category"].nunique()),
            "Distinct app categories",
        )
    with hero_cols[3]:
        render_kpi_card(
            "",
            "Installs",
            format_number(main_df["Installs"].sum()),
            "Total install footprint",
        )


def render_home_page(main_df: pd.DataFrame) -> None:
    """Render the landing page."""
    render_page_header(
        "Home",
        "Project overview, workflow, dataset health, and navigation for the BI dashboard.",
    )

    overview_col, stack_col = st.columns([1.2, 0.8])
    with overview_col:
        with st.container(border=True):
            st.subheader("Project Overview")
            st.write(
                "This dashboard presents Google Play Store app performance, "
                "category behavior, install trends, revenue indicators, and "
                "review sentiment signals using prepared internship datasets."
            )
            st.write(
                "The experience is structured for executive review: start with "
                "headline KPIs, explore category and trend views, then download "
                "the curated datasets used in the analysis."
            )

    with stack_col:
        with st.container(border=True):
            st.subheader("Technology Stack")
            render_badges(TECH_STACK)

    st.subheader("Workflow Diagram")
    workflow_cols = st.columns(5)
    workflow_steps = [
        ("1", "Collect", "Raw app and review datasets"),
        ("2", "Clean", "Types, dates, installs, prices"),
        ("3", "Merge", "Combine app and review signals"),
        ("4", "Prepare", "Task-wise analytical datasets"),
        ("5", "Present", "BI dashboard and downloads"),
    ]
    for column, (step, title, text) in zip(workflow_cols, workflow_steps):
        with column:
            render_kpi_card(step, title, "", text)

    st.subheader("Dataset Summary")
    show_dataset_summary(main_df)

    st.subheader("Quick Navigation")
    nav_cols = st.columns(4)
    navigation = [
        ("Overview", "Executive KPIs and summary cards"),
        ("Category Analysis", "Rating, reviews, installs, revenue"),
        ("Trend Analysis", "Monthly and cumulative install movement"),
        ("Downloads", "Export aggregated and task datasets"),
    ]
    for column, (title, text) in zip(nav_cols, navigation):
        with column:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(text)


def render_overview_page(filtered_df: pd.DataFrame) -> None:
    """Render the overview page."""
    render_page_header(
        "Overview",
        "Executive summary for the currently selected sidebar filters.",
    )

    if filtered_df.empty:
        st.warning("No records match the current sidebar filters.")
        return

    st.subheader("Executive Summary")
    summary_cols = st.columns(5)
    for column, item in zip(summary_cols, executive_summary_items(filtered_df)):
        with column:
            render_kpi_card(
                item["icon"],
                item["title"],
                item["value"],
                item["subtitle"],
            )

    st.subheader("Dashboard KPIs")
    show_kpis(filtered_df)

    st.subheader("Dataset Summary")
    show_dataset_summary(filtered_df)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        render_chart(charts.create_top_categories_chart(filtered_df))
    with chart_col2:
        render_chart(charts.create_rating_distribution_chart(filtered_df))

    show_business_summary(filtered_df)


def render_category_page(task_datasets: TaskData) -> None:
    """Render category-focused task charts."""
    render_page_header(
        "Category Analysis",
        "Category-level comparison of app quality, engagement, installs, and revenue.",
    )

    render_task_section(
        "Task 1: Rating vs Reviews Analysis",
        "Compares category quality signals with user engagement volume.",
        "Task 1",
        "task1",
        task_datasets["task1"],
        lambda: charts.create_task1_chart(task_datasets["task1"]),
        task1_story,
    )

    render_task_section(
        "Task 3: Free vs Paid Apps Analysis",
        "Shows how free and paid app segments differ by installs and revenue.",
        "Task 3",
        "task3",
        task_datasets["task3"],
        lambda: charts.create_task3_chart(task_datasets["task3"]),
        task3_story,
    )


def render_trend_page(task_datasets: TaskData) -> None:
    """Render trend-focused task charts."""
    render_page_header(
        "Trend Analysis",
        "Monthly install movement and cumulative growth across prepared categories.",
    )

    render_task_section(
        "Task 4: Installs Trend Analysis",
        "Tracks install movement over time for leading categories.",
        "Task 4",
        "task4",
        task_datasets["task4"],
        lambda: charts.create_task4_chart(task_datasets["task4"]),
        task4_story,
    )

    render_task_section(
        "Task 6: Stacked Area Chart",
        "Shows cumulative install contribution over time by category.",
        "Task 6",
        "task6",
        task_datasets["task6"],
        lambda: charts.create_task6_chart(task_datasets["task6"]),
        task6_story,
    )


def render_sentiment_page(task_datasets: TaskData) -> None:
    """Render sentiment and review-related task charts."""
    render_page_header(
        "Sentiment Analysis",
        "Review-driven and app-level views that support user sentiment storytelling.",
    )

    render_task_section(
        "Task 2: Global Installs Choropleth",
        "Maps prepared category install volume into a geographic BI view.",
        "Task 2",
        "task2",
        task_datasets["task2"],
        lambda: charts.create_task2_chart(task_datasets["task2"]),
        task2_story,
    )

    render_task_section(
        "Task 5: Bubble Chart Analysis",
        "Compares app size, rating, installs, and category in one view.",
        "Task 5",
        "task5",
        task_datasets["task5"],
        lambda: charts.create_task5_chart(task_datasets["task5"]),
        task5_story,
    )


def render_downloads_page(main_df: pd.DataFrame, task_datasets: TaskData) -> None:
    """Render dataset download controls."""
    render_page_header(
        "Downloads",
        "Export the curated datasets used by the dashboard and task charts.",
    )

    with st.spinner("Preparing downloadable datasets..."):
        clean_df = load_clean_dataset()
        review_df = load_review_dataset()

    st.success("Datasets are ready for download.")

    st.subheader("Core Datasets")
    core_downloads = [
        (
            "Aggregated Dataset",
            "Merged dashboard dataset used for filters, KPIs, and overview analysis.",
            main_df,
            "aggregated_merged_dataset.csv",
        ),
        (
            "Clean App Dataset",
            "Cleaned Google Play Store app data prepared during preprocessing.",
            clean_df,
            "cleaned_app_data.csv",
        ),
        (
            "Clean Review Dataset",
            "Cleaned user review dataset used for sentiment-related analysis.",
            review_df,
            "cleaned_review_data.csv",
        ),
    ]
    render_download_grid(core_downloads)

    st.subheader("Task Datasets")
    task_downloads = [
        (
            f"{task_name.title()} Dataset",
            "Prepared task-wise dataset used by its corresponding visualization.",
            task_df,
            f"{task_name}_grouped.csv",
        )
        for task_name, task_df in task_datasets.items()
    ]
    render_download_grid(task_downloads)


def render_about_page(main_df: pd.DataFrame) -> None:
    """Render project details."""
    render_page_header(
        "About",
        "Project objective, dataset context, workflow, tools, and author information.",
    )

    sections = [
        ("Objective", show_objective),
        ("Dataset", lambda: render_dataset_about(main_df)),
        ("Workflow", show_workflow),
        ("Tools", lambda: st.write(", ".join(TECH_STACK))),
        ("Author", lambda: st.write(AUTHOR)),
    ]

    for title, renderer in sections:
        with st.container(border=True):
            st.subheader(title)
            renderer()


def render_task_section(
    title: str,
    description: str,
    task_label: str,
    task_key: str,
    task_df: pd.DataFrame,
    chart_factory: Callable[[], go.Figure],
    story_factory: Callable[[pd.DataFrame], tuple[list[str], list[str]]],
) -> None:
    """Render a chart section with insights and recommendations."""
    st.subheader(title)
    st.caption(description)
    render_time_gated_chart(task_label, task_key, chart_factory)

    insights, recommendations = story_factory(task_df)
    show_insight_recommendation(insights, recommendations)


def render_time_gated_chart(
    task_label: str,
    task_key: str,
    chart_factory: Callable[[], go.Figure],
) -> None:
    """Render a chart only during its original IST availability window."""
    start_hour, end_hour, label = TIME_WINDOWS[task_key]
    if is_time_between(start_hour, end_hour):
        render_chart(chart_factory())
    else:
        render_time_warning(task_label, label)


def render_download_grid(
    download_items: list[tuple[str, str, pd.DataFrame, str]],
) -> None:
    """Render download cards in a responsive grid."""
    columns = st.columns(3)
    for index, (title, description, dataframe, filename) in enumerate(download_items):
        with columns[index % 3]:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(description)
                st.write(
                    f"{format_number(len(dataframe))} rows | "
                    f"{format_number(len(dataframe.columns))} columns"
                )
                download_dataframe(dataframe, "Download CSV", filename)


def render_dataset_about(main_df: pd.DataFrame) -> None:
    """Render dataset details for the About page."""
    summary = dataset_summary(main_df)
    st.write(
        f"Aggregated dataset: {format_number(summary['Rows'])} rows, "
        f"{format_number(summary['Columns'])} columns, "
        f"{format_number(summary['Missing Values'])} missing values, and "
        f"{format_number(summary['Duplicate Rows'])} duplicate rows."
    )
    st.write(
        "Raw app data, raw review data, cleaned data, merged data, and task-wise "
        "datasets are included in the project folder."
    )


def render_footer() -> None:
    """Render an improved footer."""
    current_year = datetime.now().year
    st.markdown(
        f"""
        <div class="footer">
            {FOOTER_TEXT} | Year: {current_year}
        </div>
        """,
        unsafe_allow_html=True,
    )
