import pandas as pd

df = pd.read_csv("user_interest_questions_results.csv")

df.columns = map(str.lower, df.columns)

df.to_csv("user_interest_questions_results.csv", index=False)

# Source - https://stackoverflow.com/a
# Posted by roman
# Retrieved 2026-01-11, License - CC BY-SA 3.0



