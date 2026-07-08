import pandas as pd

from utils.data_overview import get_numeric_columns


def get_iqr_bounds(df: pd.DataFrame, column: str) -> tuple[float, float]:
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return float(lower_bound), float(upper_bound)


def get_outlier_rows(df: pd.DataFrame, column: str) -> pd.DataFrame:
    lower_bound, upper_bound = get_iqr_bounds(df, column)
    mask = (df[column] < lower_bound) | (df[column] > upper_bound)

    return df[mask]


def get_outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = get_numeric_columns(df)

    if not numeric_cols:
        return pd.DataFrame()

    rows = []
    for col in numeric_cols:
        lower_bound, upper_bound = get_iqr_bounds(df, col)
        outlier_count = len(get_outlier_rows(df, col))
        outlier_percentage = round((outlier_count / len(df)) * 100, 2) if len(df) > 0 else 0.0

        rows.append({
            "Column": col,
            "Lower Bound": round(lower_bound, 2),
            "Upper Bound": round(upper_bound, 2),
            "Outlier Count": outlier_count,
            "Outlier Percentage": outlier_percentage,
        })

    summary = pd.DataFrame(rows).sort_values(
        by="Outlier Percentage", ascending=False
    ).reset_index(drop=True)

    return summary


def get_total_outlier_row_count(df: pd.DataFrame) -> int:
    numeric_cols = get_numeric_columns(df)

    if not numeric_cols:
        return 0

    combined_mask = pd.Series(False, index=df.index)

    for col in numeric_cols:
        lower_bound, upper_bound = get_iqr_bounds(df, col)
        col_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        combined_mask = combined_mask | col_mask

    return int(combined_mask.sum())