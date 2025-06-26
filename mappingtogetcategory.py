import pandas as pd

# Load your combined_unique_skills DataFrame
# Example only if needed:
# combined_unique_skills = pd.DataFrame({
#     "Hard_skills": ["Python", "Data Analysis", "Project Management"],
#     "Soft_skills": ["Communication", "Teamwork", "Problem Solving"]
# })

# Load EMSI hierarchy Excel file
emsi_file = r"C:\Users\10265480\Downloads\skill_emsi_hard_hierarchy.xlsx"
combined_unique_skills = pd.read_excel("combined_unique_skills.xlsx")
emsi_df = pd.read_excel(emsi_file)

# Normalize EMSI 'name' column
emsi_df["name"] = emsi_df["name"].astype(str).str.strip().str.lower()

# Melt the combined DataFrame
melted_skills = combined_unique_skills.melt(
    var_name="skill_type",
    value_name="name"
).dropna()

# Normalize skill names for matching
melted_skills["name"] = melted_skills["name"].astype(str).str.strip().str.lower()

# Clean skill_type to "Hard" or "Soft"
melted_skills["skill_type"] = melted_skills["skill_type"].str.replace("_skills", "", case=False)

# Perform left join with EMSI hierarchy
enriched_skills = melted_skills.merge(
    emsi_df[["name", "category", "category_id"]],
    how="left",
    on="name"
)

# Reorder and reset index
enriched_skills = enriched_skills[["name", "skill_type", "category", "category_id"]].reset_index(drop=True)

# Save to Excel
enriched_skills.to_excel("skills_with_type_and_category.xlsx", index=False)
