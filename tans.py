

import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
import torch
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# ==== CONFIG ====
INPUT_FILE = r"C:\Users\10265480\Desktop\Tunisia_Jobs_All.xlsx"
OUTPUT_FILE = r"C:\Users\10265480\Desktop\Tunisia_Jobs_All_translated.xlsx"
COLUMNS_TO_TRANSLATE = ["Job Title", "Job Description"]

# Load MarianMT model (French → English)
model_name = "Helsinki-NLP/opus-mt-fr-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def is_french(text):
    try:
        return detect(text) == "fr"
    except LangDetectException:
        return False

def translate_text(text):
    if not isinstance(text, str) or not text.strip():
        return text
    if not is_french(text):
        return text
    inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model.generate(**inputs)
    translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return translated

# Load Excel
print("📥 Loading Excel file...")
df = pd.read_excel(INPUT_FILE, engine="openpyxl")
translated_df = df.copy()

# Translate specified columns with row logging
for col in COLUMNS_TO_TRANSLATE:
    if col in translated_df.columns:
        print(f"🌍 Translating column: {col}")
        translated_column = []
        for i, text in enumerate(translated_df[col]):
            print(f"🔄 Row {i+1}/{len(translated_df)}")
            translated_column.append(translate_text(text))
        translated_df[col] = translated_column
    else:
        print(f"⚠️ Column '{col}' not found in the Excel file.")

# Save the translated data
translated_df.to_excel(OUTPUT_FILE, index=False)
print(f"\n✅ Translation complete. Saved to:\n{OUTPUT_FILE}")
