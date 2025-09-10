import pandas as pd
from collections import Counter

# Load the Excel file
input_path = r"C:\Users\10265480\Desktop\Data\Jordan_TVET_with_skills(EMSI).xlsx"  # Adjust the path if needed
df = pd.read_excel(input_path, sheet_name="Sheet1")

# Collect all hard and soft skills
all_hard_skills = []
all_soft_skills = []

for skills in df["Hard_skills"].dropna():
    all_hard_skills.extend([skill.strip() for skill in skills.split(",") if skill.strip()])

for skills in df["Soft_skills"].dropna():
    all_soft_skills.extend([skill.strip() for skill in skills.split(",") if skill.strip()])

# Count them
hard_counter = Counter(all_hard_skills)
soft_counter = Counter(all_soft_skills)

# Combine results
all_skills_data = []

for skill, count in hard_counter.items():
    all_skills_data.append({"Skill": skill, "Type": "Hard", "Count": count})

for skill, count in soft_counter.items():
    existing = next((s for s in all_skills_data if s["Skill"] == skill), None)
    if existing:
        existing["Type"] = "Both"
        existing["Count"] += count
    else:
        all_skills_data.append({"Skill": skill, "Type": "Soft", "Count": count})

# Create DataFrame and sort
skills_df = pd.DataFrame(all_skills_data)
skills_df = skills_df.sort_values(by="Count", ascending=False)

# Save to Excel
output_path = "Jordan_TVET_with_skills(EMSI)_Report.xlsx"
skills_df.to_excel(output_path, index=False)
print(f"Skills report saved to {output_path}")
