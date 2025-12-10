import pandas as pd
from src.data_loader import load_raw_rides
from src.cleaner import clean_rides


def _get_clean_data() -> pd.DataFrame:
    raw = load_raw_rides()
    return clean_rides(raw)


def test_cleaner_converts_times_to_datetime():
    df = _get_clean_data()
    assert str(df["Start Time"].dtype).startswith("datetime64")
    assert str(df["End Time"].dtype).startswith("datetime64")


def test_cleaner_creates_duration_column():
    df = _get_clean_data()
    assert "Duration (min)" in df.columns
    assert df["Duration (min)"].min() > 0