import os
import json

# Directory containing the PDF JSON files
pdf_json_directory = "pdf_json_files"

# Iterate through the JSON files in the directory
for json_filename in os.listdir(pdf_json_directory):
    if json_filename.startswith("._"):
        continue
    if json_filename.endswith(".json"):
        print(f"Processing JSON file: {json_filename}")
        
        # Load the JSON data from the JSON file
        json_file_path = os.path.join(pdf_json_directory, json_filename)
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)

        # Create a list to store the dataset information
        dataset_info = []

        # Create a separate list for datasets with additional information
        additional_datasets = []

        # Iterate through the datasets in the JSON data
        for dataset in json_data["datasets"]:
            dataset_name = dataset[0] if isinstance(dataset, list) else dataset  # Use the first element if it's a list
            print(f"Processing dataset: {dataset_name}")

            # Convert dataset_name to a string
            dataset_name_str = str(dataset_name)

            # Find matching dataset JSON file by partial match
            matching_files = []
            for root, _, files in os.walk("PROD_20230409"):
                matching_files.extend([f for f in files if f.startswith(dataset_name_str)])

            if len(matching_files) == 1:
                dataset_filename = matching_files[0]
                dataset_path = os.path.join("PROD_20230409", dataset_filename)

                # Open the dataset file and load data
                with open(dataset_path, "r") as dataset_file:
                    dataset_data = json.load(dataset_file)

                # Try to get vl1 and vl2 from the dataset JSON, set to "N/A" if not found
                try:
                    vl1 = dataset_data["ScienceKeywords"][0]["VariableLevel1"]
                except KeyError:
                    vl1 = "N/A"
                
                try:
                    vl2 = dataset_data["ScienceKeywords"][0]["VariableLevel2"]
                except KeyError:
                    vl2 = "N/A"

                # Check if the dataset has additional information
                if len(dataset) > 2:
                    additional_info = {
                        "globalId": dataset_name_str,
                        "doi": dataset_data["DOI"],
                        "shortName": dataset_data["ShortName"],
                        "longName": dataset_data["CollectionCitations"][0]["Title"],
                        "abstract": dataset_data["Abstract"].replace("\n", ""),
                        "vl1": vl1,
                        "vl2": vl2
                    }
                    additional_datasets.append(additional_info)
                else:
                    # Add the dataset information to the list
                    dataset_info.append({
                        "globalId": dataset_name_str,
                        "doi": dataset_data["DOI"],
                        "shortName": dataset_data["ShortName"],
                        "longName": dataset_data["CollectionCitations"][0]["Title"],
                        "abstract": dataset_data["Abstract"].replace("\n", ""),
                        "vl1": vl1,
                        "vl2": vl2
                    })

        # Extend the original dataset_info list with additional_datasets
        dataset_info.extend(additional_datasets)

        # Update the JSON data with the dataset information
        json_data["datasets"] = dataset_info

        # Save the updated JSON file
        with open(json_file_path, "w") as updated_json_file:
            json.dump(json_data, updated_json_file, indent=4)
            print(f"Updated JSON file: {json_filename}")

