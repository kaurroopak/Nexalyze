import pandas as pd
from scipy import stats

from utils.data_overview import get_numeric_columns


def get_statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = get_numeric_columns(df)

    if not numeric_cols:
        return pd.DataFrame()

    numeric_df = df[numeric_cols]

    summary = numeric_df.describe().T

    summary["skewness"] = numeric_df.apply(
        lambda col: stats.skew(col, nan_policy="omit")
    )
    summary["kurtosis"] = numeric_df.apply(
        lambda col: stats.kurtosis(col, nan_policy="omit")
    )

    return summary.round(2)


def interpret_skewness(skew_value: float) -> str:
    """
    Converts a raw skewness number into a plain-English label.

    Thresholds used here follow a common rule of thumb:
    |skew| < 0.5           -> approximately symmetric
    0.5 <= |skew| < 1       -> moderately skewed
    |skew| >= 1             -> highly skewed
    """
    if skew_value > 1:
        return "Highly right-skewed"
    elif skew_value > 0.5:
        return "Moderately right-skewed"
    elif skew_value < -1:
        return "Highly left-skewed"
    elif skew_value < -0.5:
        return "Moderately left-skewed"
    else:
        return "Approximately symmetric"