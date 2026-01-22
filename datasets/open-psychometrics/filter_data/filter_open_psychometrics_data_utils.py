from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re

def get_stop_words():
    stop_words = set(stopwords.words('english'))

    # domain-specific stop words
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
    stop_words.add("studying")
    stop_words.add("concentration")
    stop_words.add("honor")
    stop_words.add("honour")
    stop_words.add("honors")
    stop_words.add("honours")
    stop_words.add("degree")
    stop_words.add("advanced")
    stop_words.add("emphasis")
    stop_words.add("applied")
    stop_words.add("theory")
    stop_words.add("theoretical")
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
    stop_words.add("higher")
    stop_words.add("e") # e for electronic e.g. e-commerce
    stop_words.add("professional")
    stop_words.add("modern")
    stop_words.add("nil")
    stop_words.add("na")
    stop_words.add("attended")
    stop_words.add("creative")
    
    # for cao-college-courses title preprocessing
    stop_words.add("common")
    stop_words.add("entry")
    stop_words.add("combination")
    stop_words.add("two")
    stop_words.add("includes")
    stop_words.add("preference")
    stop_words.add("full")
    stop_words.add("time")
    stop_words.add("concurrent")
    stop_words.add("undenominated")
    stop_words.add("integrated")
    stop_words.add("explore")
    stop_words.add("streams")
    stop_words.add("award")
    stop_words.add("options")
    stop_words.add("placement")
    stop_words.add("portfolio")
    stop_words.add("yrs")
    stop_words.add("pathway")
    stop_words.add("pathfinder")
    stop_words.add("restricted")
    stop_words.add("maitrise")

    return stop_words

stop_words = get_stop_words()
stemmer = SnowballStemmer("english")  # better results than porter stemmer

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[\.\?=!£#\'`¬\*]', '', text) # remove certain symbols
    text = re.sub(r'\d+', '', text) # remove numbers

    for abbreviation, expanded_college_major in COLLEGE_MAJOR_ABBREVIATIONS_ACRONYMS_AND_SUBSTITUTIONS_MAP.items():
        pattern = r'\b' + re.escape(abbreviation) + r'\b'
        text = re.sub(pattern, expanded_college_major, text)

    text = re.sub(r'[\(\)\{\}\[\]&/+,;:\\|\-]', ' ', text) # sub certain symbols for spaces

    text = text.strip()

    # don't put this in `COLLEGE_MAJOR_ABBREVIATIONS_ACRONYMS_AND_SUBSTITUTIONS_MAP`, because that would expand out tokens.
    # FYI: "science" is a stop word!
    if text == "science":
        text = "physical science"

    tokens = word_tokenize(text)
    cleaned_tokens = []
    for word in tokens:
        if word not in stop_words:
            stemmed_word = stemmer.stem(word)

            if stemmed_word not in cleaned_tokens:
                cleaned_tokens.append(stemmed_word)

    return ' '.join(cleaned_tokens)


COLLEGE_MAJOR_ABBREVIATIONS_ACRONYMS_AND_SUBSTITUTIONS_MAP = {
    'maths': 'mathematics',
    'teacher': 'teaching',
    'teaching': 'education',
    'pharmaceutical': 'pharmacy',
    'technician': 'technology',
    'admin': 'administration',
    'bio': 'biological',
    'phy': 'physics',
    'chem': 'chemistry',
    'chemistry': 'chemical',
    'dentist': 'dentistry',
    'dental': 'dentistry',
    'agri': 'agriculture',
    'ag': 'agriculture',
    'hrm': 'human resource management',
    'it': 'information technology',
    'tech': 'technology',
    'llb': 'law',
    'bcl': 'civil law'
}


FUZZY_MATCH_THRESHOLD = 85  # obtained mostly from vibes and trial/error, negligible performance increase comparing 80/85/90
def get_fuzzy_college_major_category_match(text, preprocessed_college_majors_and_major_categories, preprocessed_major_to_major_category_dict):
    max_score = 0
    maxText = ""

    for college_major_or_major_category in preprocessed_college_majors_and_major_categories:
        score = fuzz.ratio(text, college_major_or_major_category)

        if score >= FUZZY_MATCH_THRESHOLD and score > max_score:
            max_score = score
            if college_major_or_major_category in preprocessed_major_to_major_category_dict:
                maxText = preprocessed_major_to_major_category_dict[college_major_or_major_category]
            else:
                maxText = college_major_or_major_category

    return maxText


def reverse_college_major_category_preprocessing(df, unique_college_major_categories):
    reverse_preprocessed_college_major_category_dict = {}
    for unique_college_major_category in unique_college_major_categories:
        reverse_preprocessed_college_major_category_dict[preprocess_text(unique_college_major_category)] = unique_college_major_category

    df['college_major_category'] = df['college_major_category'].map(reverse_preprocessed_college_major_category_dict).fillna(df['college_major_category'])

    df = df.sort_values(by=['college_major_category'])

    return df

RIASEC_TYPES = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
def get_aggregated_college_major_categories_df(df, holland_code_columns, HOLLAND_CODE_PREFIXES):
    aggregated_major_categories_df = df.groupby('college_major_category')[holland_code_columns].mean().reset_index()

    MAX_QUESTION_VALUE = 4
    for prefix in HOLLAND_CODE_PREFIXES:
        score_cols = [col for col in aggregated_major_categories_df.columns if col.startswith(prefix) and col[1:].isdigit()]
        
        if score_cols:
            aggregated_major_categories_df[prefix] = round((aggregated_major_categories_df[score_cols].mean(axis=1) / MAX_QUESTION_VALUE), 4) # normalize

    aggregated_major_categories_df = aggregated_major_categories_df[['college_major_category']+HOLLAND_CODE_PREFIXES]
    aggregated_major_categories_df = aggregated_major_categories_df.rename(columns={'R':RIASEC_TYPES[0], 'I':RIASEC_TYPES[1], 'A':RIASEC_TYPES[2], 'S':RIASEC_TYPES[3], 'E':RIASEC_TYPES[4], 'C':RIASEC_TYPES[5]}) 

    return aggregated_major_categories_df
