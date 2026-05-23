pip install neo4j
from neo4j import GraphDatabase
import json
import os,glob
driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth = ("neo4j", "shannon-spain-field-switch-topic-8121"))
session=driver.session()
#replace "/Users/lisettek-h/Desktop/PROD_2022031" with the path to your json files
files=glob.glob("/Users/lisettek-h/Desktop/PROD_2022031/*.json")
#shows that the files have been loaded correctly 
files 

for file in files:
    try:
        file_name = os.path.basename(file)
        ql = """
        CALL apoc.load.json("file://"+$path) YIELD value 
        """
        x = {"path": file_name}
        results = session.run(ql, x)

        for record in results:
            value = record["value"]

        # Create Dataset node
        cypher_query = """
        MERGE (dataset:Dataset {
            collectionProgress: $collectionProgress,
            entryTitle: $entryTitle,
            isoTopicCategories: $isoTopicCategories,
            shortName: $shortName
        })
        SET dataset.dataLanguage = $dataLanguage
        RETURN dataset
        """
        params = {
            "collectionProgress": value.get("CollectionProgress"),
            "dataLanguage": value.get("DataLanguage"),
            "entryTitle": value.get("EntryTitle"),
            "isoTopicCategories": value.get("ISOTopicCategories"),
            "shortName": value.get("ShortName")
        }

        result = session.run(cypher_query, **params)
        datasetNode = result.single()["dataset"]

        # Create CollectionCitations nodes and relationships

        citations = value.get("CollectionCitations")
        if citations:
            for citation in citations:
                cypher_query = """
                    MATCH (dataset:Dataset {shortName: $shortName})
                    MERGE (dataset)-[:HAS_CITATION]->(c:Citation {title: $title})
                    ON CREATE SET c += {
                        creator: $creator,
                        seriesName: $seriesName,
                        releasePlace: $releasePlace
                    }
                    MERGE (p:Publisher {name: $publisher})
                    MERGE (c)-[:PUBLISHED_BY]->(p)
                    """
                params = {
                    "shortName": value.get("ShortName"),
                    "title": citation.get("Title"),
                    "creator": citation.get("Creator"),
                    "seriesName": citation.get("SeriesName"),
                    "releasePlace": citation.get("ReleasePlace"),
                    "publisher": citation.get("Publisher"),
                }

                session.run(cypher_query, **params)


        # Extract ScienceKeywords
        keywords = value.get("ScienceKeywords")
        if keywords:
            for keyword in keywords:
                cypher_query = """
                MATCH (dataset:Dataset {shortName: $shortName})
                MERGE (dataset)-[:HAS_KEYWORD]->(sk:ScienceKeyword {term: $term})
                ON CREATE SET sk += {
                    category: $category,
                    topic: $topic,
                    variableLevel1: $variableLevel1,
                    variableLevel2: $variableLevel2
                }
                """
                params = {
                    "shortName": value.get("ShortName"),
                    "term": keyword.get("Term"),
                    "category": keyword.get("Category"),
                    "topic": keyword.get("Topic"),
                    "variableLevel1": keyword.get("VariableLevel1"),
                    "variableLevel2": keyword.get("VariableLevel2")
                }

                session.run(cypher_query, **params)

        # Create relationship between Citation and Publisher
        cypher_query = """
        MATCH (dataset:Dataset {shortName: $shortName})-[:HAS_CITATION]->(c:Citation)
        MERGE (c)-[:PUBLISHED_BY]->(:Publisher)
        """
        params = {
            "shortName": value.get("ShortName")
        }
        session.run(cypher_query, **params)

    except Exception as e:
        print(f"Error reading file {file}: {str(e)}")
        traceback.print_exc()
        continue

