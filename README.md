# Nexalyze &#9889; — Instant EDA Studio

Nexalyze is a modern, Exploratory Data Analysis (EDA) dashboard built with Streamlit. Upload any CSV file and instantly get dataset overviews, missing value analysis, duplicate detection, statistical summaries, correlation heatmaps, outlier detection (IQR method), rich visualizations, and a one-click cleaned data export — all wrapped in a clean, card-based SaaS-style UI with working dark/light themes.

## Features

- **Dashboard** — At-a-glance KPI cards (rows, columns, missing %, duplicates, memory usage, numeric/categorical split) plus auto-generated Quick Insights.
- **Overview** — Full dataset preview, column-level details (dtype, null count, unique values).
- **Data Quality** — Missing value summary and percentage-by-column chart, nullity matrix and correlation heatmap (via `missingno`), duplicate row detection.
- **Visualizations** — Interactive histograms, correlation heatmaps, scatter plots (with color-by category), category bar charts, missing value donut chart, data type breakdown, and boxplots — all built with Plotly.
- **Correlation** — Dedicated full-width correlation heatmap with column selection.
- **Outliers** — IQR-based outlier detection with per-column bounds, counts, and row-level inspection.
- **Insights** — Automatically generated natural-language insights about your dataset.
- **Reports / Export** — Clean your dataset (remove duplicates, handle missing values via drop/mean/median) and download the result as CSV.
- **Dark / Light theme toggle** — Switch themes from the sidebar; persists during the session.
- **Fully functional sidebar navigation** — Real Streamlit sidebar with working page switching (not static HTML).

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Streamlit |
| Data handling | Pandas |
| Charts | Plotly Express |
| Missing data visuals | missingno + Matplotlib |
| Styling | Custom CSS (`assets/style.css`) injected via `st.markdown` |
| Icons | Inline Lucide-style SVGs (no emoji/external icon fonts) |

## Project Structure

```
nexalyze/
├── app.py                     # Main Streamlit app (UI, layout, navigation)
├── requirements.txt           # Python dependencies
├── assets/
│   └── style.css              # Custom dark/light theme styling
└── utils/
    ├── data_overview.py       # Basic dataset info, column type summaries
    ├── missing_values.py      # Missing value detection & summaries
    ├── duplicates.py          # Duplicate row detection
    ├── statistics.py          # Descriptive statistics, skewness interpretation
    ├── outliers.py            # IQR-based outlier detection
    ├── visualizations.py      # Plotly/Matplotlib chart builders
    ├── cleaning.py            # Dataset cleaning & CSV export utilities
    └── insights.py            # Auto-generated key insights
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kaurroopak/Nexalyze.git
   cd Nexalyze
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

5. Open the URL shown in your terminal (typically `http://localhost:8501`) and upload a CSV file to get started.

## Usage

1. Click **Upload Dataset** in the top-right of the hero section, or use the upload panel that appears on first load.
2. Drag and drop a `.csv` file or browse to select one.
3. Navigate between sections (Dashboard, Overview, Data Quality, Visualizations, Correlation, Outliers, Insights, Reports) using the sidebar.
4. On the **Reports** page, choose a duplicate/missing-value cleaning strategy and click **Download Cleaned CSV** to export your processed dataset.
5. Toggle **Dark Mode / Light Mode** from the sidebar footer at any time.

## Notes

- Only `.csv` files are supported in the current version.
- All business logic (missing values, duplicates, statistics, outliers, visualizations, insights, cleaning) lives in `utils/` and is UI-framework agnostic.
- The custom theme is fully contained in `assets/style.css` — modify CSS variables at the top of the file (`--bg`, `--accent`, `--accent-2`, etc.) to reskin the app without touching `app.py`.

## License

This project is provided as-is for personal and educational use.
