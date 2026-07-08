import pandas as pd

from utils.data_overview import (
    get_basic_info,
    get_numeric_columns,
    get_categorical_columns,
)
from utils.missing_values import has_missing_values, get_most_missing_column
from utils.duplicates import get_duplicate_count, get_duplicate_percentage
from utils.outliers import get_total_outlier_row_count


def get_highest_correlation_pair(df: pd.DataFrame) -> tuple[str, str, float] | None:
    numeric_cols = get_numeric_columns(df)

    if len(numeric_cols) < 2:
        return None

    corr_matrix = df[numeric_cols].corr().abs()

    for col in corr_matrix.columns:
        corr_matrix.loc[col, col] = 0

    stacked = corr_matrix.stack()

    if stacked.empty or stacked.max() == 0:
        return None

    col_1, col_2 = stacked.idxmax()
    correlation_value = float(corr_matrix.loc[col_1, col_2])

    return (col_1, col_2, round(correlation_value, 2))


def generate_key_insights(df: pd.DataFrame) -> list[str]:
    insights: list[str] = []

    info = get_basic_info(df)
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)

    # --- Basic shape insight ---
    insights.append(
        f"The dataset has **{info['rows']:,} rows** and **{info['columns']} columns** "
        f"({len(numeric_cols)} numeric, {len(categorical_cols)} categorical)."
    )

    # --- Missing values insight ---
    if has_missing_values(df):
        col_name, pct = get_most_missing_column(df)
        insights.append(
            f"The column with the most missing data is **'{col_name}'** "
            f"at **{pct}%** missing."
        )
    else:
        insights.append("No missing values were found in this dataset.")

    # --- Duplicates insight ---
    duplicate_count = get_duplicate_count(df)
    if duplicate_count > 0:
        duplicate_pct = get_duplicate_percentage(df)
        insights.append(
            f"There are **{duplicate_count:,} duplicate rows** "
            f"({duplicate_pct}% of the dataset)."
        )
    else:
        insights.append("No duplicate rows were found in this dataset.")

    # --- Correlation insight ---
    top_corr = get_highest_correlation_pair(df)
    if top_corr is not None:
        col_1, col_2, corr_value = top_corr
        direction = "positive" if corr_value > 0 else "negative"
        insights.append(
            f"The strongest correlation is between **'{col_1}'** and "
            f"**'{col_2}'** ({direction}, r = {corr_value})."
        )

    # --- Outliers insight ---
    if numeric_cols:
        total_outlier_rows = get_total_outlier_row_count(df)
        if total_outlier_rows > 0:
            outlier_pct = round((total_outlier_rows / len(df)) * 100, 2) if len(df) > 0 else 0.0
            insights.append(
                f"**{total_outlier_rows:,} rows** ({outlier_pct}%) contain at "
                "least one outlier value (IQR method)."
            )
        else:
            insights.append("No outliers were detected in any numeric column.")

    return insights