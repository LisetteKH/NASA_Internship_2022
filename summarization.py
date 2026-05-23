import json 
import os
import re
from transformers import pipeline

#call summarization transformer
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

pdf_json_directory = "pdf_json_files"


def main(): 
    for json_filename in os.listdir(pdf_json_directory):
        if json_filename.startswith("._"):
            continue
        if json_filename.endswith(".json"):
            print(f"Processing JSON file: {json_filename}")
            
            json_file_path = os.path.join(pdf_json_directory, json_filename)

            input_file = json_file_path
            output_file = json_file_path

            json_file(input_file, output_file)

#summarize the pdf content
def get_summary(content):
    summary = summarization_pipeline(content, max_length=500, min_length=150, do_sample=False)
    summary = summary[0]['summary_text']

    return summary

#extract the content needed 
def json_file(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            pdf_data = json.load(infile)

            pdf_content = pdf_data.get("pdf_content", "")
            print("PDF content has been extracted")
            keywords = ["Introduction", "Description", "Technical Summary", "Extended User Guide"]

            start_Index = None
            end_Index = None
            cleaned_content = ""

        
#define a regualar expression to extract content 
            for keyword in keywords:
                #pattern = re.compile(f'{keywords}\s+(\w[\w\s]*)')
                match = re.search(rf'{keyword}\s+(?=[\w\d])', pdf_content, re.IGNORECASE)

                if match:
                    start_Index = match.end()
                    end_Index = start_Index + 1000
                    #end_Index = start_Index + 1000
                    break

            if start_Index is not None: 
                content = pdf_content[start_Index:end_Index]
            else:
                content = pdf_content
            
            #print(content)

            words = content.split()
            cleaned_sentence = ' '.join(words)
            cleaned_sentence = re.sub(r'\s*\.\s*\.\s*', '', cleaned_sentence)
            cleaned_content += cleaned_sentence + ' '

            #print(cleaned_content)
            #min_words_threshold = 50

            #sentences = re.split(r'(?<=[.!?])\s+', content)
            #readability = 0
            #cleaned_content = ""

            #for sentence in sentences:
                #words = sentence.split()
                #readability += len(words)
 
                #if readability < min_words_threshold:
                    #break

                #cleaned_sentence = ' '.join(words)
                #cleaned_sentence = re.sub(r'\s*\.\s*\.\s*', '', cleaned_sentence)
                #cleaned_content += cleaned_sentence + ' '

            if len(cleaned_content.split()) >= 1024:
                cleaned_content = cleaned_content[:500]
            #print(cleaned_content)


#feed cleaned content into summary function
            if len(cleaned_content.split()) <= 5:
                pdf_data["pdf_content"] = "No summary available"

            else:
                summarized_content = get_summary(cleaned_content)
                if summarized_content.equals('None'):
                    summarized_content = 'No summary available'
                    pdf_data["pdf_content"] = summarized_content

                else: 
                    pdf_data["pdf_content"] = summarized_content

                print(summarized_content)
                
        with open(output_file, 'w') as outfile:
            json.dump(pdf_data, outfile, indent=2)
        
    except json.JSONDecodeError as e:
        print(f"Error loading JSON from {input_file}: {e}")
    except Exception as e:
        print(f"An error occurred while processing {input_file}: {e}")

if __name__ == "__main__":
    main()
