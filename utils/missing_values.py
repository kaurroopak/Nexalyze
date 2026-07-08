import pandas as pd

def get_missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100

    summary = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing_count.values,
        "Missing Percentage": missing_percent.round(2).values,
    })

    summary = summary.sort_values(
        by="Missing Percentage", ascending=False
    ).reset_index(drop=True)

    return summary


def has_missing_values(df: pd.DataFrame) -> bool:
    return bool(df.isnull().values.any())


def get_most_missing_column(df: pd.DataFrame) -> tuple[str, float] | None:
    if not has_missing_values(df):
        return None

    summary = get_missing_value_summary(df)
    top_row = summary.iloc[0]
    return (str(top_row["Column"]), float(top_row["Missing Percentage"]))


def get_rows_with_any_missing(df: pd.DataFrame) -> int:
    return int(df.isnull().any(axis=1).sum())