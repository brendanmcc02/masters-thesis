import numpy as np
import json
import pandas as pd
import sys
sys.path.append('../datasets/open-psychometrics/filter_data')
from filter_open_psychometrics_data_utils import preprocess_text

CAO_COLLEGE_COURSES_FILE_LOCATION = '../datasets/cao-college-courses/cao-college-courses.json'
USER_INTEREST_QUESTIONS_DATASET_FILEPATH = "user_interest_questions.csv"

RIASEC_INTERESTS = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
POINTS_VECTOR_DIMENSION_SIZE = 1

POINTS_VECTOR_INDEX = len(RIASEC_INTERESTS)
STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX = POINTS_VECTOR_INDEX + 1

MIN_COURSE_POINTS = 0
MAX_COURSE_POINTS = 625

NUMBER_OF_COLLEGE_COURSE_CATEGORIES_TO_RECOMMEND = 5
NUMBER_OF_RECOMMENDED_COURSES_PER_CATEGORY = 4
NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS = NUMBER_OF_COLLEGE_COURSE_CATEGORIES_TO_RECOMMEND * NUMBER_OF_RECOMMENDED_COURSES_PER_CATEGORY

FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP = {4: 1.0,
                                      3: 0.25, 
                                      2: 0.01, 
                                      1: 0.001, # let this be non-zero so it penalises the interest/category - otherwise it gets counted as NaN and isn't factored into the open psychometrics model/data!
                                      0: 0.001} # let this be non-zero so it penalises the interest/category - otherwise it gets counted as NaN and isn't factored into the open psychometrics model/data!
RIASEC_INTEREST_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT = 0.5
COLLEGE_COURSE_CATEGORY_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT = 1.0

def get_college_course_categories():
    df = pd.read_csv(USER_INTEREST_QUESTIONS_DATASET_FILEPATH)

    college_course_categories = df['college_course_category'].unique().tolist()
    
    return sorted(college_course_categories)

def get_user_interest_questions_college_course_categories():
    df = pd.read_csv(USER_INTEREST_QUESTIONS_DATASET_FILEPATH)

    college_course_categories = df['college_course_category'].tolist()
    
    return college_course_categories

def get_user_interest_questions_riasec_interests():
    df = pd.read_csv(USER_INTEREST_QUESTIONS_DATASET_FILEPATH)

    riasec_interests = df['riasec_interest'].tolist()
    
    return riasec_interests

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

preprocess_college_course_titles()

COLLEGE_COURSE_CATEGORIES = get_college_course_categories()
USER_INTEREST_QUESTIONS_COLLEGE_COURSE_CATEGORIES = get_user_interest_questions_college_course_categories()
USER_INTEREST_QUESTIONS_RIASEC_INTERESTS = get_user_interest_questions_riasec_interests()
VECTORIZED_REPRESENTATION_DIMENSION_SIZE = len(RIASEC_INTERESTS) + POINTS_VECTOR_DIMENSION_SIZE + len(COLLEGE_COURSE_CATEGORIES)

def get_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences):
    filtered_college_courses = get_filtered_college_courses(user_college_course_preferences)

    user_vector = get_user_vector(user_interest_questions_results_vector, user_college_course_preferences)

    college_course_recommendations = []
    top_k_college_course_category_indexes = get_top_k_college_course_category_indexes(user_vector, k=NUMBER_OF_COLLEGE_COURSE_CATEGORIES_TO_RECOMMEND)

    
    for college_course_category_index in top_k_college_course_category_indexes:
        masked_college_course_category_course_recommendations = get_masked_college_course_category_course_recommendations(user_vector, college_course_category_index, filtered_college_courses)

        add_new_college_course_recommendations(masked_college_course_category_course_recommendations, college_course_recommendations)

    return college_course_recommendations[0:NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS]

def get_user_vector(user_interest_questions_results_vector, user_college_course_preferences):
    user_riasec_vector = get_user_riasec_vector(user_interest_questions_results_vector)

    user_categories_vector = get_user_categories_vector(user_interest_questions_results_vector)

    user_points_vector = get_normalized_points_vector(user_college_course_preferences["expected_points"])

    return np.concatenate((user_riasec_vector, user_points_vector, user_categories_vector), axis=0)

def get_user_categories_vector(user_riasec_questions_vector):
    user_categories_vector = np.zeros(len(COLLEGE_COURSE_CATEGORIES))

    for i in range(len(user_riasec_questions_vector)):
        user_categories_vector_index = COLLEGE_COURSE_CATEGORIES.index(USER_INTEREST_QUESTIONS_COLLEGE_COURSE_CATEGORIES[i])
        user_categories_vector[user_categories_vector_index] += FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[user_riasec_questions_vector[i]]

    for i in range(len(user_categories_vector)):
        user_categories_vector[i] = custom_normalized_sigmoid_function(user_categories_vector[i], COLLEGE_COURSE_CATEGORY_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT)

    print_stringified_college_course_categories_vector(user_categories_vector)

    return user_categories_vector

def add_weighted_preference_to_user_vector(user_vector, five_point_likert_scale_preference_value, riasec_interest_or_college_course_category, all_riasec_interests_or_college_course_categories, number_of_covered_riasec_interests_or_college_course_categories):
    weighted_preference = FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[five_point_likert_scale_preference_value]
    # distribute the weight for multi-interest/category subjects
    distributed_weighted_preference = weighted_preference / np.sqrt(number_of_covered_riasec_interests_or_college_course_categories)
    index_to_access = all_riasec_interests_or_college_course_categories.index(riasec_interest_or_college_course_category)
    user_vector[index_to_access] += distributed_weighted_preference

def custom_normalized_sigmoid_function(value, tuning_constant):
    return 1 - np.exp(-tuning_constant * value)

def get_top_k_college_course_category_indexes(user_vector, k):
    top_college_course_categories = {}

    for i in range(STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX, len(user_vector)):
        top_college_course_categories[i] = user_vector[i]

    top_college_course_category_indexes = sorted(
            top_college_course_categories, 
            key=top_college_course_categories.get, 
            reverse=True
        )

    return top_college_course_category_indexes[0:k]

def get_masked_college_course_category_course_recommendations(user_vector, college_course_category_index, filtered_college_courses):
    masked_college_course_category_user_vector = get_masked_college_course_category_user_vector(user_vector, college_course_category_index)
    cached_masked_college_course_category_user_vector_magnitude = np.linalg.norm(masked_college_course_category_user_vector)
    
    for course in filtered_college_courses:
        course["similarity_score"] = get_cosine_similarity(masked_college_course_category_user_vector, cached_masked_college_course_category_user_vector_magnitude, course["vectorized_representation"])

    masked_college_course_category_course_recommendations = sorted(
        filtered_college_courses,
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    return masked_college_course_category_course_recommendations

def get_masked_college_course_category_user_vector(user_vector, college_course_category_index):
    masked_college_course_category_user_vector = user_vector.copy()
    
    for i in range(STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX, len(user_vector)):
        if i == college_course_category_index:
            masked_college_course_category_user_vector[i] = 1.0
        else:
            masked_college_course_category_user_vector[i] = 0.0

    return masked_college_course_category_user_vector

def add_new_college_course_recommendations(masked_college_course_category_course_recommendations_to_add, previously_recommended_college_courses):
    number_of_new_courses_added = 0

    while number_of_new_courses_added < NUMBER_OF_RECOMMENDED_COURSES_PER_CATEGORY:
        if is_new_college_course_recommendation(masked_college_course_category_course_recommendations_to_add[number_of_new_courses_added], previously_recommended_college_courses):
            previously_recommended_college_courses.append(masked_college_course_category_course_recommendations_to_add[number_of_new_courses_added].copy())
            number_of_new_courses_added += 1
        else:
            del masked_college_course_category_course_recommendations_to_add[number_of_new_courses_added]

def is_new_college_course_recommendation(college_course_to_check, previously_recommended_college_courses):
    for previously_recommended_college_course in previously_recommended_college_courses:
        if is_exact_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check) or is_substring_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
            print("Not recommending " + college_course_to_check['title'] + ", " + college_course_to_check['college'] + " because " + previously_recommended_college_course['title'] + ", " + previously_recommended_college_course['college'] + " is already recommended.\n")
            return False
        
    return True

def is_exact_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
    return previously_recommended_college_course['preprocessed_title'] == college_course_to_check['preprocessed_title']

SUBSTRING_MATCH_PREPROCESSED_COLLEGE_COURSE_TITLE_EDGE_CASES = ["engin", "technolog", "therapi", "servic", "manag", "art", "public", "nurs", "educ", "sport", "architectur"] # business???
def is_substring_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
    tokenized_college_course_title_words = previously_recommended_college_course['preprocessed_title'].split(' ')

    for token in tokenized_college_course_title_words:
        if token not in SUBSTRING_MATCH_PREPROCESSED_COLLEGE_COURSE_TITLE_EDGE_CASES and token in college_course_to_check['preprocessed_title']:
            return True

    return False

def get_normalized_points_vector(points):
    # some courses have null points i.e. no points information (they are new courses)
    if not points:
        points = 0.0
    
    # somec courses are over 625 points (because of portfolios, interviews, etc.)
    # so if the course exceeds 625 points, vectorize the course as if it had 625 points (keeps the normalisation between 0 and 625 points)
    points = min(points, MAX_COURSE_POINTS)

    return np.array([(points - MIN_COURSE_POINTS) / (MAX_COURSE_POINTS - MIN_COURSE_POINTS)])

def get_user_riasec_vector(user_interest_questions_results_vector):
    user_riasec_vector = np.zeros(len(RIASEC_INTERESTS))

    for i in range(len(user_interest_questions_results_vector)):
        user_riasec_vector_index = RIASEC_INTERESTS.index(USER_INTEREST_QUESTIONS_RIASEC_INTERESTS[i])
        user_riasec_vector[user_riasec_vector_index] += FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[user_interest_questions_results_vector[i]]

    print_stringified_riasec_vector(user_riasec_vector)

    for i in range(len(user_riasec_vector)):
        user_riasec_vector[i] = custom_normalized_sigmoid_function(user_riasec_vector[i], RIASEC_INTEREST_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT)

    print_stringified_riasec_vector(user_riasec_vector)

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
        vectorized_representation[STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX + COLLEGE_COURSE_CATEGORIES.index(category)] = distributed_category_weight

    return vectorized_representation

def get_cosine_similarity(user_vector, cached_user_vector_magnitude, course_vector):
    return np.dot(user_vector, course_vector) / (cached_user_vector_magnitude * np.linalg.norm(course_vector))

def print_stringified_college_course_categories_vector(college_course_categories_vector):
    for i in range(len(college_course_categories_vector)):
        print(COLLEGE_COURSE_CATEGORIES[i] + ": " + str(round(college_course_categories_vector[i], 2)) + ("\n" if i == len(college_course_categories_vector)-1 else ""))

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

def print_college_course_recommendations(college_course_recommendations):
    for rec in college_course_recommendations:
        print(rec["title"] + "\n" + rec["preprocessed_title"] + "\n" + rec["college"] + "\n" + str(rec["interests"]) + "\n" + str(rec["categories"]) + "\nPoints: " + str(rec["points"]) + "\nSimilarity: " + (str(round(rec["similarity_score"]*100.0, 1)) if "similarity_score" in rec else "-1") + "%\n")
        # print(rec['vectorized_representation'])

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

def get_user_interest_questions_results_df(user_name, user_interest_questions_results_df):
    user_row = user_interest_questions_results_df.loc[
        user_interest_questions_results_df['name'] == user_name
    ]

    return user_row.drop(columns=['name']).values[0]
