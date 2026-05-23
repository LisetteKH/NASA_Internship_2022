import os
import weaviate
from weaviate.batch import Batch
from weaviate.util import generate_uuid5
import json

weaviate_url = "http://localhost:8080"
client = weaviate.Client(weaviate_url)
client.is_ready()

uuid_counter = 1

# Directory path containing JSON files
json_folder = "/Volumes/Passport/mac_desktop /Senior_Project/pdf_json_files"  # Replace with the path to your JSON folder

# Define a function to add PDF objects
def add_pdf(batch: Batch, pdf_data: dict, pdf_id) -> str:
    if pdf_data['pdf_name'].startswith("README"):
        print("Skipping this file it is is not informative")
        return "Skipped"
     
    print(f"PDF Name before adding: {pdf_data['pdf_name']}")
    # Create an array of dataset objects
    for dataset in pdf_data["datasets"]:
        print(f"PDF {pdf_data['pdf_name']}")
        print(dataset)
        print(str(pdf_data['pdf_content']))
        pdf_object = {
            "link": pdf_data["link"],
            "globalId": pdf_data["datasets"][0]["globalId"],
            "abstract": pdf_data["datasets"][0]["abstract"],
            "vl1": pdf_data["datasets"][0]["vl1"],
            "vl2": pdf_data["datasets"][0]["vl2"],
            "content": pdf_data["pdf_content"]
        }

        # Add PDF to the batch
        batch.add_data_object(data_object=pdf_object, class_name="PDF", uuid=pdf_id)

        # Print the PDF name added to Weaviate
        print(f"PDF name added to Weaviate: {pdf_data['pdf_name']}")

    return pdf_id

# Configure batch processing
client.batch.configure(batch_size=50, dynamic=True, callback=None, timeout_retries=10)

# Iterate through JSON files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        json_path = os.path.join(json_folder, filename)

        try:
            # Load the JSON file
            with open(json_path, "r") as json_file:
                pdf_info = json.load(json_file)

            # Generate a unique PDF ID
            pdf_id = generate_uuid5(uuid_counter)
            uuid_counter += 1

            # Create PDF objects using batch processing
            with client.batch as batch:
                add_pdf(batch=batch, pdf_data=pdf_info, pdf_id=pdf_id)
        except UnicodeDecodeError:
            # Handle UnicodeDecodeError by skipping the current file
            print(f"Error reading file: {filename}. Skipping to the next file.")
            continue
        except weaviate.exceptions.ConnectionError:
            # Handle ConnectionError by skipping the current batch and continue with the next batch
            print("ConnectionError occurred. Skipping the current batch.")
            continue





