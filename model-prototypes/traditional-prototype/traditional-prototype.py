# should not have vector representation - just straight up filter them
    # * nfq level
    # * location
    # * isAdditionalPortfolioTestInterviewRequired

import json
import numpy as np
import pandas as pd
from utils import *
from sklearn.preprocessing import LabelEncoder

clean_riasec_college_major_categories = pd.read_csv("../../datasets/open-psychometrics/clean_riasec_college_major_categories.tsv", sep='\t')
feature_columns = [ 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 
                    'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 
                    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

X = clean_riasec_college_major_categories[feature_columns]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(clean_riasec_college_major_categories['major_category'])

weighted_categories_model = get_weighted_categories_model(X, y, False)

# change to cao-college-courses.json when done!
with open("../../datasets/cao-college-courses/split-json-chunks/output_part_1.json", 'r', encoding='utf-8') as f: 
    cao_courses = json.load(f)

min_points = get_min_points(cao_courses)
max_points = get_max_points(cao_courses)

for course in cao_courses:
    add_vectorized_course_as_attribute(course, min_points, max_points)

lc_subjects_preferences = {} # "Physics": 1.0, "History": 0.0
user_riasec_vector = [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

user_categories_vector = get_weighted_categories_vector(user_riasec_vector, weighted_categories_model)
user_points_vector = get_normalized_points_vector(589, min_points, max_points)

simplified_user_riasec_vector = get_simplified_user_riasec_vector(user_riasec_vector, lc_subjects_preferences)

user_vector = np.concatenate((simplified_user_riasec_vector, user_points_vector, user_categories_vector), axis=0)

k = 20
top_k_results = get_top_k_results(cao_courses, user_vector, k)


for res in top_k_results:
    print(res["title"] + " " + str(round(res["similarity"]*100.0, 1)) + "%")
