import numpy as np

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

    vectorized_representation[POINTS_VECTOR_INDEX] = get_normalized_points(course['points'], min_points, max_points)

    one_hot_encode(course, vectorized_representation)

    return vectorized_representation

def get_normalized_points(points, min_points, max_points):
    if not points:
        points = 0.0
    
    return (points - min_points) / (max_points - min_points)

def one_hot_encode(course, vectorized_representation):
    for category in course['categories']:
        vectorized_representation[STARTING_CATEGORY_VECTOR_INDEX + COLLEGE_MAJOR_CATEGORIES.index(category)] = 1.0

# TODO
# ML/vector model
def get_weighted_categories_vector(user_riasec_vector):
    return np.zeros(len(COLLEGE_MAJOR_CATEGORIES))

def get_normalized_vectorized_riasec(user_riasec):
    for i in range(len(user_riasec)):
        user_riasec[i] /= MAX_RIASEC_QUESTION_VALUE

    return user_riasec

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

