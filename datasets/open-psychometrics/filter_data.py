# dataset: https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses
# original found here (identical): https://openpsychometrics.org/_rawdata/

import pandas as pd
import re
# import fuzzywuzzy


try:
    df = pd.read_csv('raw_riasec_college_majors.tsv', sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')

undergrad_or_postgrad_filter = (df['education'] == 3) | (df['education'] == 4)
df = df[undergrad_or_postgrad_filter]

df['major'] = df['major'].str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)

non_empty_major_filter = ~(df['major'].fillna('').eq(''))
df = df[non_empty_major_filter]

dirty_college_major_filter = ~( (df['major'] == 'yes') | (df['major'] == 'no') | (df['major'] == 'na') | (df['major'] == 'none') | (df["major"] == "do not know") | (df["major"] == "dont know") | (df["major"] == "idk") | (df["major"] == "n. a.") | (df["major"] == "non") | (df['major'] == 'other') | (df['major'] == 'multiple'))
df = df[dirty_college_major_filter]

filtered_columns = []

holland_code_prefixes = ['R', 'I', 'A', 'S', 'E', 'C']
for prefix in holland_code_prefixes[::-1]:
    score_cols = [col for col in df.columns if col.startswith(prefix) and col[1:].isdigit()]
    
    if score_cols:
        df[prefix] = (df[score_cols].mean(axis=1) - 1) / 4  # normalize mean between 0.0 and 1.0
        filtered_columns.insert(0, prefix)

filtered_columns.insert(0, 'major')
riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
df = df[filtered_columns].rename(columns={'R':riasec_types[0], 'I':riasec_types[1], 'A':riasec_types[2], 'S':riasec_types[3], 'E':riasec_types[4], 'C':riasec_types[5]})

common_college_major_abbreviations_map = {
    'art': 'arts',
    'sci': 'science',
    'sciences': 'science',
    'math': 'mathematics',
    'maths': 'mathematics',
    'mathematic': 'mathematics',
    'cs': 'computer science',
    'comp': 'computer',
    'econ': 'economics',
    'lit': 'literature',
    'poli': 'political',
    'polsci': 'political science',
    'pol': 'political',
    'psych': 'psychology',
    'pysch': 'psychology', # common mis-spelling # could probably get rid of with fuzzy wuzzy?
    'pyschology': 'psychology', # common mis-spelling # could probably get rid of with fuzzy wuzzy?
    'archaeology' : 'archeology', # common mis-spelling # could probably get rid of with fuzzy wuzzy?
    'tech': 'technology',
    'technologies': 'technology',
    'info': 'information',
    'it': 'information technology',
    'eng': 'engineering',
    'engineer': 'engineering',
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
    'nurse': 'nursing',
    'communication': 'communications',
    'pr': 'public relations',
    'networking': 'networks',
    'teacher': 'education',
    'teaching': 'education',
    'counselor': 'counseling',
    'theatre': 'theater', # american spelling # could probably get rid of with fuzzy wuzzy?
}

for abbreviation, expaned_college_major in common_college_major_abbreviations_map.items():
    pattern = r'\b' + re.escape(abbreviation) + r'\b'
    df['major'] = df['major'].str.replace(pat=pattern, repl=expaned_college_major, regex=True)

try:
    college_majors_df = pd.read_csv("filtered_college_majors_2012_usa.tsv", sep='\t', low_memory=False)
except Exception as e:
    print(f'An error occurred while reading the CSV file: {e}')

college_majors_and_college_major_categories = set(
    college_majors_df["College Major Category"].unique().tolist() +
    college_majors_df["College Major"].tolist()
)

is_defined_college_major = df['major'].isin(college_majors_and_college_major_categories)

clean_df = df[is_defined_college_major].copy()
dirty_df = df[~is_defined_college_major].copy()

# TODO spell check here?
# or fuzzy wuzzy would be better?

# the values in this dict need to be in college_majors
college_major_mapping_dict = {
    # arts
    'ba': 'arts', # bachelor of arts
    'drama': 'drama and theater arts',
    'drama arts': 'drama and theater arts',
    'theater arts': 'drama and theater arts',
    'theater': 'drama and theater arts',
    'visual arts': 'visual and performing arts',
    'performing arts': 'visual and performing arts',
    'graphic design': 'commercial art and graphic design',
    'commercial art': 'commercial art and graphic design',
    'photographic arts': 'film video and photographic arts',
    'film': 'film video and photographic arts',
    'film school': 'film video and photographic arts',
    'cinema': 'film video and photographic arts',
    'musical studies': 'music',
    'design': 'commercial art and graphic design',
    
    # humanities
    'liberal studies': 'liberal arts',
    'literature': 'english language and literature',
    'english': 'english language and literature',
    'english literature': 'english language and literature',
    'philosophy': 'philosophy and religious studies',
    'ethics': 'philosophy and religious studies',
    'religious studies': 'philosophy and religious studies',
    'religion': 'philosophy and religious studies',
    'bible': 'philosophy and religious studies',
    'arts history': 'art history and criticism', # art -> arts ; abbreviation expansion
    'arts criticism': 'art history and criticism', # art -> arts ; abbreviation expansion
    'anthropology':'anthropology and archeology',
    'archeology':'anthropology and archeology',
    'foreign langauge': 'foreign languages',
    'translation': 'foreign languages',
    'french': 'foreign languages',
    'german': 'foreign languages',
    'chinese': 'foreign languages',
    'japanese': 'foreign languages',
    'korean': 'foreign languages',
    'italian': 'foreign languages',
    'spanish': 'foreign languages',
    'russian': 'foreign languages',
    'languages': 'foreign languages',
    'philology': 'linguistics and comparative language and literature',
    'linguistics': 'linguistics and comparative language and literature',
    'classics': 'humanities & liberal arts',
    'civilization': 'area ethnic and civilization studies',
    'international studies': 'intercultural and international studies',
    'intercultural studies': 'intercultural and international studies',
    'theology': 'theology and religious vocations',

    # biology
    'plant science': 'plant science and agronomy',
    'agronomy': 'plant science and agronomy',
    'biochemical': 'biochemical sciences',
    'biochemistry': 'biochemical sciences',
    'cognitive science': 'cognitive science and biopsychology',
    'biopsychology': 'cognitive science and biopsychology',
    'kinesiology': 'physiology',
    'physical therapy': 'physiology',
    'physio': 'physiology',
    'physiotherapy': 'physiology',
    'environmental': 'environmental science',
    'biological': 'biology', # bio -> biological; abbreviation expansion
    'neuro': 'neuroscience',
    'neuropsychology': 'neuroscience',
    'neurobiology': 'neuroscience',
    'neurology': 'physiology',
    'genetic': 'genetics',
    'ecological science': 'ecology',
    
    # health
    'public health': 'community and public health',
    'community health': 'community and public health',
    'medicine': 'general medical and health services',
    'medical': 'general medical and health services',
    'doctor': 'general medical and health services',
    'dentist': 'general medical and health services',
    'dental science': 'general medical and health services',
    'dental': 'general medical and health services',
    'dental hygiene': 'general medical and health services',
    'dental assistant': 'general medical and health services',
    'dental assisting': 'general medical and health services',
    'dentistry': 'general medical and health services',
    'health services': 'general medical and health services',
    'healthcare': 'general medical and health services',
    'pharmacist': 'pharmacology',
    'pharmacy': 'pharmacology',
    'pharmaceutic': 'pharmacology',
    'pharmaceutical': 'pharmacology',
    'pharmacy technology': 'pharmacology',
    'pharmaceuticals': 'pharmacology',
    'pharmaceutical science': 'pharmacology',
    'health science': 'biology',
    'life science': 'biology',
    'nutrition': 'nutrition sciences',
    'midwife': 'nursing',
    'midwifery': 'nursing',

    # business
    'actuary': 'actuarial science',
    'actuarial': 'actuarial science',
    'actuarial studies': 'actuarial science',
    'operations logistics': 'operations logistics and e-commerce',
    'operations management': 'operations logistics and e-commerce',
    'e-commerce': 'operations logistics and e-commerce',
    'business marketing': 'marketing and marketing research',
    'marketing': 'marketing and marketing research',
    'marketing management': 'marketing and marketing research',
    'human resource': 'human resources and personnel management',
    'human resources': 'human resources and personnel management', # could probably get rid of this with fuzzywuzzy
    'human resource management': 'human resources and personnel management',
    'human resources management': 'human resources and personnel management', # could probably get rid of this with fuzzywuzzy
    'human resource development': 'human resources and personnel management',
    'human resources development': 'human resources and personnel management', # could probably get rid of this with fuzzywuzzy
    'personnel management': 'human resources and personnel management',
    'commerce': 'general business',
    'business management': 'business management and administration',
    'administration': 'business management and administration',
    'business administration': 'business management and administration',
    'administrative science': 'business management and administration',
    'mba': 'business management and administration',
    'management': 'business management and administration',
    'economy': 'economics',
    'hotel management': 'hospitality management',
    'international commerce': 'international business',
    'international trade': 'international business',
    'management information systems': 'management information systems and statistics',
    'medical administration' : 'miscellaneous business & medical administration',
    
    # communications
    'mass communications': 'mass media',
    'media communications': 'mass media',
    'communication studies': 'communications',
    'communications studies': 'communications', # could probably get rid of this with fuzzywuzzy
    'advertising': 'advertising and public relations',
    'public relations': 'advertising and public relations',
    'media': 'mass media',
    'media studies': 'mass media',

    # computers & math
    'computer science and mathematics': 'mathematics and computer science',
    'computer': 'computer and information systems',
    'computing': 'computer and information systems',
    'computers': 'computer and information systems', # could probably get rid of this with fuzzywuzzy
    'computer information system': 'computer and information systems', # could probably get rid of this with fuzzywuzzy
    'computer information systems': 'computer and information systems',
    'computer systems': 'computer and information systems',
    'computer information technology': 'computer and information systems',
    'information technology': 'computer and information systems',
    'information systems': 'computer and information systems',
    'computer technology': 'computer and information systems',
    'statistics': 'statistics and decision science',
    'computer programming': 'computer programming and data processing',
    'programming': 'computer programming and data processing',
    'data processing': 'computer programming and data processing',
    'computer networks': 'computer networking and telecommunications', # networking -> networks ; abbreviation expansion
    'networks': 'computer networking and telecommunications', # networking -> networks ; abbreviation expansion
    'cybersecurity': 'computer networking and telecommunications',
    'telecommunications': 'computer networking and telecommunications',
    'computer studies': 'computer and information systems',
    'software engineering': 'computer science',

    # education
    # note "teacher" & "teaching" -> "education"
    'educational studies': 'education',
    'educational administration': 'educational administration and supervision',
    'primary education': 'elementary education',
    'secondary education': 'secondary teacher education',
    'higher education': 'secondary teacher education',
    'special education': 'special needs education',
    'mathematics education': 'mathematics teacher education',
    'arts education': 'art and music education', # art -> arts
    'music education': 'art and music education',
    'science education': 'science and computer teacher education',
    'school counseling': 'school student counseling',

    # engineering
    'biomedical science': 'biomedical engineering',
    'biotech': 'biological engineering',
    'biotech engineering': 'biological engineering',
    'biotechnology': 'biological engineering',
    'electronics': 'electrical engineering',
    'architectural studies': 'architecture',
    'architect': 'architecture',
    'industrial engineering': 'industrial and manufacturing engineering',
    'manufacturing engineering': 'industrial and manufacturing engineering',

    # agriculture
    'agriculture': 'general agriculture',
    'agriculture production': 'agriculture production and management',
    'agriculture management': 'agriculture production and management',
    'food': 'food science',

    # physical science
    'science': 'multi-disciplinary or general science',
    'geology': 'geology and earth science',
    'earth science': 'geology and earth science',
    'geological science': 'geology and earth science',
    'astronomy': 'astronomy and astrophysics',
    'astrophysics': 'astronomy and astrophysics',

    # law
    'law': 'law & public policy',
    'international law': 'law & public policy',
    'lawyer': 'law & public policy',
    'legal': 'law & public policy',
    'legal studies': 'law & public policy',
    'paralegal': 'law & public policy',
    'paralegal studies': 'law & public policy',
    'criminal justice': 'criminal justice and fire protection',

    # psych
    'counseling': 'counseling psychology',
    'counselling': 'counseling psychology',
    'therapy': 'counseling psychology',

    # social science
    'political science': 'political science and government',
    'politics': 'political science and government',
    'government': 'political science and government',
    'sociological': 'sociology',
    'international affairs': 'international relations',
    'international development': 'international relations',
    'international politics': 'international relations',

    # industrial arts
    'family science':'family and consumer sciences',
    'consumer science':'family and consumer sciences',
    'culinary': 'cosmetology services and culinary arts',
    'culinary arts': 'cosmetology services and culinary arts',
    'culinary science': 'cosmetology services and culinary arts',
    'hospitality': 'hospitality management',
}

dirty_df['major'] = dirty_df['major'].replace(college_major_mapping_dict)
college_major_mapping_values_set = set(college_major_mapping_dict.values())
is_mapped_filter = dirty_df['major'].isin(college_major_mapping_values_set)

mapped_df = dirty_df[is_mapped_filter].copy()
clean_df = pd.concat([clean_df, mapped_df], ignore_index=True)
dirty_df = dirty_df[~is_mapped_filter].copy()

clean_df.to_csv("clean_riasec_college_majors.tsv", sep='\t', index=False)
dirty_df.to_csv("dirty_riasec_college_majors.tsv", sep='\t', index=False)
