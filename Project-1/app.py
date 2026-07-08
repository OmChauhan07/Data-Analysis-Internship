"""Streamlit entry point for the Google Play Store Analytics dashboard."""

import streamlit as st

from dashboard import pages
from dashboard.config import LAYOUT, PAGE_ICON, PAGE_TITLE
from dashboard.data_loader import load_all_task_datasets, load_main_dataset
from dashboard.filters import apply_filters, create_sidebar, show_filter_summary
from dashboard.helpers import apply_custom_css


def main() -> None:
    """Run the dashboard application."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
    )
    apply_custom_css()

    with st.spinner("Loading dashboard datasets..."):
        load_progress = st.progress(0, text="Loading aggregated dataset")
        main_df = load_main_dataset()
        load_progress.progress(55, text="Loading task datasets")
        task_datasets = load_all_task_datasets()
        load_progress.progress(100, text="Dashboard data ready")
        load_progress.empty()

    filters = create_sidebar(main_df)
    filtered_df = apply_filters(main_df, filters)
    show_filter_summary(filters)

    pages.render_dashboard(main_df, filtered_df, task_datasets)


if __name__ == "__main__":
    main()
