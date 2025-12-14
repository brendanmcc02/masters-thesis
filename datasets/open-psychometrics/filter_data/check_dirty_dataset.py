import pandas as pd

dirty_df = pd.read_csv('dirty_riasec_college_majors.tsv', sep='\t', low_memory=False)

MIN_COLLEGE_MAJOR_PREPROCESSED_FREQUENCY = 100

value_counts = dirty_df['major_preprocessed'].value_counts()

frequent_values_series = value_counts[value_counts >= MIN_COLLEGE_MAJOR_PREPROCESSED_FREQUENCY]

# turn the old index (the major name) into a column.
frequent_dirty_college_major_preprocessed_df = frequent_values_series.reset_index()
frequent_dirty_college_major_preprocessed_df.columns = ['major_preprocessed', 'count']
frequent_dirty_college_major_preprocessed_df = frequent_dirty_college_major_preprocessed_df.sort_values(by='count', ascending=False)

frequent_dirty_college_major_preprocessed_df.to_csv('frequent_dirty_college_major_preprocessed.tsv', sep='\t', index=False)
