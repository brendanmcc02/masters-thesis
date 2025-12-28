from traditional_prototype_utils import *

user_college_course_preferences = { "nfq_levels": [8], 
                                    "colleges": ["Trinity College Dublin", 
                                                 "University College Dublin", 
                                                 "Dublin City University"], 
                                    "expected_points": 732}

user_riasec_vector = [ 1, 2, 0, 2, 1, 3, 1, 2, # R
                       3, 3, 3, 1, 1, 1, 1, 1, # I
                       0, 0, 2, 2, 0, 2, 2, 0, # A
                       0, 2, 3, 3, 1, 1, 2, 0, # S
                       3, 1, 1, 2, 2, 1, 3, 0, # E
                       3, 0, 2, 1, 2, 4, 4, 3] # C

user_leaving_cert_subject_preferences = { 
                                "Mathematics": 3, 
                                "English": 1, 
                                "Irish": 2, 
                                "Economics": 3, 
                                "Accounting": 4, 
                                "Physics": 3, 
                                "German": 3
                                }

filtered_cao_courses = get_filtered_cao_courses(user_college_course_preferences)

top_k_recommendations = get_top_k_recommendations(filtered_cao_courses, user_riasec_vector, user_college_course_preferences, user_leaving_cert_subject_preferences, k=20, should_retrain_model=False  )

for rec in top_k_recommendations:
    print(rec["title"] + "\n" + rec["college"] + "\nPoints: " + str(rec["points"]) + "\nCategories: " + str(rec["categories"]) + "\nSimilarity: " + str(round(rec["similarity"]*100.0, 1)) + "%\n")
