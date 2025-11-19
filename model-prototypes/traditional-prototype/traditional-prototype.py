# should not have vector representation - just straight up filter them
    # * nfq level
    # * location

import json
import numpy as np

NUMBER_OF_RIASEC_CATEGORIES = 6
NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY = 8
NUMBER_OF_COLLEGE_MAJOR_CATEGORIES = 15
VECTOR_REPRESENTATION_DIMENSION_SIZE = NUMBER_OF_RIASEC_CATEGORIES + NUMBER_OF_COLLEGE_MAJOR_CATEGORIES + 1 # + 1 for points

POINTS_VECTOR_INDEX = 6
STARTING_CATEGORY_VECTOR_INDEX = POINTS_VECTOR_INDEX + 1

MAX_RIASEC_QUESTION_VALUE = 4.0 # assuming 0-4, not 1-5!
RIASEC_CATEGORIES = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
COLLEGE_MAJOR_CATEGORIES = ['agriculture & natural resources', 'arts', 'biology & life science', 'business', 'communications & journalism', 'computers & mathematics', 'education', 'engineering', 'health', 'humanities & liberal arts', 'industrial arts & consumer services', 'law & public policy', 'physical sciences', 'psychology & social work', 'social science']

def get_min_points(cao_courses):
    min_points = 625

    for course in cao_courses:
        if course['points']:
            min_points = min(min_points, course['points'])

    return min_points

def get_max_points(cao_courses):
    max_points = 0

    for course in cao_courses:
        if course['points']:
            max_points = max(max_points, course['points'])

    return max_points

def add_vectorized_course_as_attribute(course, min_points, max_points):
    course['vector_representation'] = get_vectorized_representation(course, min_points, max_points)

def get_vectorized_representation(course, min_points, max_points):
    vectorized_representation = np.zeros(VECTOR_REPRESENTATION_DIMENSION_SIZE)

    for interest in course['interests']:
        vectorized_representation[RIASEC_CATEGORIES.index(interest)] = 1.0

    vectorized_representation[POINTS_VECTOR_INDEX] = get_normalized_points(course['points'], min_points, max_points)

    one_hot_encode(course, vectorized_representation)

    return vectorized_representation

def get_normalized_points(points, min_points, max_points):
    if not points:
        points = 0.0
    
    return (points - min_points) / (max_points - min_points)

def one_hot_encode(course, vectorized_representation):
    for category in course['categories']:
        vectorized_representation[STARTING_CATEGORY_VECTOR_INDEX + COLLEGE_MAJOR_CATEGORIES.index(category)] = 1.0

# TODO
# ML/vector model
def get_weighted_categories_vector(user_riasec_vector):
    return np.zeros(len(COLLEGE_MAJOR_CATEGORIES))

def get_normalized_vectorized_riasec(user_riasec):
    for i in range(len(user_riasec)):
        user_riasec[i] /= MAX_RIASEC_QUESTION_VALUE

    return user_riasec

# TODO
def get_simplified_user_riasec_vector(user_riasec_vector, lc_subjects_preferences):
    simplified_user_riasec_vector = []
    # reduce 48 -> 6 dimensions
    for i in range(0, len(user_riasec_vector), NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY):
        simplified_user_riasec_vector.append(np.mean(user_riasec_vector[i:i+NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY]))

    # for each lc_subject:
    #   factor in the corresponding riasec of that subject to the user_riasec_vector

    return np.array(simplified_user_riasec_vector, dtype='float32')


# change to cao-college-courses.json when done!
with open("../../datasets/cao-college-courses/split-json-chunks/output_part_1.json", 'r', encoding='utf-8') as f: 
    cao_courses = json.load(f)

min_points = get_min_points(cao_courses)
max_points = get_max_points(cao_courses)

for course in cao_courses:
    add_vectorized_course_as_attribute(course, min_points, max_points)

lc_subjects_preferences = {"Physics": 1.0, "History": 0.0}
user_riasec_vector = get_normalized_vectorized_riasec([0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
user_categories_vector = get_weighted_categories_vector(user_riasec_vector)
user_points_vector = get_normalized_points(624, min_points, max_points)

simplified_user_riasec_vector = get_simplified_user_riasec_vector(user_riasec_vector, lc_subjects_preferences)

# user_vector = np.concatenate((simplified_user_riasec_vector, user_points_vector, user_categories_vector), axis=0)
