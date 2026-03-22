import json
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

file = open("../datasets/cao-college-courses.json")
courses = json.load(file)

academic_interests_df = pd.read_csv("../college-course-recommender-system/user_interest_questions.csv")
academic_interests_list = academic_interests_df["college_course_category"].unique().tolist()

academic_interests_dict = {}
riasec_interests_dict = {"realistic":0, "investigative":0, "artistic":0, "social":0, "enterprising":0, "conventional":0}

for a in academic_interests_list:
    academic_interests_dict[a] = riasec_interests_dict.copy()

for course in courses:
    for a in course["categories"]:
        for r in course["riasec_interests"]:
            academic_interests_dict[a][r] += 1

x_axis_stuff = ["R", "I", "A", "S", "E", "C"]
for academic_interest in academic_interests_list:
    plt.title(academic_interest.capitalize())
    plt.xlabel("RIASEC trait")
    plt.ylabel("Frequency")
    plt.bar(x_axis_stuff, academic_interests_dict[academic_interest].values())
    plt.show()
