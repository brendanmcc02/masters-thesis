import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

area_ethnicities = ["american studies", "asian studies", "african studies", "african american studies", "european studies", "latin american studies"]

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
    stop_words.add("honors")
    stop_words.add("honours")
    stop_words.add("degree")
    stop_words.add("advanced")
    stop_words.add("emphasis")
    stop_words.add("applied")
    stop_words.add("associate")
    stop_words.add("associates")
    stop_words.add("university")
    stop_words.add("department")
    stop_words.add("year")
    stop_words.add("years")
    stop_words.add("pre")
    stop_words.add("academic")
    stop_words.add("academics")
    stop_words.add("general")
    stop_words.add("north")
    stop_words.add("south")
    stop_words.add("east")
    stop_words.add("west")
    stop_words.add("western")
    stop_words.add("southeast")
    stop_words.add("american")
    stop_words.add("asian")
    stop_words.add("african")
    stop_words.add("european")
    stop_words.add("focus")

    return stop_words

stop_words = get_stop_words()
stemmer = SnowballStemmer("english")  # better results than porter stemmer # e.g. 

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[\.\?=!£#`¬]', '', text) # remove numbers and symbols
    text = re.sub(r'\d+', '', text) # remove numbers

    text = substitute_edge_cases(text)

    for abbreviation, expaned_college_major in common_college_major_abbreviations_and_acronyms_map.items():
        pattern = r'\b' + re.escape(abbreviation) + r'\b'
        text = re.sub(pattern, expaned_college_major, text)

    text = re.sub(r'[\(\)\{\}\[\]&/+,;:\\|\-]', ' ', text)

    tokens = word_tokenize(text)
    cleaned_tokens = []
    for word in tokens:
        if word not in stop_words:
            stemmed_word = stemmer.stem(word)
            cleaned_tokens.append(stemmed_word)

    return ' '.join(cleaned_tokens)


def substitute_edge_cases(text):
    if text == "general" or text == "general studies":
        return "multidisciplinary"
    
    if text == "civil" or text == "aerospace":
        return text + " engineering"
    
    for area_ethnicity in area_ethnicities:
        if text == area_ethnicity:
            return "area ethnic studies"

    return text

common_college_major_abbreviations_and_acronyms_map = {
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
    'mathematic': 'mathematics',
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
    'psych': 'psychology',
    'tech': 'technology',
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
    'hrm': 'human resource development',
    'pr': 'public relations',
    'premed': 'medical preparatory programs',
    '3rd': 'third',
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
}


# # the values in this dict need to be in college_majors
# college_major_mapping_dict = {
#     # arts
    
#     'drama': 'drama and theater arts',
#     'drama arts': 'drama and theater arts',
#     'theater arts': 'drama and theater arts',
#     'theater': 'drama and theater arts',
#     'visual arts': 'visual and performing arts',
#     'performing arts': 'visual and performing arts',
#     'graphic design': 'commercial art and graphic design',
#     'commercial art': 'commercial art and graphic design',
#     'photographic arts': 'film video and photographic arts',
#     'film': 'film video and photographic arts',
#     'film school': 'film video and photographic arts',
#     'cinema': 'film video and photographic arts',
#     'musical studies': 'music',
#     'design': 'commercial art and graphic design',
    
#     # humanities
#     'liberal studies': 'liberal arts',
#     'literature': 'english language and literature',
#     'english': 'english language and literature',
#     'english literature': 'english language and literature',
#     'philosophy': 'philosophy and religious studies',
#     'ethics': 'philosophy and religious studies',
#     'religious studies': 'philosophy and religious studies',
#     'religion': 'philosophy and religious studies',
#     'bible': 'philosophy and religious studies',
#     'arts history': 'art history and criticism', # art -> arts ; abbreviation expansion
#     'arts criticism': 'art history and criticism', # art -> arts ; abbreviation expansion
#     'anthropology':'anthropology and archeology',
#     'archeology':'anthropology and archeology',
#     'foreign langauge': 'foreign languages',
#     'translation': 'foreign languages',
#     'french': 'foreign languages',
#     'german': 'foreign languages',
#     'chinese': 'foreign languages',
#     'japanese': 'foreign languages',
#     'korean': 'foreign languages',
#     'italian': 'foreign languages',
#     'spanish': 'foreign languages',
#     'russian': 'foreign languages',
#     'languages': 'foreign languages',
#     'philology': 'linguistics and comparative language and literature',
#     'linguistics': 'linguistics and comparative language and literature',
#     'classics': 'humanities & liberal arts',
#     'civilization': 'area ethnic and civilization studies',
#     'international studies': 'intercultural and international studies',
#     'intercultural studies': 'intercultural and international studies',
#     'theology': 'theology and religious vocations',

#     # biology
#     'plant science': 'plant science and agronomy',
#     'agronomy': 'plant science and agronomy',
#     'biochemical': 'biochemical sciences',
#     'biochemistry': 'biochemical sciences',
#     'cognitive science': 'cognitive science and biopsychology',
#     'biopsychology': 'cognitive science and biopsychology',
#     'kinesiology': 'physiology',
#     'physical therapy': 'physiology',
#     'physio': 'physiology',
#     'physiotherapy': 'physiology',
#     'environmental': 'environmental science',
#     'biological': 'biology', # bio -> biological; abbreviation expansion
#     'neuro': 'neuroscience',
#     'neuropsychology': 'neuroscience',
#     'neurobiology': 'neuroscience',
#     'neurology': 'physiology',
#     'genetic': 'genetics',
#     'ecological science': 'ecology',
    
#     # health
#     'public health': 'community and public health',
#     'community health': 'community and public health',
#     'medicine': 'general medical and health services',
#     'medical': 'general medical and health services',
#     'doctor': 'general medical and health services',
#     'dentist': 'general medical and health services',
#     'dental science': 'general medical and health services',
#     'dental': 'general medical and health services',
#     'dental hygiene': 'general medical and health services',
#     'dental assistant': 'general medical and health services',
#     'dental assisting': 'general medical and health services',
#     'dentistry': 'general medical and health services',
#     'health services': 'general medical and health services',
#     'healthcare': 'general medical and health services',
#     'pharmacist': 'pharmacology',
#     'pharmacy': 'pharmacology',
#     'pharmaceutic': 'pharmacology',
#     'pharmaceutical': 'pharmacology',
#     'pharmacy technology': 'pharmacology',
#     'pharmaceuticals': 'pharmacology',
#     'pharmaceutical science': 'pharmacology',
#     'health science': 'biology',
#     'life science': 'biology',
#     'nutrition': 'nutrition sciences',
#     'midwife': 'nursing',
#     'midwifery': 'nursing',

#     # business
#     'actuary': 'actuarial science',
#     'actuarial': 'actuarial science',
#     'actuarial studies': 'actuarial science',
#     'operations logistics': 'operations logistics and e-commerce',
#     'operations management': 'operations logistics and e-commerce',
#     'e-commerce': 'operations logistics and e-commerce',
#     'business marketing': 'marketing and marketing research',
#     'marketing': 'marketing and marketing research',
#     'marketing management': 'marketing and marketing research',
#     'human resource': 'human resources and personnel management',
#     'human resources': 'human resources and personnel management', # could probably get rid of this with fuzzywuzzy
#     'human resource management': 'human resources and personnel management',
#     'human resources management': 'human resources and personnel management', # could probably get rid of this with fuzzywuzzy
#     'human resource development': 'human resources and personnel management',
#     'human resources development': 'human resources and personnel management', # could probably get rid of this with fuzzywuzzy
#     'personnel management': 'human resources and personnel management',
#     'commerce': 'general business',
#     'business management': 'business management and administration',
#     'administration': 'business management and administration',
#     'business administration': 'business management and administration',
#     'administrative science': 'business management and administration',
#     'mba': 'business management and administration',
#     'management': 'business management and administration',
#     'economy': 'economics',
#     'hotel management': 'hospitality management',
#     'international commerce': 'international business',
#     'international trade': 'international business',
#     'management information systems': 'management information systems and statistics',
#     'medical administration' : 'miscellaneous business & medical administration',
    
#     # communications
#     'mass communications': 'mass media',
#     'media communications': 'mass media',
#     'communication studies': 'communications',
#     'communications studies': 'communications', # could probably get rid of this with fuzzywuzzy
#     'advertising': 'advertising and public relations',
#     'public relations': 'advertising and public relations',
#     'media': 'mass media',
#     'media studies': 'mass media',

#     # computers & math
#     'computer science and mathematics': 'mathematics and computer science',
#     'computer': 'computer and information systems',
#     'computing': 'computer and information systems',
#     'computers': 'computer and information systems', # could probably get rid of this with fuzzywuzzy
#     'computer information system': 'computer and information systems', # could probably get rid of this with fuzzywuzzy
#     'computer information systems': 'computer and information systems',
#     'computer systems': 'computer and information systems',
#     'computer information technology': 'computer and information systems',
#     'information technology': 'computer and information systems',
#     'information systems': 'computer and information systems',
#     'computer technology': 'computer and information systems',
#     'statistics': 'statistics and decision science',
#     'computer programming': 'computer programming and data processing',
#     'programming': 'computer programming and data processing',
#     'data processing': 'computer programming and data processing',
#     'computer networks': 'computer networking and telecommunications', # networking -> networks ; abbreviation expansion
#     'networks': 'computer networking and telecommunications', # networking -> networks ; abbreviation expansion
#     'cybersecurity': 'computer networking and telecommunications',
#     'telecommunications': 'computer networking and telecommunications',
#     'computer studies': 'computer and information systems',
#     'software engineering': 'computer science',

#     # education
#     # note "teacher" & "teaching" -> "education"
#     'educational studies': 'education',
#     'educational administration': 'educational administration and supervision',
#     'primary education': 'elementary education',
#     'secondary education': 'secondary teacher education',
#     'higher education': 'secondary teacher education',
#     'special education': 'special needs education',
#     'mathematics education': 'mathematics teacher education',
#     'arts education': 'art and music education', # art -> arts
#     'music education': 'art and music education',
#     'science education': 'science and computer teacher education',
#     'school counseling': 'school student counseling',

#     # engineering
#     'biomedical science': 'biomedical engineering',
#     'biotech': 'biological engineering',
#     'biotech engineering': 'biological engineering',
#     'biotechnology': 'biological engineering',
#     'electronics': 'electrical engineering',
#     'architectural studies': 'architecture',
#     'architect': 'architecture',
#     'industrial engineering': 'industrial and manufacturing engineering',
#     'manufacturing engineering': 'industrial and manufacturing engineering',

#     # agriculture
#     'agriculture': 'general agriculture',
#     'agriculture production': 'agriculture production and management',
#     'agriculture management': 'agriculture production and management',
#     'food': 'food science',

#     # physical science
#     'science': 'multi-disciplinary or general science',
#     'geology': 'geology and earth science',
#     'earth science': 'geology and earth science',
#     'geological science': 'geology and earth science',
#     'astronomy': 'astronomy and astrophysics',
#     'astrophysics': 'astronomy and astrophysics',

#     # law
#     'law': 'law & public policy',
#     'international law': 'law & public policy',
#     'lawyer': 'law & public policy',
#     'legal': 'law & public policy',
#     'legal studies': 'law & public policy',
#     'paralegal': 'law & public policy',
#     'paralegal studies': 'law & public policy',
#     'criminal justice': 'criminal justice and fire protection',

#     # psych
#     'counseling': 'counseling psychology',
#     'counselling': 'counseling psychology',
#     'therapy': 'counseling psychology',

#     # social science
#     'political science': 'political science and government',
#     'politics': 'political science and government',
#     'government': 'political science and government',
#     'sociological': 'sociology',
#     'international affairs': 'international relations',
#     'international development': 'international relations',
#     'international politics': 'international relations',

#     # industrial arts
#     'family science':'family and consumer sciences',
#     'consumer science':'family and consumer sciences',
#     'culinary': 'cosmetology services and culinary arts',
#     'culinary arts': 'cosmetology services and culinary arts',
#     'culinary science': 'cosmetology services and culinary arts',
#     'hospitality': 'hospitality management',
# }
