# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd
# import fuzzywuzzy


try:
    df = pd.read_csv('raw_riasec_college_majors.tsv', sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')

undergrad_or_postgrad_filter = (df['education'] == 3) | (df['education'] == 4)
df = df[undergrad_or_postgrad_filter]

df['major'] = df['major'].str.strip().str.lower()

non_empty_major_filter = ~(df['major'].fillna('').eq(''))
df = df[non_empty_major_filter]

dirty_college_major_filter = ~( (df['major'] == 'yes') | (df['major'] == 'no') | (df['major'] == 'na') | (df['major'] == 'none') | (df["major"] == "do not know") | (df["major"] == "dont know") | (df["major"] == "idk") | (df["major"] == "n. a."))
df = df[dirty_college_major_filter]

filtered_columns = []

holland_code_prefixes = ['R', 'I', 'A', 'S', 'E', 'C']
for prefix in holland_code_prefixes[::-1]:
    score_cols = [col for col in df.columns if col.startswith(prefix) and col[1:].isdigit()]
    
    if score_cols:
        df[prefix] = (df[score_cols].mean(axis=1) - 1) / 4  # normalize mean between 0.0 and 1.0
        filtered_columns.insert(0, prefix)

filtered_columns.insert(0, 'major')
riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
df = df[filtered_columns].rename(columns={'R':riasec_types[0], 'I':riasec_types[1], 'A':riasec_types[2], 'S':riasec_types[3], 'E':riasec_types[4], 'C':riasec_types[5]})

# TODO dual major?

try:
    college_majors_df = pd.read_csv("filtered_college_majors_2012_usa.tsv", sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')

college_major_categories = college_majors_df["College Major Category"].unique()
college_majors = college_majors_df["College Major"].tolist()

college_majors_and_college_major_categories = set()
for c in college_major_categories:
    college_majors_and_college_major_categories.add(c)

for c in college_majors:
    college_majors_and_college_major_categories.add(c)

is_clean_college_major = df['major'].isin(college_majors_and_college_major_categories)

clean_df = df[is_clean_college_major].copy()
dirty_df = df[~is_clean_college_major].copy()

clean_df.to_csv("clean_riasec_college_majors.tsv", sep='\t', index=False)
dirty_df.to_csv("dirty_riasec_college_majors.tsv", sep='\t', index=False)
