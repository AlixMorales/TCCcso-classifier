import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))

# Load provisions
df = pd.read_csv("outputs/provisions_from_spacing.csv")
df["label"] = ""
df["explanation"] = ""

# Better prompt for strict formatting
instructions = (
    "You are a legal assistant tasked with identifying whether a paragraph from a legal document "
    "is a standalone legal provision.\n\n"

    "Classify each paragraph as:\n"
    "- \"provision\": if it establishes a legal rule, right, obligation, restriction, or process. "
    "It must contain enforceable or actionable content.\n"
    "- \"not_provision\": if it is a title, part heading, metadata, citation, date, or reference to other sections.\n\n"

    "Here are examples:\n"
    "1. 'PART III – GENERAL PROVISIONS' → not_provision\n"
    "2. 'Section 3. A person shall not participate in a public assembly without notifying authorities.' → provision\n"
    "3. '[Date of assent: June 13, 1950]' → not_provision\n\n"

    "Respond ONLY with a JSON object in this format, it is important that your response consists of only a JSON because extra text generates noise:\n"
    "{\n"
    "  \"label\": \"provision\" or \"not_provision\",\n"
    "  \"explanation\": \"Brief explanation of your decision\"\n"
    "}\n"
)


# Loop through paragraphs
for i, row in df.iterrows():
    text = row["text"]
    print(f"Classifying paragraph {i}...")

    try:
        response = client.responses.create(
            model="gpt-4o",
            instructions=instructions,
            input=text,
            temperature=0.2
        )
        output = response.output_text.strip()

        # Validate output
        if not output.startswith("{"):
            raise ValueError(f"Non-JSON response: {output[:100]}")

        parsed = json.loads(output)
        df.at[i, "label"] = parsed.get("label", "unknown")
        df.at[i, "explanation"] = parsed.get("explanation", "")

    except Exception as e:
        print(f"Error at row {i}: {e}")
        df.at[i, "label"] = "error"
        df.at[i, "explanation"] = str(e)

    time.sleep(1.2)  # Stay within rate limits

# Save output
output_path = "outputs/filtered_provision.csv"
df.to_csv(output_path, index=False)
print(f"\n Saved filtered provisions to {output_path}")