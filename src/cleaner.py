
import pandas as pd


def clean_rides(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw bike share dataset.

    - Convert Start/End Time to datetime
    - Create 'Duration (min)' column
    - Drop rows with missing or invalid times/durations
    """

    df = df.copy()

    # Convert time columns
    df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce")
    df["End Time"] = pd.to_datetime(df["End Time"], errors="coerce")

    # Drop invalid times
    df = df.dropna(subset=["Start Time", "End Time"])

    # Duration column
    if "Trip  Duration" in df.columns:
        df["Duration (min)"] = df["Trip  Duration"] / 60
    else:
        df["Duration (min)"] = (
            df["End Time"] - df["Start Time"]
        ).dt.total_seconds() / 60

    # Drop non-positive or crazy durations
    df = df[df["Duration (min)"] > 0]
    df = df[df["Duration (min)"] < 240]  # cap at 4 hours to remove outliers

    return df