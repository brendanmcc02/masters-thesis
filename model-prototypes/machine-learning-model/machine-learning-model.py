# not the biggest fan of this:
# * by aggregating all the 8 questions of each RIASEC category together, you lose a lot of valuable information
#   * e.g. someone might love bio & health science (high investigative), but hates math (resulting in an overall average investigative score)
# * aggregating these values together removes a lot of the nuance behind this, resulting in an incredibly simplistic & reductionistic model

import pandas as pd
import numpy as np
import random as rd

RIASEC_CATEGORIES = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']

class RandomModel:
    def train(self, train_data):
        self.major_categories = train_data['major_category'].unique().tolist()

    def predict(self, test_df):
        return test_df.apply(self.predict_row, axis=1)

    def predict_row(self, row):
        random_index = rd.randint(0, len(self.major_categories)-1)
        return self.major_categories[random_index]

class MostFrequentModel:
    mostFrequentOutput = ""
    def train(self, train_data):
        category_counts = train_data['major_category'].value_counts()
        self.mostFrequentOutput = category_counts.index[0]

    def predict(self, test_df):
        return test_df.apply(self.predict_row, axis=1)

    def predict_row(self, row):
        return self.mostFrequentOutput

def evaluate(y_pred, user_df):
    result = 0.0
    y_actual = get_y_actual_from_df(user_df)
    y_pred = list(y_pred)
    
    for i in range(len(y_actual)):
        if y_pred[i] == y_actual[i]:
            result += 1.0

    return round((result / len(y_actual)), 3)
    
def get_y_actual_from_df(user_df):
    categories_to_exclude = RIASEC_CATEGORIES + ['name']
    ranked_college_major_preferences = user_df.drop(columns=categories_to_exclude).copy().values

    return list(ranked_college_major_preferences)


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
