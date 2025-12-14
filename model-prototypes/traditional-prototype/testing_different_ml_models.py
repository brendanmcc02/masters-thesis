import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import top_k_accuracy_score, accuracy_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from collections import defaultdict

number_of_top_k = 3

dataset = pd.read_csv("../../datasets/open-psychometrics/clean_riasec_college_major_categories.tsv", sep='\t')

feature_columns = [ 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8',
                    'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 
                    'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
                    'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 
                    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',
                    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

X = dataset[feature_columns]
y = dataset['major_category']

# encode the output variable as numerical values
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# stratify ensures proportion of output variables remains the same in the sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, stratify=y ,random_state=42
)

logistic_regression_model = LogisticRegression(
    multi_class='multinomial',
    solver='saga', # negligible performance differences, saga is the quickest
    C=1.0, # different values have negligible impact
    max_iter=1000,
    warm_start=True, 
    random_state=42
)

logistic_regression_model.fit(X_train, y_train)
y_predicted_class_probabilities_logistic_regression = logistic_regression_model.predict_proba(X_test)
y_predicted_logistic_regression = logistic_regression_model.predict(X_test)

college_major_categories = dataset['major_category'].unique()

predicted_college_major_counts = defaultdict(int)

for pred in y_predicted_logistic_regression:
    predicted_college_major_counts[int(pred)] += 1

test_college_major_category_counts = defaultdict(int)

for college_major_category in y_test:    
    test_college_major_category_counts[int(college_major_category)] += 1

## random baseline model
number_of_classes = len(np.unique(y_train))
number_of_random_samples = len(y_test)
np.random.seed(42) # Ensure random baseline is reproducible
random_scores = np.random.rand(number_of_random_samples, number_of_classes)
y_predicted_class_probabilities_random = random_scores / random_scores.sum(axis=1, keepdims=True)

## most frequent baseline model
most_frequent_model = DummyClassifier(strategy='most_frequent')
most_frequent_model.fit(X_train, y_train)
y_predicted_class_probabilities_most_frequent = most_frequent_model.predict_proba(X_test)
y_predicted_most_frequent = most_frequent_model.predict(X_test)

print("\n# PROPORTIONS")
print("CATEGORY    PREDICTED    ACTUAL")
for i in range(len(college_major_categories)):
    actual_proportion = round((test_college_major_category_counts[i] / len(y_test)) * 100, 1)
    pred_proportion = round((predicted_college_major_counts[i] / len(y_test)) * 100, 1)
    print(college_major_categories[i] + " " + str(pred_proportion) + "%     " + str(actual_proportion) + "%")

print("\n# EVALUATION")
print("Logistic Regression Top-" + str(number_of_top_k) + " Test Accuracy:        " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_logistic_regression, k=number_of_top_k), 3)))
print("Logistic Regression Top-1 Test Accuracy:                                   " + str(round(accuracy_score(y_test, y_predicted_logistic_regression), 3)))
print("Random Model Top-" + str(number_of_top_k) + " Test Accuracy:               " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_random, k=number_of_top_k), 3)))
print("Most Frequent Model Top-" + str(number_of_top_k) + " Test Accuracy:        " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_most_frequent, k=number_of_top_k), 3)))
print("Most Frequent Model Top-1 Test Accuracy:                                   " + str(round(accuracy_score(y_test, y_predicted_most_frequent), 3)))

# # TRAINED MODELS, TOP K ACCURACY (K=3)
# Multinomial Naive Bayes Test Accuracy:    0.562
# Categorical Naive Bayes Test Accuracy:    0.551
# Logistic Regression Test Accuracy:        0.639 # fast
# Logistic Regression Train Accuracy:       0.645 # no indication of significant over-fitting
# SVM Test Accuracy:                        0.636 # so long
# Gradient Boosting Machines Test Accuracy: 0.636 # fast
# Random Forest Test Accuracy:              0.618
# MLP Test Accuracy:                        0.622

# # BASELINE MODELS
# Random Model Test Accuracy:               0.199
# Most Frequent Model Test Accuracy:        0.349


# 0-2 LIKERT SCALE
# Logistic Regression Test Accuracy:        0.629
# Logistic Regression Test Accuracy:        0.633

# # TOP K ACCURACY (K=1)
# Logistic Regression Test Accuracy:        0.363
# Random Model Test Accuracy:               0.065
# Most Frequent Model Test Accuracy:        0.229

# # TOP K ACCURACY (K=2)
# Logistic Regression Test Accuracy:        0.53
# Random Model Test Accuracy:               0.131
# Most Frequent Model Test Accuracy:        0.289

# # TOP K ACCURACY (K=4)
# Logistic Regression Test Accuracy:        0.723
# Random Model Test Accuracy:               0.265
# Most Frequent Model Test Accuracy:        0.382

# # TOP K ACCURACY (K=5)
# Logistic Regression Test Accuracy:        0.788
# Random Model Test Accuracy:               0.332
# Most Frequent Model Test Accuracy:        0.385


# CATEGORY                              PREDICTED    ACTUAL
# agriculture & natural resources       0.0%         0.4%
# arts                                  2.6%         4.6%
# biology & life science                2.9%         4.4%
# business                              25.7%        16.8%
# communications & journalism           0.1%         3.2%
# computers & mathematics               1.0%         3.7%
# education                             0.1%         3.4%
# engineering                           8.3%         7.8%
# health                                3.0%         5.2%
# humanities & liberal arts             11.2%        12.0%
# industrial arts & consumer services   0.0%         0.3%
# law & public policy                   0.0%         3.2%
# physical sciences                     1.8%         6.1%
# psychology & social work              43.2%        22.9%
# social science                        0.2%         5.9%

