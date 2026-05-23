import weaviate

weaviate_url = "http://localhost:8080"
client = weaviate.Client(weaviate_url)
client.schema.delete_all()

schema = {
    "classes": [
        {
            "class": "Dataset",
            "description": "A dataset of observation granules of a specific Project/Mission/Instrument",
            "properties": [
                {
                    "name": "globalId",
                    "dataType": ["string"],
                    "description": "The UUID5 based on the short name",
                },
                {
                    "name": "doi",
                    "dataType": ["string"],
                    "description": "Digital Object Identifier of the dataset",
                },
                {
                    "name": "shortName",
                    "dataType": ["string"],
                    "description": "The unique controlled name of the dataset",
                },
                {
                    "name": "longName",
                    "dataType": ["text"],
                    "description": "The long name description of the dataset",
                },
                {
                    "name": "daac",
                    "dataType": ["string"],
                    "description": "Name of the DAAC",
                },
                {
                    "name": "abstract",
                    "dataType": ["text"],
                    "description": "Abstract text of the dataset",
                },
                {
                    "name": "hasVariable",
                    "dataType": ["Variable"],
                    "description": "The physical variable of the dataset",
                },
                {
                    "name": "hasPublication",
                    "dataType": ["Publication"],
                    "description": "The Publication that cites the dataset",
                },
                {
                    "name": "hasKeyword",
                    "dataType": ["Keyword"],
                    "description": "The GCMD keyword that the dataset is tagged with",
                },
            ],
	},
	{
            "class": "Variable",
            "description": "Physical variable associated with a dataset",
            "properties": [
                {
                    "name": "globalId",
                    "dataType": ["string"],
                    "description": "The UUID5 based on the short name",
                },
                {
                    "name": "shortName",
                    "dataType": ["string"],
                   "description": "The short name of the variable",
                },
                {
                    "name": "longName",
                    "dataType": ["text"],
                    "description": "The long name of the variable",
                },
                {
                    "name": "variableMeasurement",
                    "dataType": ["string[]"],
                    "description": "The physical phenomena the variable is measuring",
                },
                {
                    "name": "ofDataset",
                    "dataType": ["Dataset"],
                    "description": "The variable of the dataset",
                },
            ],
        },
        {
            "class": "Publication",
            "description": "A Publication using EOS dataset",
            "properties": [
                {
                    "name": "globalId",
                    "dataType": ["string"],
                    "description": "The UUID5 based on the publication DOI",
                },
                {
                    "name": "title",
                    "dataType": ["text"],
                    "description": "The title of the publication",
                },
                {
                    "name": "doi",
                    "dataType": ["string"],
                   "description": "The DOI for the publication",
                },
                {
                    "name": "abstract",
                    "dataType": ["text"],
                    "description": "The abstract for the publication",
                },
                {
                    "name": "year",
                    "dataType": ["int"],
                    "description": "The year of the publication",
                },
                {
                    "name": "authors",
                    "dataType": ["text[]"],
                    "description": "The author(s) of the publication",
                },
                {
                    "name": "citesDataset",
                    "dataType": ["Dataset"],
                    "description": "The dataset this publication cites",
                },
            ],
	},
	{
            "class": "Keyword",
            "description": "A science keyword",
            "properties": [
                {
                    "name": "globalId",
                    "dataType": ["string"],
                    "description": "The UUID5 based on the keyword name",
                },
                {
                    "name": "name",
                    "dataType": ["text"],
                   "description": "The name of the science keyword",
                },
                {
                    "name": "level",
                    "dataType": ["string"],
                    "description": "The GCMD level of the keyword",
                },
                {
                    "name": "isKeywordOf",
                    "dataType": ["Dataset"],
                    "description": "The dataset that a keyword is tagged with",
                },
            ],
	},
    ]
}

# Create schema
client.schema.create(schema)
