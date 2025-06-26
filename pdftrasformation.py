import fitz  # PyMuPDF
import pandas as pd

def read_pdf_by_page(file_path):
    """Extract text from each page and return a list of strings."""
    doc = fitz.open(file_path)
    pages_text = []
    for i, page in enumerate(doc):
        page_text = page.get_text()
        print(f"Page {i+1}: {len(page_text)} characters extracted.")
        pages_text.append(page_text)
    return pages_text

# Set your actual PDF path
pdf_path = r"C:\Users\10265480\Desktop\Toutes les formations ESIB.pdf"

# Extract text page-by-page
all_pages_text = read_pdf_by_page(pdf_path)

# Create a DataFrame: one row per page
df = pd.DataFrame({
    "Page Number": list(range(1, len(all_pages_text) + 1)),
    "Page Text": all_pages_text
})

# Export to Excel with formatting
output_file = "Toutes_les_formations_ESIB_by_page.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='PDF Pages')
    worksheet = writer.sheets['PDF Pages']
    worksheet.set_column('B:B', 100)  # Widen text column
    worksheet.set_default_row(100)    # Set row height for readability

print(f"\n✅ Each page has been saved in a separate row in: {output_file}")