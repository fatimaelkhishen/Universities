import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
import torch

# ==== CONFIGURATION ====
INPUT_FILE = "Toutes_les_formations_ESIB_by_page.xlsx"
OUTPUT_FILE = "Toutes_les_formations_ESIB_by_page_translated.xlsx"

# MarianMT model for French to English translation
model_name = "Helsinki-NLP/opus-mt-fr-en"

# Load model and tokenizer
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def translate_text(text):
    # Skip or return original if not a string
    if not isinstance(text, str):
        return text

    # Tokenize input properly with current recommended method
    inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True).to(device)

    # Generate translation output ids
    outputs = model.generate(**inputs)

    # Decode translated text
    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    return translated_text

# Load Excel file
df = pd.read_excel(INPUT_FILE, engine="openpyxl")
translated_df = df.copy()

# Translate headers
print("🔤 Translating column headers...")
translated_columns = {}
for col in df.columns:
    translated_col = translate_text(col)
    print(f"{col} → {translated_col}")
    translated_columns[col] = translated_col
translated_df.rename(columns=translated_columns, inplace=True)

# Translate each cell in all columns
for col in translated_df.columns:
    print(f"🌐 Translating column: {col}")
    translated_df[col] = translated_df[col].apply(translate_text)

# Save translated Excel
translated_df.to_excel(OUTPUT_FILE, index=False)
print(f"\n✅ Translated Excel saved as: {OUTPUT_FILE}")
