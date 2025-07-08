import pandas as pd
import fitz  # PyMuPDF
import requests
import os
from pathlib import Path

# --- Setup ---
input_excel = "University_of_Jordan_Links.xlsx"
output_excel = "University_of_Jordan_PDF_Texts.xlsx"
download_folder = "temp_pdfs"
os.makedirs(download_folder, exist_ok=True)

# --- PDF Text Extractor ---
def read_pdf_by_page(file_path):
    """Extract text from each page and return a list of strings."""
    doc = fitz.open(file_path)
    return [page.get_text() for page in doc]

# --- Load Excel ---
df = pd.read_excel(input_excel)

# --- Extract Texts ---
all_rows = []
for index, row in df.iterrows():
    url = row["Link"]
    filename = os.path.join(download_folder, f"doc_{index}.pdf")
    
    # Download PDF
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Downloaded: {filename}")
        else:
            print(f"❌ Failed to download PDF at index {index}")
            continue
    except Exception as e:
        print(f"❌ Error downloading PDF: {e}")
        continue

    # Extract text from pages
    try:
        pages = read_pdf_by_page(filename)
        for page_num, page_text in enumerate(pages, 1):
            all_rows.append({
                "Main School": row.get("Main School", ""),
                "Specific School": row.get("Specific School", ""),
                "Department": row.get("Department", ""),
                "PDF URL": url,
                "Page Number": page_num,
                "Page Text": page_text
            })
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        continue

# --- Export to Excel ---
output_df = pd.DataFrame(all_rows)
with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
    output_df.to_excel(writer, index=False, sheet_name='PDF Pages')
    worksheet = writer.sheets['PDF Pages']
    worksheet.set_column('F:F', 100)  # Page Text column
    worksheet.set_default_row(100)    # Set row height

print(f"\n✅ Finished: Extracted PDF texts saved to {output_excel}")
