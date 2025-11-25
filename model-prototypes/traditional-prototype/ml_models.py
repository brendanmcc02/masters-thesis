import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB, CategoricalNB
from sklearn.metrics import top_k_accuracy_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier

dataset = pd.read_csv("../../datasets/open-psychometrics/clean_riasec_college_major_categories.tsv", sep='\t')

feature_columns = [ 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 
                    'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 
                    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

X = dataset[feature_columns]
y = dataset['major_category']

# encode the output variable as numerical values
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# stratify ensures proportion of output variables remains the same in the sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y ,random_state=42
)

# actual models

## multinomial naive bayes
# multinomial_naive_bayes_model = MultinomialNB()
# multinomial_naive_bayes_model.fit(X_train, y_train)
# y_predicted_class_probabilities_multinomial_naive_bayes = multinomial_naive_bayes_model.predict_proba(X_test)

## categorical naive bayes
# categorical_naive_bayes_model = CategoricalNB()
# categorical_naive_bayes_model.fit(X_train, y_train)
# y_predicted_class_probabilities_categorical_naive_bayes = categorical_naive_bayes_model.predict_proba(X_test)

## logistic regression
# logistic_regression_model = LogisticRegression(
#     multi_class='multinomial',
#     solver='saga', # negligible performance differences, saga is the quickest
#     C=1.0, # different values have negligible impact
#     max_iter=1000,
#     warm_start=True,
#     random_state=42
# )
# logistic_regression_model.fit(X_train, y_train)
# y_predicted_class_probabilities_logistic_regression = logistic_regression_model.predict_proba(X_test)

## multi-layer perceptron
# (48, 20, 15) architecture: 48 inputs -> 2 hidden layers of 50 neurons each -> 15 outputs
# alpha is the L2 penalty, similar to regularization
# mlp_model = MLPClassifier(
#     hidden_layer_sizes=(50, 50), 
#     max_iter=500, # Often needs many iterations
#     alpha=0.0001,
#     warm_start=True,
#     random_state=42
# )
# mlp_model.fit(X_train, y_train)
# y_predicted_class_probabilities_mlp = mlp_model.predict_proba(X_test)

## support vector machine (svm)
svm_model = SVC(
    kernel='linear', 
    C=1.0,
    random_state=42)
# Note: SVMs scale poorly with N, so using a LinearSVC or linear kernel is often necessary for 77k rows.
# For SVC, it's highly recommended to scale your features (0-4) before training.
# svm_model = SVC(kernel='rbf', C=1.0, random_state=42) # slower
svm_model.fit(X_train, y_train)
y_predicted_class_probabilities_svm = svm_model.predict_proba(X_test)

## gradient boosting machines (gbm)
hgbm_model = HistGradientBoostingClassifier(random_state=42)
hgbm_model.fit(X_train, y_train)
y_predicted_class_probabilities_hgbm = hgbm_model.predict_proba(X_test)

# random forest
# n_estimators is the number of trees; often start with 100 or 200
random_forest_model = RandomForestClassifier(
    n_estimators=200, 
    warm_start=True,
    random_state=42, 
    n_jobs=-1)
random_forest_model.fit(X_train, y_train)
y_predicted_class_probabilities_random_forest = random_forest_model.predict_proba(X_test)

# baselines

## random
number_of_classes = len(np.unique(y_train))
number_of_random_samples = len(y_test)
np.random.seed(42) # Ensure random baseline is reproducible
random_scores = np.random.rand(number_of_random_samples, number_of_classes)
y_predicted_class_probabilities_random = random_scores / random_scores.sum(axis=1, keepdims=True)

## most frequent
most_frequent_model = DummyClassifier(strategy='most_frequent')
most_frequent_model.fit(X_train, y_train)
y_predicted_class_probabilities_most_frequent = most_frequent_model.predict_proba(X_test)

# evaluation

number_of_top_k = 3

print("\n# ACTUAL MODELS")
# print("Multinomial Naive Bayes Accuracy:    " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_multinomial_naive_bayes, k=number_of_top_k), 3)))
# print("Categorical Naive Bayes Accuracy:    " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_categorical_naive_bayes, k=number_of_top_k), 3)))
# print("Logistic Regression Accuracy:        " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_logistic_regression, k=number_of_top_k), 3)))
# print("MLP Accuracy:                        " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_mlp, k=number_of_top_k), 3)))
print("SVM Accuracy:                        " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_svm, k=number_of_top_k), 3)))
print("Gradient Boosting Machines Accuracy: " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_hgbm, k=number_of_top_k), 3)))
print("Random Forest Accuracy:              " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_random_forest, k=number_of_top_k), 3)))

print("\n# BASELINE MODELS")
print("Random Model Accuracy:               " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_random, k=number_of_top_k), 3)))
print("Most Frequent Model Accuracy:        " + str(round(top_k_accuracy_score(y_test, y_predicted_class_probabilities_most_frequent, k=number_of_top_k), 3)))

# # ACTUAL MODELS
# Multinomial Naive Bayes Accuracy:    0.562
# Categorical Naive Bayes Accuracy:    0.551
# Logistic Regression Accuracy:        0.639

# # BASELINE MODELS
# Random Model Accuracy:               0.199
# Most Frequent Model Accuracy:        0.349

