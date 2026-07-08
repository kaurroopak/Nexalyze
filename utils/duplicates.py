import pandas as pd

def get_duplicate_count(df: pd.DataFrame) -> int:
    return int(df.duplicated(keep="first").sum())


def get_duplicate_percentage(df: pd.DataFrame) -> float:
    if len(df) == 0:
        return 0.0
    count = get_duplicate_count(df)
    return round((count / len(df)) * 100, 2)


def get_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.duplicated(keep=False)].sort_values(by=list(df.columns))


def has_duplicates(df: pd.DataFrame) -> bool:
    return get_duplicate_count(df) > 0


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(keep="first").reset_index(drop=True)