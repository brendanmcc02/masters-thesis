from college_course_recommender_system_utils import *
import random as rd

user_data, user_timestamp = get_user_data_and_timestamp()

user_college_course_preferences = get_user_college_course_preferences(user_data)

user_interest_questions_results_vector = get_user_interest_questions_results_vector(user_data)

baseline_college_course_recommendations = get_baseline_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences)

actual_college_course_recommendations = get_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences)

user_college_course_recommendations_results_df = pd.read_csv(USER_COLLEGE_COURSE_RECOMMENDATIONS_DATASET_FILEPATH, sep='\t')

user_college_course_recommendations_results = [user_timestamp]

for i in range(len(actual_college_course_recommendations)):
    course_id_and_title = "" + actual_college_course_recommendations[i]["id"] + " " + actual_college_course_recommendations[i]["title"]
    user_college_course_recommendations_results.append(course_id_and_title)

for i in range(len(baseline_college_course_recommendations)):
    course_id_and_title = "" + baseline_college_course_recommendations[i]["id"] + " " + baseline_college_course_recommendations[i]["title"]
    user_college_course_recommendations_results.append(course_id_and_title)

user_college_course_recommendations_results_df.loc[-1] = user_college_course_recommendations_results

user_college_course_recommendations_results_df.to_csv(sep='\t')

recommendation_sets = [baseline_college_course_recommendations, actual_college_course_recommendations]

rd.shuffle(recommendation_sets)

for i in range(len(recommendation_sets)):
    print("\nRECOMMENDATION SET " + str(i+1) + ": \n")
    print(get_stringified_college_course_recommendations(recommendation_sets[i]))
