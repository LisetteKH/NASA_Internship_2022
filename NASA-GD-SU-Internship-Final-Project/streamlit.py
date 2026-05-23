import streamlit as st
import requests
import weaviate
from transformers import pipeline

# Set the URL of your Weaviate instance
weaviate_url = "http://localhost:8080"
# Initialize the Weaviate client
client = weaviate.Client(weaviate_url)

# Initialize the question-answering pipeline and summarization pipeline
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", tokenizer="bert-large-uncased-whole-word-masking-finetuned-squad")
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to get dataset information, including the summary
def get_dataset_info(global_id, abstract, link):
    try:
        #near_text_filter = {
            #"concepts": [global_id],
            #"certainty": 0.6
        #}
        #response = client.query.get("PDF", ['abstract', 'link']).with_near_text(near_text_filter).do()
        #datasets = response['data']['Get']['PDF']
        #if datasets:
            #dataset = datasets[0]

            #abstract = dataset['abstract']
        print("Abstract inside the function: ", abstract)
        summary = summarization_pipeline(abstract, max_length=50, min_length=30, do_sample=False)
        summary = summary[0]['summary_text']
        print("Summary inside the function: ", summary)
        dataset_info = {
            "globalId": global_id,
            "abstract": abstract,
            "summary": summary, 
            "link": link
            }
        return dataset_info
        #else:
            #return {"globalId": global_id, "abstract": "Abstract not found", "summary": "Summary not found", "link": "Link not found"}
    except Exception as e:
        print(f"Error retrieving dataset information: {str(e)}")
        return {"globalId": global_id, "abstract": "Error retrieving dataset information", "summary": "Summary not found", "link": "Link not found"}

def answer_question(question, summary):
    answer = qa_pipeline(question=question, context=summary)
    return answer['answer']

# Streamlit app
def main():
    st.title("GES-DISC Dataset Query")

    # Input text box for user query
    query = st.text_input("Enter a keyword or question to find helpful PDFs and associated datasets:", "")

    if query:
        near_text_filter = {
            "concepts": [query],
            "certainty": 0.6
        }
        # Use the Weaviate client to query similar vectors for the "PDF" class
        response = client.query.get("PDF", ["link", "globalId", "abstract", "content"]).with_additional(["distance"]).with_near_text(near_text_filter).do()

        pdfs = response['data']['Get']['PDF']

        st.write("Here are the PDF results:")
        for pdf in pdfs:
            st.write(f"Link: {pdf['link']}")
            print(f"PDF content: {pdf['content']}")
            st.write(f"Summary: {pdf['content']}")
            st.write(f"GlobalId: {pdf['globalId']}")
            #st.write(f"Abstract: {pdf['abstract']}")

            with st.form(key=f"summary_{pdf['globalId']}_{pdf['link']}"):
                summarySubmit_button = st.form_submit_button(label="Summary of Dataset")
                if summarySubmit_button:
                    globalID = pdf['globalId']
                    abstract = pdf['abstract']
                    link = pdf['link']
                    #print("Before get_dataset_info is called: ", abstract)
                    dataset_info = get_dataset_info(globalID, abstract, link)
                    st.write(dataset_info["summary"])


            # Create a form to submit questions for each PDF
            with st.form(key=f"form_{pdf['globalId']}_{pdf['link']}"):
                question = st.text_input("Ask a question about this PDF:", "")
                #st.write('To get a summary of the dataset ask, "What is the main topic of this dataset?"')
                submit_button = st.form_submit_button(label="Submit Question")

                if submit_button and question:
                    # Store PDF and dataset information for this button
                    #globalID = pdf['globalId']
                    abstract = pdf['abstract']
                    #link = pdf['link']
                    #print("Before get_dataset_info is called: ", abstract)
                    #dataset_info = get_dataset_info(globalID, abstract, link)
                    answer = answer_question(question, abstract)
                    st.write(f"You: {question}")
                    st.write(f"Chatbot: {answer.capitalize()}")

            

if __name__ == "__main__":
    main()
