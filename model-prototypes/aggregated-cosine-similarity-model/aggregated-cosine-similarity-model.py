# not the biggest fan of this:
# * by aggregating all the 8 questions of each RIASEC category together, you lose a lot of valuable information
#   * e.g. someone might love bio & health science (high investigative), but hates math (resulting in an overall average investigative score)
# * aggregating these values together removes a lot of the nuance behind this, resulting in an incredibly simplistic & reductionistic model

import pandas as pd
import numpy as np
import random as rd
import math

NUMBER_OF_RECOMMENDATIONS = 3
RIASEC_CATEGORIES = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']

class AggregatedCosineSimilarityModel:
    major_category_vectors = {}

    def train(self, train_data):
        major_categories = train_data['major_category'].unique().tolist()
        
        riasec_vectors_array = train_data[RIASEC_CATEGORIES].values
        category_vectors = list(riasec_vectors_array)

        for i in range(len(major_categories)):
            self.major_category_vectors[major_categories[i]] = category_vectors[i]

    def predict(self, test_df):
        return test_df.apply(self.predict_row, axis=1)

    def predict_row(self, row):
        ranking = []

        user_vector = row[RIASEC_CATEGORIES].values

        for major_category in self.major_category_vectors.keys():
            ranking.append((major_category, self.get_cosine_similarity(user_vector, self.major_category_vectors[major_category])))

        ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
        ranked_college_major_categories = [item[0] for item in ranking]

        return ranked_college_major_categories[:NUMBER_OF_RECOMMENDATIONS]
    
    def get_cosine_similarity(self, a, b):
        a_magnitude = np.linalg.norm(a)
        b_magnitude = np.linalg.norm(b)

        if a_magnitude == 0.0 or b_magnitude == 0.0:
            return 0.0

        return np.dot(a, b) / (a_magnitude * b_magnitude)


class RandomModel:
    major_categories = []

    def train(self, train_data):
        self.major_categories = train_data['major_category'].unique().tolist()

    def predict(self, test_df):
        return test_df.apply(self.predict_row, axis=1)

    def predict_row(self, row):
        ranking = []

        for _ in range(NUMBER_OF_RECOMMENDATIONS):
            random_index = rd.randint(0, len(self.major_categories)-1)
            while self.major_categories[random_index] in ranking:
                random_index = rd.randint(0, len(self.major_categories)-1)

            ranking.append(self.major_categories[random_index])

        return ranking

def evaluate(y_pred, user_df):
    results = []
    y_actual = get_y_actual_from_df(user_df)
    y_pred = list(y_pred)

    ideal_ranking = get_ideal_normalized_discounted_cumulative_gain_ranking()
    
    for i in range(len(y_actual)):
        results.append(normalized_discounted_cumulative_gain(y_pred[i], y_actual[i], ideal_ranking))
        # print("\n" + str(user_df['name'][i]))
        # print("PRED\tACTUAL")
        # for j in range(len(y_actual[i])):
        #     print(y_pred[i][j] + "\t" + y_actual[i][j])

    return round(np.mean(results), 3)
    
def get_y_actual_from_df(user_df):
    categories_to_exclude = RIASEC_CATEGORIES + ['name']
    ranked_college_major_preferences = user_df.drop(columns=categories_to_exclude).copy().values

    return list(ranked_college_major_preferences)

def normalized_discounted_cumulative_gain(y_pred, y_actual, ideal_ranking):
    discounted_cumulative_gains = 0
    for i in range(len(y_pred)):
        if y_pred[i] in y_actual:
            relevance_score = 1
        else:
            relevance_score = 0
    
        discounted_cumulative_gains += (relevance_score / math.log2((i+1)+1))

    return discounted_cumulative_gains / ideal_ranking

def get_ideal_normalized_discounted_cumulative_gain_ranking():
    discounted_cumulative_gains = 0
    for i in range(NUMBER_OF_RECOMMENDATIONS):
        discounted_cumulative_gains += (1 / math.log2((i+1)+1))

    return discounted_cumulative_gains

aggregated_riasec_major_categories_df = pd.read_csv('../../datasets/open-psychometrics/clean_aggregated_riasec_college_major_categories.tsv', sep='\t', low_memory=False)
test_df = pd.read_csv('friends-open-psychometrics-data.tsv', sep='\t', low_memory=False)

aggregatedCosineSimilarityModel = AggregatedCosineSimilarityModel()
aggregatedCosineSimilarityModel.train(aggregated_riasec_major_categories_df)
y_pred = aggregatedCosineSimilarityModel.predict(test_df)
print("Aggregated Cosine Similarity Model Performance: " +str(evaluate(y_pred, test_df)))

randomModel = RandomModel()
randomModel.train(aggregated_riasec_major_categories_df)
random_model_results = []
for i in range(5000):
    y_pred = randomModel.predict(test_df)
    random_model_results.append(evaluate(y_pred, test_df))
print("Random RIASEC Model Performance: " + str(round(np.mean(random_model_results), 3)))
