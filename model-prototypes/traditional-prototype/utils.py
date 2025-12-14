# ignores warnings
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import json
import pandas as pd

NUMBER_OF_RIASEC_CATEGORIES = 6
NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY = 8
NUMBER_OF_COLLEGE_MAJOR_CATEGORIES = 15
VECTOR_REPRESENTATION_DIMENSION_SIZE = NUMBER_OF_RIASEC_CATEGORIES + NUMBER_OF_COLLEGE_MAJOR_CATEGORIES + 1 # + 1 for points

POINTS_VECTOR_INDEX = 6
STARTING_CATEGORY_VECTOR_INDEX = POINTS_VECTOR_INDEX + 1

MIN_POINTS = 0 # global variables, will be modified
MAX_POINTS = 0 # global variables, will be modified

MAX_RIASEC_QUESTION_VALUE = 4.0 # assuming 0-4, not 1-5!
RIASEC_CATEGORIES = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
COLLEGE_MAJOR_CATEGORIES = ['agriculture & natural resources', 'arts', 'biology & life science', 'business', 'communications & journalism', 'computers & mathematics', 'education', 'engineering', 'health', 'humanities & liberal arts', 'industrial arts & consumer services', 'law & public policy', 'physical sciences', 'psychology & social work', 'social science']

LC_SUBJECTS_TO_RIASEC_MAP = {
                            # practical
                            "Construction Studies": ["Realistic"], 
                            "Engineering": ["Realistic", "Investigative"], 
                            "Technology": ["Realistic", "Investigative"], 
                            # sciences
                            "Agricultural Science": ["Investigative"], 
                            "Applied Maths": ["Investigative"], 
                            "Biology": ["Investigative"], 
                            "Chemistry": ["Investigative"], 
                            "Mathematics": ["Investigative"], 
                            "Physics": ["Investigative"], 
                            "Physics and Chemistry": ["Investigative"], 
                            "Computer Science": ["Investigative"], 
                            # arts
                            "Art": ["Artistic"], 
                            "Drama, Film and Theatre Studies": ["Artistic"], 
                            "Music": ["Artistic"], 
                            "Design and Communication Graphics": ["Investigative", "Artistic"], 
                            # humanities
                            "Arabic": ["Artistic"], 
                            "Classical Studies": ["Artistic"], 
                            "English": ["Artistic"], 
                            "French": ["Artistic"], 
                            "Irish": ["Artistic"], 
                            "German": ["Artistic"], 
                            "Hebrew Studies": ["Artistic"], 
                            "History": ["Artistic"], 
                            "Ukrainian": ["Artistic"], 
                            "Italian": ["Artistic"], 
                            "Japanese": ["Artistic"], 
                            "Latin": ["Artistic"], 
                            "Russian": ["Artistic"], 
                            "Spanish": ["Artistic"], 
                            "Ancient Greek": ["Artistic"], 
                            "Mandarin-Chinese": ["Artistic"], 
                            "Polish": ["Artistic"], 
                            "Lithuanian": ["Artistic"], 
                            "Portuguese": ["Artistic"],
                            # social sciences
                            "Geography": ["Investigative", "Social"], 
                            "Religious Education": ["Investigative", "Social"], 
                            "Physical Education": ["Realistic", "Social"], 
                            "Politics and Society": ["Investigative", "Social", "Enterprising"], 
                            "Climate Action and Sustainable Development": ["Social"], 
                            "Home Economics": ["Realistic", "Social", "Conventional"],
                            # business
                            "Accounting": ["Conventional"], 
                            "Business": ["Enterprising", "Conventional"], 
                            "Economics": ["Investigative", "Enterprising"]
                            }

RIASEC_DATASET_FEATURE_COLUMNS = [ 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 
                                   'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 
                                   'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

def get_min_points():
    # some courses have null points, so there's no need to calculate the min
    return 0.0

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

    vectorized_representation[POINTS_VECTOR_INDEX] = get_normalized_points_vector(course['points'], min_points, max_points)

    one_hot_encode(course, vectorized_representation)

    return vectorized_representation

def get_normalized_points_vector(points, min_points, max_points):
    if not points:
        points = 0.0
    
    return np.array([(points - min_points) / (max_points - min_points)])

def one_hot_encode(course, vectorized_representation):
    for category in course['categories']:
        vectorized_representation[STARTING_CATEGORY_VECTOR_INDEX + COLLEGE_MAJOR_CATEGORIES.index(category)] = 1.0

def get_weighted_categories_model(should_retrain_model):
    clean_riasec_college_major_categories = pd.read_csv("../../datasets/open-psychometrics/clean_riasec_college_major_categories.tsv", sep='\t')
    X = clean_riasec_college_major_categories[RIASEC_DATASET_FEATURE_COLUMNS]
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(clean_riasec_college_major_categories['major_category'])

    saved_model_filename = "saved_logistic_regression_model.joblib"
    if should_retrain_model:
        model = LogisticRegression(
            multi_class='multinomial',
            solver='saga', # negligible performance differences, saga is the quickest
            C=1.0, # different values have negligible impact
            max_iter=1000,
            random_state=42
        )

        model.fit(X, y)
        joblib.dump(model, saved_model_filename)
    else:
        model = joblib.load(saved_model_filename)

    return model

def get_weighted_categories_vector(user_riasec_vector, model):
    user_riasec_vector = np.array(user_riasec_vector).reshape(1, -1) # 1d -> 2d array
    model_class_probabilities = model.predict_proba(user_riasec_vector)
    normalized_model_class_probabilities = get_normalized_vector(model_class_probabilities[0]) # interested in only the first element

    return normalized_model_class_probabilities

def get_normalized_vector(vector):
    maxValue = 0.0
    minValue = 1.0

    for val in vector:
        maxValue = max(maxValue, val)
        minValue = min(minValue, val)

    for i in range(len(vector)):
        vector[i] = (vector[i] - minValue) / (maxValue - minValue)

    return vector

def get_simplified_user_riasec_vector(user_riasec_vector, lc_subjects_preferences):
    riasec_category_vectors= []
    # reduce 48 -> 6 dimensions
    for i in range(0, len(user_riasec_vector), NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY):
        riasec_category_vectors.append(user_riasec_vector[i:i+NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY])

    simplified_user_riasec_vector = factor_lc_subjects_into_riasec(riasec_category_vectors, lc_subjects_preferences)

    normalized_simplified_user_riasec_vector = get_normalized_vector(simplified_user_riasec_vector)

    return np.array(normalized_simplified_user_riasec_vector, dtype='float32')

def factor_lc_subjects_into_riasec(riasec_category_vectors, lc_subjects_preferences):
    for subject in lc_subjects_preferences:
        subject_interests = LC_SUBJECTS_TO_RIASEC_MAP[subject]

        for interest in subject_interests:
            riasec_category_vectors[RIASEC_CATEGORIES.index(interest)].append(lc_subjects_preferences[subject])

    simplified_user_riasec_vector = np.zeros(len(RIASEC_CATEGORIES))

    for i in range(len(riasec_category_vectors)):
        simplified_user_riasec_vector[i] = np.mean(riasec_category_vectors[i])

    return simplified_user_riasec_vector

def get_top_k_results(cao_courses, user_vector, k):
    cached_user_vector_magnitude = np.linalg.norm(user_vector)
    for course in cao_courses:
        course["similarity"] = get_cosine_similarity(user_vector, cached_user_vector_magnitude, course["vector_representation"])

    results = sorted(
        cao_courses,
        key=lambda x: x["similarity"],
        reverse=True
    )
    top_k_results = results[0:k]

    return top_k_results

def get_cosine_similarity(user_vector, cached_user_vector_magnitude, course_vector):
    return np.dot(user_vector, course_vector) / (cached_user_vector_magnitude * np.linalg.norm(course_vector))

# TODO what about courses with portfolios that have excessive points?
# no one would get recommended courses over 625 points
def get_filtered_cao_courses(user_college_course_preferences):
    with open("../../datasets/cao-college-courses/cao-college-courses.json", 'r', encoding='utf-8') as f: 
        cao_courses = json.load(f)

    filtered_cao_courses = []
    for course in cao_courses:
        if (course["nfqLevel"] in user_college_course_preferences["nfq_levels"] and 
            course["college"] in user_college_course_preferences["colleges"] and 
            course["points"] <= user_college_course_preferences["expected_points"]):
            filtered_cao_courses.append(course)

    global MIN_POINTS
    global MAX_POINTS

    MIN_POINTS = get_min_points()
    MAX_POINTS = get_max_points(filtered_cao_courses)

    for course in filtered_cao_courses:
        add_vectorized_course_as_attribute(course, MIN_POINTS, MAX_POINTS)

    return filtered_cao_courses

def get_top_k_recommendations(filtered_cao_courses, user_riasec_vector, user_college_course_preferences, user_lc_subject_preferences, k, should_retrain_model):
    weighted_categories_model = get_weighted_categories_model(should_retrain_model)
    user_categories_vector = get_weighted_categories_vector(user_riasec_vector, weighted_categories_model)

    user_points_vector = get_normalized_points_vector(user_college_course_preferences["expected_points"], MIN_POINTS, MAX_POINTS)

    simplified_user_riasec_vector = get_simplified_user_riasec_vector(user_riasec_vector, user_lc_subject_preferences)

    user_vector = np.concatenate((simplified_user_riasec_vector, user_points_vector, user_categories_vector), axis=0)

    return get_top_k_results(filtered_cao_courses, user_vector, k)
