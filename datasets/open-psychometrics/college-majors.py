# NOTE: many manual changes have been made to this dataset AFTER this script has been run!
# please git checkout to fb61ac1 to find the manually changes!
import pandas as pd

df = pd.read_csv("raw_college_majors_2012_usa.csv", low_memory=False)

df = df.rename(columns={"Major": "College Major", "Major_Category": "College Major Category"})

na_filter = (df["College Major"] != "N/A (less than bachelor's degree)")
df = df[na_filter]

df["College Major"] = df["College Major"].str.strip().str.lower()
df["College Major Category"] = df["College Major Category"].str.strip().str.lower()

df = df.filter(items=["College Major", "College Major Category"])
# df.to_csv("filtered_college_majors_2012_usa.tsv", sep='\t', index=False)