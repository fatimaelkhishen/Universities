import fitz  # PyMuPDF
import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
import torch
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# ==== CONFIG ====
INPUT_FILE = r"C:\Users\10265480\Desktop\BB - TUN - PE BTP Chef de chantier routes et VRD.pdf"
OUTPUT_FILE = r"C:\Users\10265480\Desktop\BB - TUN - PE BTP Chef de chantier routes et VRD.translated.xlsx"
COLUMN_TO_TRANSLATE = "Page Text"

# Load MarianMT model (French → English)
model_name = "Helsinki-NLP/opus-mt-fr-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# --- Language detection
def is_french(text):
    try:
        return detect(text) == "fr"
    except LangDetectException:
        return False

# --- Translation
def translate_text(text):
    if not isinstance(text, str) or not text.strip():
        return text
    if not is_french(text):
        return text

    max_length = 450  # chunk size
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    translated_chunks = []

    for chunk in chunks:
        inputs = tokenizer([chunk], return_tensors="pt", padding=True, truncation=True).to(device)
        outputs = model.generate(**inputs)
        translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        translated_chunks.append(translated)

    return "\n".join(translated_chunks)

# === Load PDF and extract text
print("📄 Reading PDF pages...")
doc = fitz.open(INPUT_FILE)
page_texts = [page.get_text() for page in doc]
doc.close()

# === Create DataFrame
df = pd.DataFrame({COLUMN_TO_TRANSLATE: page_texts})
translated_df = df.copy()

# === Translate column
print(f"🌍 Translating column: '{COLUMN_TO_TRANSLATE}'")
translated_column = []

for i, text in enumerate(translated_df[COLUMN_TO_TRANSLATE]):
    print(f"🔄 Translating page {i + 1}/{len(translated_df)}...")
    translated_column.append(translate_text(text))

translated_df[COLUMN_TO_TRANSLATE] = translated_column

# === Save to Excel
translated_df.to_excel(OUTPUT_FILE, index=False)
print(f"\n✅ Translation complete. File saved to:\n{OUTPUT_FILE}")
