import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import top_k_accuracy_score, accuracy_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from imblearn.ensemble import BalancedRandomForestClassifier
from collections import defaultdict

def print_top_k_accuracy(y_actual, model_name, number_of_top_k, train_or_test_label, y_predicted_class_probabilities):
    print(str(round(top_k_accuracy_score(y_actual, y_predicted_class_probabilities, k=number_of_top_k), 3)) + " - " + model_name + " Top-" + str(number_of_top_k) + " " + train_or_test_label + " Accuracy")

def print_top_1_accuracy(y_actual, model_name, train_or_test_label, y_predicted):
    print(str(round(accuracy_score(y_actual, y_predicted), 3)) + " - " + model_name + " Top-1 " + train_or_test_label + " Accuracy")

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

# ## logistic regression
# logistic_regression_model = LogisticRegression(
#     class_weight='balanced', # prevents disproporionate predictions
#     multi_class='multinomial',
#     solver='saga', # negligible performance differences, saga is the quickest
#     C=1.0, # different values have negligible impact
#     max_iter=1000,
#     random_state=42)
# logistic_regression_model.fit(X_train, y_train)
# y_predicted_class_probabilities_logistic_regression = logistic_regression_model.predict_proba(X_test)
# y_predicted_logistic_regression = logistic_regression_model.predict(X_test)

## hist gradient boosting machines
hist_gradient_boosting_machine_model = HistGradientBoostingClassifier(
    class_weight='balanced', # prevents disproporionate predictions
    random_state=42)
hist_gradient_boosting_machine_model.fit(X_train, y_train)
y_predicted_class_probabilities_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict_proba(X_test)
y_predicted_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict(X_test)
y_predicted_train_class_probabilities_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict_proba(X_train)
y_predicted_train_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict(X_train)

# ## balanced random forest classifier
# balanced_random_forest_model = BalancedRandomForestClassifier(
#     n_estimators=200,
#     random_state=42,
#     replacement=True,
#     sampling_strategy='all',  # Resamples all classes to match the minority class size
#     n_jobs=-1
# )
# balanced_random_forest_model.fit(X_train, y_train)
# y_predicted_class_probabilities_balanced_random_forest = balanced_random_forest_model.predict_proba(X_test)
# y_predicted_balanced_random_forest = balanced_random_forest_model.predict(X_test)

## most frequent baseline model
most_frequent_model = DummyClassifier(strategy='most_frequent')
most_frequent_model.fit(X_train, y_train)
y_predicted_class_probabilities_most_frequent = most_frequent_model.predict_proba(X_test)
y_predicted_most_frequent = most_frequent_model.predict(X_test)

# proportions
college_major_categories = dataset['major_category'].unique()

y_predicted = [y_predicted_hist_gradient_boosting_machine]
for y_pred in y_predicted:
    predicted_college_major_counts = defaultdict(int)
    for pred in y_pred:
        predicted_college_major_counts[int(pred)] += 1

    test_college_major_category_counts = defaultdict(int)

    for college_major_category in y_test:    
        test_college_major_category_counts[int(college_major_category)] += 1

    print("\n# PROPORTIONS")
    print("CATEGORY    PREDICTED    ACTUAL")
    sum_of_squared_differences = 0.0
    for i in range(len(college_major_categories)):
        actual_proportion = round((test_college_major_category_counts[i] / len(y_test)) * 100, 1)
        pred_proportion = round((predicted_college_major_counts[i] / len(y_test)) * 100, 1)
        sum_of_squared_differences += (actual_proportion - pred_proportion)**2
        print(college_major_categories[i] + " " + str(pred_proportion) + "%     " + str(actual_proportion) + "%")

    print("Sum of Squared Differences: " + str(round(sum_of_squared_differences, 2)))


print("\n# EVALUATION")
# print_top_k_accuracy("Logistic Regression", number_of_top_k, "test", y_predicted_class_probabilities_logistic_regression)
print_top_k_accuracy(y_test, "Hist Gradient Boosting Machines", number_of_top_k, "test", y_predicted_class_probabilities_hist_gradient_boosting_machine)
print_top_k_accuracy(y_train, "Hist Gradient Boosting Machines", number_of_top_k, "train", y_predicted_train_class_probabilities_hist_gradient_boosting_machine)
# print_top_k_accuracy("Balanced Random Forest", number_of_top_k, "test", y_predicted_class_probabilities_balanced_random_forest)
# print_top_k_accuracy("Most Frequent", number_of_top_k, "test", y_predicted_class_probabilities_most_frequent)
# print_top_1_accuracy("Logistic Regression", "test", y_predicted_logistic_regression)
print_top_1_accuracy(y_test, "Hist Gradient Boosting Machine", "test", y_predicted_hist_gradient_boosting_machine)
print_top_1_accuracy(y_train, "Hist Gradient Boosting Machine", "train", y_predicted_train_hist_gradient_boosting_machine)
# print_top_1_accuracy("Balanced Random Forest", "test", y_predicted_balanced_random_forest)
# print_top_1_accuracy("Most Frequent", "test", y_predicted_most_frequent)


# # TRAINED MODELS, TOP K ACCURACY (K=3), EDUCATION_FILTER >= 2
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

# NO EDUCATION FILTER
# Logistic Regression Top-3 Test Accuracy:        0.645
# Logistic Regression Top-1 Test Accuracy:        0.37

# no substring match
# Logistic Regression Top-3 Test Accuracy:        0.66
# Logistic Regression Top-1 Test Accuracy:        0.379


# Logistic Regression, class_weight = 'balanced'
# # PROPORTIONS
# CATEGORY    PREDICTED    ACTUAL
# agriculture & natural resources 4.5%     0.6%
# arts 7.3%     3.9%
# biology & life science 7.0%     5.6%
# business 9.7%     16.4%
# communications 6.4%     2.7%
# computers & mathematics 7.3%     4.8%
# education 8.4%     4.3%
# engineering 8.2%     9.0%
# health 8.7%     7.7%
# humanities & liberal arts 3.9%     9.9%
# industrial arts & consumer services 5.9%     0.8%
# law & public policy 3.5%     3.3%
# physical sciences 5.8%     2.4%
# psychology & social work 10.3%     22.8%
# social science 3.1%     5.7%
# Sum of Squared Differences: 348.63


# # EVALUATION
# Logistic Regression Top-3 Test Accuracy:        0.536
# Most Frequent Model Top-3 Test Accuracy:        0.31
# Logistic Regression Top-1 Test Accuracy:        0.265
# Most Frequent Model Top-1 Test Accuracy:        0.228

# HGBM, class_weight='balanced'
# # PROPORTIONS
# CATEGORY    PREDICTED    ACTUAL
# agriculture & natural resources 1.9%     0.6%
# arts 8.2%     3.9%
# biology & life science 7.9%     5.6%
# business 12.1%     16.4%
# communications 6.0%     2.7%
# computers & mathematics 7.2%     4.8%
# education 8.0%     4.3%
# engineering 8.7%     9.0%
# health 8.7%     7.7%
# humanities & liberal arts 5.0%     9.9%
# industrial arts & consumer services 2.3%     0.8%
# law & public policy 3.2%     3.3%
# physical sciences 5.1%     2.4%
# psychology & social work 12.0%     22.8%
# social science 3.8%     5.7%
# Sum of Squared Differences: 229.2


# # EVALUATION
# Gradient Boosting Machines Top-3 Test Accuracy: 0.56
# Most Frequent Model Top-3 Test Accuracy:         0.31
# Gradient Boosting Machines Top-1 Test Accuracy:        0.285
# Most Frequent Model Top-1 Test Accuracy:        0.228

# random forest, class_weight='balanced'/'balanced_subsample' (same results basically)
# # PROPORTIONS
# CATEGORY    PREDICTED    ACTUAL
# agriculture & natural resources 0.1%     0.6%
# arts 1.6%     3.9%
# biology & life science 3.4%     5.6%
# business 25.6%     16.4%
# communications 0.0%     2.7%
# computers & mathematics 0.9%     4.8%
# education 0.2%     4.3%
# engineering 9.5%     9.0%
# health 4.4%     7.7%
# humanities & liberal arts 6.0%     9.9%
# industrial arts & consumer services 0.0%     0.8%
# law & public policy 0.1%     3.3%
# physical sciences 0.2%     2.4%
# psychology & social work 47.8%     22.8%
# social science 0.1%     5.7%

# # EVALUATION
# Random Forest Top-3 Test Accuracy: 0.636
# Most Frequent Model Top-3 Test Accuracy:         0.31
# Random Forest Top-1 Test Accuracy:        0.357
# Most Frequent Model Top-1 Test Accuracy:        0.228


## balanced random forest
# # PROPORTIONS
# CATEGORY    PREDICTED    ACTUAL
# agriculture & natural resources 2.1%     0.6%
# arts 8.8%     3.9%
# biology & life science 8.7%     5.6%
# business 12.3%     16.4%
# communications 6.8%     2.7%
# computers & mathematics 6.7%     4.8%
# education 6.5%     4.3%
# engineering 9.3%     9.0%
# health 10.0%     7.7%
# humanities & liberal arts 4.3%     9.9%
# industrial arts & consumer services 1.9%     0.8%
# law & public policy 3.2%     3.3%
# physical sciences 6.1%     2.4%
# psychology & social work 10.3%     22.8%
# social science 3.0%     5.7%
# Sum of Squared Differences: 293.13000000000005

# # EVALUATION
# Gradient Boosting Machines Top-3 Test Accuracy: 0.56
# Balanced Random Forest Top-3 Test Accuracy: 0.523
# Gradient Boosting Machines Top-1 Test Accuracy:        0.285
# Balanced Random Forest Top-1 Test Accuracy:        0.264
