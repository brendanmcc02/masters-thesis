from college_course_recommender_system_utils import *

user_vector = [0.68177608, 0.96330079, 0,         0.99251609, 0,         0,
 0.8,         0,         0,         0,         0,         0,
 0,         0,         0,         0,         0,         0.988891,
 0,         0,         0,         0,         0,         0,
 0,         0,         0,         0]

user_vector_magnitude = np.linalg.norm(user_vector)

course_vector = [0.57735027, 0.57735027, 0,         0.57735027, 0,         0,
 0.75,     0,         0,         0,         0,         0,
 0,         0,         0,         0,         0,         0.70710678,
 0,         0,         0,         0,         0.70710678, 0,
 0,         0,         0,         0]

def get_cosine_similarity(user_vector, cached_user_vector_magnitude, course_vector):
    dot_product = np.dot(user_vector, course_vector)
    product_of_magnitudes = cached_user_vector_magnitude * np.linalg.norm(course_vector)

    return dot_product / product_of_magnitudes

print(str(get_cosine_similarity(user_vector, user_vector_magnitude, course_vector)))

# 1.0 user - 0.90 course
# 0.8923947197804365

# 1.0 user - 1.0 points
# 0.8913368765723351

# 0.9 user - 0.9 course
# 0.886213602808258

# 0.9 user - 0.8 course
# 0.8871628989838112

