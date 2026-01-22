from college_course_recommender_system_utils import *

user_college_course_preferences = { "nfq_levels": [8],
                                    "colleges": [
                                                "Trinity College Dublin",
                                                "University College Dublin",
                                                "Royal College of Surgeons in Ireland",
                                                "University College Cork"
                                        ],
                                    "expected_points": 625}

user_interest_questions_results_df = pd.read_csv("user_interest_questions_results.csv")
user_interest_questions_results_vector = get_user_interest_questions_results_df("aysha", user_interest_questions_results_df)

# baseline_college_course_recommendations = get_baseline_college_course_recommendations(user_college_course_preferences)

# print("BASELINE COLLEGE COURSE RECOMMENDATIONS:\n")
# print_college_course_recommendations(baseline_college_course_recommendations)

college_course_recommendations = get_college_course_recommendations(user_interest_questions_results_vector, user_college_course_preferences)

print("COLLEGE COURSE RECOMMENDATIONS:\n")
print_college_course_recommendations(college_course_recommendations)
