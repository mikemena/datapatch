# core/excel.py
import pandas as pd
from datetime import datetime

def read_excel(filepath: str) -> pd.DataFrame:
    """
    Reads an Excel file and adds tracking columns for API responses.

    Args:
        filepath (str): Path to the Excel file

    Returns:
        pd.DataFrame: DataFrame with added tracking columns
    """
    # Read the Excel file
    df = pd.read_excel(filepath)

    tracking_columns = [
        'api_response',
        'api_status',
        'error_details',
        'process_date'
    ]

    for col in tracking_columns:
        if col not in df.columns:
            df[col] = None

    return df

def save_results(df: pd.DataFrame, original_path: str):
    """Save a DataFrame to an Excel file."""

    # Generate timestamp
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')

    # Create a new file name with timestamp
    output_path = f"{original_path.rsplit('.', 1)[0]}_{timestamp}_results.xlsx"

    # Save to excel
    df.to_excel(output_path, index=False)