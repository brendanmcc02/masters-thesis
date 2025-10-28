# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd


def filterData(input_file, output_file):
    try:
        df = pd.read_csv(input_file, sep="\t", low_memory=False)
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return
    
    undergrad_or_postgrad_filter = (df['education'] == 3) | (df['education'] == 4)
    df_preprocessed_majors = df[undergrad_or_postgrad_filter]

    non_empty_major_filter = ~df_preprocessed_majors["major"].fillna("").str.strip().eq("")
    df_filtered = df_preprocessed_majors[non_empty_major_filter].copy()

    filtered_columns = ["major"]

    holland_code_prefixes = ["R", "I", "A", "S", "E", "C"]
    for prefix in holland_code_prefixes[::-1]:
        score_cols = [col for col in df_filtered.columns if col.startswith(prefix) and col[1:].isdigit()]
        
        if score_cols:
            df_filtered[prefix] = (df_filtered[score_cols].mean(axis=1) - 1) / 4  # normalize mean between 0-1
            filtered_columns.insert(0, prefix)

    df_output = df_filtered[filtered_columns].rename(columns={"major": "College Major", "R":"Realistic", "I":"Investigative", "A":"Artistic", "S":"Social", "E":"Enterprising", "C":"Conventional"})
    df_output.to_csv(output_file, index=False, sep="\t")


filterData("raw_data.tsv", "filtered_data.tsv")