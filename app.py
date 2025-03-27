import os
import sys
sys.path.append(r"C:\Users\Raúl Pérez\AppData\Roaming\Python\Python312\Scripts")
try:
    import openai
except ImportError:
    raise ImportError("The 'openai' module is not installed. Ensure it is installed and the path is correctly set.")
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
openai.api_key = os.getenv("api_key")

# Load the CSO Matrix typology from file
with open("data/cso-matrix.txt", "r", encoding="utf-8") as f:
    matrix_typology = f.read()

def classify_provision(provision_text):
    prompt = f"""
You are a legal AI trained to classify CSO laws using the following matrix:

{matrix_typology}

Provision: "{provision_text}"

Tasks:
1. Classify the provision as Restrictive or Permissive.
2. Assign it to one of the matrix categories: Formation, Governance, Operations, or Resources.
3. Match the closest constitutional right (e.g. Freedom of Association, Assembly, Petition).
4. Indicate whether the law is Constitutional, Unconstitutional, or Neutral.
5. Explain your reasoning.

Return in this format:
{{
  "type": "...",
  "category": "...",
  "constitutional_provision": "...",
  "constitutional_alignment": "...",
  "explanation": "..."
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful legal classification assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content