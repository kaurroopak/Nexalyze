import pandas as pd

def get_basic_info(df: pd.DataFrame) -> dict:
    num_rows, num_cols = df.shape
    memory_bytes = df.memory_usage(deep=True).sum()
    memory_mb = float(memory_bytes / (1024 ** 2))
    duplicate_rows = int(df.duplicated().sum())

    return {
        "rows": num_rows,
        "columns": num_cols,
        "memory_usage_mb": round(memory_mb, 2),
        "duplicate_rows": duplicate_rows,
    }


def get_column_types_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame({
        "Column": df.columns,
        "Dtype": df.dtypes.astype(str).values,
        "Non-Null Count": df.notnull().sum().values,
        "Null Count": df.isnull().sum().values,
        "Unique Values": df.nunique().values,
    })
    return summary


def get_numeric_and_categorical_counts(df: pd.DataFrame) -> dict:
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)
    return {
        "numeric_count": len(numeric_cols),
        "categorical_count": len(categorical_cols),
    }


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["number"]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()