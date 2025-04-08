import fitz  # PyMuPDF
import re
import json
import sys
from classifier import classify_provision

def extract_provisions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Split into numbered sections like "3. ...", "4. ..." until the next section
    pattern = r"\n(\d{1,2}\.)\s+(.*?)(?=\n\d{1,2}\.\s+|PART|\Z)"
    matches = re.findall(pattern, full_text, re.DOTALL)

    provisions = []
    for section_number, text in matches:
        cleaned = text.strip()
        if len(cleaned) > 50:  # skip short irrelevant items
            provisions.append(cleaned)

    return provisions

def classify_pdf(pdf_path, output_path=None):
    provisions = extract_provisions_from_pdf(pdf_path)
    print(f"Extracted {len(provisions)} provisions from {pdf_path}\n")

    results = []
    for i, provision in enumerate(provisions, 1):
        print(f"🔍 Classifying provision {i} of {len(provisions)}:")
        print(provision[:100].replace("\n", " ") + "...\n")
        try:
            result = classify_provision(provision)
            results.append(result)
        except Exception as e:
            print(f"Error on provision {i}: {e}")
        print("-" * 60 + "\n")

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"Saved results to {output_path}")

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_classifier.py path/to/file.pdf [output.json]")
    else:
        pdf_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        classify_pdf(pdf_path, output_path)
