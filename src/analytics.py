import pandas as pd


def compute_summary(df: pd.DataFrame) -> dict:
    """
    Compute basic summary metrics from the cleaned rides data.
    Returns a dictionary with total trips, avg duration, and user type counts.
    """
    total_trips = len(df)
    avg_duration = df["Duration (min)"].mean()

    user_type_counts: dict[str, int] = {}
    if "User Type" in df.columns:
        user_type_counts = df["User Type"].value_counts().to_dict()

    return {
        "total_trips": int(total_trips),
        "avg_duration_min": round(float(avg_duration), 2),
        "user_type_counts": user_type_counts,
    }


def trips_by_hour(df: pd.DataFrame) -> pd.Series:
    """
    Group trips by hour of day using the Start Time column.
    Returns a Series indexed by hour (0–23).
    """
    if not pd.api.types.is_datetime64_any_dtype(df["Start Time"]):
        df = df.copy()
        df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce")

    series = df.groupby(df["Start Time"].dt.hour).size()
    series = series.sort_index()
    return series


def top_start_stations(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Return top N most used start stations."""
    return df["Start Station Name"].value_counts().head(n)


def top_end_stations(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Return top N most used end stations."""
    return df["End Station Name"].value_counts().head(n)


def busiest_date(df: pd.DataFrame) -> tuple[pd.Timestamp, int]:
    """
    Return the calendar date with the highest number of trips
    and the corresponding trip count.
    """
    if not pd.api.types.is_datetime64_any_dtype(df["Start Time"]):
        df = df.copy()
        df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce")

    by_date = df.groupby(df["Start Time"].dt.date).size()
    busiest_day = by_date.idxmax()
    max_trips = int(by_date.max())

    return pd.Timestamp(busiest_day), max_trips