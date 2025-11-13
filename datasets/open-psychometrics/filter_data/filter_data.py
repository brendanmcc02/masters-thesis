# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd
from utils import *

df = pd.read_csv('raw_riasec_college_majors.tsv', sep='\t', low_memory=False)

# education level of 2 = high school educated,
# technically shouldn't include this, 
# but it increases the final dataset size by ~30k
# either:
# 1. the person didn't go to college, but in the field they put down their current profession
# 2. the person was college-educated but put down high-school educated (unlikely but possible)
undergrad_or_postgrad_filter = (df['education'] == 2) |(df['education'] == 3) | (df['education'] == 4)
df = df[undergrad_or_postgrad_filter].copy()

non_empty_major_filter = ~(df['major'].fillna('').eq(''))
df = df[non_empty_major_filter].copy()

HTML_ENTITY_REGEX = r'&#[0-9]+;'
df = df[~df['major'].str.contains(HTML_ENTITY_REGEX, regex=True)].copy()

print("text preprocessing on riasec dataset")
df['major_preprocessed'] = df['major'].apply(preprocess_text)
df['major_category'] = ''

non_empty_major_preprocessed_filter = ~(df['major_preprocessed'].fillna('').eq(''))
df = df[non_empty_major_preprocessed_filter].copy()

NUMBER_OF_QUESTIONS_PER_VOCATIONAL_INTEREST = 8
holland_code_prefixes = ['R', 'I', 'A', 'S', 'E', 'C']
for prefix in holland_code_prefixes:
    for i in range(1, NUMBER_OF_QUESTIONS_PER_VOCATIONAL_INTEREST+1):
        column = prefix + str(i)
        # some RIASEC questions have 0 as an answer,
        # but all values should range from 1=dislike, 3=neutral, 5=like
        df[column] = df[column].replace(0, 1)
        # adjust the scale from 1-5 to 0-4
        df[column] -= 1

filtered_columns = []
MAX_QUESTION_VALUE = 4
for prefix in holland_code_prefixes[::-1]:
    score_cols = [col for col in df.columns if col.startswith(prefix) and col[1:].isdigit()]
    
    if score_cols:
        df[prefix] = df[score_cols].mean(axis=1) / MAX_QUESTION_VALUE # normalize
        filtered_columns.insert(0, prefix)

filtered_columns.insert(0, 'major_category')
filtered_columns.insert(1, 'major_preprocessed')
filtered_columns.insert(2, 'major')
riasec_types = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
df = df[filtered_columns].rename(columns={'R':riasec_types[0], 'I':riasec_types[1], 'A':riasec_types[2], 'S':riasec_types[3], 'E':riasec_types[4], 'C':riasec_types[5], 'major':'major_original'}) 

non_empty_major_preprocessed_filter = ~(df['major_preprocessed'].fillna('').eq(''))
df = df[non_empty_major_preprocessed_filter].copy()

college_majors_and_categories_df = pd.read_csv("filtered_college_majors_2012_usa.tsv", sep='\t', low_memory=False)

print("exact college major category match")

unique_college_major_categories = college_majors_and_categories_df["college_major_category"].unique()
college_majors_and_categories_df['college_major_category'] = college_majors_and_categories_df['college_major_category'].apply(preprocess_text)
unique_college_major_categories_preprocessed = college_majors_and_categories_df["college_major_category"].unique()
college_major_categories = set(unique_college_major_categories_preprocessed.tolist())
is_defined_college_major_category = df['major_preprocessed'].isin(college_major_categories)

clean_df = df[is_defined_college_major_category].copy()
clean_df['major_category'] = clean_df['major_preprocessed']
dirty_df = df[~is_defined_college_major_category].copy()

print("exact college major match")

college_majors_and_categories_df['college_major'] = college_majors_and_categories_df['college_major'].apply(preprocess_text)

college_majors = set(college_majors_and_categories_df["college_major"].unique().tolist())
is_defined_college_major = dirty_df['major_preprocessed'].isin(college_majors)

clean_df_to_append = dirty_df[is_defined_college_major].copy()
dirty_df = dirty_df[~is_defined_college_major].copy()

major_to_major_category_dict = college_majors_and_categories_df.set_index('college_major')['college_major_category'].to_dict()

clean_df_to_append['major_category'] = clean_df_to_append['major_preprocessed'].map(major_to_major_category_dict).fillna(clean_df_to_append['major_category'])
clean_df = pd.concat([clean_df, clean_df_to_append], ignore_index=True)

print("substring match for majors")
dirty_df['major_category'] = dirty_df['major_preprocessed'].apply(get_substring_matches, college_majors=college_majors, major_to_major_category_dict=major_to_major_category_dict)
has_substring_match_mask = dirty_df['major_category'].str.len() > 0

clean_df_to_append = dirty_df[has_substring_match_mask].copy()
clean_df_to_append = clean_df_to_append.explode('major_category', ignore_index=True)
clean_df = pd.concat([clean_df, clean_df_to_append], ignore_index=True)

dirty_df = dirty_df[~has_substring_match_mask].copy()

print("fuzzy match for majors and major categories")
dirty_df['major_category'] = dirty_df['major_preprocessed'].apply(fuzzy_match, college_majors_and_categories=list(college_majors) + list(college_major_categories), major_to_major_category_dict=major_to_major_category_dict)

has_fuzzy_match_mask = dirty_df['major_category'].str.len() > 0

clean_df_to_append = dirty_df[has_fuzzy_match_mask].copy()
clean_df = pd.concat([clean_df, clean_df_to_append], ignore_index=True)

dirty_df = dirty_df[~has_fuzzy_match_mask].copy()

# reverse pre-processing for final output
reverse_preprocessed_college_major_category_dict = {}
for unique_college_major_category in unique_college_major_categories:
    reverse_preprocessed_college_major_category_dict[preprocess_text(unique_college_major_category)] = unique_college_major_category

clean_df['major_category'] = clean_df['major_category'].map(reverse_preprocessed_college_major_category_dict).fillna(clean_df['major_category'])

clean_df = clean_df.sort_values(by=['major_category'])
clean_df.to_csv("../clean_riasec_college_majors.tsv", sep='\t', index=False)

aggregated_major_categories_df = clean_df.groupby('major_category')[riasec_types].mean().round(4).reset_index()
aggregated_major_categories_df = aggregated_major_categories_df[['major_category']+riasec_types]
aggregated_major_categories_df.to_csv("../clean_aggregated_riasec_college_major_categories.tsv", sep='\t', index=False)

dirty_df = dirty_df.sort_values(by=['major_preprocessed'])
dirty_df.to_csv("dirty_riasec_college_majors.tsv", sep='\t', index=False)

# # TODO - aggregated
# filtered_columns = []
# MAX_QUESTION_VALUE = 4
# for prefix in holland_code_prefixes[::-1]:
#     score_cols = [col for col in df.columns if col.startswith(prefix) and col[1:].isdigit()]
    
#     if score_cols:
#         df[prefix] = df[score_cols].mean(axis=1) / MAX_QUESTION_VALUE # normalize
#         filtered_columns.insert(0, prefix)
##
