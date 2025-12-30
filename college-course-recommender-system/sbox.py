import numpy as np
import pandas as pd

class LeavingCertSubject:
    riasec_interests = []
    college_major_categories = []

    def __init__(self, riasec_interests, college_major_categories):
        self.riasec_interests = riasec_interests
        self.college_major_categories = college_major_categories

RIASEC_INTERESTS = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
college_majors_and_major_categories_df = pd.read_csv("../../datasets/open-psychometrics/filter_data/college_majors_and_major_categories.tsv", sep='\t', low_memory=False)
COLLEGE_MAJOR_CATEGORIES = college_majors_and_major_categories_df["college_major_category"].unique().tolist()

LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP = {
                            # practical
                            "Construction Studies": LeavingCertSubject(["realistic"], ["industrial arts & consumer services"]),
                            "Engineering": LeavingCertSubject(["realistic", "investigative"], ["engineering"]),
                            "Technology": LeavingCertSubject(["realistic", "investigative"], ["computers & mathematics", "engineering"]),
                            # life sciences
                            "Agricultural Science": LeavingCertSubject(["investigative"], ["life science"]),
                            "Biology": LeavingCertSubject(["investigative"], ["life science", "healthcare"]),
                            # physical sciences
                            "Chemistry": LeavingCertSubject(["investigative"], ["physical science"]),
                            "Physics": LeavingCertSubject(["investigative"], ["physical science"]),
                            "Physics and Chemistry": LeavingCertSubject(["investigative"], ["physical science"]),
                            # formal sciences
                            "Applied Mathematics": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            "Computer Science": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            "Mathematics": LeavingCertSubject(["investigative"], ["computers & mathematics"]),
                            # arts
                            "Art": LeavingCertSubject(["artistic"], ["arts"]),
                            "Drama, Film and Theatre Studies": LeavingCertSubject(["artistic"], ["arts"]),
                            "Music": LeavingCertSubject(["artistic"], ["arts"]),
                            "Design and Communication Graphics": LeavingCertSubject(["artistic", "investigative", "realistic"], ["arts", "engineering"]),
                            # languages
                            "Arabic": LeavingCertSubject(["artistic"], ["humanities"]),
                            "French": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Irish": LeavingCertSubject(["artistic"], ["humanities"]),
                            "German": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Ukrainian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Italian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Japanese": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Latin": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Russian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Spanish": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Mandarin-Chinese": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Polish": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Lithuanian": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Portuguese": LeavingCertSubject(["artistic"], ["humanities"]),
                            # humanities
                            "Ancient Greek": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Classical Studies": LeavingCertSubject(["artistic"], ["humanities"]),
                            "English": LeavingCertSubject(["artistic"], ["humanities", "communications"]),
                            "Hebrew Studies": LeavingCertSubject(["artistic"], ["humanities"]),
                            "History": LeavingCertSubject(["artistic"], ["humanities"]),
                            "Religious Education": LeavingCertSubject(["artistic"], ["humanities"]), 
                            # social sciences
                            "Geography": LeavingCertSubject(["investigative", "social"], ["physical science", "social science"]), 
                            "Politics and Society": LeavingCertSubject(["investigative", "social", "enterprising"], ["law", "social science"]), 
                            "Climate Action and Sustainable Development": LeavingCertSubject(["social"], ["law", "social science"]), 
                            # business
                            "Accounting": LeavingCertSubject(["conventional", "enterprising"], ["business"]), 
                            "Business": LeavingCertSubject(["conventional", "enterprising"], ["business", "law"]),
                            "Economics": LeavingCertSubject(["investigative"], ["business", "social science"]),
                            # misc
                            "Physical Education": LeavingCertSubject(["realistic", "social"], ["healthcare"]),
                            "Home Economics": LeavingCertSubject(["realistic", "social"], ["industrial arts & consumer services"]),
                            }

def get_user_leaving_cert_riasec_vector(user_leaving_cert_subject_preferences):
    user_leaving_cert_riasec_vector = np.zeros(len(RIASEC_INTERESTS))

    for subject in user_leaving_cert_subject_preferences:
        number_of_subject_riasec_interests = len(LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].riasec_interests)
        for riasec_interest in LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].riasec_interests:
            weighted_subject_preference = FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[user_leaving_cert_subject_preferences[subject]]
            # distribute the weight for multi-interest/category subjects
            distributed_weighted_subject_preference = weighted_subject_preference / np.sqrt(number_of_subject_riasec_interests)
            index_to_access = RIASEC_INTERESTS.index(riasec_interest)
            user_leaving_cert_riasec_vector[index_to_access] += distributed_weighted_subject_preference

    return get_normalized_user_leaving_cert_vector(user_leaving_cert_riasec_vector)

def get_user_leaving_cert_college_major_categories_vector(user_leaving_cert_subject_preferences):
    user_leaving_cert_college_major_categories_vector = np.zeros(len(COLLEGE_MAJOR_CATEGORIES))

    for subject in user_leaving_cert_subject_preferences:
        number_of_subject_college_major_categories = len(LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].college_major_categories)
        for college_major_category in LEAVING_CERT_SUBJECTS_RIASEC_AND_CATEGORIES_MAP[subject].college_major_categories:
            weighted_subject_preference = FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP[user_leaving_cert_subject_preferences[subject]]
            # distribute the weight for multi-interest/category subjects
            distributed_weighted_subject_preference = weighted_subject_preference / np.sqrt(number_of_subject_college_major_categories)
            index_to_access = COLLEGE_MAJOR_CATEGORIES.index(college_major_category)
            user_leaving_cert_college_major_categories_vector[index_to_access] += distributed_weighted_subject_preference

    return get_normalized_user_leaving_cert_vector(user_leaving_cert_college_major_categories_vector)

def get_normalized_user_leaving_cert_vector(user_leaving_cert_vector):
    for i in range(len(user_leaving_cert_vector)):
        if user_leaving_cert_vector[i] == 0.0:
            # we don't want to penalise interests/college major categories which have no data:
            # this is under the assumption that a rating of '0' (strongly dislike) has a non-zero weight!
            user_leaving_cert_vector[i] = np.nan 
        else:
            user_leaving_cert_vector[i] = custom_normalized_sigmoid_function(user_leaving_cert_vector[i])

    return user_leaving_cert_vector

FIVE_POINT_LIKERT_SCALE_WEIGHT_MAP = {4: 1.0,
                                      3: 0.5, 
                                      2: 0.25, 
                                      1: 0.05, 
                                      0: 0.01} # let this be non-zero so it penalises the interest/category - otherwise it gets counted as NaN and isn't factored into the Open psychometrics model/data!
NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT = 1.3

def print_stringified_category_vector(category_vector):
    for i in range(len(category_vector)):
        print(COLLEGE_MAJOR_CATEGORIES[i] + ": " + str(round(category_vector[i], 2)))
    print("\n")

# converts real-numbered value to a value from 0.0 to 1.0
def custom_normalized_sigmoid_function(value):
    return 1 - np.exp(-NORMALIZED_SIGMOID_FUNCTION_TUNING_CONSTANT * value)


user_leaving_cert_subject_preferences = { 
                                "Mathematics": 4, 
                                "English": 4, 
                                "Irish": 1, 
                                "Physics": 4, 
                                "Computer Science": 4, 
                                "Design and Communication Graphics": 4, 
                                "German": 2
                                }

# user_leaving_cert_subject_preferences = { 
#                                 "Mathematics": 4, 
#                                 "English": 4, 
#                                 "Irish": 1, 
#                                 "Design and Communication Graphics": 4, 
#                                 "Computer Science": 4, 
#                                 "Physics": 4, 
#                                 "German": 2
#                                 }

# user_leaving_cert_subject_preferences = { 
#                                 "Mathematics": 4, 
#                                 "English": 4, 
#                                 "Irish": 1, 
#                                 "Design and Communication Graphics": 4, 
#                                 "Computer Science": 4, 
#                                 "Physics": 4, 
#                                 "German": 2
#                                 }

print_stringified_category_vector(get_user_leaving_cert_college_major_categories_vector(user_leaving_cert_subject_preferences))

# print(get_user_leaving_cert_riasec_vector(user_leaving_cert_subject_preferences))