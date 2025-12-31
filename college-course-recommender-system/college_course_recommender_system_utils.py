# ignore sklearn warnings
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import joblib
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import json
import pandas as pd

RIASEC_INTERESTS = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
college_majors_and_major_categories_df = pd.read_csv("../datasets/open-psychometrics/filter_data/college_majors_and_major_categories.tsv", sep='\t', low_memory=False)
COLLEGE_MAJOR_CATEGORIES = college_majors_and_major_categories_df["college_major_category"].unique().tolist()
VECTORIZED_REPRESENTATION_DIMENSION_SIZE = len(RIASEC_INTERESTS) + len(COLLEGE_MAJOR_CATEGORIES) + 1 # + 1 for points

POINTS_VECTOR_INDEX = len(RIASEC_INTERESTS)
STARTING_COLLEGE_MAJOR_CATEGORY_VECTOR_INDEX = POINTS_VECTOR_INDEX + 1

MIN_POINTS = 0 # global variables, will be modified
MAX_POINTS = 0 # global variables, will be modified

NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS = 20
NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY = 8
MAX_RIASEC_QUESTION_VALUE = 4.0 # assuming 0-4, not 1-5!

FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP = {4: 1.0,
                                      3: 0.25, 
                                      2: 0.01, 
                                      1: 0.001, # let this be non-zero so it penalises the interest/category - otherwise it gets counted as NaN and isn't factored into the open psychometrics model/data!
                                      0: 0.001} # let this be non-zero so it penalises the interest/category - otherwise it gets counted as NaN and isn't factored into the open psychometrics model/data!
CUSTOM_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT = 1.0

class LeavingCertSubject:
    riasec_interests = []
    college_major_categories = []

    def __init__(self, riasec_interests, college_major_categories):
        self.riasec_interests = riasec_interests
        self.college_major_categories = college_major_categories

LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP = {
                            # practical
                            "Construction Studies": LeavingCertSubject(["realistic"], ["industrial arts & consumer services"]),
                            "Engineering": LeavingCertSubject(["realistic", "investigative"], ["engineering"]),
                            "Technology": LeavingCertSubject(["realistic", "investigative"], ["computers & mathematics", "engineering"]),
                            # life sciences
                            "Agricultural Science": LeavingCertSubject(["investigative"], ["life science"]),
                            "Biology": LeavingCertSubject(["investigative"], ["life science", "healthcare"]),
                            # physical sciences
                            "Chemistry": LeavingCertSubject(["investigative"], ["physical science"]),
                            "Physics": LeavingCertSubject(["investigative"], ["physical science"]),
                            "Physics and Chemistry": LeavingCertSubject(["investigative"], ["physical science"]),
                            # formal sciences
                            "Applied Mathematics": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            "Computer Science": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            "Mathematics": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            # arts
                            "Art": LeavingCertSubject(["artistic"], ["arts"]),
                            "Drama, Film and Theatre Studies": LeavingCertSubject(["artistic"], ["arts"]),
                            "Music": LeavingCertSubject(["artistic"], ["arts"]),
                            "Design and Communication Graphics": LeavingCertSubject(["artistic", "investigative", "realistic"], ["arts", "engineering"]),
                            # languages
                            "Arabic": LeavingCertSubject(["artistic"], ["humanities"]),
                            "French": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Irish": LeavingCertSubject(["artistic"], ["humanities"]),
                            "German": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Ukrainian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Italian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Japanese": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Latin": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Russian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Spanish": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Mandarin-Chinese": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Polish": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Lithuanian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Portuguese": LeavingCertSubject(["artistic"], ["humanities"]),
                            # humanities
                            "Ancient Greek": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Classical Studies": LeavingCertSubject(["artistic"], ["humanities"]),
                            "English": LeavingCertSubject(["artistic"], ["humanities", "communications"]),
                            "Hebrew Studies": LeavingCertSubject(["artistic"], ["humanities"]),
                            "History": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Religious Education": LeavingCertSubject(["artistic"], ["humanities"]), 
                            # social sciences
                            "Geography": LeavingCertSubject(["investigative", "social"], ["physical science", "social science"]), 
                            "Politics and Society": LeavingCertSubject(["investigative", "social", "enterprising"], ["law", "social science"]), 
                            "Climate Action and Sustainable Development": LeavingCertSubject(["social"], ["law", "social science"]), 
                            # business
                            "Accounting": LeavingCertSubject(["conventional", "enterprising"], ["business"]), 
                            "Business": LeavingCertSubject(["conventional", "enterprising"], ["business", "law"]),
                            "Economics": LeavingCertSubject(["investigative"], ["business", "social science"]),
                            # misc
                            "Physical Education": LeavingCertSubject(["realistic", "social"], ["healthcare"]),
                            "Home Economics": LeavingCertSubject(["realistic", "social"], ["industrial arts & consumer services"]),
                            }


RIASEC_DATASET_FEATURE_COLUMNS = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8',
                                  'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8',
                                  'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
                                  'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8',
                                  'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',
                                  'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

def get_college_course_recommendations(filtered_college_courses, user_riasec_questions_vector, user_college_course_preferences, user_leaving_cert_subject_preferences, should_reuse_trained_open_psychometrics_model):
    user_vector = get_user_vector(should_reuse_trained_open_psychometrics_model, user_riasec_questions_vector, user_leaving_cert_subject_preferences, user_college_course_preferences)

    college_course_recommendations = get_multiple_category_college_course_recommendations(user_vector, filtered_college_courses, max_number_of_courses_recommended_per_category=5)

    return college_course_recommendations[0:NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS]

def get_user_vector(should_reuse_trained_open_psychometrics_model, user_riasec_questions_vector, user_leaving_cert_subject_preferences, user_college_course_preferences):
    user_categories_vector = get_user_categories_vector(should_reuse_trained_open_psychometrics_model, user_riasec_questions_vector, user_leaving_cert_subject_preferences)

    user_points_vector = get_normalized_points_vector(user_college_course_preferences["expected_points"], MIN_POINTS, MAX_POINTS)

    user_riasec_vector = get_user_riasec_vector(user_riasec_questions_vector, user_leaving_cert_subject_preferences)

    return np.concatenate((user_riasec_vector, user_points_vector, user_categories_vector), axis=0)

def get_user_categories_vector(should_reuse_trained_open_psychometrics_model, user_riasec_questions_vector, user_leaving_cert_subject_preferences):
    open_psychometrics_model = get_open_psychometrics_model(should_reuse_trained_open_psychometrics_model)
    user_open_psychometrics_college_major_categories_vector = get_user_open_psychometrics_college_major_categories_vector(user_riasec_questions_vector, open_psychometrics_model)

    user_leaving_cert_college_major_categories_vector = get_user_leaving_cert_college_major_categories_vector(user_leaving_cert_subject_preferences)

    user_categories_vector = get_combined_college_major_category_vectors(user_open_psychometrics_college_major_categories_vector, user_leaving_cert_college_major_categories_vector)

    print_stringified_college_major_categories_vector(user_categories_vector)

    return user_categories_vector

def get_open_psychometrics_model(should_reuse_trained_open_psychometrics_model):
    clean_riasec_college_major_categories = pd.read_csv("../datasets/open-psychometrics/clean_riasec_college_major_categories.tsv", sep='\t')
    X = clean_riasec_college_major_categories[RIASEC_DATASET_FEATURE_COLUMNS]
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(clean_riasec_college_major_categories['college_major_category'])

    saved_model_filename = "saved_model.joblib"
    if should_reuse_trained_open_psychometrics_model:
        model = joblib.load(saved_model_filename)
    else:
        model = HistGradientBoostingClassifier(
            class_weight='balanced',
            l2_regularization=1.0,
            # max_leaf_nodes=None,
            random_state=42)

        model.fit(X, y)
        joblib.dump(model, saved_model_filename)

    return model

def get_user_open_psychometrics_college_major_categories_vector(user_riasec_vector, model):
    user_riasec_vector = np.array(user_riasec_vector).reshape(1, -1) # 1d -> 2d array
    model_class_probabilities = model.predict_proba(user_riasec_vector)
    normalized_model_class_probabilities = get_normalized_vector(model_class_probabilities[0]) # interested in only the first element

    return normalized_model_class_probabilities

def get_user_leaving_cert_college_major_categories_vector(user_leaving_cert_subject_preferences):
    user_leaving_cert_college_major_categories_vector = np.zeros(len(COLLEGE_MAJOR_CATEGORIES))

    for subject in user_leaving_cert_subject_preferences:
        for college_major_category in LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].college_major_categories:
            add_weighted_preference_to_user_vector(user_leaving_cert_college_major_categories_vector, user_leaving_cert_subject_preferences[subject], college_major_category, COLLEGE_MAJOR_CATEGORIES, len(LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].college_major_categories))

    return get_normalized_user_leaving_cert_vector(user_leaving_cert_college_major_categories_vector)

def add_weighted_preference_to_user_vector(user_vector, five_point_likert_scale_preference_value, riasec_interest_or_college_major_category, all_riasec_interests_or_college_major_categories, number_of_covered_riasec_interests_or_college_major_categories):
    weighted_preference = FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[five_point_likert_scale_preference_value]
    # distribute the weight for multi-interest/category subjects
    distributed_weighted_preference = weighted_preference / np.sqrt(number_of_covered_riasec_interests_or_college_major_categories)
    index_to_access = all_riasec_interests_or_college_major_categories.index(riasec_interest_or_college_major_category)
    user_vector[index_to_access] += distributed_weighted_preference

def get_normalized_user_leaving_cert_vector(user_leaving_cert_vector):
    for i in range(len(user_leaving_cert_vector)):
        if user_leaving_cert_vector[i] == 0.0:
            # we don't want to penalise interests/college major categories which have no data:
            # this is under the assumption that a rating of '0' or '1' (strong/soft dislike) has a non-zero weight!
            user_leaving_cert_vector[i] = np.nan 
        else:
            user_leaving_cert_vector[i] = custom_normalized_sigmoid_function(user_leaving_cert_vector[i])

    return user_leaving_cert_vector

def custom_normalized_sigmoid_function(value):
    return 1 - np.exp(-CUSTOM_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT * value)

def get_multiple_category_college_course_recommendations(user_vector, filtered_college_courses, max_number_of_courses_recommended_per_category):
    multiple_category_college_course_recommendations = []
    top_k_college_major_category_indexes = get_top_k_college_major_category_indexes(user_vector, k=3)

    for college_major_category_index in top_k_college_major_category_indexes:
        masked_college_major_category_course_recommendations = get_masked_college_major_category_course_recommendations(user_vector, college_major_category_index, filtered_college_courses)

        add_new_college_course_recommendations(masked_college_major_category_course_recommendations, multiple_category_college_course_recommendations, max_number_of_courses_recommended_per_category)

    return multiple_category_college_course_recommendations

def get_top_k_college_major_category_indexes(user_vector, k):
    top_college_major_categories = {}

    for i in range(STARTING_COLLEGE_MAJOR_CATEGORY_VECTOR_INDEX, len(user_vector)):
        top_college_major_categories[i] = user_vector[i]

    top_college_major_category_indexes = sorted(
            top_college_major_categories, 
            key=top_college_major_categories.get, 
            reverse=True
        )

    return top_college_major_category_indexes[0:k]

def get_masked_college_major_category_course_recommendations(user_vector, college_major_category_index, filtered_college_courses):
    masked_college_major_category_user_vector = get_masked_college_major_category_user_vector(user_vector, college_major_category_index)
    cached_masked_college_major_category_user_vector_magnitude = np.linalg.norm(masked_college_major_category_user_vector)
    
    for course in filtered_college_courses:
        course["similarity"] = get_cosine_similarity(masked_college_major_category_user_vector, cached_masked_college_major_category_user_vector_magnitude, course["vectorized_representation"])

    masked_college_major_category_course_recommendations = sorted(
        filtered_college_courses,
        key=lambda x: x["similarity"],
        reverse=True
    )

    return masked_college_major_category_course_recommendations

def get_masked_college_major_category_user_vector(user_vector, college_major_category_index):
    masked_college_major_category_user_vector = user_vector.copy()
    
    for i in range(STARTING_COLLEGE_MAJOR_CATEGORY_VECTOR_INDEX, len(user_vector)):
        if i == college_major_category_index:
            masked_college_major_category_user_vector[i] = 1.0
        else:
            masked_college_major_category_user_vector[i] = 0.0

    return masked_college_major_category_user_vector

def add_new_college_course_recommendations(masked_college_major_category_course_recommendations_to_add, previously_recommended_college_courses, max_number_of_courses_recommended_per_category):
    number_of_new_courses_added = 0

    while number_of_new_courses_added < max_number_of_courses_recommended_per_category:
        if is_new_college_course_recommendation(masked_college_major_category_course_recommendations_to_add[number_of_new_courses_added]['title'], previously_recommended_college_courses):
            previously_recommended_college_courses.append(masked_college_major_category_course_recommendations_to_add[number_of_new_courses_added])
            number_of_new_courses_added += 1
        else:
            del masked_college_major_category_course_recommendations_to_add[number_of_new_courses_added]

def is_new_college_course_recommendation(college_course_title, previously_recommended_college_courses):
    for course in previously_recommended_college_courses:
        if course['title'] == college_course_title:
            return False
        
    return True

def get_combined_college_major_category_vectors(user_open_psychometrics_college_major_categories_vector, user_leaving_cert_college_major_categories_vector):
    user_college_major_category_vector = np.zeros(len(COLLEGE_MAJOR_CATEGORIES))
    
    for i in range(len(user_leaving_cert_college_major_categories_vector)):

        if np.isnan(user_leaving_cert_college_major_categories_vector[i]):
            user_college_major_category_vector[i] = user_open_psychometrics_college_major_categories_vector[i]
        else:
            # mean
            user_college_major_category_vector[i] = (user_open_psychometrics_college_major_categories_vector[i] + user_leaving_cert_college_major_categories_vector[i]) / 2.0
            # max
            # user_college_major_category_vector[i] = max(user_open_psychometrics_college_major_categories_vector[i], user_leaving_cert_college_major_categories_vector[i])

    return user_college_major_category_vector

def get_normalized_points_vector(points, min_points, max_points):
    if not points:
        points = 0.0
    
    return np.array([(points - min_points) / (max_points - min_points)])

def get_user_riasec_vector(user_open_psychometrics_questions_vector, user_leaving_cert_subject_preferences):
    user_riasec_vector = np.zeros(len(RIASEC_INTERESTS))

    user_riasec_vector = get_summed_open_psychometrics_preferences_to_user_riasec_vector(user_riasec_vector, user_open_psychometrics_questions_vector)

    # print("OP raw sums:")
    # print_stringified_riasec_vector(user_riasec_vector)

    user_riasec_vector = get_summed_leaving_cert_subject_preferences_to_user_riasec_vector(user_riasec_vector, user_leaving_cert_subject_preferences)

    # print("OP + LC raw sums:")
    # print_stringified_riasec_vector(user_riasec_vector)

    for i in range(len(user_riasec_vector)):
        user_riasec_vector[i] = custom_normalized_sigmoid_function(user_riasec_vector[i])

    print_stringified_riasec_vector(user_riasec_vector)

    return user_riasec_vector

def get_summed_leaving_cert_subject_preferences_to_user_riasec_vector(user_riasec_vector, user_leaving_cert_subject_preferences):
    for subject in user_leaving_cert_subject_preferences:
        for riasec_interest in LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].riasec_interests:
            add_weighted_preference_to_user_vector(user_riasec_vector, user_leaving_cert_subject_preferences[subject], riasec_interest, RIASEC_INTERESTS, len(LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].riasec_interests))

    return user_riasec_vector

def get_summed_open_psychometrics_preferences_to_user_riasec_vector(user_riasec_vector, user_open_psychometrics_questions_vector):
    for i in range(len(user_open_psychometrics_questions_vector)):
        user_riasec_vector[i//NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY] += FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[user_open_psychometrics_questions_vector[i]]

    return user_riasec_vector

def get_min_points():
    # some courses have null points, so there's no need to calculate the min
    return 0.0

def get_max_points(college_courses):
    max_points = 0

    for course in college_courses:
        if course['points']:
            max_points = max(max_points, course['points'])

    return max_points

def add_vectorized_college_course_as_attribute(course, min_points, max_points):
    course['vectorized_representation'] = get_vectorized_college_course_representation(course, min_points, max_points)

def get_vectorized_college_course_representation(college_course, min_points, max_points):
    vectorized_representation = np.zeros(VECTORIZED_REPRESENTATION_DIMENSION_SIZE)

    for interest in college_course['interests']:
        distributed_interest_weight = 1.0 / np.sqrt(len(college_course['interests']))
        vectorized_representation[RIASEC_INTERESTS.index(interest)] = distributed_interest_weight

    vectorized_representation[POINTS_VECTOR_INDEX] = get_normalized_points_vector(college_course['points'], min_points, max_points)

    for category in college_course['categories']:
        distributed_category_weight = 1.0 / np.sqrt(len(college_course['categories']))
        vectorized_representation[STARTING_COLLEGE_MAJOR_CATEGORY_VECTOR_INDEX + COLLEGE_MAJOR_CATEGORIES.index(category)] = distributed_category_weight

    return vectorized_representation

def get_normalized_vector(vector):
    maxValue = 0.0
    minValue = 1.0

    for val in vector:
        maxValue = max(maxValue, val)
        minValue = min(minValue, val)

    for i in range(len(vector)):
        vector[i] = (vector[i] - minValue) / (maxValue - minValue)

    return vector

def get_cosine_similarity(user_vector, cached_user_vector_magnitude, course_vector):
    return np.dot(user_vector, course_vector) / (cached_user_vector_magnitude * np.linalg.norm(course_vector))

def get_unique_college_course_recommendations(college_course_recommendations):
    college_course_titles = set()
    unique_college_course_recommendations = []

    for college_course in college_course_recommendations:
        if college_course['title'] not in college_course_titles:
            college_course_titles.add(college_course['title'])
            unique_college_course_recommendations.append(college_course)

    return unique_college_course_recommendations

# TODO what about courses with portfolios that have excessive points?
# no one would get recommended courses over 625 points
def get_filtered_college_courses(user_college_course_preferences):
    with open("../datasets/cao-college-courses/cao-college-courses.json", 'r', encoding='utf-8') as f: 
        college_courses = json.load(f)

    filtered_college_courses = []
    for course in college_courses:
        if (course["nfqLevel"] in user_college_course_preferences["nfq_levels"] and 
            course["college"] in user_college_course_preferences["colleges"] and 
            course["points"] <= user_college_course_preferences["expected_points"]):
            filtered_college_courses.append(course)

    global MIN_POINTS
    global MAX_POINTS

    MIN_POINTS = get_min_points()
    MAX_POINTS = get_max_points(filtered_college_courses)

    for course in filtered_college_courses:
        add_vectorized_college_course_as_attribute(course, MIN_POINTS, MAX_POINTS)

    return filtered_college_courses

def print_stringified_college_major_categories_vector(college_major_categories_vector):
    for i in range(len(college_major_categories_vector)):
        print(COLLEGE_MAJOR_CATEGORIES[i] + ": " + str(round(college_major_categories_vector[i], 2)) + ("\n" if i == len(college_major_categories_vector)-1 else ""))

def print_stringified_riasec_vector(riasec_vector):
    for i in range(len(riasec_vector)):
        print(RIASEC_INTERESTS[i] + ": " + str(round(riasec_vector[i], 2)) + ("\n" if i == len(riasec_vector)-1 else ""))
