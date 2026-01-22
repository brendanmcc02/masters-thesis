import pandas as pd

df = pd.read_csv("user_interest_questions.csv")

for q in df["question"]:
    print(str(q))
