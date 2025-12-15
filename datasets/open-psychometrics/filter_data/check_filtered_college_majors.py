import pandas as pd
from filter_open_psychometrics_data_utils import preprocess_text

clean_df = pd.read_csv('../clean_riasec_college_major_categories.tsv', sep='\t', low_memory=False)

college_majors_and_categories_df = pd.read_csv('filtered_college_majors_2012_usa.tsv', sep='\t', low_memory=False)

college_majors_and_categories_df["college_major_preprocessed"] = college_majors_and_categories_df["college_major"].apply(preprocess_text)

exact_college_major_matches_df = clean_df[clean_df['major_preprocessed'].isin(college_majors_and_categories_df["college_major_preprocessed"])].copy()

major_counts_series = exact_college_major_matches_df['major_preprocessed'].value_counts()
complete_major_counts_series = major_counts_series.reindex(
    college_majors_and_categories_df["college_major_preprocessed"], 
    fill_value=0
)
major_counts_df = complete_major_counts_series.reset_index()
major_counts_df = major_counts_df.merge(
    college_majors_and_categories_df[['college_major', 'college_major_preprocessed']].drop_duplicates(),
    on='college_major_preprocessed',
    how='left' # Use 'left' to keep all counts, even if a preprocessed major matches multiple original majors (which should be rare)
)

major_counts_df = major_counts_df.sort_values(by='count', ascending=True)
major_counts_df.to_csv('exact_college_major_matches_frequencies.tsv', sep='\t', index=False)
