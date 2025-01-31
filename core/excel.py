import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Union

def read_excel(filepath: Union[str, Path]) -> pd.DataFrame:
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

def save_results(df: pd.DataFrame, original_path: Union[str, Path]):
    """Save a DataFrame to an Excel file."""

    # Generate timestamp
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')

    # Create a new file name with timestamp
    output_path = original_path.parent / f"{original_path.stem}_{timestamp}_results{original_path.suffix}"

    # Save to excel
    df.to_excel(output_path, index=False)

    return output_path