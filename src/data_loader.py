from pathlib import Path
import pandas as pd

# Adjust this if your CSV name changes
DATA_FILE_NAME = "Bike share ridership 2024-08 (3).csv"

# src/data/Bike share ridership 2024-08 (3).csv
DATA_PATH = Path(__file__).parent / "data" / DATA_FILE_NAME


def load_raw_rides() -> pd.DataFrame:
    """
    Load the raw Bike Share Toronto ridership CSV as a DataFrame.

    Raises:
        FileNotFoundError: if the CSV is not found at the expected path.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found at: {DATA_PATH}. "
            "Make sure the file is inside src/data."
        )

    df = pd.read_csv(DATA_PATH)
    return df