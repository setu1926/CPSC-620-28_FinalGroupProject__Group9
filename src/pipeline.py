from src.data_loader import load_raw_rides
from src.cleaner import clean_rides


def get_clean_data():
    """
    Load the raw ridership data and return a cleaned DataFrame.

    This function is used by both the dashboard and tests so that
    we have a single, reusable data pipeline entry-point.
    """
    raw = load_raw_rides()
    cleaned = clean_rides(raw)
    return cleaned
