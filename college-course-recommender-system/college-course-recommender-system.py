from college_course_recommender_system_utils import *
import random as rd

user_data, user_timestamp = get_user_data_and_timestamp()

user_college_course_preferences = get_user_college_course_preferences(user_data)

user_interest_questions_results_vector = get_user_interest_questions_results_vector(user_data)

baseline_college_course_recommendations = get_baseline_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences)

actual_college_course_recommendations = get_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences)

write_user_college_course_recommendations(user_timestamp, actual_college_course_recommendations, baseline_college_course_recommendations)

recommendation_sets = [baseline_college_course_recommendations, actual_college_course_recommendations]

rd.shuffle(recommendation_sets)

for i in range(len(recommendation_sets)):
    print("\nRECOMMENDATION SET " + str(i+1) + ": \n")
    print(get_stringified_college_course_recommendations(recommendation_sets[i]))
