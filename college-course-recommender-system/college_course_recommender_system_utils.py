import numpy as np
import json
import pandas as pd
from college_course_title_nlp_utils import *
from google import genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)

IS_DEBUG=True

CAO_COLLEGE_COURSES_FILE_LOCATION = '../datasets/cao-college-courses.json'
USER_INTEREST_QUESTIONS_DATASET_FILEPATH = "user_interest_questions.csv"
SURVEY_PART_1_RESPONSES_DATASET_LOCATION = "survey-part-1-responses.tsv"
SURVEY_PART_1_RESPONSES_DATASET_NFQ_LEVELS_COLUMN_NAME = "NFQ Levels"
SURVEY_PART_1_RESPONSES_DATASET_EXPECTED_LEAVING_CERT_POINTS_COLUMN_NAME = "Expected Leaving Cert Points"
SURVEY_PART_1_RESPONSES_DATASET_COLLEGES_STARTING_COLUMN_NAME = "Colleges - "
SURVEY_PART_2_RESPONSES_DATASET_LOCATION = "survey-part-2-responses.tsv"

RIASEC_INTERESTS = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
POINTS_VECTOR_DIMENSION_SIZE = 1

POINTS_VECTOR_INDEX = len(RIASEC_INTERESTS)
STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX = POINTS_VECTOR_INDEX + 1

MIN_COURSE_POINTS = 0
MAX_COURSE_POINTS = 625

MINIMUM_NUMBER_OF_COLLEGE_COURSE_CATEGORIES_TO_RECOMMEND = 5
MAXIMUM_NUMBER_OF_RECOMMENDED_COURSES_PER_CATEGORY = 4
NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS = MINIMUM_NUMBER_OF_COLLEGE_COURSE_CATEGORIES_TO_RECOMMEND * MAXIMUM_NUMBER_OF_RECOMMENDED_COURSES_PER_CATEGORY

FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP = {5: 1.0,
                                      4: 0.25, 
                                      3: 0.01, 
                                      2: 0,
                                      1: 0}
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

def get_user_interest_activities():
    df = pd.read_csv(USER_INTEREST_QUESTIONS_DATASET_FILEPATH)

    activities = df['activity'].str.lower().tolist()

    return activities

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
            "points": int(course['points']),
            "isAdditionalPortfolioTestInterviewRequired": course['isAdditionalPortfolioTestInterviewRequired'],
            "overview": course['overview'],
            "riasec_interests": course["riasec_interests"],
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
    top_college_course_category_user_vector_indexes = get_top_college_course_category_user_vector_indexes(user_vector)

    for college_course_category_user_vector_index in top_college_course_category_user_vector_indexes:
        if len(college_course_recommendations) == NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS:
            add_justifications_for_college_course_recommendations(college_course_recommendations, user_vector)
            return college_course_recommendations
        
        filtered_college_course_category_courses = get_filtered_college_course_category_courses(filtered_college_courses, college_course_category_user_vector_index)
        masked_college_course_category_course_recommendations = get_masked_college_course_category_course_recommendations(user_vector, college_course_category_user_vector_index, filtered_college_course_category_courses, top_college_course_category_user_vector_indexes)

        add_unique_college_course_recommendations(masked_college_course_category_course_recommendations, college_course_recommendations)

    add_justifications_for_college_course_recommendations(college_course_recommendations, user_vector)

    return college_course_recommendations

def get_user_vector(user_interest_questions_results_vector, user_college_course_preferences):
    user_riasec_vector = get_user_riasec_vector(user_interest_questions_results_vector)

    user_points_vector = get_normalized_points_vector(user_college_course_preferences["expected_points"])

    user_categories_vector = get_user_college_course_categories_vector(user_interest_questions_results_vector)

    return np.concatenate((user_riasec_vector, user_points_vector, user_categories_vector), axis=0)

def get_user_college_course_categories_vector(user_riasec_questions_vector):
    user_categories_vector = np.zeros(len(COLLEGE_COURSE_CATEGORIES))

    for i in range(len(user_riasec_questions_vector)):
        user_categories_vector_index = COLLEGE_COURSE_CATEGORIES.index(USER_INTEREST_QUESTIONS_COLLEGE_COURSE_CATEGORIES[i])
        user_categories_vector[user_categories_vector_index] += FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[user_riasec_questions_vector[i]]

    for i in range(len(user_categories_vector)):
        user_categories_vector[i] = custom_normalized_sigmoid_function(user_categories_vector[i], COLLEGE_COURSE_CATEGORY_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT)

    if IS_DEBUG:
        print(get_stringified_college_course_categories_vector(user_categories_vector))

    return user_categories_vector

def custom_normalized_sigmoid_function(value, tuning_constant):
    return 1 - np.exp(-tuning_constant * value)

def get_top_college_course_category_user_vector_indexes(user_vector):
    top_college_course_categories = {}

    for i in range(STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX, len(user_vector)):
        top_college_course_categories[i] = user_vector[i]

    top_college_course_category_user_vector_indexes = sorted(
            top_college_course_categories, 
            key=top_college_course_categories.get, 
            reverse=True
        )

    return top_college_course_category_user_vector_indexes

def get_filtered_college_course_category_courses(filtered_college_courses, college_course_category_user_vector_index):
    filtered_college_course_category_courses = []
    college_course_category_to_filter_by = COLLEGE_COURSE_CATEGORIES[college_course_category_user_vector_index - STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX]

    for course in filtered_college_courses:
        if college_course_category_to_filter_by in course["categories"]:
           filtered_college_course_category_courses.append(course.copy())

    return filtered_college_course_category_courses

def get_masked_college_course_category_course_recommendations(user_vector, college_course_category_user_vector_index, filtered_college_courses, top_college_course_category_user_vector_indexes):
    masked_college_course_category_user_vector = get_masked_college_course_category_user_vector(user_vector, college_course_category_user_vector_index, top_college_course_category_user_vector_indexes)

    cached_masked_college_course_category_user_vector_magnitude = np.linalg.norm(masked_college_course_category_user_vector)
    
    for course in filtered_college_courses:
        course["similarity_score"] = get_cosine_similarity(masked_college_course_category_user_vector, cached_masked_college_course_category_user_vector_magnitude, course["vectorized_representation"])

    masked_college_course_category_course_recommendations = sorted(
        filtered_college_courses,
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    return masked_college_course_category_course_recommendations

def get_masked_college_course_category_user_vector(user_vector, college_course_category_user_vector_index, top_college_course_category_user_vector_indexes):
    masked_college_course_category_user_vector = user_vector.copy()

    mask_riasec_interests_in_user_vector_for_college_course_category(college_course_category_user_vector_index, masked_college_course_category_user_vector)

    mask_college_course_categories_in_user_vector(college_course_category_user_vector_index, masked_college_course_category_user_vector, top_college_course_category_user_vector_indexes)

    if IS_DEBUG:
        print(COLLEGE_COURSE_CATEGORIES[college_course_category_user_vector_index - STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX] + str(masked_college_course_category_user_vector))

    return masked_college_course_category_user_vector

def mask_riasec_interests_in_user_vector_for_college_course_category(college_course_category_user_vector_index, masked_college_course_category_user_vector):
    masked_riasec_interests_for_college_course_category = get_riasec_interests_for_college_course_category(college_course_category_user_vector_index)

    for i in range(0, POINTS_VECTOR_INDEX):
        if RIASEC_INTERESTS[i] not in masked_riasec_interests_for_college_course_category:
            masked_college_course_category_user_vector[i] = 0.0

def mask_college_course_categories_in_user_vector(college_course_category_user_vector_index, masked_college_course_category_user_vector, top_college_course_category_user_vector_indexes):
    # education is a special case
    # we want to recommend education courses that match their categories
    # e.g. interest in math + education = maths teacher
    # e.g. interest in business + education = business teacher
    if (college_course_category_user_vector_index - STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX) == COLLEGE_COURSE_CATEGORIES.index("education"):
        college_course_category_user_vector_indexes = top_college_course_category_user_vector_indexes[0:MINIMUM_NUMBER_OF_COLLEGE_COURSE_CATEGORIES_TO_RECOMMEND]
    else:
        college_course_category_user_vector_indexes = [college_course_category_user_vector_index]

    for i in range(STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX, len(masked_college_course_category_user_vector)):
        if i not in college_course_category_user_vector_indexes:
            masked_college_course_category_user_vector[i] = 0.0

def get_riasec_interests_for_college_course_category(college_course_category_user_vector_index):
    college_course_category = COLLEGE_COURSE_CATEGORIES[college_course_category_user_vector_index - STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX]

    match college_course_category:
        case "agriculture":
            return ["realistic", "investigative", "enterprising", "conventional"]
        case "architecture and construction":
            return ["realistic", "investigative", "artistic", "enterprising", "conventional"]
        case "business":
            return ["enterprising", "conventional"]
        case "chemical science":
            return ["realistic", "investigative"]
        case "computers":
            return ["realistic", "investigative", "artistic", "enterprising", "conventional"]
        case "communications":
            return ["investigative", "artistic", "enterprising"]
        case "creative arts":
            return ["realistic", "investigative", "artistic"]
        case "education":
            # education is a unique case where we want to recommend education courses that match their riasec makeup, so we don't want to mask anything
            # e.g. strong affininty towards A + education = arts teacher
            # e.g. strong affininty towards I + education = maths/science teacher
            return RIASEC_INTERESTS
        case "engineering":
            return ["realistic", "investigative"]
        case "environment":
            return ["realistic", "investigative", "enterprising"]
        case "healthcare":
            return ["realistic", "investigative", "social", "conventional"] # C for pharmacy technician
        case "hospitality":
            return ["realistic", "artistic", "social", "enterprising", "conventional"]
        case "humanities":
            return ["investigative", "artistic"]
        case "languages":
            # we also want courses that have languages as an option, e.g. Business with German, Computer Science and Linguistics
            return RIASEC_INTERESTS
        case "law":
            return ["investigative", "social", "enterprising", "conventional"]
        case "life science":
            return ["realistic", "investigative"]
        case "mathematics":
            return ["investigative", "conventional"]
        case "physical science":
            return ["realistic", "investigative"]
        case "social science":
            return ["investigative", "social"]
        case "sport":
            return ["realistic", "investigative", "social", "enterprising"]
        case "welfare":
            return ["social"]
        case _:
            print("Error! Unrecognised college_course_category!" + college_course_category + college_course_category_user_vector_index)
            return []

def add_unique_college_course_recommendations(masked_college_course_category_course_recommendations_to_add, previously_recommended_college_courses):
    number_of_unique_courses_added = 0

    for i in range(len(masked_college_course_category_course_recommendations_to_add)):
        if number_of_unique_courses_added == MAXIMUM_NUMBER_OF_RECOMMENDED_COURSES_PER_CATEGORY or len(previously_recommended_college_courses) == NUMBER_OF_COLLEGE_COURSE_RECOMMENDATIONS:
            return

        if is_unique_college_course_recommendation(masked_college_course_category_course_recommendations_to_add[i], previously_recommended_college_courses):
            previously_recommended_college_courses.append(masked_college_course_category_course_recommendations_to_add[i].copy())
            number_of_unique_courses_added += 1

def is_unique_college_course_recommendation(college_course_to_check, previously_recommended_college_courses):
    for previously_recommended_college_course in previously_recommended_college_courses:
        if is_college_course_duplicate(previously_recommended_college_course, college_course_to_check):
            if IS_DEBUG:
                print("Not recommending " + college_course_to_check['title'] + " " + college_course_to_check['id'] + " because " + previously_recommended_college_course['title'] + " " + previously_recommended_college_course['id'] + " is already recommended.\n")

            return False
        
    return True

def is_college_course_duplicate(previously_recommended_college_course, college_course_to_check):
    return is_exact_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check) or is_substring_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check)

def is_exact_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
    return previously_recommended_college_course['preprocessed_title'] == college_course_to_check['preprocessed_title']

SUBSTRING_MATCH_PREPROCESSED_COLLEGE_COURSE_TITLE_EDGE_CASES = ["engin", "technolog", "therapi", "servic", "manag", "art", "public", "educ", "sport", "architectur", "intern", "medicin", "comput"]
def is_substring_match_with_preprocessed_college_course_title(previously_recommended_college_course, college_course_to_check):
    tokenized_college_course_title_words = previously_recommended_college_course['preprocessed_title'].split(' ')

    for token in tokenized_college_course_title_words:
        if token not in SUBSTRING_MATCH_PREPROCESSED_COLLEGE_COURSE_TITLE_EDGE_CASES and token in college_course_to_check['preprocessed_title'] and are_both_college_courses_education_or_non_education(previously_recommended_college_course, college_course_to_check):
            return True

    return False

def are_both_college_courses_education_or_non_education(previously_recommended_college_course, college_course_to_check):
    return ("education" in previously_recommended_college_course["categories"]) == ("education" in college_course_to_check["categories"])

def get_normalized_points_vector(points):
    # somec courses are over 625 points (because of portfolios, interviews, etc.)
    # so if the course exceeds 625 points, vectorize the course as if it had 625 points (keeps the normalisation between 0 and 625 points)
    points = min(points, MAX_COURSE_POINTS)

    return np.array([(points - MIN_COURSE_POINTS) / (MAX_COURSE_POINTS - MIN_COURSE_POINTS)])

def get_user_riasec_vector(user_interest_questions_results_vector):
    user_riasec_vector = np.zeros(len(RIASEC_INTERESTS))

    for i in range(len(user_interest_questions_results_vector)):
        user_riasec_vector_index = RIASEC_INTERESTS.index(USER_INTEREST_QUESTIONS_RIASEC_INTERESTS[i])
        user_riasec_vector[user_riasec_vector_index] += FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[user_interest_questions_results_vector[i]]

    for i in range(len(user_riasec_vector)):
        user_riasec_vector[i] = custom_normalized_sigmoid_function(user_riasec_vector[i], RIASEC_INTEREST_NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT)

    if IS_DEBUG:
        print(get_stringified_riasec_vector(user_riasec_vector))

    return user_riasec_vector

def add_vectorized_college_course_as_attribute(course):
    course['vectorized_representation'] = get_vectorized_college_course_representation(course)

def get_vectorized_college_course_representation(college_course):
    vectorized_representation = np.zeros(VECTORIZED_REPRESENTATION_DIMENSION_SIZE)

    for interest in college_course["riasec_interests"]:
        vectorized_representation[RIASEC_INTERESTS.index(interest)] = 1.0

    vectorized_representation[POINTS_VECTOR_INDEX] = get_normalized_points_vector(college_course['points'])[0]

    for category in college_course['categories']:
        vectorized_representation[STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX + COLLEGE_COURSE_CATEGORIES.index(category)] = 1.0

    return vectorized_representation

def get_cosine_similarity(user_vector, cached_user_vector_magnitude, course_vector):
    return np.dot(user_vector, course_vector) / (cached_user_vector_magnitude * np.linalg.norm(course_vector))

def get_stringified_college_course_categories_vector(college_course_categories_vector):
    stringified_college_course_categories_vector = ""
    for i in range(len(college_course_categories_vector)):
        stringified_college_course_categories_vector += COLLEGE_COURSE_CATEGORIES[i] + ": " + str(round(college_course_categories_vector[i], 2)) + "\n" + ("\n" if i == len(college_course_categories_vector)-1 else "")

    return stringified_college_course_categories_vector

def get_stringified_riasec_vector(riasec_vector):
    stringified_riasec_vector = ""

    for i in range(len(riasec_vector)):
        stringified_riasec_vector += RIASEC_INTERESTS[i] + ": " + str(round(riasec_vector[i], 2)) + "\n" + ("\n" if i == len(riasec_vector)-1 else "")

    return stringified_riasec_vector

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

def get_stringified_college_course_recommendations(college_course_recommendations):
    stringified_college_course_recommendations = ""

    for i in range(len(college_course_recommendations)):
        stringified_college_course_recommendations += str(i+1) + ".\n"
        stringified_college_course_recommendations += "ID & Title: " + college_course_recommendations[i]["id"] + " " + college_course_recommendations[i]["title"] + "\n"

        if IS_DEBUG:
            stringified_college_course_recommendations += "Preprocessed title: " + college_course_recommendations[i]["preprocessed_title"] + "\n"

        stringified_college_course_recommendations += "College: " + college_course_recommendations[i]["college"] + "\n"
        stringified_college_course_recommendations += "RIASEC Interests: " + get_stringified_interests_or_categories(college_course_recommendations[i]["riasec_interests"]) + "\n"
        stringified_college_course_recommendations += "Categories: " + get_stringified_interests_or_categories(college_course_recommendations[i]["categories"]) + "\n"
        stringified_college_course_recommendations += "Points: " + str(college_course_recommendations[i]["points"]) + "\n"
        stringified_college_course_recommendations += "Similarity: " + (str(round(college_course_recommendations[i]["similarity_score"]*100.0, 1)) if "similarity_score" in college_course_recommendations[i] else "-1") + "%" + "\n"
        stringified_college_course_recommendations += "Overview: " + college_course_recommendations[i]["overview"] + "\n"
        if IS_DEBUG:
            stringified_college_course_recommendations += "Vectorized Representation: " + str(college_course_recommendations[i]['vectorized_representation']) + "\n"
        
        if "recommendation_justification" in college_course_recommendations[i]:
            stringified_college_course_recommendations += "Why we recommended this: " + college_course_recommendations[i]['recommendation_justification'] + "\n"
        
        stringified_college_course_recommendations += "\n\n"

    return stringified_college_course_recommendations

def get_baseline_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences):
    filtered_college_courses = get_filtered_college_courses(user_college_course_preferences)

    baseline_college_course_recommendations = sorted(
        filtered_college_courses,
        key=lambda x: x["points"],
        reverse=True
    )

    unique_baseline_college_course_recommendations = []

    for _ in range(MINIMUM_NUMBER_OF_COLLEGE_COURSE_CATEGORIES_TO_RECOMMEND):
        add_unique_college_course_recommendations(baseline_college_course_recommendations, unique_baseline_college_course_recommendations)

    user_vector = get_user_vector(user_interest_questions_results_vector, user_college_course_preferences)
    cached_user_vector_magnitude = np.linalg.norm(user_vector)

    add_justifications_for_college_course_recommendations(unique_baseline_college_course_recommendations, user_vector)

    for course in unique_baseline_college_course_recommendations:
        course["similarity_score"] = get_cosine_similarity(user_vector, cached_user_vector_magnitude, course["vectorized_representation"])

    return unique_baseline_college_course_recommendations

def add_justifications_for_college_course_recommendations(college_course_recommendations, user_vector):
    if not IS_DEBUG:
        for i in range(len(parsed_college_course_justifications)):
            college_course_recommendations[i]["recommendation_justification"] = ""
            return

    prompt = get_gemini_prompt(college_course_recommendations, user_vector)

    response = GEMINI_CLIENT.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    parsed_college_course_justifications = get_parsed_college_course_justifications(response.text)

    if len(parsed_college_course_justifications) != len(college_course_recommendations):
        print("parsing error!")
        print("len parse" + str(len(parsed_college_course_justifications)))
        print("len recs" + str(len(college_course_recommendations)))

    for i in range(len(parsed_college_course_justifications)):
        college_course_recommendations[i]["recommendation_justification"] = parsed_college_course_justifications[i]

def get_gemini_prompt(college_course_recommendations, user_vector):
    gemini_prompt = "Act as an expert in Guidance Counseling for Irish College Courses. I am creating a Recommender System for Irish College Courses. You will have 2 pieces of information about the user:\n1. Their RIASEC makeup - each value is normalised between 0.0 and 1.0. \n2. Their college course category interest scores - each value is also normalised between 0.0 and 1.0. These scores represent their interests towards different areas of study.\n\nThe user of this Recommender System has the the following information:\n\n"

    gemini_prompt += "User RIASEC Interest Scores:\n\n" + get_stringified_riasec_vector(user_vector[0:len(RIASEC_INTERESTS)])

    gemini_prompt += "User College Course Category Interest Scores:\n\n" + get_stringified_college_course_categories_vector(user_vector[STARTING_COLLEGE_COURSE_CATEGORY_VECTOR_INDEX:])

    gemini_prompt += "And here are the college courses that were recommended to the user:\n\n" + get_stringified_college_course_recommendations(college_course_recommendations)

    gemini_prompt += "\nI would like you to generate a justification for each recommendation. The justification for each recommendation should be no longer than 30 words. Please do not directly cite any raw score values in your written justification, as the user cannot see this. Please use the name of the course in your justification, and use the title of the course instead of saying \"this course\", etc.. I would like your output to strictly follow the format provided below - do not add any additional text, as I will parse your response:\nSample Output:\n```\n1. With a maximum Investigative score, your profile aligns strongly with Mathematics, which demands the high-level logical reasoning, analytical depth, and complex problem-solving skills you naturally possess.\n2. Computer Science suits your Investigative nature and technical interests, offering a perfect outlet for your strong analytical capabilities through software engineering, programming, and developing innovative technological solutions.\n3. Dental Science uniquely balances your highest traits; it requires the intellectual rigor of an investigator, the social empathy for patient care, and the realistic coordination for clinical procedures.\n4. etc.\n```"

    return gemini_prompt

def get_parsed_college_course_justifications(response_text):
    parsed_college_course_justifications = re.split(r'[1-2]?[0-9]{1}\. ', response_text)

    parsed_college_course_justifications.pop(0)

    for i in range(len(parsed_college_course_justifications)):
        parsed_college_course_justifications[i] = parsed_college_course_justifications[i].strip()

    return parsed_college_course_justifications

def get_stringified_interests_or_categories(interests_or_categories):
    stringified_interests_or_categories = ""

    for i in range(len(interests_or_categories)):
        if i > 0:
            stringified_interests_or_categories += ", "

        interest_or_category_to_add = interests_or_categories[i]

        split_interest_or_category_to_add = interest_or_category_to_add.split()

        for j in range(len(split_interest_or_category_to_add)):
            split_interest_or_category_to_add[j] = split_interest_or_category_to_add[j].capitalize()

        interest_or_category_to_add = ' '.join(split_interest_or_category_to_add)

        stringified_interests_or_categories += interest_or_category_to_add

    return stringified_interests_or_categories

def get_user_data():
    df = pd.read_csv(SURVEY_PART_1_RESPONSES_DATASET_LOCATION, sep='\t')

    df = df.fillna("")

    df.pop("Timestamp")

    # just get the last row (latest entry)
    return df.iloc[-1]

def get_user_colleges(user_data):
    user_colleges = ""

    for column_name, value in user_data.items():
        if column_name.startswith(SURVEY_PART_1_RESPONSES_DATASET_COLLEGES_STARTING_COLUMN_NAME) and value != "":
            user_colleges += str(value) + ", "

    if user_colleges[-1] == " ":
        user_colleges = user_colleges[0:len(user_colleges)-2]

    return user_colleges.split(", ")

def get_user_college_course_preferences(user_data):
    user_college_course_preferences = {"nfq_levels": [], "colleges": [], "expected_points": 0}

    nfq_levels = get_user_nfq_levels(user_data[SURVEY_PART_1_RESPONSES_DATASET_NFQ_LEVELS_COLUMN_NAME])
    expected_points = get_user_expected_leaving_cert_points(str(user_data[SURVEY_PART_1_RESPONSES_DATASET_EXPECTED_LEAVING_CERT_POINTS_COLUMN_NAME]))
    colleges = get_user_colleges(user_data)

    user_college_course_preferences["nfq_levels"] = nfq_levels
    user_college_course_preferences["expected_points"] = expected_points
    user_college_course_preferences["colleges"] = colleges

    return user_college_course_preferences

def get_user_nfq_levels(raw_nfq_levels):
    raw_nfq_levels = raw_nfq_levels.replace("Level ", "")

    nfq_levels = raw_nfq_levels.split(", ")

    for i in range(len(nfq_levels)):
        nfq_levels[i] = int(nfq_levels[i])

    return nfq_levels

def get_user_expected_leaving_cert_points(raw_leaving_cert_points):
    raw_leaving_cert_points = re.findall(r'\d+', raw_leaving_cert_points)

    return int(raw_leaving_cert_points[0])

def get_user_interest_questions_results_vector(user_data):
    user_data = user_data.drop([SURVEY_PART_1_RESPONSES_DATASET_NFQ_LEVELS_COLUMN_NAME, SURVEY_PART_1_RESPONSES_DATASET_EXPECTED_LEAVING_CERT_POINTS_COLUMN_NAME])
    columns_to_remove = [column for column in user_data.index if column.startswith(SURVEY_PART_1_RESPONSES_DATASET_COLLEGES_STARTING_COLUMN_NAME)]
    user_data = user_data.drop(columns_to_remove)

    user_interest_activities = get_user_interest_activities()
    user_interest_questions_results_vector = np.zeros(len(user_interest_activities))

    for column_name, value in user_data.items():
        column_name = column_name.lower()

        index_to_access = user_interest_activities.index(column_name)
        user_interest_questions_results_vector[index_to_access] = int(value) - 1

    for i in range(len(user_interest_questions_results_vector)):
        if user_interest_questions_results_vector[i] not in [1, 2, 3, 4, 5]:
            print("missing activity! " + str(user_interest_activities[i]))

    return user_interest_questions_results_vector

