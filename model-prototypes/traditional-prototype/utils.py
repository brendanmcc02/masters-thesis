# ignores warnings
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

NUMBER_OF_RIASEC_CATEGORIES = 6
NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY = 8
NUMBER_OF_COLLEGE_MAJOR_CATEGORIES = 15
VECTOR_REPRESENTATION_DIMENSION_SIZE = NUMBER_OF_RIASEC_CATEGORIES + NUMBER_OF_COLLEGE_MAJOR_CATEGORIES + 1 # + 1 for points

POINTS_VECTOR_INDEX = 6
STARTING_CATEGORY_VECTOR_INDEX = POINTS_VECTOR_INDEX + 1

MAX_RIASEC_QUESTION_VALUE = 4.0 # assuming 0-4, not 1-5!
RIASEC_CATEGORIES = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
COLLEGE_MAJOR_CATEGORIES = ['agriculture & natural resources', 'arts', 'biology & life science', 'business', 'communications & journalism', 'computers & mathematics', 'education', 'engineering', 'health', 'humanities & liberal arts', 'industrial arts & consumer services', 'law & public policy', 'physical sciences', 'psychology & social work', 'social science']

LC_SUBJECTS_TO_RIASEC_MAP = {
                            # practical
                            "Construction Studies": ["Realistic"], 
                            "Engineering": ["Realistic", "Investigative"], 
                            "Technology": ["Realistic", "Investigative"], 
                            # sciences
                            "Agricultural Science": ["Investigative"], 
                            "Applied Maths": ["Investigative"], 
                            "Biology": ["Investigative"], 
                            "Chemistry": ["Investigative"], 
                            "Mathematics": ["Investigative"], 
                            "Physics": ["Investigative"], 
                            "Physics and Chemistry": ["Investigative"], 
                            "Computer Science": ["Investigative"], 
                            # arts
                            "Art": ["Artistic"], 
                            "Drama, Film and Theatre Studies": ["Artistic"], 
                            "Music": ["Artistic"], 
                            "Design and Communication Graphics": ["Investigative", "Artistic"], 
                            # humanities
                            "Arabic": ["Artistic"], 
                            "Classical Studies": ["Artistic"], 
                            "English": ["Artistic"], 
                            "French": ["Artistic"], 
                            "Irish": ["Artistic"], 
                            "German": ["Artistic"], 
                            "Hebrew Studies": ["Artistic"], 
                            "History": ["Artistic"], 
                            "Ukrainian": ["Artistic"], 
                            "Italian": ["Artistic"], 
                            "Japanese": ["Artistic"], 
                            "Latin": ["Artistic"], 
                            "Russian": ["Artistic"], 
                            "Spanish": ["Artistic"], 
                            "Ancient Greek": ["Artistic"], 
                            "Mandarin-Chinese": ["Artistic"], 
                            "Polish": ["Artistic"], 
                            "Lithuanian": ["Artistic"], 
                            "Portuguese": ["Artistic"],
                            # social sciences
                            "Geography": ["Investigative", "Social"], 
                            "Religious Education": ["Investigative", "Social"], 
                            "Physical Education": ["Realistic", "Social"], 
                            "Politics and Society": ["Investigative", "Social", "Enterprising"], 
                            "Climate Action and Sustainable Development": ["Social"], 
                            "Home Economics": ["Realistic", "Social", "Conventional"],
                            # business
                            "Accounting": ["Conventional"], 
                            "Business": ["Enterprising", "Conventional"], 
                            "Economics": ["Investigative", "Enterprising"]
                            }

def get_min_points(cao_courses):
    min_points = 625

    for course in cao_courses:
        if course['points']:
            min_points = min(min_points, course['points'])

    return min_points

def get_max_points(cao_courses):
    max_points = 0

    for course in cao_courses:
        if course['points']:
            max_points = max(max_points, course['points'])

    return max_points

def add_vectorized_course_as_attribute(course, min_points, max_points):
    course['vector_representation'] = get_vectorized_representation(course, min_points, max_points)

def get_vectorized_representation(course, min_points, max_points):
    vectorized_representation = np.zeros(VECTOR_REPRESENTATION_DIMENSION_SIZE)

    for interest in course['interests']:
        vectorized_representation[RIASEC_CATEGORIES.index(interest)] = 1.0

    vectorized_representation[POINTS_VECTOR_INDEX] = get_normalized_points_vector(course['points'], min_points, max_points)

    one_hot_encode(course, vectorized_representation)

    return vectorized_representation

def get_normalized_points_vector(points, min_points, max_points):
    if not points:
        points = 0.0
    
    return np.array([(points - min_points) / (max_points - min_points)])

def one_hot_encode(course, vectorized_representation):
    for category in course['categories']:
        vectorized_representation[STARTING_CATEGORY_VECTOR_INDEX + COLLEGE_MAJOR_CATEGORIES.index(category)] = 1.0

def get_weighted_categories_model(X_train, y_train, isFirstTimeRunning):
    saved_model_filename = "logistic_regression_model.joblib"
    if isFirstTimeRunning:
        model = LogisticRegression(
            multi_class='multinomial',
            solver='saga', # negligible performance differences, saga is the quickest
            C=1.0, # different values have negligible impact
            max_iter=1000,
            random_state=42
        )

        model.fit(X_train, y_train)
        joblib.dump(model, saved_model_filename)
    else:
        model = joblib.load(saved_model_filename)

    return model

def get_weighted_categories_vector(user_riasec_vector, model):
    user_riasec_vector = np.array(user_riasec_vector).reshape(1, -1) # 1d -> 2d array
    model_class_probabilities = model.predict_proba(user_riasec_vector)
    normalized_model_class_probabilities = get_normalized_vector(model_class_probabilities[0]) # interested in only the first element

    return normalized_model_class_probabilities

# TODO maybe some problems with normalizing,
# what if they are all really high, they get set to 0,
# can we somehow just expand it to 1.0 but not set to 0 or something?
def get_normalized_vector(vector):
    maxValue = 0.0
    minValue = 1.0

    for val in vector:
        maxValue = max(maxValue, val)
        minValue = min(minValue, val)

    for i in range(len(vector)):
        vector[i] = (vector[i] - minValue) / (maxValue - minValue)

    return vector

def get_simplified_user_riasec_vector(user_riasec_vector, lc_subjects_preferences):
    riasec_category_vectors= []
    # reduce 48 -> 6 dimensions
    for i in range(0, len(user_riasec_vector), NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY):
        riasec_category_vectors.append(user_riasec_vector[i:i+NUMBER_OF_QUESTIONS_PER_RIASEC_CATEGORY])

    simplified_user_riasec_vector = factor_lc_subjects_into_riasec(riasec_category_vectors, lc_subjects_preferences)

    return np.array(simplified_user_riasec_vector, dtype='float32')

def factor_lc_subjects_into_riasec(riasec_category_vectors, lc_subjects_preferences):
    for subject in lc_subjects_preferences:
        subject_interests = LC_SUBJECTS_TO_RIASEC_MAP[subject]

        for interest in subject_interests:
            riasec_category_vectors[RIASEC_CATEGORIES.index(interest)].append(lc_subjects_preferences[subject])

    simplified_user_riasec_vector = np.zeros(len(RIASEC_CATEGORIES))

    for i in range(len(riasec_category_vectors)):
        simplified_user_riasec_vector[i] = np.mean(riasec_category_vectors[i])

    return simplified_user_riasec_vector

def get_top_k_results(cao_courses, user_vector, k):
    cached_user_vector_magnitude = np.linalg.norm(user_vector)
    for course in cao_courses:
        course["similarity"] = get_cosine_similarity(user_vector, cached_user_vector_magnitude, course["vector_representation"])

    results = sorted(
        cao_courses,
        key=lambda x: x["similarity"],
        reverse=True
    )
    top_k_results = results[0:k]

    return top_k_results

def get_cosine_similarity(user_vector, cached_user_vector_magnitude, course_vector):
    return np.dot(user_vector, course_vector) / (cached_user_vector_magnitude * np.linalg.norm(course_vector))

