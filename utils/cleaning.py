import pandas as pd

from utils.duplicates import remove_duplicates
from utils.data_overview import get_numeric_columns, get_categorical_columns


def handle_missing_values(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    if strategy == "none":
        return df.copy()

    if strategy == "drop_rows":
        return df.dropna().reset_index(drop=True)

    cleaned_df = df.copy()

    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)

    for col in numeric_cols:
        if strategy == "fill_mean":
            fill_value = cleaned_df[col].mean()
        else:  # "fill_median"
            fill_value = cleaned_df[col].median()
        cleaned_df[col] = cleaned_df[col].fillna(fill_value)

    for col in categorical_cols:
        mode_values = cleaned_df[col].mode()
        if len(mode_values) > 0:
            cleaned_df[col] = cleaned_df[col].fillna(mode_values[0])

    return cleaned_df


def clean_dataset(
    df: pd.DataFrame,
    remove_duplicate_rows: bool,
    missing_value_strategy: str,
) -> pd.DataFrame:
    working_df = df.copy()

    if remove_duplicate_rows:
        working_df = remove_duplicates(working_df)

    working_df = handle_missing_values(working_df, missing_value_strategy)

    return working_df


def convert_df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")