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
    'sci': 'science',
    'sciences': 'science',
    'math': 'mathematics',
    'maths': 'mathematics',
    'cs': 'computer science',
    'comp': 'computer',
    'econ': 'economics',
    'lit': 'literature',
    'poli': 'political',
    'polsci': 'political science',
    'pol': 'political',
    'psych': 'psychology',
    'pysch': 'psychology', # common mis-spelling
    'pyschology': 'psychology', # common mis-spelling
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
    'nurse': 'nursing'
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

# the values in this dict need to be in college_majors
college_major_mapping_dict = {
    'art': 'arts',
    'ba': 'arts', # bachelor of arts
    'liberal studies': 'liberal arts',
    'literature': 'english language and literature',
    'english': 'english language and literature',
    'information technology': 'computer and information systems',
    'information systems': 'computer and information systems',
    'political science': 'political science and government',
    'government': 'political science and government',
    'anthropology':'anthropology and archeology',
    'archeology':'anthropology and archeology',
    'science': 'multi-disciplinary or general science',
    'philosophy': 'philosophy and religious studies',
    'religious studies': 'philosophy and religious studies',
    'art history': 'art history and criticism',
    'agriculture': 'general agriculture',
    'agriculture production': 'agriculture production and management',
    'agriculture management': 'agriculture production and management',
    'plant science': 'plant science and agronomy',
    'agronomy': 'plant science and agronomy',
    'theater arts': 'drama and theater arts',
    'visual arts': 'visual and performing arts',
    'performing arts': 'visual and performing arts',
    'graphic design': 'commercial art and graphic design',
    'commercial art': 'commercial art and graphic design',
    'photographic arts': 'film video and photographic arts',
    'biochemical': 'biochemical sciences',
    'cognitive science': 'cognitive science and biopsychology',
    'biopsychology': 'cognitive science and biopsychology',
    'actuary': 'actuarial science',
    'business management': 'business management and administration',
    'operations logistics': 'operations logistics and e-commerce',
    'e-commerce': 'operations logistics and e-commerce',
    'marketing': 'marketing and marketing research',
    'human resources': 'human resources and personnel management',
    'human resource management': 'human resources and personnel management',
    'personnel management': 'human resources and personnel management',
    'statistics': 'statistics and decision science',
    'advertising': 'advertising and public relations',
    'public relations': 'advertising and public relations',
    'computer programming': 'computer programming and data processing',
    'data processing': 'computer programming and data processing',
    'computer networking': 'computer networking and telecommunications',
    'telecommunications': 'computer networking and telecommunications',
    'educational administration': 'educational administration and supervision',
    'higher education': 'secondary teacher education',
    'law': 'law & public policy',
    'communication': 'communications',
    'public health': 'community and public health',
    'community health': 'community and public health',
    'commerce': 'general business',
    'administration': 'business management and administration',
    'medicine': 'general medical and health services',
    'doctor': 'general medical and health services',
    'health services': 'general medical and health services',
    'family science':'family and consumer sciences',
    'consumer science':'family and consumer sciences',
    'counseling': 'counseling psychology',
    'counselling': 'counseling psychology',
    'biomedical science': 'biomedical engineering',
    # 'classics': #TODO
    # 'foreign langauge': 'foreign languages',
    # 'french'
    # 'german'
    # 'chinese'
    # 'japanese'
    # 'korean'
    # 'italian'
    # 'spanish'
    # 'pharmacy'
    # 'philology'
}

dirty_df['major'] = dirty_df['major'].replace(college_major_mapping_dict)
college_major_mapping_values_set = set(college_major_mapping_dict.values())
is_mapped_filter = dirty_df['major'].isin(college_major_mapping_values_set)

mapped_df = dirty_df[is_mapped_filter].copy()
clean_df = pd.concat([clean_df, mapped_df], ignore_index=True)
dirty_df = dirty_df[~is_mapped_filter].copy()

clean_df.to_csv("clean_riasec_college_majors.tsv", sep='\t', index=False)
dirty_df.to_csv("dirty_riasec_college_majors.tsv", sep='\t', index=False)
