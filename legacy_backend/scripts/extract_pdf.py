import os
import fitz  # PyMuPDF
import json

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

if __name__ == "__main__":
    pdf_path = "data/sample.pdf"

    if not os.path.exists(pdf_path):
        print(f"Le fichier {pdf_path} est introuvable.")
        exit(1)

    print(f" Lecture de : {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    output_dir = "data"
    output_path = os.path.join(output_dir, "extracted_text.json")

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"text": text}, f, ensure_ascii=False, indent=2)

    print(" Texte extrait avec succès et sauvegardé dans 'data/extracted_text.json'")
