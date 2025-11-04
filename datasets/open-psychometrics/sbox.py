# same pre-processing would have to be applied to college majors sst!

# lower casing
# punctuation removal
# abbreviation expansion
# symbol expansion
# stopword removal
# stemming
# fuzzy match with college majors sst -> if over certain threshold, then match!


import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# nltk.download('stopwords')
stop_words = stopwords.words('english')
# print(str(stop_words))

porter_stemmer = PorterStemmer()

def preprocess_text(text, common_college_major_abbreviations_and_acronyms_map):
    text = text.lower()
    text = re.sub(r'[\.\?=!£#]', '', text)

    for abbreviation, expaned_college_major in common_college_major_abbreviations_and_acronyms_map.items():
        pattern = r'\b' + re.escape(abbreviation) + r'\b'
        text = re.sub(pattern, expaned_college_major, text)

    text = re.sub(r'[\(\)\{\}\[\]&/+,;:\\|\-]', ' ', text)
    
    tokens = word_tokenize(text)
    cleaned_tokens = []
    for word in tokens:
        if word not in stop_words:
            stemmed_word = porter_stemmer.stem(word)
            cleaned_tokens.append(stemmed_word)

    return ' '.join(cleaned_tokens)

common_college_major_abbreviations_and_acronyms_map = {
    'cpa': 'accounting',
    'ba': 'arts',
    'ma': 'arts',
    'bs': 'science',
    'ms': 'science',
    'bsc': 'science',
    'msc': 'science',
    'bba': 'business',
    'mba': 'business',
    'bed': 'education',
    'beng': 'engineering',
    'bcom': 'business',
    'bcomm': 'business',
    'bfa': 'fine arts',
    'mfa': 'fine arts',
    'llb': 'law',
    'jd': 'law',
    'bsw': 'social work',
    'mpa': 'public administration',
    'mph': 'public health',
    'md': 'medicine',
    'ee': 'electrical engineering',
    'eee': 'electrical engineering',
    'dnp': 'nursing',
    'aud': 'audiology',
    'msw': 'social work',
    'mlis': 'library science',
    'aas': 'applied science',
    'aa': 'arts',
    'as': 'science',
    'sci': 'science',
    'math': 'mathematics',
    'maths': 'mathematics',
    'mathematic': 'mathematics',
    'cs': 'computer science',
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
    'hrm': 'human resources management',
    'pr': 'public relations',
    # 'teacher': 'education',
    # 'teaching': 'education', # skeptical about this
    'premed': 'medical preparatory programs'
}


print(preprocess_text("telecommunications", common_college_major_abbreviations_and_acronyms_map))


#I.T/computing&networking and physics -> #i.t./computing&networking and physics
#I.T/computing&networking and physics -> #it/computing&networking and physics
#I.T/computing&networking and physics -> #information technology/computing&networking and physics
#I.T/computing&networking and physics -> #information technology and computing and networking and physics
#I.T/computing&networking and physics -> #informat technolog computi network physic
