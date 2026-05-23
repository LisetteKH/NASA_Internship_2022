
import weaviate
import json
import uuid
import requests
from io import BytesIO

# Weaviate configuration
weaviate_url = "http://localhost:8080"
client = weaviate.Client(weaviate_url)
client.schema.delete_all()

merged_schema = {
    "classes": [
        {
            "class": "PDF",
            "description": "Represents a PDF document",
            "properties": [
                {
                    "name": "link",
                    "dataType": ["text"],
                    "description": "The link to the PDF document"
                },
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The content of the PDF document"
                },
                {
                    "name": "globalId",
                    "dataType": ["text"],
                    "description": "The global identifier for the dataset"
                },
                {
                    "name": "doi",
                    "dataType": ["text"],
                    "description": "The DOI (Digital Object Identifier) for the dataset"
                },
                {
                    "name": "shortName",
                    "dataType": ["text"],
                    "description": "The short name of the dataset"
                },
                {
                    "name": "longName",
                    "dataType": ["text"],
                    "description": "The long name or title of the dataset"
                },
                {
                    "name": "abstract",
                    "dataType": ["text"],
                    "description": "The abstract or description of the dataset"
                },
                {
                    "name": "vl1",
                    "dataType": ["text"],
                    "description": "Variable Level 1 information of the dataset"
                },
                {
                    "name": "vl2",
                    "dataType": ["text"],
                    "description": "Variable Level 2 information of the dataset"
                }
            ]
        }
    ]
}

# Create schema
client.schema.create(merged_schema)

