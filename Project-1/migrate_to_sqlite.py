"""Migration script to transfer all project CSV datasets into a single SQLite database."""

import csv
from pathlib import Path
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
SQLITE_DB = DATA_DIR / "playstore.sqlite"

# Map file paths to clean table names
DATASETS = {
    # Raw Data
    DATA_DIR / "Raw_Data" / "googleplaystore.csv": "raw_apps",
    DATA_DIR / "Raw_Data" / "googleplaystore_user_reviews.csv": "raw_reviews",
    # Cleaned Data
    DATA_DIR / "Cleaned_Data" / "cleaned_app_data.csv": "cleaned_apps",
    DATA_DIR / "Cleaned_Data" / "cleaned_review_data.csv": "cleaned_reviews",
    DATA_DIR / "Cleaned_Data" / "aggregated_merged_dataset.csv": "aggregated_merged_apps",
    DATA_DIR / "Cleaned_Data" / "merged_dataset.csv": "merged_apps_reviews",
    DATA_DIR / "Cleaned_Data" / "eda_prepared_dataset.csv": "eda_prepared_apps",
    DATA_DIR / "Cleaned_Data" / "review_sentiment_eda_dataset.csv": "review_sentiment_eda",
    # Task-wise Data
    DATA_DIR / "Task_wise_dataset" / "task1_grouped.csv": "task1_grouped",
    DATA_DIR / "Task_wise_dataset" / "task2_grouped.csv": "task2_grouped",
    DATA_DIR / "Task_wise_dataset" / "task3_grouped.csv": "task3_grouped",
    DATA_DIR / "Task_wise_dataset" / "task4_grouped.csv": "task4_grouped",
    DATA_DIR / "Task_wise_dataset" / "task5_grouped.csv": "task5_grouped",
    DATA_DIR / "Task_wise_dataset" / "task6_grouped.csv": "task6_grouped",
}


def infer_sqlite_type(value: str) -> str:
    """Infer SQLite column type from sample values."""
    if value == "" or value is None:
        return "NULL"
    try:
        int(value)
        return "INTEGER"
    except ValueError:
        pass
    try:
        float(value)
        return "REAL"
    except ValueError:
        pass
    return "TEXT"


def migrate_csv_standard(csv_path: Path, table_name: str, conn: sqlite3.Connection) -> tuple[int, int]:
    """Migrate CSV using Python's standard csv library."""
    encodings = ["utf-8", "utf-8-sig", "latin1"]
    lines = None
    for enc in encodings:
        try:
            with open(csv_path, "r", encoding=enc) as f:
                reader = csv.reader(f)
                lines = list(reader)
            break
        except UnicodeDecodeError:
            continue

    if not lines or len(lines) == 0:
        return 0, 0

    headers = [col.strip().replace(" ", "_").replace("-", "_").replace(".", "_") for col in lines[0]]
    rows = lines[1:]

    # Sample rows to infer data types
    col_types = []
    for col_idx in range(len(headers)):
        inferred = "TEXT"
        for row in rows[:500]:
            if col_idx < len(row) and row[col_idx] != "":
                t = infer_sqlite_type(row[col_idx])
                if t == "REAL":
                    inferred = "REAL"
                elif t == "INTEGER" and inferred != "REAL":
                    inferred = "INTEGER"
                elif t == "TEXT":
                    inferred = "TEXT"
                    break
        col_types.append(inferred)

    col_defs = ", ".join(f'"{col}" {ctype}' for col, ctype in zip(headers, col_types))
    placeholders = ", ".join("?" for _ in headers)

    cursor = conn.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    cursor.execute(f'CREATE TABLE "{table_name}" ({col_defs})')

    # Normalize rows to match header length
    clean_rows = []
    for row in rows:
        if len(row) < len(headers):
            row = row + [None] * (len(headers) - len(row))
        elif len(row) > len(headers):
            row = row[: len(headers)]
        # convert empty string to None
        clean_rows.append([None if v == "" else v for v in row])

    cursor.executemany(f'INSERT INTO "{table_name}" VALUES ({placeholders})', clean_rows)
    conn.commit()
    return len(clean_rows), len(headers)


def main():
    print(f"Database destination: {SQLITE_DB}")
    conn = sqlite3.connect(SQLITE_DB)

    print("\nStarting migration...")
    print(f"{'Table Name':<28} | {'Rows':>8} | {'Columns':>8} | {'Status':<10}")
    print("-" * 62)

    total_tables = 0
    total_rows = 0

    for csv_path, table_name in DATASETS.items():
        if not csv_path.exists():
            print(f"{table_name:<28} | {'-':>8} | {'-':>8} | Missing File")
            continue

        try:
            num_rows, num_cols = migrate_csv_standard(csv_path, table_name, conn)
            print(f"{table_name:<28} | {num_rows:>8,} | {num_cols:>8} | Success")
            total_tables += 1
            total_rows += num_rows
        except Exception as e:
            print(f"{table_name:<28} | {'ERROR':>8} | {'-':>8} | {e}")

    conn.close()
    print("-" * 62)
    print(f"Total Tables Created: {total_tables}")
    print(f"Total Rows Migrated:  {total_rows:,}")
    print(f"SQLite file saved at: {SQLITE_DB.resolve()}\n")


if __name__ == "__main__":
    main()
