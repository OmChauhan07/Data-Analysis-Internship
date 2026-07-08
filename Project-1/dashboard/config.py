"""Application configuration and constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
RAW_DATA_DIR = DATA_DIR / "Raw_Data"
CLEANED_DATA_DIR = DATA_DIR / "Cleaned_Data"
TASK_DATA_DIR = DATA_DIR / "Task_wise_dataset"
ASSETS_DIR = BASE_DIR / "assets"

PAGE_TITLE = "Google Play Store Analytics Dashboard"
PAGE_ICON = ""
LAYOUT = "wide"

AUTHOR = "Om Chauhan"
DATA_SOURCE = "Google Play Store Apps and User Reviews datasets"
FOOTER_TEXT = (
    "Google Play Store Analytics Dashboard | "
    f"Developed by {AUTHOR} | Internship Project | "
    'Data Source: <strong><a href="https://www.kaggle.com/datasets/lava18/google-play-store-apps" target="_blank">Kaggle</a></strong> | '
    '<strong><a href="https://github.com/OmChauhan07" target="_blank">GitHub</a></strong> | '
    '<strong><a href="https://www.linkedin.com/in/om-chauhan-21043824b/" target="_blank">LinkedIn</a></strong>'
)

GOOGLE_COLORS = {
    "blue": "#4285F4",
    "red": "#EA4335",
    "yellow": "#FBBC05",
    "green": "#34A853",
    "gray": "#5F6368",
    "light_gray": "#F8F9FA",
    "border": "#DADCE0",
    "text": "#202124",
}

GOOGLE_PALETTE = [
    GOOGLE_COLORS["blue"],
    GOOGLE_COLORS["green"],
    GOOGLE_COLORS["yellow"],
    GOOGLE_COLORS["red"],
]

PLOTLY_TEMPLATE = "plotly_white"
DEFAULT_CHART_HEIGHT = 650
DEFAULT_MIN_RATING = 3.5

MAIN_DATASET = CLEANED_DATA_DIR / "aggregated_merged_dataset.csv"
CLEAN_DATASET = CLEANED_DATA_DIR / "cleaned_app_data.csv"
REVIEW_DATASET = CLEANED_DATA_DIR / "cleaned_review_data.csv"
MERGED_DATASET = CLEANED_DATA_DIR / "merged_dataset.csv"

TASK_DATASETS = {
    "task1": TASK_DATA_DIR / "task1_grouped.csv",
    "task2": TASK_DATA_DIR / "task2_grouped.csv",
    "task3": TASK_DATA_DIR / "task3_grouped.csv",
    "task4": TASK_DATA_DIR / "task4_grouped.csv",
    "task5": TASK_DATA_DIR / "task5_grouped.csv",
    "task6": TASK_DATA_DIR / "task6_grouped.csv",
}

TIME_WINDOWS = {
    "task1": (15, 17, "3 PM and 5 PM IST"),
    "task2": (18, 20, "6 PM and 8 PM IST"),
    "task3": (13, 14, "1 PM and 2 PM IST"),
    "task4": (18, 21, "6 PM and 9 PM IST"),
    "task5": (17, 19, "5 PM and 7 PM IST"),
    "task6": (16, 18, "4 PM and 6 PM IST"),
}

PAGE_TABS = [
    "Home",
    "Overview",
    "Category Analysis",
    "Trend Analysis",
    "Sentiment Analysis",
    "Downloads",
    "About",
]

HERO_BADGES = ["Python", "Pandas", "NumPy", "Plotly", "Streamlit"]

TECH_STACK = [
    "Python",
    "Pandas",
    "NumPy",
    "Plotly",
    "Streamlit",
    "Jupyter Notebook",
]
