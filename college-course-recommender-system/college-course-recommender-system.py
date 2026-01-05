from college_course_recommender_system_utils import *

user_college_course_preferences = { "nfq_levels": [8],
                                    "colleges": ["Trinity College Dublin",
                                                 "University College Dublin",
                                                 "Royal College of Surgeons in Ireland"],
                                    "expected_points": 601}

user_open_psychometrics_questions_vector = [0, 0, 0, 0, 0, 0, 0, 0, # R
                                            3, 3, 4, 4, 4, 3, 3, 2, # I
                                            0, 2, 0, 0, 2, 0, 0, 0, # A
                                            4, 3, 1, 1, 2, 3, 2, 1, # S
                                            0, 1, 3, 0, 2, 1, 0, 1, # E
                                            1, 1, 4, 3, 4, 2, 2, 2] # C

user_leaving_cert_subject_preferences = { 
                                "Mathematics": 4,
                                "English": 2,
                                "Irish": 1,
                                "Physics": 4,
                                "Computer Science": 4,
                                "Design and Communication Graphics": 4,
                                "German": 2
                                }

college_course_recommendations = get_college_course_recommendations(user_open_psychometrics_questions_vector, user_college_course_preferences, user_leaving_cert_subject_preferences, should_reuse_trained_open_psychometrics_model=True)

baseline_college_course_recommendations = get_baseline_college_course_recommendations(user_college_course_preferences)

print("BASELINE COLLEGE COURSE RECOMMENDATIONS:\n")
print_college_course_recommendations(baseline_college_course_recommendations)

print("COLLEGE COURSE RECOMMENDATIONS:\n")
print_college_course_recommendations(college_course_recommendations)
