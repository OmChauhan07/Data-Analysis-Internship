"""Cached dataset loaders for the dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard.config import (
    CLEAN_DATASET,
    MAIN_DATASET,
    MERGED_DATASET,
    REVIEW_DATASET,
    TASK_DATASETS,
)


@st.cache_data(show_spinner=False, ttl=3600)
def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file with Streamlit caching and error handling."""
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Error loading dataset: {path.name} ({e}).")
        return pd.DataFrame()


@st.cache_data(show_spinner="Loading dashboard dataset...", ttl=3600)
def load_main_dataset() -> pd.DataFrame:
    """Load the aggregated dataset used for filters and KPIs."""
    return load_csv(MAIN_DATASET)


@st.cache_data(show_spinner=False, ttl=3600)
def load_clean_dataset() -> pd.DataFrame:
    """Load the cleaned app dataset."""
    return load_csv(CLEAN_DATASET)


@st.cache_data(show_spinner=False, ttl=3600)
def load_review_dataset() -> pd.DataFrame:
    """Load the cleaned reviews dataset."""
    return load_csv(REVIEW_DATASET)


@st.cache_data(show_spinner=False, ttl=3600)
def load_merged_dataset() -> pd.DataFrame:
    """Load the merged app and review dataset."""
    return load_csv(MERGED_DATASET)


@st.cache_data(show_spinner=False, ttl=3600)
def load_task1() -> pd.DataFrame:
    """Load Task 1 grouped data."""
    return load_csv(TASK_DATASETS["task1"])


@st.cache_data(show_spinner=False, ttl=3600)
def load_task2() -> pd.DataFrame:
    """Load Task 2 grouped data."""
    return load_csv(TASK_DATASETS["task2"])


@st.cache_data(show_spinner=False, ttl=3600)
def load_task3() -> pd.DataFrame:
    """Load Task 3 grouped data."""
    return load_csv(TASK_DATASETS["task3"])


@st.cache_data(show_spinner=False, ttl=3600)
def load_task4() -> pd.DataFrame:
    """Load Task 4 grouped data."""
    return load_csv(TASK_DATASETS["task4"])


@st.cache_data(show_spinner=False, ttl=3600)
def load_task5() -> pd.DataFrame:
    """Load Task 5 grouped data."""
    return load_csv(TASK_DATASETS["task5"])


@st.cache_data(show_spinner=False, ttl=3600)
def load_task6() -> pd.DataFrame:
    """Load Task 6 grouped data."""
    return load_csv(TASK_DATASETS["task6"])


@st.cache_data(show_spinner=False, ttl=3600)
def load_all_task_datasets() -> dict[str, pd.DataFrame]:
    """Load all task datasets once and return them by task name."""
    return {
        "task1": load_task1(),
        "task2": load_task2(),
        "task3": load_task3(),
        "task4": load_task4(),
        "task5": load_task5(),
        "task6": load_task6(),
    }


def dataset_summary(df: pd.DataFrame) -> dict[str, int]:
    """Return a compact quality summary for a dataframe."""
    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": int(df.isna().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
    }
