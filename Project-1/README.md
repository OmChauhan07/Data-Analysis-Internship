# 📱 PlayStore Interlligence: App Analytics & Sentiment Mining Dashboard

An interactive, portfolio-quality Business Intelligence Dashboard built with Streamlit and Plotly to analyze Google Play Store applications and user reviews. This project processes raw app and review data to deliver executive KPIs, category insights, trend analysis, and geographic visualizations.

## Live Demo

https://play-store-data-analysis-dashboard.streamlit.app/

## 🚀 Key Features

- **Executive Overview**: High-level KPIs including total apps, average rating, install volume, and estimated revenue.
- **Dynamic Filtering**: Interactive sidebar filters for app categories, ratings, app type (Free/Paid), and install ranges.
- **Category Analysis**: Compare average ratings, user engagement, and monetization across different app categories.
- **Trend & Growth**: Track monthly install momentum and cumulative growth for top-performing categories.
- **Geographic Insights**: Explore global install patterns via an interactive choropleth map.
- **Sentiment & Review Storytelling**: Interactive bubble charts and sentiment metrics derived from user reviews.
- **Reviewer Mode**: Ability to bypass time-locked features to view all visualizations at any time (ideal for technical evaluations).
- **Data Export**: Direct CSV downloads for the aggregated datasets right from the dashboard.

## 🧰 Technology Stack

- **Python 3.9+**
- **Streamlit**: For building the interactive web application and UI.
- **Pandas & NumPy**: For robust data cleaning, aggregation, and manipulation.
- **Plotly Express & Graph Objects**: For creating interactive, beautiful data visualizations.

## 📂 Project Structure

```text
Project-1/
├── Data/                   # Raw and cleaned datasets
│   ├── Cleaned_Data/
│   ├── Raw_Data/
│   └── Task_wise_dataset/
├── dashboard/              # Core application logic
│   ├── chart_utils.py      # Plotly chart utilities and styling
│   ├── charts.py           # Builders for dashboard visualizations
│   ├── config.py           # Global constants and configuration
│   ├── data_loader.py      # Data loading and caching logic
│   ├── filters.py          # Sidebar and filtering logic
│   ├── helpers.py          # Formatting and UI helpers
│   ├── insights.py         # Business logic and narrative text
│   ├── kpi.py              # KPI calculation and rendering
│   └── pages.py            # Streamlit tab rendering logic
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🛠️ Installation & Setup

1. **Clone the repository** (if hosted on GitHub) or navigate to the project folder:
   ```bash
   cd Project-1
   ```

2. **Create a virtual environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```
   The dashboard will automatically open in your default web browser at `http://localhost:8501`.

## 🔎 Reviewer Mode (Bypass Time Locks)

During the internship, certain charts were restricted to specific hours (IST). For portfolio and review purposes, a **"Bypass Time Locks"** option has been added to the sidebar. It is enabled by default to ensure recruiters and evaluators can view all visualizations regardless of their current time zone or time of day.

## 👤 Author

**Om Chauhan**  
*Data Analysis Internship Project*  

---
*Developed as part of a Data Analysis Internship to demonstrate data engineering, visualization, and product storytelling capabilities.*
