import pandas as pd

df = pd.read_csv("user_interest_questions.csv")

x = df["college_course_category"].unique().tolist()

for i in x:
    print(str(i))
