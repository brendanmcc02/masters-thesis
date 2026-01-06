from college_course_recommender_system_utils import *

# # brendan
# user_college_course_preferences = { "nfq_levels": [8],
#                                     "colleges": ["Trinity College Dublin",
#                                                  "University College Dublin",
#                                                  "Royal College of Surgeons in Ireland"],
#                                     "expected_points": 601}

# user_open_psychometrics_questions_vector = [0, 0, 0, 0, 0, 0, 0, 0, # R
#                                             3, 3, 4, 4, 4, 3, 3, 2, # I
#                                             0, 2, 0, 0, 2, 0, 0, 0, # A
#                                             4, 3, 1, 1, 2, 3, 2, 1, # S
#                                             0, 1, 3, 0, 2, 1, 0, 1, # E
#                                             1, 1, 4, 3, 4, 2, 2, 2] # C

# user_leaving_cert_subject_preferences = { 
#                                 "Mathematics": 4,
#                                 "English": 2,
#                                 "Irish": 1,
#                                 "Physics": 4,
#                                 "Computer Science": 4,
#                                 "Design and Communication Graphics": 4,
#                                 "German": 2
#                                 }

# aysha
# her recs suck ASS
user_college_course_preferences = { "nfq_levels": [8],
                                    "colleges": ["Trinity College Dublin",
                                                 "University College Dublin",
                                                 "Royal College of Surgeons in Ireland"],
                                    "expected_points": 625}

user_open_psychometrics_questions_vector = [2, 0, 0, 2, 0, 0, 1, 0, # R
                                            4, 3, 3, 4, 3, 3, 2, 2, # I
                                            0, 2, 3, 1, 3, 2, 0, 3, # A
                                            4, 4, 4, 2, 4, 3, 4, 4, # S
                                            0, 0, 2, 0, 2, 1, 1, 1, # E
                                            2, 0, 1, 2, 2, 3, 2, 2] # C

user_leaving_cert_subject_preferences    = {"Mathematics": 3, # can re-phrase question as "how much would you enjoy/find interesting studying this in college?"
                               "English": 4, # can re-phrase question as "how much would you enjoy/find interesting studying this in college?"
                               "Irish": 4, # can re-phrase question as "how much would you enjoy/find interesting studying this in college?"
                               "Business": 2, 
                               "Chemistry": 4, 
                               "Biology": 3, # can re-phrase question as "how much would you enjoy/find interesting studying this in college?"
                               "German": 4 # can re-phrase question as "how much would you enjoy/find interesting studying this in college?"
                                }

# # vivi
# user_college_course_preferences = { "nfq_levels": [8],
#                                     "colleges": ["Trinity College Dublin",
#                                                  "University College Dublin",
#                                                  "Dublin City University"],
#                                     "expected_points": 576}

# user_open_psychometrics_questions_vector = [ 1, 2, 0, 2, 1, 3, 1, 2, # R
#                        3, 3, 3, 1, 1, 1, 1, 1, # I
#                        0, 0, 2, 2, 0, 2, 2, 0, # A
#                        0, 2, 3, 3, 1, 1, 2, 0, # S
#                        3, 1, 1, 2, 2, 1, 3, 0, # E
#                        3, 0, 2, 1, 2, 4, 4, 3] # C

# user_leaving_cert_subject_preferences = { 
#                                 "Mathematics": 3, 
#                                 "English": 1, 
#                                 "Irish": 2, 
#                                 "Economics": 3, 
#                                 "Accounting": 4, 
#                                 "Physics": 3, 
#                                 "German": 3
#                                 }

# # adam - TODO points
# user_college_course_preferences = { "nfq_levels": [8],
#                                     "colleges": ["Trinity College Dublin",
#                                                  "University College Dublin",
#                                                  "Dublin City University"],
#                                     "expected_points": 576}
# user_open_psychometrics_questions_vector = [ 2, 2, 3, 3, 2, 2, 3, 2, # R
#                        2, 0, 0, 1, 1, 0, 1, 2, # I
#                        0, 0, 2, 0, 0, 0, 3, 0, # A
#                        0, 2, 0, 3, 1, 0, 0, 0, # S
#                        4, 3, 2, 2, 2, 3, 3, 0, # E
#                        3, 0, 3, 1, 2, 3, 3, 2] # C

# user_leaving_cert_subject_preferences = { 
#                                 "Mathematics": 3, 
#                                 "English": 2, 
#                                 "Irish": 2, 
#                                 "Spanish": 3, 
#                                 "Accounting": 4, 
#                                 "Economics": 4, 
#                                 "Physical Education": 4
#                                 }

# # matthew - TODO points
# user_college_course_preferences = { "nfq_levels": [8],
#                                     "colleges": ["Trinity College Dublin",
#                                                  "University College Dublin",
#                                                  "Dublin City University"],
#                                     "expected_points": 576}
# user_open_psychometrics_questions_vector = [ 2, 1, 2, 3, 3, 3, 2, 1, # R
#                        1, 0, 0, 2, 1, 0, 0, 1, # I
#                        0, 0, 0, 2, 0, 0, 4, 0, # A
#                        0, 0, 1, 3, 1, 0, 1, 0, # S
#                        3, 2, 2, 3, 3, 1, 4, 0, # E
#                        0, 0, 2, 1, 0, 3, 3, 2] # C

# user_leaving_cert_subject_preferences = { 
#                                 "Mathematics": 2, 
#                                 "English": 1, 
#                                 "Irish": 1, 
#                                 "Business": 3, 
#                                 "Economics": 4, 
#                                 "Physical Education": 4, 
#                                 "Spanish": 2
#                                 }

college_course_recommendations = get_college_course_recommendations(user_open_psychometrics_questions_vector, user_college_course_preferences, user_leaving_cert_subject_preferences, should_reuse_trained_open_psychometrics_model=True)

baseline_college_course_recommendations = get_baseline_college_course_recommendations(user_college_course_preferences)

print("BASELINE COLLEGE COURSE RECOMMENDATIONS:\n")
print_college_course_recommendations(baseline_college_course_recommendations)

print("COLLEGE COURSE RECOMMENDATIONS:\n")
print_college_course_recommendations(college_course_recommendations)
