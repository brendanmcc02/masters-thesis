import csv
import re
import numpy as np
import pandas as pd
from college_course_title_nlp_utils import *
from college_course_recommender_system_utils import *

USER_EVALUATION_METRICS_DATASET_FILEPATH = "user-evaluation-metrics.tsv"
SURVEY_PART_1_RESPONSES_DATASET_NFQ_LEVELS_COLUMN_NAME = "NFQ Levels"
SURVEY_PART_1_RESPONSES_DATASET_EXPECTED_LEAVING_CERT_POINTS_COLUMN_NAME = "Expected Leaving Cert Points"
SURVEY_PART_1_RESPONSES_DATASET_COLLEGES_STARTING_COLUMN_NAME = "Colleges - "
SURVEY_PART_2_RESPONSES_DATASET_GROUND_TRUTH_COLLEGE_COURSE_COLUMN_NAME = "Please list the courses (Level 8) on your CAO Application."
RECOMMENDATION_SET_1_PREAMBLE = "[RECOMMENDATION SET 1] "
RECOMMENDATION_SET_2_PREAMBLE = "[RECOMMENDATION SET 2] "
SURVEY_PART_2_RESPONSES_DATASET_RECOMMENDATION_SET_1_RELEVANCE_COLUMN_NAME = RECOMMENDATION_SET_1_PREAMBLE + "Please take some time to look at your college course Recommendations."
SURVEY_PART_2_RESPONSES_DATASET_RECOMMENDATION_SET_2_RELEVANCE_COLUMN_NAME = RECOMMENDATION_SET_2_PREAMBLE + "Please take some time to look at your college course Recommendations."
SURVEY_PART_2_RESPONSES_DATASET_DIVERSITY_SET_1_COLUMN_NAME = RECOMMENDATION_SET_1_PREAMBLE + "How much would you agree with the following statement?  The courses recommended from set 1 offered a diverse variety of choices (e.g. different fields of study, colleges, etc.)"
SURVEY_PART_2_RESPONSES_DATASET_DIVERSITY_SET_2_COLUMN_NAME = RECOMMENDATION_SET_2_PREAMBLE + "How much would you agree with the following statement?  The courses recommended from set 2 offered a diverse variety of choices (e.g. different fields of study, colleges, etc.)"
SURVEY_PART_2_RESPONSES_DATASET_TRUST_SET_1_COLUMN_NAME = RECOMMENDATION_SET_1_PREAMBLE + "How much would you agree with the following statement?  I trust that the system recommended courses from set 1 that are well-suited to my interests and preferences."
SURVEY_PART_2_RESPONSES_DATASET_TRUST_SET_2_COLUMN_NAME = RECOMMENDATION_SET_2_PREAMBLE + "How much would you agree with the following statement?  I trust that the system recommended courses from set 2 that are well-suited to my interests and preferences."
SURVEY_PART_2_RESPONSES_DATASET_FEEDBACK_COLUMN_NAME = "Any feedback?"


def get_user_interest_activities():
    df = pd.read_csv(USER_INTEREST_QUESTIONS_DATASET_FILEPATH)

    activities = df['activity'].str.lower().tolist()

    return activities

def get_user_data_and_timestamp(survey_part_x_responses_dataset_location):
    df = pd.read_csv(survey_part_x_responses_dataset_location, sep='\t')

    df = df.fillna("")

    # just get the last row (latest entry)
    timestamp = df.iloc[-1]["Timestamp"]
    df.pop("Timestamp")

    return df.iloc[-1], timestamp

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

    return max(min(int(raw_leaving_cert_points[0]), MAX_COURSE_POINTS), MIN_COURSE_POINTS)

def get_user_interest_questions_results_vector(user_data):
    user_data = user_data.drop([SURVEY_PART_1_RESPONSES_DATASET_NFQ_LEVELS_COLUMN_NAME, SURVEY_PART_1_RESPONSES_DATASET_EXPECTED_LEAVING_CERT_POINTS_COLUMN_NAME])
    columns_to_remove = [column for column in user_data.index if column.startswith(SURVEY_PART_1_RESPONSES_DATASET_COLLEGES_STARTING_COLUMN_NAME)]
    user_data = user_data.drop(columns_to_remove)

    user_interest_activities = get_user_interest_activities()
    user_interest_questions_results_vector = np.zeros(len(user_interest_activities))

    for column_name, value in user_data.items():
        column_name = column_name.lower()

        index_to_access = user_interest_activities.index(column_name)
        user_interest_questions_results_vector[index_to_access] = int(value)

    for i in range(len(user_interest_questions_results_vector)):
        if user_interest_questions_results_vector[i] not in [1, 2, 3, 4, 5]:
            print("missing activity! " + str(user_interest_activities[i]))

    return user_interest_questions_results_vector

def write_user_college_course_recommendations_to_markdown(actual_college_course_recommendations, baseline_college_course_recommendations):
    markdown_output = ""
    recommendation_sets = [actual_college_course_recommendations, baseline_college_course_recommendations]

    for i in range(len(recommendation_sets)):
        markdown_output += "# RECOMMENDATION SET " + str(i+1) + "\n\n"
        markdown_output += get_stringified_markdown_college_course_recommendations(recommendation_sets[i], is_gemini_prompt=False)

    with open("user-college-course-recommendations.md", "w") as file:
        file.write(markdown_output)


def write_user_evaluation_to_csv(user_data_part_2, user_timestamp_part_1, user_timestamp_part_2, actual_college_course_recommendations, baseline_college_course_recommendations):
    preprocessed_unique_user_ground_truth_courses = get_preprocessed_unique_user_ground_truth_courses(user_data_part_2)

    actual_recommended_relevant_college_courses = get_recommended_relevant_college_courses(user_data_part_2, SURVEY_PART_2_RESPONSES_DATASET_RECOMMENDATION_SET_1_RELEVANCE_COLUMN_NAME, actual_college_course_recommendations)
    baseline_recommended_relevant_college_courses = get_recommended_relevant_college_courses(user_data_part_2, SURVEY_PART_2_RESPONSES_DATASET_RECOMMENDATION_SET_2_RELEVANCE_COLUMN_NAME, baseline_college_course_recommendations)

    actual_diversity_metric = user_data_part_2[SURVEY_PART_2_RESPONSES_DATASET_DIVERSITY_SET_1_COLUMN_NAME]
    baseline_diversity_metric = user_data_part_2[SURVEY_PART_2_RESPONSES_DATASET_DIVERSITY_SET_2_COLUMN_NAME]

    actual_trust_metric = user_data_part_2[SURVEY_PART_2_RESPONSES_DATASET_TRUST_SET_1_COLUMN_NAME]
    baseline_trust_metric = user_data_part_2[SURVEY_PART_2_RESPONSES_DATASET_TRUST_SET_2_COLUMN_NAME]

    actual_precision_metric = get_precision_metric(len(actual_recommended_relevant_college_courses), len(actual_college_course_recommendations))
    baseline_precision_metric = get_precision_metric(len(baseline_recommended_relevant_college_courses), len(baseline_college_course_recommendations))

    actual_recall_metric = get_recall_metric(preprocessed_unique_user_ground_truth_courses, actual_recommended_relevant_college_courses)
    baseline_recall_metric = get_recall_metric(preprocessed_unique_user_ground_truth_courses, baseline_recommended_relevant_college_courses)

    actual_f1_score = get_f1_score(actual_precision_metric, actual_recall_metric)
    baseline_f1_score = get_f1_score(baseline_precision_metric, baseline_recall_metric)

    actual_novelty_metric = get_novelty_metric(actual_college_course_recommendations, preprocessed_unique_user_ground_truth_courses)
    baseline_novelty_metric = get_novelty_metric(baseline_college_course_recommendations, preprocessed_unique_user_ground_truth_courses)

    actual_serendipity_metric = get_serendipity_metric(actual_college_course_recommendations, preprocessed_unique_user_ground_truth_courses, actual_recommended_relevant_college_courses)
    baseline_serendipity_metric = get_serendipity_metric(baseline_college_course_recommendations, preprocessed_unique_user_ground_truth_courses, baseline_recommended_relevant_college_courses)

    user_evaluation_metrics = [user_timestamp_part_1, user_timestamp_part_2, actual_diversity_metric, baseline_diversity_metric, actual_trust_metric, baseline_trust_metric, actual_precision_metric, baseline_precision_metric, actual_recall_metric, baseline_recall_metric, actual_f1_score, baseline_f1_score, actual_novelty_metric, baseline_novelty_metric, actual_serendipity_metric, baseline_serendipity_metric, user_data_part_2[SURVEY_PART_2_RESPONSES_DATASET_FEEDBACK_COLUMN_NAME]]

    with open(USER_EVALUATION_METRICS_DATASET_FILEPATH, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(user_evaluation_metrics)

def get_preprocessed_unique_user_ground_truth_courses(user_data_part_2):
    raw_courses = user_data_part_2[SURVEY_PART_2_RESPONSES_DATASET_GROUND_TRUTH_COLLEGE_COURSE_COLUMN_NAME]

    courses = re.split(r'\d\. +', raw_courses)
    courses.pop(0)

    for i in range(len(courses)):
        courses[i] = parse_title_from_cao_college_course(courses[i].strip())

    print("\n\nGround truth courses before uniqueifying:\n" + str(courses) + "\n")

    for i in range(len(courses)):
        courses[i] = preprocess_college_title(courses[i])

    preprocessed_unique_user_ground_truth_courses = list(set(courses))

    print("Ground truth courses after uniqueifying and preprocessing:\n" + str(preprocessed_unique_user_ground_truth_courses) + "\n\n")

    return preprocessed_unique_user_ground_truth_courses

def parse_title_from_cao_college_course(raw_course_id_and_title):
    # TR033 - TR033
    match = re.search(r'[A-Z]{2}\d{3} - [A-Z]{2}\d{3}', raw_course_id_and_title)

    if match:
        title = raw_course_id_and_title[match.end():].strip()
        return title

    # TR033 ABC
    match = re.search(r'[A-Z]{2}\d{3} [A-Z]{3}', raw_course_id_and_title)

    if match:
        title = raw_course_id_and_title[match.end():].strip()
        return title
    
    # TR033
    match = re.search(r'[A-Z]{2}\d{3}', raw_course_id_and_title)

    if match:
        title = raw_course_id_and_title[match.end():].strip()
        return title

    print("id not found in college course!" + raw_course_id_and_title)

    return raw_course_id_and_title

def get_recommended_relevant_college_courses(user_data_part_2, column_name, college_course_recommendations):
    recommended_relevant_college_courses_indices = re.findall(r'\d+', user_data_part_2[column_name])

    recommended_relevant_college_courses = []

    for i in recommended_relevant_college_courses_indices:
        recommended_relevant_college_courses.append(college_course_recommendations[int(i)].copy())

    return recommended_relevant_college_courses

def get_precision_metric(num_relevant_recommended_items, num_college_course_recommendations):
    return round(num_relevant_recommended_items / num_college_course_recommendations, 2)

def get_recall_metric(preprocessed_unique_user_ground_truth_courses, recommended_relevant_college_courses):
    all_relevant_courses = preprocessed_unique_user_ground_truth_courses.copy()

    for course in recommended_relevant_college_courses:
        if is_course_new(course, all_relevant_courses):
            all_relevant_courses.append(course["preprocessed_title"])

    return round(len(recommended_relevant_college_courses) / len(all_relevant_courses), 2)

def is_course_new(course, all_preprocessed_unique_relevant_courses):
    if course["preprocessed_title"] in all_preprocessed_unique_relevant_courses:
        return False

    return True

def get_f1_score(precision, recall):
    return round(2.0 * ((precision * recall) / (precision + recall)), 2)

def get_novelty_metric(college_course_recommendations, preprocessed_unique_user_ground_truth_courses):
    number_of_recommendations_not_in_user_ground_truth = 0

    for rec in college_course_recommendations:
        if rec["preprocessed_title"] not in preprocessed_unique_user_ground_truth_courses:
            number_of_recommendations_not_in_user_ground_truth += 1

    return number_of_recommendations_not_in_user_ground_truth / len(college_course_recommendations)

def get_serendipity_metric(college_course_recommendations, preprocessed_unique_user_ground_truth_courses, recommended_relevant_college_courses):
    number_of_serendipitous_recommendations = 0

    for relevant_rec in recommended_relevant_college_courses:
        if relevant_rec["preprocessed_title"] not in preprocessed_unique_user_ground_truth_courses:
            number_of_serendipitous_recommendations += 1

    return number_of_serendipitous_recommendations / len(college_course_recommendations)
