import re
import streamlit as st
import weaviate

# Set the URL of your Weaviate instance
weaviate_url = "http://localhost:8080"
weaviate_url2 = "http://localhost:8899"
# Initialize the Weaviate client
client = weaviate.Client(weaviate_url)
client2 = weaviate.Client(weaviate_url2)

# Streamlit app
def main():
    st.title("GES-DISC Dataset Query")

    # Input text box for user query
    query = st.text_input("Enter your query here:", "")

    # Button to execute the query
    if st.button("Search"):
        if query:
            near_text_filter = {
                 "concepts": [query],
                 "certainty" : 0.6
            }
            count = 0
            # Use the Weaviate client to query similar vectors for the "Dataset" class
            response1 =   client.query.get("Dataset", ["shortName", "abstract", "longName", "doi", "vl1", "vl2"]).with_additional(["distance"]).with_near_text(near_text_filter).with_limit(1433).do()

            # Extract the datasets that have similar vectors to the user's query
            datasets = response1['data']['Get']['Dataset']

            if datasets:
                st.write("Here are the datasets that might be relevant")
                st.write(f"Total Dataset Displayed: {len(datasets)}")
                for dataset in datasets:
                    st.write(f"Short Name: {dataset['shortName']}")
                    st.write(f"Long Name: {dataset['longName']}")
                    st.write(f"Science Keyword #1: {dataset['vl1']}")
                    st.write(f"Science Keyword #2: {dataset['vl2']}")
                    st.write(f"Abstract: {dataset['abstract']}")
                    st.write(f"DOI: {dataset['doi']}")
            else:
                st.write("I couldn't find a relevant dataset for your query.")
if __name__ == "__main__":
    main()
