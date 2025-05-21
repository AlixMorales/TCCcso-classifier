import fitz  # PyMuPDF
import re

def extract_provisions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Flexible pattern: capture sections like "3.  Title here" with variable spacing
    pattern = r"\n(\d{1,2})\.\s{1,5}(.*?)(?=\n\d{1,2}\.\s+|PART|\Z)"
    #pattern = r"\n((\d{1,3}(\s*\(\d{0,2}\))?))\s+(.*?)(?=\n\d{1,3}(\s*\(\d{0,2}\))?\s+|PART\s|\Z)"
    matches = re.findall(pattern, full_text, re.DOTALL)

    provisions = []
    for section_number, text in matches:
    #for match in matches:
    #    section_number = match[0]
    #    text = match[3]
        # Flatten multiline section titles and remove excessive whitespace
        cleaned_text = " ".join(text.strip().splitlines())
        full_provision = f"{section_number.strip()}. {cleaned_text}"
        if len(cleaned_text) > 50:  # Skip irrelevant short matches
            provisions.append(full_provision)

    return provisions

if __name__ == "__main__":
    path = "KenyaPublicOrderAct.pdf"
    provisions = extract_provisions_from_pdf(path)

    print(f"\nExtracted {len(provisions)} provisions from {path}:\n")
    for i, provision in enumerate(provisions, 1):
        print(f"Provision {i}:\n{provision}\n{'-'*80}\n")