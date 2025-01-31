from .base_patch import BasePatch
import pandas as pd
from typing import Dict, Any

class ProviderCategoryPatch(BasePatch):
    """Example patch for customer data"""

    @property
    def patch_type(self) -> str:
        return "provider_category"

    def generate_payload(self, row: pd.Series) -> Dict[str, Any]:
        # Example payload generation
        return {
            "providerId": row.get("providerId"),
            "fbNumber": row.get("fbNumber"),
            "categoryCode": row.get("categoryCode"),
            "newCategoryCode": row.get("newCategoryCode")
        }