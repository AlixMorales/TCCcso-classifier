import os
import json
import time
import datetime
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# === Setup ===
load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))

# === Configuration ===
filtered_csv_path = "outputs/filtered_provisions_20250526_155535.csv"
matrix_path = "data/cso-matrix.txt"

# === Load filtered provisions ===
df = pd.read_csv(filtered_csv_path)
df = df[df["label"] == "provision"]

# === Upload CSO Matrix to vector store ===
print(" Creating vector store...")
vector_store = client.vector_stores.create(name="CSO_Matrix_Store")
vector_store_id = vector_store.id

print(" Uploading matrix...")
with open(matrix_path, "rb") as f:
    client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id,
        files=[f]
    )

# === Provision classifier (using file search only) ===
def classify_provision(provision_text, vector_store_id):
    instructions = (
        "You are a legal classification assistant trained in civil society regulation.\n"
        "Use the File Search tool to read the uploaded CSO Matrix.\n"
        "Find the closest matching matrix concept for the following provision.\n\n"

        "Classify the provision as either:\n"
        "- Restrictive: if it imposes barriers or burdens on CSO activity.\n"
        "- Permissive: if it enables, supports, or simplifies CSO activity.\n\n"

        "Assign the provision to one of the four CSO Matrix subgroups: Formation, Governance, Operations, Resources.\n"
        "Once assigned, do not change the category.\n\n"

        "Always return only a structured JSON with these fields:\n"
        "- provision  (exact provision text) \n"
        "- matched_matrix_provision (Closest concept from matrix, as it appears in the matrix.)\n"
        "- subgroup (Formation | Governance | Operations | Resources)\n"
        "- type (Restrictive | Permissive)\n"
        "- explanation (Brief legal reasoning and justification based on the matrix)"
    )

    start_time = time.time()

    response = client.responses.create(
        model="gpt-4o",
        instructions=instructions,
        input=provision_text,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }],
        temperature=0.2
    )

    end_time = time.time()
    print(f" Classified in {round(end_time - start_time, 2)}s")
    return response.output_text

# === Classify all provisions ===
results = []
for i, row in df.iterrows():
    provision = row["text"]
    print(f"\n Classifying provision {i} of {len(df)}")
    try:
        output = classify_provision(provision, vector_store_id)
        results.append({
            "provision": provision,
            "output": output
        })
    except Exception as e:
        print(f" Error: {e}")
        results.append({
            "provision": provision,
            "output": f"ERROR: {e}"
        })
    time.sleep(1.2)  # safe buffer

# === Save results ===
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
output_path = f"outputs/classified_provisions_{timestamp}.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n Classification complete. Saved to {output_path}")