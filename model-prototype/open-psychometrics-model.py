import pandas as pd
import numpy as np

class OpenPsychometricsModel:
    NUMBER_OF_RECOMMENDATIONS = 5
    RIASEC_CATEGORIES = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']

    major_category_vectors = {}

    def __init__(self):
        pass

    def train(self, train_data):
        major_categories = train_data['major_category'].tolist()
        
        riasec_vectors_array = train_data[self.RIASEC_CATEGORIES].values
        category_vectors = list(riasec_vectors_array)

        for i in range(len(major_categories)):
            self.major_category_vectors[major_categories[i]] = category_vectors[i]

    def predict(self, test_df):
        return test_df.apply(self.predict_row, axis=1)

    def predict_row(self, row):
        ranking = []

        user_vector = row[self.RIASEC_CATEGORIES].values

        for major_category in self.major_category_vectors.keys():
            ranking.append((major_category, self.get_cosine_similarity(user_vector, self.major_category_vectors[major_category])))

        ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
        ranked_college_major_categories = [item[0] for item in ranking]

        return ranked_college_major_categories[:self.NUMBER_OF_RECOMMENDATIONS]

    def evaluate(self, model_output, user_df):
        user_generated_output = self.get_user_generated_output_from_df(user_df)

        # maybe use spearson (or whatever it's called)
        # or Kendall Rank Correlation Co-efficient (explained in aggarwal's book)
        return 1.0
    
    def get_user_generated_output_from_df(self, user_df):
        categories_to_exclude = self.RIASEC_CATEGORIES + ['name']
        ranked_college_major_preferences = user_df.drop(columns=categories_to_exclude).copy().values

        return list(ranked_college_major_preferences)

    def get_cosine_similarity(a, b):
        a_magnitude = np.linalg.norm(a)
        b_magnitude = np.linalg.norm(b)

        if a_magnitude == 0.0 or b_magnitude == 0.0:
            return 0.0

        return np.dot(a, b) / (a_magnitude * b_magnitude)

model = OpenPsychometricsModel()
aggregated_riasec_major_categories_df = pd.read_csv('../datasets/open-psychometrics/clean_aggregated_riasec_college_major_categories.tsv', sep='\t', low_memory=False)
model.train(aggregated_riasec_major_categories_df)

test_df = pd.read_csv('friends-open-psychometrics-data.tsv', sep='\t', low_memory=False)
model_output = model.predict(test_df)

model.evaluate(model_output, test_df)
