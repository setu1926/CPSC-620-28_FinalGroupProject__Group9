
import pandas as pd
from src.data_loader import load_raw_rides


def test_load_raw_rides_returns_dataframe():
    df = load_raw_rides()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_raw_rides_has_expected_columns():
    df = load_raw_rides()
    cols = set(df.columns)

    expected = {
        "Trip Id",
        "Trip  Duration",
        "Start Time",
        "End Time",
        "Start Station Name",
        "End Station Name",
        "Bike Id",
    }

    # Just check that at least some of these exist
    assert {"Trip Id", "Start Time", "End Time"}.issubset(cols)