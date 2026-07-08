import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================================
# LUCIDE-STYLE SVG ICONS (inline, no emojis)
# =========================================================================

_ICON_PATHS = {
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "layout-dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "clipboard-list": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    "columns": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/><path d="M15 3v18"/>',
    "percent": '<line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "save": '<path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7"/><path d="M7 3v4a1 1 0 0 0 1 1h7"/>',
    "hash": '<line x1="4" x2="20" y1="9" y2="9"/><line x1="4" x2="20" y1="15" y2="15"/><line x1="10" x2="8" y1="3" y2="21"/><line x1="16" x2="14" y1="3" y2="21"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.46 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/>',
    "table": '<path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/>',
    "bar-chart-3": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "folder-open": '<path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>',
    "pie-chart": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="M3.27 6.96 12 12.01l8.73-5.05"/><path d="M12 22.08V12"/>',
    "siren": '<path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M21 12h1"/><path d="M18.5 4.5 18 5"/><path d="M2 12h1"/><path d="M12 2v1"/><path d="m4.929 4.929.707.707"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "git-compare-arrows": '<circle cx="5" cy="6" r="3"/><path d="M12 6h5a2 2 0 0 1 2 2v7"/><path d="m15 9-3-3 3-3"/><circle cx="19" cy="18" r="3"/><path d="M12 18H7a2 2 0 0 1-2-2V9"/><path d="m9 15 3 3-3 3"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
    "upload-cloud": '<path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m16 16-4-4-4 4"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "package-search": '<path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l.5-.29"/><path d="M16.5 9.4 7.55 4.24"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M20.27 17.27 22 19"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
}


def icon(name: str, size: int = 16, color: str = "currentColor") -> str:
    path = _ICON_PATHS.get(name, "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:-3px; margin-right:7px;">{path}</svg>'
    )


from utils.data_overview import (
    get_basic_info,
    get_column_types_summary,
    get_numeric_and_categorical_counts,
    get_numeric_columns,
    get_categorical_columns,
)
from utils.missing_values import (
    get_missing_value_summary,
    has_missing_values,
    get_rows_with_any_missing,
)
from utils.duplicates import (
    get_duplicate_count,
    get_duplicate_percentage,
    get_duplicate_rows,
    has_duplicates,
)
from utils.statistics import get_statistical_summary, interpret_skewness
from utils.visualizations import (
    build_histogram,
    build_boxplot,
    build_correlation_heatmap,
    build_scatter_plot,
    build_category_bar_chart,
    build_category_pie_chart,
    build_missingno_matrix,
    build_missingno_heatmap,
)
from utils.outliers import (
    get_iqr_bounds,
    get_outlier_rows,
    get_outlier_summary,
    get_total_outlier_row_count,
)
from utils.cleaning import clean_dataset, convert_df_to_csv_bytes
from utils.insights import generate_key_insights


# =========================================================================
# PAGE CONFIG + GLOBAL STYLING
# =========================================================================

def configure_page() -> None:
    st.set_page_config(
        page_title="Nexalyze | EDA Studio",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_css() -> None:
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

    if st.session_state.get("nx_theme", "dark") == "light":
        st.markdown(
            """
            <style>
            :root{
              --bg:#F4F6FB;
              --card:#FFFFFF;
              --card-2:#F0F2F8;
              --border:rgba(15,23,42,0.08);
              --text:#101827;
              --text-dim:#5B6474;
            }
            .stApp{
              background: radial-gradient(1200px 600px at 10% -10%, rgba(124,77,255,0.06), transparent),
                          radial-gradient(1000px 500px at 100% 0%, rgba(59,130,246,0.06), transparent),
                          var(--bg) !important;
              color: var(--text) !important;
            }
            section[data-testid="stSidebar"]{
              background: linear-gradient(180deg, #FFFFFF, #F4F6FB) !important;
              border-right: 1px solid var(--border) !important;
            }
            .nx-logo{ color:#101827 !important; }
            section[data-testid="stSidebar"] .stButton > button{
              color: var(--text-dim) !important;
            }
            section[data-testid="stSidebar"] .stButton > button:hover{
              color:#101827 !important;
              background: rgba(124,77,255,0.08) !important;
            }
            .nx-hero h1{ color:#101827 !important; }
            .nx-kpi, .nx-card, .nx-feature{
              background: var(--card) !important;
              border: 1px solid var(--border) !important;
              box-shadow: 0 6px 18px rgba(15,23,42,0.06) !important;
            }
            .nx-kpi-value, .nx-card-title, .nx-feature h4{ color:#101827 !important; }
            .nx-kpi-title, .nx-feature p, .stCaption, small{ color: var(--text-dim) !important; }
            label, .stMarkdown, p, span{ color: var(--text) !important; }
            div[data-testid="stMetric"]{
              background: var(--card) !important;
              border: 1px solid var(--border) !important;
            }
            div[data-testid="stFileUploaderDropzone"]{
              background: rgba(124,77,255,0.03) !important;
              border: 2px dashed rgba(124,77,255,0.35) !important;
            }
            div[data-testid="stDataFrame"]{ border: 1px solid var(--border) !important; }
            details{
              background: var(--card) !important;
              border: 1px solid var(--border) !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def style_plotly(fig, height: int = 380):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#101827",
        plot_bgcolor="#101827",
        font_color="#E6E9F0",
        font_family="Inter, Segoe UI, sans-serif",
        margin=dict(l=30, r=20, t=50, b=30),
        height=height,
        title_font_size=15,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
    return fig


def card_title(icon_name: str, text: str, size: int = 17) -> str:
    return f'<div class="nx-card-title">{icon(icon_name, size)}{text}</div>'


# =========================================================================
# SIDEBAR -- REAL st.sidebar, restyled, with WORKING navigation
# =========================================================================

NAV_ITEMS = [
    ("Dashboard", "layout-dashboard"),
    ("Overview", "search"),
    ("Data Quality", "shield-check"),
    ("Visualizations", "bar-chart-3"),
    ("Correlation", "git-compare-arrows"),
    ("Outliers", "alert-triangle"),
    ("Insights", "sparkles"),
    ("Reports", "file-text"),
]


def render_sidebar() -> str:
    if "nx_active_page" not in st.session_state:
        st.session_state.nx_active_page = "Dashboard"

    with st.sidebar:
        st.markdown(
            f'<div class="nx-logo">{icon("zap", 20)}<div>Nexalyze</div></div>',
            unsafe_allow_html=True,
        )

        for name, icon_name in NAV_ITEMS:
            is_active = st.session_state.nx_active_page == name
            wrapper_class = "nx-nav-active" if is_active else "nx-nav-inactive"
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            label = f'{icon(icon_name, 16)}{name}'
            if st.button(name, key=f"nav_{name}", use_container_width=True):
                st.session_state.nx_active_page = name
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="nx-sidebar-footer">', unsafe_allow_html=True)

        if "nx_theme" not in st.session_state:
            st.session_state.nx_theme = "dark"

        is_dark = st.session_state.nx_theme == "dark"
        toggle_label = "Dark Mode" if is_dark else "Light Mode"
        toggle_icon = "moon" if is_dark else "sun"

        st.markdown('<div class="nx-theme-toggle">', unsafe_allow_html=True)
        if st.button(f"{toggle_label}", key="theme_toggle_btn", use_container_width=True, icon=f":material/{'dark_mode' if is_dark else 'light_mode'}:"):
            st.session_state.nx_theme = "light" if is_dark else "dark"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div>v1.0.0 &middot; Nexalyze | EDA Studio</div></div>', unsafe_allow_html=True)

    return st.session_state.nx_active_page


# =========================================================================
# HERO (Upload / Download buttons styled identically)
# =========================================================================

def render_hero(df: pd.DataFrame | None) -> None:
    left, right = st.columns([3, 1.4])

    with left:
        st.markdown(
            f'<h1>Welcome to <span>Nexalyze</span> {icon("rocket", 26)}</h1>'
            '<p style="color:#8B93A7; margin-top:.4rem; font-size:.95rem;">'
            'Upload your dataset and uncover powerful insights in seconds.</p>',
            unsafe_allow_html=True,
        )

    with right:
        b1, b2 = st.columns(2)
        with b1:
            st.session_state.setdefault("nx_show_uploader", True)
            if st.button("Upload Dataset", use_container_width=True, key="hero_upload_btn", icon=":material/upload:"):
                st.session_state.nx_show_uploader = True
                st.rerun()
        with b2:
            if df is not None:
                csv_bytes = convert_df_to_csv_bytes(df)
                st.download_button(
                    "Download Report",
                    data=csv_bytes,
                    file_name="nexalyze_report.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="hero_download_btn",
                    icon=":material/download:",
                )
            else:
                st.button("Download Report", use_container_width=True, disabled=True, key="hero_download_disabled", icon=":material/download:")


# =========================================================================
# FILE LOADING (logic untouched)
# =========================================================================

def load_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Could not read this file. Error: {e}")
        return None


def render_upload_section():
    st.markdown(
        f'<div class="nx-card" style="text-align:center; padding: 1.4rem;">'
        f'<div class="nx-card-title" style="justify-content:center;">{icon("upload-cloud", 18)}Upload Your Dataset</div>'
        '<p style="color:#8B93A7; font-size:.85rem; margin-bottom: 0.6rem;">'
        'Drag and drop a CSV file, or click below to browse. Only .csv files are supported.'
        '</p></div>',
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        label="Upload your CSV file",
        type=["csv"],
        help="Only .csv files are supported in this version.",
        label_visibility="collapsed",
    )
    return uploaded_file


# =========================================================================
# KPI CARDS
# =========================================================================

def render_kpi_cards(df: pd.DataFrame) -> None:
    info = get_basic_info(df)
    type_counts = get_numeric_and_categorical_counts(df)
    missing_summary = get_missing_value_summary(df)
    overall_missing_pct = round(missing_summary["Missing Percentage"].mean(), 2) if len(missing_summary) else 0.0

    cards = [
        ("database", "nx-purple", "Total Rows", f"{info['rows']:,}"),
        ("columns", "nx-blue", "Total Columns", f"{info['columns']}"),
        ("percent", "nx-orange", "Missing Values", f"{overall_missing_pct}%"),
        ("copy", "nx-purple", "Duplicate Rows", f"{info['duplicate_rows']:,}"),
        ("save", "nx-blue", "Memory Usage", f"{info['memory_usage_mb']} MB"),
        ("hash", "nx-orange", "Numeric / Categorical", f"{type_counts['numeric_count']} / {type_counts['categorical_count']}"),
    ]

    cards_html = "".join(
        f'<div class="nx-kpi"><div class="nx-kpi-icon {accent_class}">{icon(icon_name, 20)}</div>'
        f'<div class="nx-kpi-title">{title}</div>'
        f'<div class="nx-kpi-value">{value}</div></div>'
        for icon_name, accent_class, title, value in cards
    )

    st.markdown(f'<div class="nx-kpi-grid">{cards_html}</div>', unsafe_allow_html=True)


# =========================================================================
# QUICK INSIGHTS
# =========================================================================

def render_key_insights_section(df: pd.DataFrame) -> None:
    insights = generate_key_insights(df)
    icons_cycle = ["database", "percent", "copy", "git-compare-arrows", "alert-triangle"]

    cards_html = "".join(
        f'<div class="nx-insight"><div class="nx-insight-badge">{icon(icons_cycle[i % len(icons_cycle)], 15)}</div>'
        f'<div>{insight}</div></div>'
        for i, insight in enumerate(insights)
    )

    st.markdown(
        f'<div class="nx-card">{card_title("sparkles", "Quick Insights")}'
        f'<div class="nx-insight-grid">{cards_html}</div></div>',
        unsafe_allow_html=True,
    )


# =========================================================================
# DATASET OVERVIEW
# =========================================================================

def render_dataset_overview(df: pd.DataFrame) -> None:
    st.markdown(f'<div class="nx-card">{card_title("search", "Dataset Preview")}', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card">{card_title("clipboard-list", "Column Details")}', unsafe_allow_html=True)
    st.dataframe(get_column_types_summary(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# MISSING VALUE ANALYSIS
# =========================================================================

def render_missing_value_analysis(df: pd.DataFrame) -> None:
    st.markdown(f'<div class="nx-card">{card_title("shield-check", "Missing Value Analysis")}', unsafe_allow_html=True)

    if not has_missing_values(df):
        st.success("No missing values found in this dataset.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    summary = get_missing_value_summary(df)
    rows_affected = get_rows_with_any_missing(df)

    col1, col2 = st.columns(2)
    col1.metric("Rows With Any Missing Value", f"{rows_affected:,}")
    col2.metric(
        "Rows With Any Missing Value (%)",
        f"{round((rows_affected / len(df)) * 100, 2)}%",
    )

    st.markdown("**Missing Values by Column**")
    st.dataframe(summary, use_container_width=True)

    chart_data = summary[summary["Missing Count"] > 0]

    fig = px.bar(
        chart_data,
        x="Column",
        y="Missing Percentage",
        text="Missing Percentage",
        title="Missing Value Percentage by Column",
        labels={"Missing Percentage": "% Missing"},
        color="Missing Percentage",
        color_continuous_scale="Reds",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(yaxis_range=[0, 100])
    fig = style_plotly(fig, height=360)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_missingno_section(df: pd.DataFrame) -> None:
    st.markdown(f'<div class="nx-card">{card_title("layers", "Missing Value Patterns")}', unsafe_allow_html=True)

    if not has_missing_values(df):
        st.success("No missing values to visualize.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown("**Nullity Matrix** -- white gaps show exactly where values are missing")
    matrix_fig = build_missingno_matrix(df)
    st.pyplot(matrix_fig)

    heatmap_fig = build_missingno_heatmap(df)
    if heatmap_fig is not None:
        st.markdown(
            "**Nullity Correlation Heatmap** -- do missing values in one "
            "column tend to occur alongside missing values in another?"
        )
        st.pyplot(heatmap_fig)
    else:
        st.caption(
            "Nullity correlation heatmap requires at least 2 columns "
            "with missing values."
        )
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# DUPLICATES
# =========================================================================

def render_duplicate_analysis(df: pd.DataFrame) -> None:
    st.markdown(f'<div class="nx-card">{card_title("copy", "Duplicate Detection")}', unsafe_allow_html=True)

    if not has_duplicates(df):
        st.success("No duplicate rows found in this dataset.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    count = get_duplicate_count(df)
    percentage = get_duplicate_percentage(df)

    col1, col2 = st.columns(2)
    col1.metric("Duplicate Rows", f"{count:,}")
    col2.metric("Duplicate Percentage", f"{percentage}%")

    with st.expander("View duplicate rows"):
        st.dataframe(get_duplicate_rows(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# STATISTICAL SUMMARY
# =========================================================================

def render_statistical_summary(df: pd.DataFrame) -> None:
    st.markdown(f'<div class="nx-card">{card_title("bar-chart-3", "Statistical Summary")}', unsafe_allow_html=True)

    numeric_cols = get_numeric_columns(df)
    if not numeric_cols:
        st.info("This dataset has no numeric columns to summarize.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    summary = get_statistical_summary(df)
    st.dataframe(summary, use_container_width=True)

    st.markdown("**Distribution Shape (Skewness Interpretation)**")
    interpretation_rows = [
        {"Column": col, "Skewness": summary.loc[col, "skewness"],
         "Interpretation": interpret_skewness(summary.loc[col, "skewness"])}
        for col in summary.index
    ]
    st.dataframe(pd.DataFrame(interpretation_rows), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# CHARTS GRID
# =========================================================================

def render_charts_grid(df: pd.DataFrame) -> None:
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)

    row1 = st.columns(3)

    with row1[0]:
        st.markdown(f'<div class="nx-card">{card_title("bar-chart-3", "Distribution")}', unsafe_allow_html=True)
        if numeric_cols:
            selected_col = st.selectbox("Column", options=numeric_cols, key="histogram_column_selector")
            fig = style_plotly(build_histogram(df, selected_col))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns to plot.")
        st.markdown('</div>', unsafe_allow_html=True)

    with row1[1]:
        st.markdown(f'<div class="nx-card">{card_title("flame", "Correlation Heatmap")}', unsafe_allow_html=True)
        if len(numeric_cols) >= 2:
            selected_cols = st.multiselect(
                "Columns", options=numeric_cols, default=numeric_cols, key="correlation_columns_selector"
            )
            fig = build_correlation_heatmap(df, selected_cols)
            if fig is not None:
                fig = style_plotly(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Select at least 2 columns.")
        else:
            st.info("Need at least 2 numeric columns.")
        st.markdown('</div>', unsafe_allow_html=True)

    with row1[2]:
        st.markdown(f'<div class="nx-card">{card_title("target", "Scatter Plot")}', unsafe_allow_html=True)
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X-axis", options=numeric_cols, key="scatter_x_selector")
            default_y_index = 1 if len(numeric_cols) > 1 else 0
            y_col = st.selectbox("Y-axis", options=numeric_cols, index=default_y_index, key="scatter_y_selector")
            color_col = st.selectbox("Color by", options=["None"] + categorical_cols, key="scatter_color_selector")
            color_col = None if color_col == "None" else color_col
            fig = style_plotly(build_scatter_plot(df, x_col, y_col, color_col))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns.")
        st.markdown('</div>', unsafe_allow_html=True)

    row2 = st.columns(3)

    with row2[0]:
        st.markdown(f'<div class="nx-card">{card_title("folder-open", "Top Categories")}', unsafe_allow_html=True)
        if categorical_cols:
            selected_col = st.selectbox("Column", options=categorical_cols, key="categorical_column_selector")
            unique_count = df[selected_col].nunique()
            if unique_count > 50:
                st.caption(f"{unique_count} unique values -- showing top 10.")
            fig = style_plotly(build_category_bar_chart(df, selected_col))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns to analyze.")
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        st.markdown(f'<div class="nx-card">{card_title("pie-chart", "Missing Values")}', unsafe_allow_html=True)
        missing_summary = get_missing_value_summary(df)
        total_missing = int(missing_summary["Missing Count"].sum())
        total_cells = df.shape[0] * df.shape[1]
        donut_df = pd.DataFrame({
            "Status": ["Missing", "No Missing"],
            "Count": [total_missing, max(total_cells - total_missing, 0)],
        })
        fig = px.pie(donut_df, names="Status", values="Count", hole=0.65,
                     color="Status", color_discrete_map={"Missing": "#F43F5E", "No Missing": "#3B82F6"})
        fig.update_traces(textinfo="percent", textfont_size=12)
        fig = style_plotly(fig, height=320)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[2]:
        st.markdown(f'<div class="nx-card">{card_title("layers", "Data Types")}', unsafe_allow_html=True)
        type_counts = get_numeric_and_categorical_counts(df)
        dtype_df = pd.DataFrame({
            "Type": ["Numeric", "Categorical"],
            "Count": [type_counts["numeric_count"], type_counts["categorical_count"]],
        })
        fig = px.pie(dtype_df, names="Type", values="Count", hole=0.65,
                     color_discrete_sequence=["#7C4DFF", "#3B82F6"])
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        fig = style_plotly(fig, height=320)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card">{card_title("box", "Boxplot")}', unsafe_allow_html=True)
    if numeric_cols:
        selected_col = st.selectbox("Column", options=numeric_cols, key="boxplot_column_selector")
        fig = style_plotly(build_boxplot(df, selected_col))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No numeric columns to plot.")
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# OUTLIERS
# =========================================================================

def render_outlier_detection_section(df: pd.DataFrame) -> None:
    st.markdown(f'<div class="nx-card">{card_title("siren", "Outlier Detection (IQR Method)")}', unsafe_allow_html=True)

    numeric_cols = get_numeric_columns(df)
    if not numeric_cols:
        st.info("This dataset has no numeric columns to check for outliers.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    summary = get_outlier_summary(df)
    total_affected_rows = get_total_outlier_row_count(df)

    col1, col2 = st.columns(2)
    col1.metric("Rows With Any Outlier", f"{total_affected_rows:,}")
    col2.metric(
        "Rows With Any Outlier (%)",
        f"{round((total_affected_rows / len(df)) * 100, 2)}%" if len(df) > 0 else "0%",
    )

    st.markdown("**Outlier Summary by Column**")
    st.dataframe(summary, use_container_width=True)

    st.markdown("**Inspect Outlier Rows for a Specific Column**")
    selected_col = st.selectbox("Column", options=numeric_cols, key="outlier_column_selector")

    outlier_rows = get_outlier_rows(df, selected_col)
    lower_bound, upper_bound = get_iqr_bounds(df, selected_col)

    st.caption(
        f"Values outside [{round(lower_bound, 2)}, {round(upper_bound, 2)}] "
        f"are considered outliers for '{selected_col}'."
    )

    with st.expander(f"View {len(outlier_rows)} outlier rows for '{selected_col}'"):
        st.dataframe(outlier_rows, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# DOWNLOAD / EXPORT (Reports page)
# =========================================================================

def render_download_clean_dataset_section(df: pd.DataFrame) -> None:
    st.markdown(f'<div class="nx-card">{card_title("save", "Download Clean Dataset")}', unsafe_allow_html=True)

    remove_dupes = st.checkbox("Remove duplicate rows", value=True, key="clean_remove_duplicates_checkbox")

    missing_strategy_label = st.radio(
        "Missing value strategy",
        options=[
            "Do nothing",
            "Drop rows with missing values",
            "Fill with mean (numeric) / mode (categorical)",
            "Fill with median (numeric) / mode (categorical)",
        ],
        key="clean_missing_strategy_radio",
    )

    strategy_map = {
        "Do nothing": "none",
        "Drop rows with missing values": "drop_rows",
        "Fill with mean (numeric) / mode (categorical)": "fill_mean",
        "Fill with median (numeric) / mode (categorical)": "fill_median",
    }
    missing_strategy = strategy_map[missing_strategy_label]

    cleaned_df = clean_dataset(df, remove_dupes, missing_strategy)

    col1, col2 = st.columns(2)
    col1.metric("Rows Before", f"{len(df):,}")
    col2.metric("Rows After", f"{len(cleaned_df):,}", delta=f"{len(cleaned_df) - len(df):,}")

    st.markdown("**Preview of Cleaned Dataset**")
    st.dataframe(cleaned_df.head(10), use_container_width=True)

    csv_bytes = convert_df_to_csv_bytes(cleaned_df)

    st.download_button(
        label="Download Cleaned CSV",
        data=csv_bytes,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        key="download_clean_dataset_button",
        icon=":material/download:",
    )
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# ADVANCED FEATURES ROW
# =========================================================================

def render_advanced_features() -> None:
    features = [
        ("file-text", "Automatic Report", "Generate a comprehensive EDA report"),
        ("shield-check", "Missing Analysis", "Visualize missing data patterns"),
        ("flame", "Correlation", "Discover feature relationships"),
        ("alert-triangle", "Outlier Detection", "Detect anomalies automatically (IQR)"),
        ("download", "Download CSV", "Export your cleaned dataset"),
    ]
    cards_html = "".join(
        f'<div class="nx-feature"><div class="nx-feature-icon">{icon(icon_name, 18)}</div>'
        f'<h4>{title}</h4><p>{desc}</p></div>'
        for icon_name, title, desc in features
    )
    st.markdown(
        f'<div class="nx-card">{card_title("zap", "Advanced Features")}'
        f'<div class="nx-feature-grid">{cards_html}</div></div>',
        unsafe_allow_html=True,
    )


# =========================================================================
# MAIN
# =========================================================================

def main() -> None:
    configure_page()
    inject_css()

    active_page = render_sidebar()

    df = st.session_state.get("nx_df", None)

    render_hero(df)

    if df is None or st.session_state.get("nx_show_uploader", True):
        uploaded_file = render_upload_section()
        new_df = load_uploaded_file(uploaded_file)
        if new_df is not None:
            st.session_state.nx_df = new_df
            st.session_state.nx_show_uploader = False
            df = new_df
            st.rerun()

    if df is None:
        st.info("Upload a CSV file to get started.")
        return

    st.success(f"File loaded successfully! Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    if active_page == "Dashboard":
        render_kpi_cards(df)
        render_key_insights_section(df)
        render_charts_grid(df)
        render_advanced_features()

    elif active_page == "Overview":
        render_kpi_cards(df)
        render_dataset_overview(df)
        render_statistical_summary(df)

    elif active_page == "Data Quality":
        render_missing_value_analysis(df)
        render_missingno_section(df)
        render_duplicate_analysis(df)

    elif active_page == "Visualizations":
        render_charts_grid(df)

    elif active_page == "Correlation":
        numeric_cols = get_numeric_columns(df)
        if len(numeric_cols) >= 2:
            st.markdown(f'<div class="nx-card">{card_title("flame", "Correlation Heatmap")}', unsafe_allow_html=True)
            selected_cols = st.multiselect(
                "Select numeric columns to include",
                options=numeric_cols,
                default=numeric_cols,
                key="corr_page_columns_selector",
            )
            fig = build_correlation_heatmap(df, selected_cols)
            if fig is not None:
                fig = style_plotly(fig, height=480)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Select at least 2 columns to see the correlation heatmap.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Need at least 2 numeric columns to compute correlations.")

    elif active_page == "Outliers":
        render_outlier_detection_section(df)

    elif active_page == "Insights":
        render_key_insights_section(df)

    elif active_page == "Reports":
        render_download_clean_dataset_section(df)
        render_advanced_features()


if __name__ == "__main__":
    main()
