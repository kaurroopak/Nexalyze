import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import missingno as msno
import matplotlib.pyplot as plt
import matplotlib.figure


def build_histogram(df: pd.DataFrame, column: str, bins: int = 30) -> go.Figure:
    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        marginal="box",  
        title=f"Distribution of {column}",
        color_discrete_sequence=["#6366F1"],  
    )

    fig.update_layout(
        bargap=0.05,
        xaxis_title=column,
        yaxis_title="Frequency",
    )

    return fig


def build_boxplot(df: pd.DataFrame, column: str) -> go.Figure:
    fig = px.box(
        df,
        y=column,
        points="outliers",
        title=f"Boxplot of {column}",
        color_discrete_sequence=["#22C55E"],  
    )

    return fig

def build_correlation_heatmap(df: pd.DataFrame, numeric_cols: list[str]) -> go.Figure | None:
    if len(numeric_cols) < 2:
        return None

    corr_matrix = df[numeric_cols].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",  # shows each correlation value rounded to 2 decimals, inside its cell
        color_continuous_scale="RdBu_r",  # red = negative, blue = positive, diverging around 0
        zmin=-1,
        zmax=1,  
        title="Correlation Heatmap",
        aspect="auto", 
    )

    return fig

def build_scatter_plot( df: pd.DataFrame, x_column: str, y_column: str, color_column: str | None = None,) -> go.Figure:
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        color=color_column,  
        trendline="ols",
        title=f"{y_column} vs {x_column}",
        opacity=0.7,  
    )

    return fig

def build_category_bar_chart(df: pd.DataFrame, column: str, top_n: int = 10) -> go.Figure:
    value_counts = df[column].value_counts().head(top_n)

    fig = px.bar(
        x=value_counts.values,
        y=value_counts.index.astype(str),  
        orientation="h",
        title=f"Top {top_n} Categories in {column}",
        labels={"x": "Count", "y": column},
        color=value_counts.values,
        color_continuous_scale="Blues",
        text=value_counts.values,  # shows the count on each bar
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.update_traces(textposition="outside")

    return fig


def build_category_pie_chart(df: pd.DataFrame, column: str, top_n: int = 10) -> go.Figure:
    value_counts = df[column].value_counts()
    top_counts = value_counts.head(top_n)

    remaining_count = value_counts.iloc[top_n:].sum()

    labels = top_counts.index.astype(str).tolist()
    values = top_counts.values.tolist()

    if remaining_count > 0:
        labels.append("Other")
        values.append(remaining_count)

    fig = px.pie(
        names=labels,
        values=values,
        title=f"Category Distribution: {column}",
        hole=0.3,  
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


def build_missingno_matrix(df: pd.DataFrame) -> matplotlib.figure.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))

    msno.matrix(df, ax=ax, sparkline=False)

    fig.tight_layout()

    return fig


def build_missingno_heatmap(df: pd.DataFrame) -> matplotlib.figure.Figure | None:

    cols_with_missing = df.columns[df.isnull().any()].tolist()

    if len(cols_with_missing) < 2:
        return None

    fig, ax = plt.subplots(figsize=(8, 6))
    msno.heatmap(df[cols_with_missing], ax=ax)
    fig.tight_layout()

    return fig