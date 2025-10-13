# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses

import pandas as pd
import numpy as np


def process_csv_data(input_file, output_file):
    try:
        df = pd.read_csv(input_file, sep='\t', dtype={'major': str}, low_memory=False)
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    education_filter = (df['education'] == 2) | (df['education'] == 3) | (df['education'] == 4)
    
    major_non_empty_filter = ~df['major'].fillna('').str.strip().eq('')

    final_filter = education_filter & major_non_empty_filter

    df_filtered = df[final_filter].copy()

    columns_to_keep = ['education'] + ['major']

    missing_cols = [col for col in columns_to_keep if col not in df_filtered.columns]
    if missing_cols:
        print(f"Warning: The following required columns are missing and will be skipped: {missing_cols}")
        columns_to_keep = [col for col in columns_to_keep if col in df_filtered.columns]

    prefixes = ['R', 'I', 'A', 'S', 'E', 'C']
    for prefix in prefixes[::-1]:
        score_cols = [col for col in df_filtered.columns if col.startswith(prefix) and col[1:].isdigit()]
        
        if score_cols:
            df_filtered[prefix] = df_filtered[score_cols].mean(axis=1)
            columns_to_keep.insert(0, prefix)

    row_min = df_filtered[prefixes].min(axis=1)
    row_max = df_filtered[prefixes].max(axis=1)
    row_range = row_max - row_min
    
    for col in prefixes:
        df_filtered[col] = np.where(
            row_range == 0, 
            0.0,            
            (df_filtered[col] - row_min) / row_range
        )

        df_filtered[col] = round(df_filtered[col], 3)

    education_map = {
        2: 'High School',
        3: 'Undergraduate Degree',
        4: 'Postgraduate degree'
    }
    df_filtered['education'] = df_filtered['education'].astype(int).replace(education_map)

    df_output = df_filtered[columns_to_keep]
    df_output.to_csv(output_file, index=False, sep='\t')

process_csv_data("data.tsv", "filtered.tsv")