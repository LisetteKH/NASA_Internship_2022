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
    st.title("GES-DISC PDF and Associated Dataset Query")

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
            response2 =   client2.query.get("PDF", ["link","datasets {... on Dataset {shortname}}", "pdf_content" ]).with_additional(["id"]).with_near_text(near_text_filter).do()
            response4 =   client.query.get("Dataset", ["shortName", "abstract", "longName", "doi", "vl1", "vl2"]).with_additional(["distance"]).with_limit(1433).do()

            # Extract the datasets that have similar vectors to the user's query
            links = response2['data']['Get']['PDF']
            pdf_datasets = response4['data']['Get']['Dataset']

            # If there are datasets returned, select the most relevant one based on your logic
            if links:
                st.write(f"Total PDFs Displayed: {len(links)}")
                for link in links:
                    url = link['link']
                    #st.write(links[])
                    st.write(f"PDF Link: {url}")
                    st.write(f"Datasets Associated with the PDF:")
                    st.write(f" ")
                    for shortname in link['datasets']:
                        for dataset in pdf_datasets:
                           if (dataset['shortName'] == (shortname['shortname'])):
                             #st.write(f"inside dataset for loop meaning the shortnames are matching")
                             st.write(f"Short Name: {shortname['shortname']}")
                             st.write(f"Long Name: {dataset['longName']}")
                             st.write(f"Science Keyword #1: {dataset['vl1']}")
                             st.write(f"Science Keyword #2: {dataset['vl2']}")
                             st.write(f"Abstract: {dataset['abstract']}")
                             st.write(f"DOI: {dataset['doi']}")

            else:
                st.write("I couldn't find any relevant PDFs based on your query. Please edit your query and try again.")
if __name__ == "__main__":
    main()
