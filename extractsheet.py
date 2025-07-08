import pandas as pd

# Load the Excel file
file_path = "Jordanian Universities.xlsx"  # Replace with your local path
df = pd.read_excel(file_path, sheet_name="University of Jordan")

# Save to a new Excel file
df.to_excel("University_of_Jordan_Links.xlsx", index=False)
