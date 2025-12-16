from traditional_prototype_utils import *

user_college_course_preferences = { "nfq_levels": [8], 
                                    "colleges": ["Trinity College Dublin - TCD", 
                                                 "University College Dublin - UCD", 
                                                 "RCSI University of Medicine and Health Sciences"], 
                                    "expected_points": 589}
user_riasec_vector = [ 0, 0, 0, 0, 0, 0, 0, 0, # R
                       3, 3, 4, 4, 4, 3, 3, 2, # I
                       0, 2, 0, 0, 2, 0, 0, 0, # A
                       4, 4, 1, 2, 2, 3, 2, 1, # S
                       0, 1, 3, 0, 2, 1, 0, 1, # E
                       1, 1, 4, 3, 4, 2, 2, 2] # C
user_lc_subject_preferences = { 
                                "Mathematics": 4, 
                                "English": 3, 
                                "Irish": 1, 
                                "Physics": 4, 
                                "Design and Communication Graphics": 4, 
                                "Computer Science": 4, 
                                "German": 2
                                }

filtered_cao_courses = get_filtered_cao_courses(user_college_course_preferences)

top_k_recommendations = get_top_k_recommendations(filtered_cao_courses, user_riasec_vector, user_college_course_preferences, user_lc_subject_preferences, k=20, should_retrain_model=False)

for rec in top_k_recommendations:
    print(rec["title"] + "\n" + rec["college"] + "\nPoints: " + str(rec["points"]) + "\nSimilarity: " + str(round(rec["similarity"]*100.0, 1)) + "%\n")
