# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd
from utils import *
import fuzzywuzzy

try:
    df = pd.read_csv('raw_riasec_college_majors.tsv', sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')

undergrad_or_postgrad_filter = (df['education'] == 3) | (df['education'] == 4)
df = df[undergrad_or_postgrad_filter].copy()

non_empty_major_filter = ~(df['major'].fillna('').eq(''))
df = df[non_empty_major_filter].copy()

HTML_ENTITY_REGEX = r'&#[0-9]+;'
df = df[~df['major'].str.contains(HTML_ENTITY_REGEX, regex=True)].copy()

print("preprocessing riasec dataset")
df['major_preprocessed'] = df['major'].apply(preprocess_text)

dirty_college_major_filter = (df['major_preprocessed'] != 'ye') & (df['major_preprocessed'] != 'no') & (df['major_preprocessed'] != 'na') & (df['major_preprocessed'] != 'none') & (df["major_preprocessed"] != "know") & (df["major_preprocessed"] != "idk") & (df["major_preprocessed"] != "non") & (df['major_preprocessed'] != 'other') & (df['major_preprocessed'] != 'multipl')
df = df[dirty_college_major_filter].copy()

non_empty_major_preprocessed_filter = ~(df['major_preprocessed'].fillna('').eq(''))
df = df[non_empty_major_preprocessed_filter].copy()

# some RIASEC questions have 0 as an answer
# this shouldn't be possible, should be 1=dislike, 3=neutral, 5=like
NUMBER_OF_QUESTIONS_PER_TAXONOMY = 8
holland_code_prefixes = ['R', 'I', 'A', 'S', 'E', 'C']
for prefix in holland_code_prefixes:
    for i in range(1, NUMBER_OF_QUESTIONS_PER_TAXONOMY+1):
        column = prefix + str(i)
        df[column] = df[column].replace(0, 1)

print("calculating means of RIASEC")
filtered_columns = []
MAX_QUESTION_VALUE = 5
for prefix in holland_code_prefixes[::-1]:
    score_cols = [col for col in df.columns if col.startswith(prefix) and col[1:].isdigit()]
    
    if score_cols:
        df[prefix] = (df[score_cols].mean(axis=1) - 1) / (MAX_QUESTION_VALUE - 1)  # normalize
        filtered_columns.insert(0, prefix)

filtered_columns.insert(0, 'major_preprocessed')
filtered_columns.insert(1, 'major')
riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
df = df[filtered_columns].rename(columns={'R':riasec_types[0], 'I':riasec_types[1], 'A':riasec_types[2], 'S':riasec_types[3], 'E':riasec_types[4], 'C':riasec_types[5], 'major':'major_original'})

non_empty_major_preprocessed_filter = ~(df['major_preprocessed'].fillna('').eq(''))
df = df[non_empty_major_preprocessed_filter].copy()

df = df.sort_values(by=['major_preprocessed'])

#df.to_csv("test.tsv", sep='\t', index=False)

try:
    college_majors_df = pd.read_csv("filtered_college_majors_2012_usa.tsv", sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')

college_majors_df['college_major'] = college_majors_df['college_major'].apply(preprocess_text)
college_majors_df['college_major_category'] = college_majors_df['college_major_category'].apply(preprocess_text)

college_majors_and_college_major_categories = set(
    college_majors_df["college_major_category"].unique().tolist() +
    college_majors_df["college_major"].unique().tolist()
)

# exact matches
print("finding exact matches with pre-existing college majors dataset")
is_defined_college_major = df['major_preprocessed'].isin(college_majors_and_college_major_categories)

clean_df = df[is_defined_college_major].copy()
dirty_df = df[~is_defined_college_major].copy()




# dirty_df['major'] = dirty_df['major'].replace(college_major_mapping_dict)
# college_major_mapping_values_set = set(college_major_mapping_dict.values())
# is_mapped_filter = dirty_df['major'].isin(college_major_mapping_values_set)

# mapped_df = dirty_df[is_mapped_filter].copy()
# clean_df = pd.concat([clean_df, mapped_df], ignore_index=True)
# dirty_df = dirty_df[~is_mapped_filter].copy()

clean_df.to_csv("clean_riasec_college_majors.tsv", sep='\t', index=False)
dirty_df.to_csv("dirty_riasec_college_majors.tsv", sep='\t', index=False)

