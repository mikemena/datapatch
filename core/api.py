import time
from typing import Dict, Any
import yaml
from pathlib import Path

class APIClient:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        config_path = Path("config/api_config.yaml")
        with open(config_path) as f:
            return yaml.safe_load(f)['apis']

    def call_api(self, patch_type: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """Mock API call that simulates network delay and returns fake response"""
        api_config = self.config.get(patch_type)
        if not api_config:
            raise ValueError(f"No API configuration found for {patch_type}")

        # Simulate API delay
        time.sleep(0.5)

        # Simulate API response
        if api_config['method'] == 'POST':
            return {
                "status": "success",
                "data": payload,
                "response_id": f"mock_{int(time.time())}",
                "message": f"Mock {patch_type} created successfully"
            }
        else:
            return {
                "status": "success",
                "data": {"id": "mock_id", "name": "Mock Data"},
                "message": f"Mock {patch_type} retrieved successfully"
            }
