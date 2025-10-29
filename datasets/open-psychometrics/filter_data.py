# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd
# from spellchecker import SpellChecker # run venv: `python3 -m venv open-psychometrics-venv && source open-psychometrics-venv/bin/activate`


try:
    df = pd.read_csv('raw_riasec_college_majors.tsv', sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')
    exit

undergrad_or_postgrad_filter = (df['education'] == 3) | (df['education'] == 4)
df = df[undergrad_or_postgrad_filter]

df['major'] = df['major'].str.strip().str.lower()

non_empty_major_filter = ~(df['major'].fillna('').eq(''))
df = df[non_empty_major_filter]

dirty_college_major_filter = ~( (df['major'] == 'yes') | (df['major'] == 'no') | (df['major'] == 'na') | (df['major'] == 'none'))
df = df[dirty_college_major_filter]

# spell_checker = SpellChecker()
# df['major'] = df['major'].apply(spell_checker.correction)

filtered_columns = ['major']

holland_code_prefixes = ['R', 'I', 'A', 'S', 'E', 'C']
for prefix in holland_code_prefixes[::-1]:
    score_cols = [col for col in df.columns if col.startswith(prefix) and col[1:].isdigit()]
    
    if score_cols:
        df[prefix] = (df[score_cols].mean(axis=1) - 1) / 4  # normalize mean between 0.0 and 1.0
        filtered_columns.insert(0, prefix)

riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
df = df[filtered_columns].rename(columns={'major': 'College Major', 'R':riasec_types[0], 'I':riasec_types[1], 'A':riasec_types[2], 'S':riasec_types[3], 'E':riasec_types[4], 'C':riasec_types[5]})

# TODO split out columns with mutliple college majors


df = df.groupby('College Major')[riasec_types].mean().reset_index()

df.to_csv('filtered_riasec_college_majors.tsv', index=False, sep='\t')