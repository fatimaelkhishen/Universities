import pandas as pd
from collections import defaultdict

# Define paths to the Excel files
file_paths = [
    "University_of_Jordan_Skills_Report.xlsx",
    "Jordan_TVET_with_skills(EMSI)_Report.xlsx",
    "AjlounUNiv_with_skills_Report.xlsx"
]

# Combine data
combined_skills = defaultdict(lambda: {"Count": 0, "Type": set()})

for file_path in file_paths:
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        skill = row["Skill"].strip()
        count = int(row["Count"])
        skill_type = row["Type"]

        combined_skills[skill]["Count"] += count
        combined_skills[skill]["Type"].add(skill_type)

# Final results
final_data = []
for skill, info in combined_skills.items():
    # Determine final skill type
    types = info["Type"]
    final_type = "Both" if len(types) > 1 or "Both" in types else next(iter(types))
    final_data.append({"Skill": skill, "Type": final_type, "Count": info["Count"]})

# Create and export DataFrame
combined_df = pd.DataFrame(final_data).sort_values(by="Count", ascending=False)
combined_df.to_excel("Combined_Skills_Report.xlsx", index=False)
print("Combined skills report saved as Combined_Skills_Report.xlsx")
