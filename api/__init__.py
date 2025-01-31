from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class BasePatch(ABC):
    """Base class for all data patches"""

    def __init__(self, excel_file: str):
        self.excel_file = excel_file

    @property
    @abstractmethod
    def patch_type(self) -> str:
        """Return the type of patch"""
        pass

    @abstractmethod
    def generate_payload(self, row: pd.Series) -> Dict[str, Any]:
        """Generate API payload from a row of data"""
        pass