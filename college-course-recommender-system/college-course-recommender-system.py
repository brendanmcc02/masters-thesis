from college_course_recommender_system_utils import *
import random as rd

user_college_course_preferences = { "nfq_levels": [8],
                                    "colleges": [
                                                "Trinity College Dublin",
                                                "University College Dublin",
                                                "Royal College of Surgeons in Ireland"
                                        ],
                                    "expected_points": 625}

user_interest_questions_results_df = pd.read_csv("user_interest_questions_results.csv")
user_interest_questions_results_vector = get_user_interest_questions_results_df("brendan", user_interest_questions_results_df)

baseline_college_course_recommendations = get_baseline_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences)

actual_college_course_recommendations = get_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences)

recommendation_sets = [baseline_college_course_recommendations, actual_college_course_recommendations]

rd.shuffle(recommendation_sets)

for i in range(len(recommendation_sets)):
    print("\nRECOMMENDATION SET " + str(i+1) + ": \n")
    print(get_stringified_college_course_recommendations(recommendation_sets[i]))
