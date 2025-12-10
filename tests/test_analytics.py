import pandas as pd

from src.pipeline import get_clean_data
from src.analytics import (
    compute_summary,
    trips_by_hour,
    top_start_stations,
    top_end_stations,
    busiest_date,
)


def _get_clean_data() -> pd.DataFrame:
    return get_clean_data()


def test_compute_summary_has_basic_keys():
    df = _get_clean_data()
    summary = compute_summary(df)

    assert "total_trips" in summary
    assert "avg_duration_min" in summary
    assert isinstance(summary["total_trips"], int)
    assert summary["total_trips"] > 0
    assert summary["avg_duration_min"] > 0


def test_trips_by_hour_index_range_and_counts():
    df = _get_clean_data()
    by_hour = trips_by_hour(df)

    assert by_hour.index.min() >= 0
    assert by_hour.index.max() <= 23
    assert by_hour.sum() == len(df)


def test_top_start_stations_returns_series():
    df = _get_clean_data()
    series = top_start_stations(df, n=5)

    assert isinstance(series, pd.Series)
    assert 1 <= len(series) <= 5


def test_top_end_stations_returns_series():
    df = _get_clean_data()
    series = top_end_stations(df, n=5)

    assert isinstance(series, pd.Series)
    assert 1 <= len(series) <= 5


def test_busiest_date_matches_manual_groupby():
    df = _get_clean_data()

    day_func, count_func = busiest_date(df)

    grouped = df.groupby(df["Start Time"].dt.date).size()
    busiest_manual_day = grouped.idxmax()
    busiest_manual_count = int(grouped.max())

    assert pd.Timestamp(busiest_manual_day) == day_func
    assert busiest_manual_count == count_func