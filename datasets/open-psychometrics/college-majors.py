import pandas as pd

try:
    df = pd.read_csv("raw_college_majors_2012_usa.csv", low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')
    exit


df = df.rename(columns={"Major": "College Major", "Major_Category": "College Major Category"})

na_filter = (df["College Major"] != "N/A (less than bachelor's degree)")
df = df[na_filter]

df["College Major"] = df["College Major"].str.strip().str.lower()
df["College Major Category"] = df["College Major Category"].str.strip().str.lower()

df = df.filter(items=["College Major", "College Major Category"])
df.to_csv("filtered_college_majors_2012_usa.csv", index=False)

df = df.filter(items=["College Major Category"])

unique_major_categories = df["College Major Category"].unique()

df_unique_majors = pd.DataFrame(unique_major_categories, columns=['College_Major_Categories'])
df_unique_majors.to_csv("filtered_college_major_categories_2012_usa.csv", index=False)