from traditional_prototype_utils import *

# adam
user_college_course_preferences = { "nfq_levels": [8], 
                                    "colleges": ["Trinity College Dublin - TCD", 
                                                 "University College Dublin - UCD", 
                                                 "Dublin City University - DCU"], 
                                    "expected_points": 732}

# # matthew
# user_college_course_preferences = { "nfq_levels": [8], 
#                                     "colleges": ["Trinity College Dublin - TCD", 
#                                                  "University College Dublin - UCD", 
#                                                  "Dublin City University - DCU"], 
#                                     "expected_points": 732}

# # vivi
# user_college_course_preferences = { "nfq_levels": [8], 
#                                     "colleges": ["Trinity College Dublin - TCD", 
#                                                  "University College Dublin - UCD", 
#                                                  "Dublin City University - DCU"], 
#                                     "expected_points": 732}

# # adam
# user_riasec_vector = [ 2, 2, 3, 3, 2, 2, 3, 2, # R
#                        2, 0, 0, 1, 1, 0, 1, 2, # I
#                        0, 0, 2, 0, 0, 0, 3, 0, # A
#                        0, 2, 0, 3, 1, 0, 0, 0, # S
#                        4, 3, 2, 2, 2, 3, 3, 0, # E
#                        3, 0, 3, 1, 2, 3, 3, 2] # C

# # matthew
# user_riasec_vector = [ 2, 1, 2, 3, 3, 3, 2, 1, # R
#                        1, 0, 0, 2, 1, 0, 0, 1, # I
#                        0, 0, 0, 2, 0, 0, 4, 0, # A
#                        0, 0, 1, 3, 1, 0, 1, 0, # S
#                        3, 2, 2, 3, 3, 1, 4, 0, # E
#                        0, 0, 2, 1, 0, 3, 3, 2] # C

# vivi
user_riasec_vector = [ 1, 2, 0, 2, 1, 3, 1, 2, # R
                       3, 3, 3, 1, 1, 1, 1, 1, # I
                       0, 0, 2, 2, 0, 2, 2, 0, # A
                       0, 2, 3, 3, 1, 1, 2, 0, # S
                       3, 1, 1, 2, 2, 1, 3, 0, # E
                       3, 0, 2, 1, 2, 4, 4, 3] # C

# # adam
# user_lc_subject_preferences = { 
#                                 "Mathematics": 3, 
#                                 "English": 2, 
#                                 "Irish": 2, 
#                                 "Spanish": 3, 
#                                 "Accounting": 4, 
#                                 "Economics": 4, 
#                                 "Physical Education": 4
#                                 }

# matthew
# user_lc_subject_preferences = { 
#                                 "Mathematics": 2, 
#                                 "English": 1, 
#                                 "Irish": 1, 
#                                 "Business": 3, 
#                                 "Economics": 4, 
#                                 "Physical Education": 4, 
#                                 "Spanish": 2
#                                 }

# vivi
user_lc_subject_preferences = { 
                                "Mathematics": 3, 
                                "English": 1, 
                                "Irish": 2, 
                                "Economics": 3, 
                                "Accounting": 4, 
                                "Physics": 3, 
                                "German": 3
                                }

filtered_cao_courses = get_filtered_cao_courses(user_college_course_preferences)

top_k_recommendations = get_top_k_recommendations(filtered_cao_courses, user_riasec_vector, user_college_course_preferences, user_lc_subject_preferences, k=20, should_retrain_model=False  )

for rec in top_k_recommendations:
    print(rec["title"] + "\n" + rec["college"] + "\nPoints: " + str(rec["points"]) + "\nCategories: " + str(rec["categories"]) + "\nSimilarity: " + str(round(rec["similarity"]*100.0, 1)) + "%\n")
