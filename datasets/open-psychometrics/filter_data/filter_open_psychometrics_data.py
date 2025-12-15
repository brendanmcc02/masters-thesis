# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd
from filter_open_psychometrics_data_utils import *

df = pd.read_csv('raw_riasec_college_majors.tsv', sep='\t', low_memory=False)

non_empty_major_filter = ~(df['major'].fillna('').eq(''))
df = df[non_empty_major_filter].copy()

HTML_ENTITY_REGEX = r'&#[0-9]+;'
df = df[~df['major'].str.contains(HTML_ENTITY_REGEX, regex=True)].copy()

print("text preprocessing on riasec dataset")
df['major_preprocessed'] = df['major'].apply(preprocess_text)
df['major_category'] = ''

non_empty_major_preprocessed_filter = ~(df['major_preprocessed'].fillna('').eq(''))
df = df[non_empty_major_preprocessed_filter].copy()

HOLLAND_CODE_PREFIXES = ['R', 'I', 'A', 'S', 'E', 'C']
NUMBER_OF_QUESTIONS_PER_VOCATIONAL_INTEREST = 8
holland_code_columns = []
for prefix in HOLLAND_CODE_PREFIXES:
    for i in range(1, NUMBER_OF_QUESTIONS_PER_VOCATIONAL_INTEREST+1):
        holland_code_columns.append(prefix + str(i))

filtered_columns = []
for column in holland_code_columns:
        filtered_columns.append(column)
        # some RIASEC questions have 0 as an answer,
        # i'm assuming this should be 1 (dislike), 
        # but honestly i'n not sure,
        # maybe it should be put down as 3 (neutral) instead.
        # the readme doesn't say anything about it.
        # all values should range from 1=dislike, 3=neutral, 5=like
        df[column] = df[column].replace(0, 1)
        # adjust the scale from 1-5 to 0-4
        df[column] -= 1

filtered_columns.insert(0, 'major_category')
filtered_columns.insert(1, 'major_preprocessed')
filtered_columns.insert(2, 'major')

df = df[filtered_columns].rename(columns={'major':'major_original'}) 

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

print("fuzzy match for majors and major categories")

dirty_df['major_category'] = dirty_df['major_preprocessed'].apply(fuzzy_match, college_majors_and_categories=list(college_majors) + list(college_major_categories), major_to_major_category_dict=major_to_major_category_dict)

has_fuzzy_match_mask = dirty_df['major_category'].str.len() > 0

clean_df_to_append = dirty_df[has_fuzzy_match_mask].copy()
clean_df = pd.concat([clean_df, clean_df_to_append], ignore_index=True)

dirty_df = dirty_df[~has_fuzzy_match_mask].copy()


clean_df = reverse_college_major_category_preprocessing(clean_df, unique_college_major_categories)
clean_df.to_csv("../clean_riasec_college_major_categories.tsv", sep='\t', index=False)

aggregated_major_categories_df = get_aggregated_college_major_categories_df(clean_df, holland_code_columns, HOLLAND_CODE_PREFIXES)
aggregated_major_categories_df.to_csv("../clean_aggregated_riasec_college_major_categories.tsv", sep='\t', index=False)

dirty_df = dirty_df.sort_values(by=['major_preprocessed'])
dirty_df.to_csv("dirty_riasec_college_majors.tsv", sep='\t', index=False)


