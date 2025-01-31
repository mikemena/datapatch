from pathlib import Path
import inquirer
from core.excel import read_excel, save_results
from patches.base_patch import BasePatch
from core.api import APIClient
import yaml
from typing import Dict, Type
import importlib
import pkgutil
import patches

def load_patch_types() -> Dict[str, Type[BasePatch]]:
    """Dynamically load all patch types from patches directory"""
    patch_types = {}
    patches_dir = Path(__file__).parent / "patches"

    for _, name, _ in pkgutil.iter_modules([str(patches_dir)]):
        if name != "base_patch":
            module = importlib.import_module(f"patches.{name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                try:
                    if (
                        isinstance(attr, type) # Check if class
                        and issubclass(attr, BasePatch) # Check if subclass
                        and attr != BasePatch # Exclude base class
                    ):
                        patch = attr("")  # Temporary instance to get type
                        patch_types[patch.patch_type] = attr
                except TypeError:
                    continue
    return patch_types

def main():
    try:
        # Ensure directories exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # Get available patch types
        patch_types = load_patch_types()

        # Get excel files in data directory
        excel_files = list(data_dir.glob("*.xlsx"))

        if not excel_files:
            print("No Excel files found in data directory!")
            return

        # Prompt user for inputs
        questions = [
            inquirer.List('patch_type',
                         message="Select the type of data patch",
                         choices=list(patch_types.keys())),
            inquirer.List('excel_file',
                         message="Select the Excel file to process",
                         choices=[f.name for f in excel_files])
        ]

        answers = inquirer.prompt(questions)

        if not answers:
            print("Operation cancelled")
            return

        # Initialize selected patch
        selected_file = data_dir / answers['excel_file']
        patch_class = patch_types[answers['patch_type']]
        patch = patch_class(str(selected_file))

        # Initialize API client
        api_client = APIClient()

        # Read the Excel file
        df = read_excel(str(selected_file))
        print(f"Processing {len(df)} rows from {selected_file}")

# Process each row and call API
        for index, row in df.iterrows():
            try:
                # Generate payload
                payload = patch.generate_payload(row)
                print(f"Generated payload for row {index + 1}: {payload}")

                # Call API
                response = api_client.call_api(answers['patch_type'], payload=payload)

                # Update tracking columns
                df.at[index, 'api_response'] = str(response)
                df.at[index, 'api_status'] = response.get('status', 'unknown')
                df.at[index, 'error_details'] = None

            except Exception as e:
                print(f"Error processing row {index + 1}: {str(e)}")
                df.at[index, 'api_status'] = 'error'
                df.at[index, 'error_details'] = str(e)

        # Save updated Excel file
        save_results(df, selected_file)
        print("Processing completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()