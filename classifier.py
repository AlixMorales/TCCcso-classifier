import os
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load .env variables (to keep the API key secure)
load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))

# Load the CSO Matrix typology from file
with open("data/cso-matrix.txt", "r", encoding="utf-8") as f:
    matrix_typology = f.read()

def classify_provision(provision_text):
    prompt = f"""
    Classify the following provision using the CSO Regulatory Regime Matrix. Use the following typology as your reference:
    {matrix_typology}
    Find the closest matching concept. If no exact match exists, choose the conceptually closest category.

    Classify the provision as either:
    - Restrictive: if it imposes barriers or burdens on CSO activity.
    - Permissive: if it enables, supports, or simplifies CSO activity.

    Assign the provision to one of the four CSO Matrix subgroups: Formation, Governance, Operations, Resources.
    Once assigned, do not change the category.

    Return a JSON object like this:

    {{
    "provision": "{provision_text}",
    "matched_matrix_provision": "Closest concept from matrix, as it appears in the matrix.",
    "subgroup": "Formation | Governance | Operations | Resources",
    "type": "Restrictive | Permissive",
    "explanation": "Brief legal reasoning and justification based on the matrix."
    }}
    """

    start_time = time.time()

    response = client.responses.create(
        model="gpt-4o",
        instructions=(
            "You are a legal classification assistant trained in civil society regulation. "
            "Read the input prompt carefully and follow all formatting instructions. "
            "Do not speculate beyond the matrix provided in the prompt."
        ),
        input= prompt,
        temperature=0.2
    )

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    usage = response.usage
    print("\nToken Usage:")
    print(f"Input tokens: {usage.input_tokens}")
    print(f"Output tokens: {usage.output_tokens}")
    print(f"Total tokens: {usage.total_tokens}")
    print(f"Execution time: {duration} seconds\n")

    return response.output_text