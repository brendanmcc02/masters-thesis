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
import sys
sys.path.append('../datasets/open-psychometrics/filter_data')
from filter_open_psychometrics_data_utils import preprocess_text

CAO_COLLEGE_COURSES_FILE_LOCATION = '../datasets/cao-college-courses/cao-college-courses.json'

RIASEC_INTERESTS = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
college_majors_and_major_categories_df = pd.read_csv("../datasets/open-psychometrics/filter_data/college_majors_and_major_categories.tsv", sep='\t', low_memory=False)
COLLEGE_MAJOR_CATEGORIES = college_majors_and_major_categories_df["college_major_category"].unique().tolist()
POINTS_VECTOR_DIMENSION_SIZE = 1
VECTORIZED_REPRESENTATION_DIMENSION_SIZE = len(RIASEC_INTERESTS) + POINTS_VECTOR_DIMENSION_SIZE + len(COLLEGE_MAJOR_CATEGORIES)

POINTS_VECTOR_INDEX = len(RIASEC_INTERESTS)
STARTING_COLLEGE_MAJOR_CATEGORY_VECTOR_INDEX = POINTS_VECTOR_INDEX + 1

MIN_COURSE_POINTS = 0
MAX_COURSE_POINTS = 625

NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS = 10
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
                            "Construction Studies": LeavingCertSubject(["realistic"], ["engineering"]),
                            "Engineering": LeavingCertSubject(["realistic", "investigative"], ["engineering"]),
                            "Technology": LeavingCertSubject(["realistic", "investigative"], ["computers & mathematics", "engineering"]),
                            # life sciences
                            "Agricultural Science": LeavingCertSubject(["investigative"], ["life science"]),
                            "Biology": LeavingCertSubject(["investigative"], ["life science", "healthcare"]),
                            # physical sciences
                            "Chemistry": LeavingCertSubject(["investigative"], ["physical science"]),
                            "Physics": LeavingCertSubject(["investigative"], ["physical science"]),
                            "Physics and Chemistry": LeavingCertSubject(["investigative"], ["physical science"]),
                            # mathematical sciences
                            "Applied Mathematics": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            "Computer Science": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            "Mathematics": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            # arts
                            "Art": LeavingCertSubject(["artistic"], ["arts"]),
                            "Drama, Film and Theatre Studies": LeavingCertSubject(["artistic"], ["arts"]),
                            "Music": LeavingCertSubject(["artistic"], ["arts"]),
                            "Design and Communication Graphics": LeavingCertSubject(["artistic", "investigative", "realistic"], ["arts", "engineering"]),
                            # languages
                            "Arabic": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "French": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Irish": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "German": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Ukrainian": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Italian": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Japanese": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Latin": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Russian": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Spanish": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Mandarin-Chinese": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Polish": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Lithuanian": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            "Portuguese": LeavingCertSubject(["artistic"], ["foreign languages"]),
                            # humanities
                            "Ancient Greek": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Classical Studies": LeavingCertSubject(["artistic"], ["humanities"]),
                            "English": LeavingCertSubject(["artistic"], ["humanities"]),
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
                            "Economics": LeavingCertSubject(["investigative", "conventional"], ["business", "social science"]),
                            # sport
                            "Physical Education": LeavingCertSubject(["realistic", "social"], ["sport"]), # should this have social?
                            # hospitality
                            "Home Economics": LeavingCertSubject(["realistic", "social"], ["hospitality"]) # should this have social?
                            }


RIASEC_DATASET_FEATURE_COLUMNS = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8',
                                  'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8',
                                  'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
                                  'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8',
                                  'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',
                                  'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

def get_college_course_recommendations(user_riasec_questions_vector, user_college_course_preferences, user_leaving_cert_subject_preferences, should_reuse_trained_open_psychometrics_model):
    preprocess_college_course_titles()

    filtered_college_courses = get_filtered_college_courses(user_college_course_preferences)

    user_vector = get_user_vector(should_reuse_trained_open_psychometrics_model, user_riasec_questions_vector, user_leaving_cert_subject_preferences, user_college_course_preferences)

    college_course_recommendations = []
    top_k_college_major_category_indexes = get_top_k_college_major_category_indexes(user_vector, k=4)

    max_number_of_courses_recommended_per_category = 4
    for college_major_category_index in top_k_college_major_category_indexes:
        masked_college_major_category_course_recommendations = get_masked_college_major_category_course_recommendations(user_vector, college_major_category_index, filtered_college_courses)

        add_new_college_course_recommendations(masked_college_major_category_course_recommendations, college_course_recommendations, max_number_of_courses_recommended_per_category)
        max_number_of_courses_recommended_per_category -= 1 # recommened 4 courses for the top category, then 3 courses for the next category, then 2, then 1

    return college_course_recommendations[0:NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS]

def get_user_vector(should_reuse_trained_open_psychometrics_model, user_riasec_questions_vector, user_leaving_cert_subject_preferences, user_college_course_preferences):
    user_categories_vector = get_user_categories_vector(should_reuse_trained_open_psychometrics_model, user_riasec_questions_vector, user_leaving_cert_subject_preferences)

    user_points_vector = get_normalized_points_vector(user_college_course_preferences["expected_points"])

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
        course["similarity_score"] = get_cosine_similarity(masked_college_major_category_user_vector, cached_masked_college_major_category_user_vector_magnitude, course["vectorized_representation"])

    masked_college_major_category_course_recommendations = sorted(
        filtered_college_courses,
        key=lambda x: x["similarity_score"],
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
        if is_new_college_course_recommendation(masked_college_major_category_course_recommendations_to_add[number_of_new_courses_added], previously_recommended_college_courses):
            previously_recommended_college_courses.append(masked_college_major_category_course_recommendations_to_add[number_of_new_courses_added].copy())
            number_of_new_courses_added += 1
        else:
            del masked_college_major_category_course_recommendations_to_add[number_of_new_courses_added]

def is_new_college_course_recommendation(college_course_to_check, previously_recommended_college_courses):
    for previously_recommended_college_course in previously_recommended_college_courses:
        if is_exact_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check) or is_substring_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
            print("Not recommending " + college_course_to_check['title'] + ", " + college_course_to_check['college'] + " because " + previously_recommended_college_course['title'] + ", " + previously_recommended_college_course['college'] + " is already recommended.\n")
            return False
        
    return True

def is_exact_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
    return previously_recommended_college_course['preprocessed_title'] == college_course_to_check['preprocessed_title']

SUBSTRING_MATCH_PREPROCESSED_COLLEGE_COURSE_TITLE_EDGE_CASES = ["engin", "technolog", "therapi", "servic", "manag", "art", "public", "nurs", "educ", "sport"] # business???
def is_substring_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
    tokenized_college_course_title_words = previously_recommended_college_course['preprocessed_title'].split(' ')

    for token in tokenized_college_course_title_words:
        if token not in SUBSTRING_MATCH_PREPROCESSED_COLLEGE_COURSE_TITLE_EDGE_CASES and token in college_course_to_check['preprocessed_title']:
            return True

    return False

def get_combined_college_major_category_vectors(user_open_psychometrics_college_major_categories_vector, user_leaving_cert_college_major_categories_vector):
    user_college_major_category_vector = np.zeros(len(COLLEGE_MAJOR_CATEGORIES))
    
    for i in range(len(user_leaving_cert_college_major_categories_vector)):

        if np.isnan(user_leaving_cert_college_major_categories_vector[i]):
            user_college_major_category_vector[i] = user_open_psychometrics_college_major_categories_vector[i]
        else:
            user_college_major_category_vector[i] = (user_open_psychometrics_college_major_categories_vector[i] + user_leaving_cert_college_major_categories_vector[i]) / 2.0

    return user_college_major_category_vector

def get_normalized_points_vector(points):
    # some courses have null points i.e. no points information (they are new courses)
    if not points:
        points = 0.0
    
    # somec courses are over 625 points (because of portfolios, interviews, etc.)
    # so if the course exceeds 625 points, vectorize the course as if it had 625 points (keeps the normalisation between 0 and 625 points)
    points = min(points, MAX_COURSE_POINTS)

    return np.array([(points - MIN_COURSE_POINTS) / (MAX_COURSE_POINTS - MIN_COURSE_POINTS)])

def get_user_riasec_vector(user_open_psychometrics_questions_vector, user_leaving_cert_subject_preferences):
    user_riasec_vector = np.zeros(len(RIASEC_INTERESTS))

    user_riasec_vector = get_summed_open_psychometrics_preferences_to_user_riasec_vector(user_riasec_vector, user_open_psychometrics_questions_vector)

    user_riasec_vector = get_summed_leaving_cert_subject_preferences_to_user_riasec_vector(user_riasec_vector, user_leaving_cert_subject_preferences)

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

def add_vectorized_college_course_as_attribute(course):
    course['vectorized_representation'] = get_vectorized_college_course_representation(course)

def get_vectorized_college_course_representation(college_course):
    vectorized_representation = np.zeros(VECTORIZED_REPRESENTATION_DIMENSION_SIZE)

    for interest in college_course['interests']:
        distributed_interest_weight = 1.0 / np.sqrt(len(college_course['interests']))
        vectorized_representation[RIASEC_INTERESTS.index(interest)] = distributed_interest_weight

    vectorized_representation[POINTS_VECTOR_INDEX] = get_normalized_points_vector(college_course['points'])

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

def print_stringified_college_major_categories_vector(college_major_categories_vector):
    for i in range(len(college_major_categories_vector)):
        print(COLLEGE_MAJOR_CATEGORIES[i] + ": " + str(round(college_major_categories_vector[i], 2)) + ("\n" if i == len(college_major_categories_vector)-1 else ""))

def print_stringified_riasec_vector(riasec_vector):
    for i in range(len(riasec_vector)):
        print(RIASEC_INTERESTS[i] + ": " + str(round(riasec_vector[i], 2)) + ("\n" if i == len(riasec_vector)-1 else ""))

def get_filtered_college_courses(user_college_course_preferences):
    with open(CAO_COLLEGE_COURSES_FILE_LOCATION, 'r', encoding='utf-8') as f: 
        college_courses = json.load(f)

    filtered_college_courses = []
    for course in college_courses:
        if is_course_filtered(course, user_college_course_preferences):
            filtered_college_courses.append(course)

    for course in filtered_college_courses:
        add_vectorized_college_course_as_attribute(course)

    return filtered_college_courses

def is_course_filtered(course, user_college_course_preferences):
    # calculating a realistic/accurate min point calculation for courses that require portfolios/tests/interviews would take way too much manual labour (i think),
    # so instead, if the course requires a portfolio, and satisfies the college and nfq level requirements, just add it to the filtered courses and it could be recommended to the user even if it falls outside of their points range
    return (course["nfqLevel"] in user_college_course_preferences["nfq_levels"] and 
            course["college"] in user_college_course_preferences["colleges"] and 
            (course["points"] <= user_college_course_preferences["expected_points"] or course['isAdditionalPortfolioTestInterviewRequired']))

PREPROCESSED_SCIENCE_COURSE_TITLE_EDGE_CASES = ['Science (General)', 'Science - Explore Multiple Streams', 'Science - Undenominated', 'Science - Common Entry', 'Science (Common Entry with Award Options)', 'Science (Common Entry)', 'Science (General Entry)']
def preprocess_college_course_titles():
    with open(CAO_COLLEGE_COURSES_FILE_LOCATION, 'r', encoding='utf-8') as f: 
        college_courses = json.load(f)

    updated_college_courses = []

    for course in college_courses:
        # set general science courses to "physical sciences"
        if course['title'] in PREPROCESSED_SCIENCE_COURSE_TITLE_EDGE_CASES:
            preprocessed_title = "physic"
        else:
            preprocessed_title = preprocess_text(course['title'])

        if preprocessed_title == "":
            print("Empty preprocessed college course title! - " + course['title'])

        updated_college_courses.append({
            "id": course['id'],
            "title": course['title'],
            "preprocessed_title": preprocessed_title,
            "college": course['college'],
            "region": course['region'],
            "duration": course['duration'],
            "nfqLevel": int(course['nfqLevel']),
            "points": int(course['points']) if course['points'] else None,
            "isAdditionalPortfolioTestInterviewRequired": course['isAdditionalPortfolioTestInterviewRequired'],
            "overview": course['overview'],
            "interests": course['interests'],
            "categories": course['categories'],
        })

    with open(CAO_COLLEGE_COURSES_FILE_LOCATION, "w") as outfile:
        json.dump(updated_college_courses, outfile, indent=4)

def print_college_course_recommendations(college_course_recommendations):
    for rec in college_course_recommendations:
        print(rec["title"] + "\n" + rec["preprocessed_title"] + "\n" + rec["college"] + "\n" + str(rec["interests"]) + "\n" + str(rec["categories"]) + "\nPoints: " + str(rec["points"]) + "\nSimilarity: " + (str(round(rec["similarity_score"]*100.0, 1)) if "similarity_score" in rec else "-1") + "%\n")

def get_baseline_college_course_recommendations(user_college_course_preferences):
    filtered_college_courses = get_filtered_college_courses(user_college_course_preferences)

    baseline_college_course_recommendations = sorted(
        filtered_college_courses,
        key=lambda x: x["points"],
        reverse=True
    )

    unique_baseline_college_course_recommendations = []

    add_new_college_course_recommendations(baseline_college_course_recommendations, unique_baseline_college_course_recommendations, NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS)

    return unique_baseline_college_course_recommendations
