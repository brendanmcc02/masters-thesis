from traditional_prototype_utils import *

user_college_course_preferences = { "nfq_levels": [8], 
                                    "colleges": ["Trinity College Dublin - TCD", 
                                                 "University College Dublin - UCD", 
                                                 "RCSI University of Medicine and Health Sciences"], 
                                    "expected_points": 732}
user_riasec_vector = [ 2, 0, 0, 2, 0, 0, 1, 0, # R
                       4, 3, 3, 4, 3, 3, 2, 2, # I
                       0, 2, 3, 1, 3, 2, 0, 3, # A
                       4, 4, 4, 2, 4, 3, 4, 4, # S
                       0, 0, 2, 0, 2, 1, 1, 1, # E
                       2, 0, 1, 2, 2, 3, 2, 2] # C
user_lc_subject_preferences = { 
                                "Mathematics": 3, 
                                "English": 4, 
                                "Irish": 4, 
                                "Business": 2, 
                                "Chemistry": 4, 
                                "Biology": 3, 
                                "German": 4
                                }

filtered_cao_courses = get_filtered_cao_courses(user_college_course_preferences)

top_k_recommendations = get_top_k_recommendations(filtered_cao_courses, user_riasec_vector, user_college_course_preferences, user_lc_subject_preferences, k=20, should_retrain_model=True)

for rec in top_k_recommendations:
    print(rec["title"] + "\n" + rec["college"] + "\nPoints: " + str(rec["points"]) + "\nCategories: " + str(rec["categories"]) + "\nSimilarity: " + str(round(rec["similarity"]*100.0, 1)) + "%\n")
