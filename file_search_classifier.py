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
            "You are a legal classification assistant trained in civil society regulation. "
            "Use the File Search tool to read the uploaded documents. "
            "Use the CSO Regulatory Regime Matrix as reference to classify legal provisions found in the PDF. "
            "Find the closest matching concept. If no exact match exists, choose the conceptually closest category.\n\n"
            "Classify each provision as either:\n"
            "- Restrictive: if it imposes barriers or burdens on CSO activity.\n"
            "- Permissive: if it enables, supports, or simplifies CSO activity.\n\n"
            "Assign the provision to one of the four CSO Matrix subgroups: Formation, Governance, Operations, Resources.\n"
            "Once assigned, do not change the category.\n\n"
            "Return a JSON object for each provision like this:\n\n"
            "{\n"
            "\"provision\": \"...\",\n"
            "\"matched_matrix_provision\": \"Closest concept from matrix, as it appears in the matrix.\",\n"
            "\"subgroup\": \"Formation | Governance | Operations | Resources\",\n"
            "\"type\": \"Restrictive | Permissive\",\n"
            "\"explanation\": \"Brief legal reasoning and justification based on the matrix.\"\n"
            "}"
        ),
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }],
        input=(
            "Read the uploaded PDF and classify each legal provision using the CSO Matrix also uploaded. "
            "Return results in JSON as described in the instructions."
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