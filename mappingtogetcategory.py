import pandas as pd

# Load the combined unique skills file (e.g. from the previous merging step)
combined_unique_skills = pd.read_excel("Combined_Skills_Report.xlsx")

# Load the EMSI hierarchy file
emsi_df = pd.read_excel("Emsi_categories_skills.xlsx")

# Normalize EMSI skill names
emsi_df["name"] = emsi_df["name"].astype(str).str.strip().str.lower()

# Normalize the skill names in the combined file
combined_unique_skills["Skill"] = combined_unique_skills["Skill"].astype(str).str.strip().str.lower()

# Rename for join compatibility
combined_unique_skills.rename(columns={"Skill": "name", "Type": "skill_type"}, inplace=True)

# Merge with EMSI data to enrich with category info
enriched_skills = combined_unique_skills.merge(
    emsi_df[["name", "category_name", "category_id"]],
    how="left",
    on="name"
)

# Reorder columns and reset index
enriched_skills = enriched_skills[["name", "skill_type", "Count", "category_name", "category_id"]].reset_index(drop=True)

# Save the final enriched dataset to Excel
enriched_skills.to_excel("Combined_Skills_with_EMSI_Categories.xlsx", index=False)
print("Enriched skills saved as 'Combined_Skills_with_EMSI_Categories.xlsx'")
