import pandas as pd

def generate_columns_to_keep():
    prefixes = ['R', 'I', 'A', 'S', 'E', 'C']
    data_columns = [p + str(i) for p in prefixes for i in range(1, 9)]
    
    return data_columns + ['education'] + ['major']

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

    columns_to_keep = generate_columns_to_keep()
    
    missing_cols = [col for col in columns_to_keep if col not in df_filtered.columns]
    if missing_cols:
        print(f"Warning: The following required columns are missing and will be skipped: {missing_cols}")
        columns_to_keep = [col for col in columns_to_keep if col in df_filtered.columns]

    df_output = df_filtered[columns_to_keep]
    df_output.to_csv(output_file, index=False)

process_csv_data("data.tsv", "filtered.csv")