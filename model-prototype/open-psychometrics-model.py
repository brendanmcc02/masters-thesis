import pandas as pd
import numpy as np

def predict(row, major_category_vectors):
    ranking = []

    user_vector = row[riasec_categories].values

    for major_category in major_category_vectors.keys():
        ranking.append((major_category, getCosineSimilarity(user_vector, major_category_vectors[major_category])))

    ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
    ranked_college_major_categories = [item[0] for item in ranking]

    return ranked_college_major_categories

def getCosineSimilarity(a, b):
    a_magnitude = np.linalg.norm(a)
    b_magnitude = np.linalg.norm(b)

    if a_magnitude == 0.0 or b_magnitude == 0.0:
        return 0.0

    return np.dot(a, b) / (a_magnitude * b_magnitude)

def evaluate(model_output, user_df):
    user_generated_output = get_user_generated_output_from_df(user_df)

    return normalized_discounted_cumulative_gain(model_output, user_generated_output)

def normalized_discounted_cumulative_gain(model_output, user_generated_output):
    evaluation_metric = 0.0

    # https://gemini.google.com/u/1/app/1d8f5e432d9bddeb

    return evaluation_metric

def get_user_generated_output_from_df(user_df):
    categories_to_exclude = riasec_categories + ['name']
    ranked_college_major_preferences = user_df.drop(columns=categories_to_exclude).copy().values

    return list(ranked_college_major_preferences)


aggregated_riasec_major_categories_df = pd.read_csv('../datasets/open-psychometrics/clean_aggregated_riasec_college_major_categories.tsv', sep='\t', low_memory=False)

major_categories = aggregated_riasec_major_categories_df['major_category'].tolist()

riasec_categories = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
riasec_vectors_array = aggregated_riasec_major_categories_df[riasec_categories].values
category_vectors = list(riasec_vectors_array)

major_category_vectors = {}
for i in range(len(major_categories)):
    major_category_vectors[major_categories[i]] = category_vectors[i]

input_df = pd.read_csv('friends-open-psychometrics-data.tsv', sep='\t', low_memory=False)

model_output = input_df.apply(predict, axis=1, major_category_vectors=major_category_vectors)

evaluate(model_output, input_df)


