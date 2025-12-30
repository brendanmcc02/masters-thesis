from traditional_prototype_utils import *

user_college_course_preferences = { "nfq_levels": [8], 
                                    "colleges": ["Trinity College Dublin", 
                                                 "University College Dublin", 
                                                 "Dublin City University"], 
                                    "expected_points": 732}

user_open_psychometrics_questions_vector = [1, 2, 0, 2, 1, 3, 1, 2, # R
                                            3, 3, 3, 1, 1, 1, 1, 1, # I
                                            0, 0, 2, 2, 0, 2, 2, 0, # A
                                            0, 2, 3, 3, 1, 1, 2, 0, # S
                                            3, 1, 1, 2, 2, 1, 3, 0, # E
                                            3, 0, 2, 1, 2, 4, 4, 3] # C

user_leaving_cert_subject_preferences = { 
                                "Mathematics": 4, 
                                "English": 4, 
                                "Irish": 1, 
                                "Physics": 4, 
                                "Computer Science": 4, 
                                "Design and Communication Graphics": 4, 
                                "German": 2
                                }

get_user_riasec_vector(user_open_psychometrics_questions_vector, user_leaving_cert_subject_preferences)

# filtered_cao_courses = get_filtered_cao_courses(user_college_course_preferences)

# top_k_recommendations = get_top_k_recommendations(filtered_cao_courses, user_open_psyschometrics_questions_vector, user_college_course_preferences, user_leaving_cert_subject_preferences, k=20, should_reuse_trained_open_psychometrics_model=True)

# for rec in top_k_recommendations:
#     print(rec["title"] + "\n" + rec["college"] + "\nPoints: " + str(rec["points"]) + "\nCategories: " + str(rec["categories"]) + "\nSimilarity: " + str(round(rec["similarity"]*100.0, 1)) + "%\n")
