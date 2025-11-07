import fuzzywuzzy
from utils import *
import pandas as pd

# print(preprocess_text("I.T/computing&networking and physics"))
# print(preprocess_text("computer science"))

try:
    college_majors_df = pd.read_csv("filtered_college_majors_2012_usa.tsv", sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')

major_to_major_category_dict = college_majors_df.set_index('college_major')['college_major_category'].to_dict()
print(str(major_to_major_category_dict))
