---

## License

Copyright (c) 2026 Lisette Kamper-Hinson. All rights reserved.

This project and its contents are the intellectual property of Lisette Kamper-Hinson. 
No part of this project may be reproduced, distributed, or used without express written 
permission from the author.
---

# Enhancing Data and Knowledge Discoverability at NASA GES-DISC

**Lisette Kamper-Hinson | NASA Summer 2023**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Knowledge%20Graph-green)](https://neo4j.com/)
[![Weaviate](https://img.shields.io/badge/Weaviate-Vector%20Database-purple)](https://weaviate.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io/)

---

## Overview

The Goddard Earth Sciences Data and Information Services Center (GES-DISC) at NASA curates over 1,500 satellite datasets covering Earth science focus areas including Atmospheric Composition, Water and Energy Cycles, Climate Variability, and the Carbon Cycle and Ecosystem. Despite meticulous curation, existing metadata was insufficient to address complex user needs for dataset search, discovery, and utilization.

This project introduces a production-grade framework that integrates knowledge graphs, vector databases, transformer-based language models, and a conversational Streamlit interface to revolutionize how researchers interact with NASA scientific data.

This work was published as a peer-reviewed abstract and presented at the AGU Fall Meeting 2023 in San Francisco, CA.

**Citation:** Kamper-Hinson, L., Rezaiyan-Nojani, A., and Mehrabian, A. (2023). Enhancing Data and Knowledge Discoverability at NASA GES-DISC through Knowledge Graphs and Language Models. AGU Fall Meeting Abstracts, 2023(411), IN54A-01.

---

## The Problem

Researchers querying NASA datasets faced two core challenges:

1. **Keyword search limitations.** Traditional keyword search could not handle the ambiguity and complexity of scientific queries. A researcher looking for atmospheric carbon data might not know the exact terminology used in dataset metadata.

2. **Disconnected data sources.** Over 530 JSON metadata files and 1,960 associated PDFs existed as separate, unlinked resources. No system connected datasets to the papers that referenced and used them.

---

## Technical Architecture

### Step 1: Data Cleaning and Extraction
Starting with 530 JSON metadata files and 1,960 PDF documents, custom regular expressions were written to extract pertinent information from each file type and normalize it into a consistent structure for downstream processing.

### Step 2: Knowledge Graph (Neo4j)
A graph database was built in Neo4j to represent the hierarchical and relational structure of the dataset collection. Nodes represent datasets, focus areas, instruments, and missions. Edges represent relationships between them. This graph structure enables traversal queries that surface related datasets through chains of relationships rather than direct keyword matches.

### Step 3: Vector Database (Weaviate)
A vector database was built in Weaviate to enable semantic similarity search. Each dataset and document was embedded into a high-dimensional vector space using a transformer-based language model. Queries are embedded into the same space and matched to the nearest vectors, allowing natural language queries to retrieve relevant datasets even when exact terminology does not match.

### Step 4: Transformer Integration (Hugging Face BERT)
An encoder-decoder transformer from Hugging Face was integrated to contextualize PDF summaries for the chatbot interface. This allowed the system to generate grounded, contextually relevant responses to scientific questions rather than returning raw document excerpts.

### Step 5: Streamlit Application
A full Streamlit web application was built as the user-facing interface. Researchers can ask natural language questions about Earth science datasets or PDF documents and receive a ranked list of relevant datasets and papers. A chatbot interface powered by the transformer model enables conversational exploration of the data.

---

## System Architecture Diagram

```
User Query
    |
    v
Streamlit Interface
    |
    v
Weaviate Vector Database (semantic similarity search)
    |
    +---> Neo4j Knowledge Graph (relational traversal)
    |
    v
Hugging Face BERT Transformer (response contextualization)
    |
    v
Ranked Dataset and PDF Results
```

---

## Key Results

- 1,500+ NASA satellite datasets indexed and made discoverable through natural language queries
- 1,960 scientific PDFs linked to associated datasets through the knowledge graph
- End-to-end system deployed and demonstrated to NASA GES-DISC research teams
- Work published and presented at AGU Fall Meeting 2023, San Francisco, CA

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core pipeline and application development |
| Neo4j | Knowledge graph construction and relational querying |
| Weaviate | Vector database for semantic similarity search |
| Hugging Face BERT | Transformer-based language model for chatbot contextualization |
| Streamlit | User-facing web application and chatbot interface |
| Regular Expressions | JSON and PDF data extraction and cleaning |

---

## Future Work

- Train a domain-specific transformer on NASA dataset summaries and metadata rather than using a general-purpose pretrained model
- Integrate additional unstructured data sources to expand discoverability coverage
- Improve visual design alignment with NASA GES-DISC interface standards

---

## Author

**Lisette Kamper-Hinson**
M.S. Computer Science, Wake Forest University
[LinkedIn](https://www.linkedin.com/in/lisette-kamper-hinson) | [GitHub](https://github.com/LisetteKH)
lisette.hinson@gmail.com
