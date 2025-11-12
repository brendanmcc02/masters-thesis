import pandas as pd


def filter_data(input_file, output_file):
    input_df = pd.read_csv(input_file, sep="\t")
    
    output_df = input_df.groupby('RIASEC Element Name')['Basic Interests Element Name'].apply(
        lambda x: ", ".join(x.astype(str))
    ).reset_index(name='Basic Interest Element Names')

    output_df.to_csv(output_file, index=False, sep="\t")


filter_data("raw-basic-interests-to-riasec.tsv", "basic-interests-to-riasec.tsv")
