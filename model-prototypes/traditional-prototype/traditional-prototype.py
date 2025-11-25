# should not have vector representation - just straight up filter them
    # * nfq level
    # * location
    # * isAdditionalPortfolioTestInterviewRequired

import json
import numpy as np
from utils import *

# change to cao-college-courses.json when done!
with open("../../datasets/cao-college-courses/split-json-chunks/output_part_1.json", 'r', encoding='utf-8') as f: 
    cao_courses = json.load(f)

min_points = get_min_points(cao_courses)
max_points = get_max_points(cao_courses)

for course in cao_courses:
    add_vectorized_course_as_attribute(course, min_points, max_points)

lc_subjects_preferences = {"Physics": 1.0, "History": 0.0}
user_riasec_vector = [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
user_categories_vector = get_weighted_categories_vector(user_riasec_vector)
user_points_vector = get_normalized_points(589, min_points, max_points)

simplified_user_riasec_vector = get_simplified_user_riasec_vector(user_riasec_vector, lc_subjects_preferences)

# user_vector = np.concatenate((simplified_user_riasec_vector, user_points_vector, user_categories_vector), axis=0)
