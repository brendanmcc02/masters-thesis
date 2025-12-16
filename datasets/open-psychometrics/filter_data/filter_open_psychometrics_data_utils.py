from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import re

def get_stop_words():
    stop_words = set(stopwords.words('english'))
    stop_words.add("undergrad")
    stop_words.add("undergraduate")
    stop_words.add("postgrad")
    stop_words.add("postgraduate")
    stop_words.add("bachelor")
    stop_words.add("bachelors")
    stop_words.add("master")
    stop_words.add("masters")
    stop_words.add("phd")
    stop_words.add("doctorate")
    stop_words.add("diploma")
    stop_words.add("certified")
    stop_words.add("certificate")
    stop_words.add("major")
    stop_words.add("minor")
    stop_words.add("joint")
    stop_words.add("double")
    stop_words.add("dual")
    stop_words.add("studies")
    stop_words.add("concentration")
    stop_words.add("honor")
    stop_words.add("honour")
    stop_words.add("honors")
    stop_words.add("honours")
    stop_words.add("degree")
    stop_words.add("advanced")
    stop_words.add("emphasis")
    stop_words.add("applied")
    stop_words.add("associate")
    stop_words.add("associates")
    stop_words.add("university")
    stop_words.add("college")
    stop_words.add("school")
    stop_words.add("department")
    stop_words.add("year")
    stop_words.add("years")
    stop_words.add("pre")
    stop_words.add("academic")
    stop_words.add("academics")
    stop_words.add("general")
    stop_words.add("focus")
    stop_words.add("misc")
    stop_words.add("miscellaneous")
    stop_words.add("multidisciplinary")
    stop_words.add("interdisciplinary")
    stop_words.add("multiple")
    stop_words.add("st") # 1st -> numbers are removed before stop words
    stop_words.add("nd") # 2nd -> numbers are removed before stop words
    stop_words.add("rd") # 3rd -> numbers are removed before stop words
    stop_words.add("yes")
    stop_words.add("no")
    stop_words.add("nah")
    stop_words.add("none")
    stop_words.add("know")
    stop_words.add("idk")
    stop_words.add("other")
    stop_words.add("dont")
    stop_words.add("known")
    stop_words.add("unknown")
    stop_words.add("nothing")
    stop_words.add("choice")
    stop_words.add("yet")
    stop_words.add("sure")
    stop_words.add("undeclared")
    stop_words.add("undecided")
    stop_words.add("maybe")
    stop_words.add("attend")
    stop_words.add("not")
    stop_words.add("applicable")
    stop_words.add("north")
    stop_words.add("south")
    stop_words.add("east")
    stop_words.add("west")
    stop_words.add("science")
    stop_words.add("sciences")
    stop_words.add("foreign")
    stop_words.add("mass")
    stop_words.add("subject")
    stop_words.add("currently")
    stop_words.add("attending")
    stop_words.add("field")
    stop_words.add("early")
    stop_words.add("middle")
    stop_words.add("e") # e for electronic e.g. e-commerce

    return stop_words

stop_words = get_stop_words()
stemmer = SnowballStemmer("english")  # better results than porter stemmer

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[\.\?=!£#`¬\*]', '', text) # remove numbers and symbols
    text = re.sub(r'\d+', '', text) # remove numbers

    for abbreviation, expanded_college_major in college_major_abbreviations_acronyms_and_substitutions_map.items():
        pattern = r'\b' + re.escape(abbreviation) + r'\b'
        text = re.sub(pattern, expanded_college_major, text)

    text = re.sub(r'[\(\)\{\}\[\]&/+,;:\\|\-]', ' ', text)

    tokens = word_tokenize(text)
    cleaned_tokens = []
    for word in tokens:
        if word not in stop_words:
            stemmed_word = stemmer.stem(word)
            cleaned_tokens.append(stemmed_word)

    return ' '.join(cleaned_tokens)


college_major_abbreviations_acronyms_and_substitutions_map = {
    'cpa': 'accounting',
    'ba': 'arts',
    'ma': 'arts',
    'aa': 'arts',
    'bfa': 'fine arts',
    'mfa': 'fine arts',
    'bs': 'science',
    'ms': 'science',
    'bsc': 'science',
    'msc': 'science',
    'as': 'science',
    'sci': 'science',
    'mlis': 'library science',
    'aas': 'applied science',
    'math': 'mathematics',
    'maths': 'mathematics',
    'cs': 'computer science',
    'bba': 'business',
    'mba': 'business',
    'bcom': 'business',
    'mcom': 'business',
    'bcomm': 'business',
    'bed': 'education',
    'beng': 'engineering',
    'ee': 'electrical engineering',
    'eee': 'electrical engineering',
    'llb': 'law',
    'jd': 'law',
    'bsw': 'social work',
    'mpa': 'public administration',
    'mph': 'public health',
    'md': 'medicine',
    'dnp': 'nursing',
    'aud': 'audiology',
    'msw': 'social work',
    'comp': 'computer',
    'econ': 'economics',
    'lit': 'literature',
    'poli': 'political',
    'pol': 'political',
    'polsci': 'political science',
    'pharmaceutical': 'pharmacy',
    'psych': 'psychology',
    'tech': 'technology',
    'technician': 'technology',
    'info': 'information',
    'it': 'information technology',
    'eng': 'engineering',
    'admin': 'administration',
    'ag': 'agriculture',
    'agri': 'agriculture',
    'bio': 'biological',
    'biochem': 'biochemical',
    'arch': 'architecture',
    'biomed': 'biomedical',
    'chem': 'chemical',
    'mech': 'mechanical',
    'env': 'environmental',
    'aero': 'aerospace',
    'ed': 'education',
    'telecomms': 'telecommunications',
    'telecomm': 'telecommunications',
    'hr': 'human resources',
    'hrm': 'human resource management',
    'hrd': 'human resource development',
    'pr': 'public relations',
    'gen': 'general',
    'french': 'foreign language',
    'german': 'foreign language',
    'italian': 'foreign language',
    'spanish': 'foreign language',
    'korean': 'foreign language',
    'chinese': 'foreign language',
    'japanese': 'foreign language',
    'russian': 'foreign language',
    'portuguese': 'foreign language',
    'latin': 'foreign language',
    'premed': 'medicine',
    'med': 'medicine',
    'medical': 'medicine',
    'doctor': 'medicine',
    'dentist': 'dentistry',
    'dental': 'dentistry',
    'vet': 'veterinarian',
    'veterinary medicine': 'veterinarian',
    'veterinary': 'veterinarian',
    'liberal studies': 'liberal arts',
    'speech language pathology': 'speech pathology',
    'speech therapy': 'speech pathology',
    'dietetics': 'nutrition sciences'
}


FUZZY_MATCH_THRESHOLD = 85  # obtained mostly from vibes and trial/error, negligible performance increase comparing 80/85/90
def fuzzy_match(text, college_majors_and_categories, major_to_major_category_dict):
    maxScore = 0
    maxText = ""

    for collegeMajorOrCategory in college_majors_and_categories:
        score = fuzz.ratio(text, collegeMajorOrCategory)

        if score >= FUZZY_MATCH_THRESHOLD and score > maxScore:
            maxScore = score
            if collegeMajorOrCategory in major_to_major_category_dict:
                maxText = major_to_major_category_dict[collegeMajorOrCategory]
            else:
                maxText = collegeMajorOrCategory

    return maxText


def reverse_college_major_category_preprocessing(df, unique_college_major_categories):
    reverse_preprocessed_college_major_category_dict = {}
    for unique_college_major_category in unique_college_major_categories:
        reverse_preprocessed_college_major_category_dict[preprocess_text(unique_college_major_category)] = unique_college_major_category

    df['major_category'] = df['major_category'].map(reverse_preprocessed_college_major_category_dict).fillna(df['major_category'])

    df = df.sort_values(by=['major_category'])

    return df

RIASEC_TYPES = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
def get_aggregated_college_major_categories_df(df, holland_code_columns, HOLLAND_CODE_PREFIXES):
    aggregated_major_categories_df = df.groupby('major_category')[holland_code_columns].mean().reset_index()

    MAX_QUESTION_VALUE = 4
    for prefix in HOLLAND_CODE_PREFIXES:
        score_cols = [col for col in aggregated_major_categories_df.columns if col.startswith(prefix) and col[1:].isdigit()]
        
        if score_cols:
            aggregated_major_categories_df[prefix] = round((aggregated_major_categories_df[score_cols].mean(axis=1) / MAX_QUESTION_VALUE), 4) # normalize

    aggregated_major_categories_df = aggregated_major_categories_df[['major_category']+HOLLAND_CODE_PREFIXES]
    aggregated_major_categories_df = aggregated_major_categories_df.rename(columns={'R':RIASEC_TYPES[0], 'I':RIASEC_TYPES[1], 'A':RIASEC_TYPES[2], 'S':RIASEC_TYPES[3], 'E':RIASEC_TYPES[4], 'C':RIASEC_TYPES[5]}) 

    return aggregated_major_categories_df

# # commenting out because this surprisingly reduces HGBM model performance by ~0.02
# def get_most_frequently_occuring_college_major_category_with_substring_match(column_value, college_majors, major_to_major_category_dict):
#     college_major_categories_counts = defaultdict(int)
#     for major in college_majors:
#         category = major_to_major_category_dict[major]

#         if major in column_value:
#             college_major_categories_counts[category] += 1

#     if len(college_major_categories_counts) > 0:
#         sorted_college_major_categories = sorted(college_major_categories_counts, key=college_major_categories_counts.get, reverse=True)
#         return sorted_college_major_categories[0] # just return the most frequently occuring college major category
    
#     return ""
