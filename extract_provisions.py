import fitz  # PyMuPDF
import re

def extract_provisions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Extract numbered sections (like 3., 4., etc.)
    pattern = r"\n(\d{1,2}\.)\s+(.*?)(?=\n\d{1,2}\.\s+|PART|\Z)"
    matches = re.findall(pattern, full_text, re.DOTALL)

    provisions = []
    for section_number, text in matches:
        cleaned = text.strip()
        if len(cleaned) > 50:
            provisions.append(cleaned)

    return provisions

if __name__ == "__main__":
    provisions = extract_provisions_from_pdf("PublicOrderAct26of1950.pdf")

    print(f"\n Extracted {len(provisions)} provisions:\n")
    for i, provision in enumerate(provisions, 1):
        print(f"Provision {i}:\n{provision}\n{'-'*80}\n")
