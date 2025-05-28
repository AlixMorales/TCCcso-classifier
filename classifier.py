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

def classify_provision_with_file_search(provision_text, matrix_path):
    # Create vector store
    vector_store = client.vector_stores.create(name="CSO_Matrix_Vector_Store")
    vector_store_id = vector_store.id

    # Upload the CSO matrix
    print("Matriz uploaded")
    with open(matrix_path, "rb") as f:
        client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=[f]
        )

    # API
    print("\nClassifying...\n")
    start_time = time.time()

    response = client.responses.create(
        model="gpt-4.1",
        instructions=("""
            You are a legal classification assistant trained in civil society regulation.
            Read the input prompt carefully and follow all formatting instructions, do not speculate beyond the matrix provided.
            
            When prompted a legal provision, explain who has the duty to do what's stated in the provision, what has to be done and what are the consequences of not following said provision.
            Think about the institutional grammar, these are the legal components to consider:
                                  • Attribute (A) identifies to whom the institutional statement applies, and if no attributes
                                    are named, then the default assumption is all members of the group;
                                    • Deontic (D) denotes the expectation of behavior identified by the qualifiers ‘may’ (permit-
                                    ted), ‘must’ (obliged), and ‘must not’ (forbidden);
                                    • AIm (I) prescribes particular action or outcome, or specifies forbidden actions or outcomes;
                                    • Condition (C) explains when and where the institutional statement applies, and if no
                                    conditions exist, then the default assumption is that it applies to all persons, at all times and
                                    all places, under all circumstances;
                                    • Or Else (O) provides the institutionally assigned sanction for noncompliance. This com-
                                    ponent must have three qualifications: (i) sanctioning provision is the result of an explicit
                                    collective-choice decision that is separate from any internal or social penalty, (ii) be backed by
                                    at least one other institutional statement that if noncompliance occurs changes the DEONTIC
                                    assigned to some AIM for at least one actor, and (iii) affect the constraints and opportunities
                                    of actors responsible for monitoring the conformance of offenders.
                      
            
                      
            Use the File Search tool to find the closest matching concept in the CSO Matrix.
            Find the closest matching concept in the legal provision. If no exact match exists, choose the conceptually closest category.
                      
        I classify provisions as either restrictive or permissive using a two-step process. First, a provision is permissive if its reasonable and impartial enforcement improves trust, accountability, or resolves “voluntary failures”. Classification advances to the second stage if there is no clear demand-side prediction. Here, a provision is restrictive if its reasonable and impartial enforcement limits organizational autonomy or stifles organizational emergence.
                      
            Assign the provision to one of the four CSO Matrix subgroups: Formation, Governance, Operations, Resources.
            Once assigned, do not change the category.
                      
            Always return only a JSON object like this:

            {{
            "provision": "the exact provision text provided",
            "interpretation: "Who has the duty, what has to be done, and what are the consequences of not following said provision.",
            "matched_matrix_provision": "Closest concept from matrix, exactly as it appears in the matrix.",
            "subgroup": "Formation | Governance | Operations | Resources",
            "type": "Restrictive | Permissive",
            "explanation": "Brief legal reasoning and justification based on the matrix."
            }}
    
            """
        ),
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }],
        input=(
            f"""
            Classify the following provision using the CSO Matrix: {provision_text}
            """
        ),
        temperature=0.2
    )

    end_time = time.time()
    print(f"Completed in {round(end_time - start_time, 2)} seconds.")
    return response.output_text