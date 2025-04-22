import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))

def upload_file_to_vector_store(filepath, vector_store_id):
    print(f"Uploading and indexing {filepath}...")
    with open(filepath, "rb") as f:
        client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=[f]
        )

def classify_with_file_search(pdf_path, matrix_path, output_path=None):
    # Create a new vector store
    print("Creating vector store...")
    vector_store = client.vector_stores.create(name="CSO_Classification_Store")
    vector_store_id = vector_store.id

    # Upload PDF and matrix file to the vector store
    upload_file_to_vector_store(pdf_path, vector_store_id)
    upload_file_to_vector_store(matrix_path, vector_store_id)

    # Create the classification response using Responses API with vector store
    print("\nSending classification request...")
    response = client.responses.create(
        model="gpt-4o",
        instructions=(
            "You are a legal assistant trained in CSO regulation. "
            "Use the file search tool to classify provisions from the PDF using the matrix as reference. "
            "For each provision, return: 'provision', 'matched_matrix_provision', 'subgroup', 'type', and 'explanation'."
        ),
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }],
        input=(
            "Classify the provisions found in the PDF file using the CSO Matrix as reference. "
            "Provide a JSON result per provision."
        ),
        temperature=0.2
    )


    print("\nResponse received:\n")
    print(response.output_text)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(response.output_text, f, indent=4, ensure_ascii=False)
        print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python file_search_classifier.py path/to/pdf path/to/matrix.txt [output.json]")
    else:
        pdf_path = sys.argv[1]
        matrix_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        classify_with_file_search(pdf_path, matrix_path, output_path)