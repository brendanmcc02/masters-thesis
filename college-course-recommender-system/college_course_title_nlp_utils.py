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
    stop_words.add("theory")
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
    stop_words.add("online")
    stop_words.add("systems")
    stop_words.add("system")
    stop_words.add("pathway")
    stop_words.add("pure")
    stop_words.add("practice")
    stop_words.add("plus")
    stop_words.add("sc")

    return stop_words

stop_words = get_stop_words()
stemmer = SnowballStemmer("english")  # better results than porter stemmer

def preprocess_college_title(text):
    text = text.lower()
    text = re.sub(r'[\.\?=!£#\'`¬\*]', '', text) # remove certain symbols
    text = re.sub(r'\d+', '', text) # remove numbers

    for abbreviation, expanded_college_major in COLLEGE_MAJOR_ABBREVIATIONS_ACRONYMS_AND_SUBSTITUTIONS_MAP.items():
        pattern = r'\b' + re.escape(abbreviation) + r'\b'
        text = re.sub(pattern, expanded_college_major, text)

    text = re.sub(r'[\(\)\{\}\[\]&/+,;:\\|\-]', ' ', text) # sub certain symbols for spaces

    text = text.strip()

    tokens = word_tokenize(text)
    cleaned_tokens = []
    for word in tokens:
        if word not in stop_words:
            stemmed_word = stemmer.stem(word)

            if stemmed_word not in cleaned_tokens:
                cleaned_tokens.append(stemmed_word)

            if len(cleaned_tokens) > 1 and "scienc" in cleaned_tokens:
                cleaned_tokens.remove("scienc")

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
    'ict': 'information and communication technology',
    'tech': 'technology',
    'llb': 'law',
    'bcl': 'civil law',
    'mgt': 'management'
}
