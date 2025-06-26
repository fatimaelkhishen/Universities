import pandas as pd

# File names
files = [
    'usj_output_with_skills.xlsx',
    'Toutes_les_formations_ESIB_by_page_translated_with_skills.xlsx',
    'CAtalogue - master data science - USJ_paragraphs_with_skills.xlsx'
]

hard_skills_set = set()
soft_skills_set = set()

# Function to safely extract skills
def extract_skills(series):
    skills_set = set()
    for entry in series.dropna():
        entry_str = str(entry)
        skills = [s.strip() for s in entry_str.split(',') if s.strip()]
        skills_set.update(skills)
    return skills_set

# Read and process each file
for file in files:
    df = pd.read_excel(file)
    
    if 'Hard_skills' in df.columns:
        hard_skills_set.update(extract_skills(df['Hard_skills']))
    
    if 'Soft_skills' in df.columns:
        soft_skills_set.update(extract_skills(df['Soft_skills']))

# Align lengths
max_len = max(len(hard_skills_set), len(soft_skills_set))
hard_skills_list = list(hard_skills_set) + [''] * (max_len - len(hard_skills_set))
soft_skills_list = list(soft_skills_set) + [''] * (max_len - len(soft_skills_set))

# Create output DataFrame
output_df = pd.DataFrame({
    'Hard_skills': hard_skills_list,
    'Soft_skills': soft_skills_list
})

# Save to Excel
output_df.to_excel('combined_unique_skills.xlsx', index=False)

print("✅ Unique skills saved to 'combined_unique_skills.xlsx'")
