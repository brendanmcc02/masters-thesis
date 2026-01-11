import pandas as pd

df = pd.read_csv("ratings.csv", low_memory=False)

cols = ["Name", "Year", "Rating"]
df = df[cols].copy()

df.to_csv("ratings.csv", index=False)
