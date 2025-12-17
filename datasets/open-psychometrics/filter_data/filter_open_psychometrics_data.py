# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd
from filter_open_psychometrics_data_utils import *

df = pd.read_csv('raw_riasec_college_majors.tsv', sep='\t', low_memory=False)

non_empty_major_filter = ~(df['college_major'].fillna('').eq(''))
df = df[non_empty_major_filter].copy()

HTML_ENTITY_REGEX = r'&#[0-9]+;'
df = df[~df['college_major'].str.contains(HTML_ENTITY_REGEX, regex=True)].copy()

print("text preprocessing")
df['college_major_preprocessed'] = df['college_major'].apply(preprocess_text)
df['college_major_category'] = ''

non_empty_college_major_preprocessed_filter = ~(df['college_major_preprocessed'].fillna('').eq(''))
df = df[non_empty_college_major_preprocessed_filter].copy()

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

filtered_columns.insert(0, 'college_major_category')
filtered_columns.insert(1, 'college_major_preprocessed')
filtered_columns.insert(2, 'college_major')

df = df[filtered_columns].copy()

non_empty_college_major_preprocessed_filter = ~(df['college_major_preprocessed'].fillna('').eq(''))
df = df[non_empty_college_major_preprocessed_filter].copy()

college_majors_and_major_categories_df = pd.read_csv("college_majors_and_major_categories.tsv", sep='\t', low_memory=False)

print("exact college major category match")

unique_college_major_categories = college_majors_and_major_categories_df["college_major_category"].unique()
college_majors_and_major_categories_df['college_major_category_preprocessed'] = college_majors_and_major_categories_df['college_major_category'].apply(preprocess_text)
unique_college_major_categories_preprocessed = college_majors_and_major_categories_df["college_major_category_preprocessed"].unique()
college_major_categories_preprocessed = set(unique_college_major_categories_preprocessed.tolist())
is_exact_match_college_major_category = df['college_major_preprocessed'].isin(college_major_categories_preprocessed)

clean_df = df[is_exact_match_college_major_category].copy()
clean_df['college_major_category'] = clean_df['college_major_preprocessed']
dirty_df = df[~is_exact_match_college_major_category].copy()

print("exact college major match")

college_majors_and_major_categories_df['college_major_preprocessed'] = college_majors_and_major_categories_df['college_major'].apply(preprocess_text)

college_majors_preprocessed = set(college_majors_and_major_categories_df["college_major_preprocessed"].unique().tolist())

# TEMP - check for duplicates
occurred = set()
for major in college_majors_and_major_categories_df['college_major_preprocessed']:
     if major in occurred:
          print("Duplicate preprocessed major!: " + str(major))

     occurred.add(str(major))
########

is_defined_college_major = dirty_df['college_major_preprocessed'].isin(college_majors_preprocessed)

clean_df_to_append = dirty_df[is_defined_college_major].copy()
dirty_df = dirty_df[~is_defined_college_major].copy()

preprocessed_major_to_major_category_dict = college_majors_and_major_categories_df.set_index('college_major_preprocessed')['college_major_category_preprocessed'].to_dict()

clean_df_to_append['college_major_category'] = clean_df_to_append['college_major_preprocessed'].map(preprocessed_major_to_major_category_dict).fillna(clean_df_to_append['college_major_category'])
clean_df = pd.concat([clean_df, clean_df_to_append], ignore_index=True)

# print("substring match college majors for most frequently occuring major category")

# dirty_df['college_major_category'] = dirty_df['college_major_preprocessed'].apply(get_most_frequently_occuring_college_major_category_with_substring_match, college_majors_preprocessed=college_majors_preprocessed, preprocessed_major_to_major_category_dict=preprocessed_major_to_major_category_dict)
# has_substring_match_mask = dirty_df['college_major_category'].str.len() > 0

# clean_df_to_append = dirty_df[has_substring_match_mask].copy()
# clean_df = pd.concat([clean_df, clean_df_to_append], ignore_index=True)

# dirty_df = dirty_df[~has_substring_match_mask].copy()

print("fuzzy match for majors and major categories")

dirty_df['college_major_category'] = dirty_df['college_major_preprocessed'].apply(get_fuzzy_college_major_category_match, preprocessed_college_majors_and_major_categories=list(college_majors_preprocessed) + list(college_major_categories_preprocessed), preprocessed_major_to_major_category_dict=preprocessed_major_to_major_category_dict)

has_fuzzy_match_mask = dirty_df['college_major_category'].str.len() > 0

clean_df_to_append = dirty_df[has_fuzzy_match_mask].copy()
clean_df = pd.concat([clean_df, clean_df_to_append], ignore_index=True)

dirty_df = dirty_df[~has_fuzzy_match_mask].copy()

clean_df = reverse_college_major_category_preprocessing(clean_df, unique_college_major_categories)
clean_df.to_csv("../clean_riasec_college_major_categories.tsv", sep='\t', index=False)

dirty_df = dirty_df.sort_values(by=['college_major_preprocessed'])
dirty_df.to_csv("dirty_riasec_college_majors.tsv", sep='\t', index=False)

college_major_preprocessed_counts_series = clean_df['college_major_preprocessed'].value_counts()

college_majors_and_major_categories_df['number_of_exact_college_major_matches'] = college_majors_and_major_categories_df['college_major_preprocessed'].map(college_major_preprocessed_counts_series).fillna(0).astype(int)
college_majors_and_major_categories_df = college_majors_and_major_categories_df[['college_major', 
                                                                                 'college_major_preprocessed', 
                                                                                 'number_of_exact_college_major_matches', 
                                                                                 'college_major_category', 
                                                                                 'college_major_category_preprocessed']] # re-order columns
college_majors_and_major_categories_df.to_csv('college_majors_and_major_categories.tsv', sep='\t', index=False)

# aggregated_major_categories_df = get_aggregated_college_major_categories_df(clean_df, holland_code_columns, HOLLAND_CODE_PREFIXES)
# aggregated_major_categories_df.to_csv("../clean_aggregated_riasec_college_major_categories.tsv", sep='\t', index=False)
