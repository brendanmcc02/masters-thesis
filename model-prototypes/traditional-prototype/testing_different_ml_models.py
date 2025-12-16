import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import top_k_accuracy_score, accuracy_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
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
# y_predicted_test_class_probabilities_logistic_regression = logistic_regression_model.predict_proba(X_test)
# y_predicted_test_logistic_regression = logistic_regression_model.predict(X_test)
# y_predicted_train_class_probabilities_logistic_regression = logistic_regression_model.predict_proba(X_train)
# y_predicted_train_logistic_regression = logistic_regression_model.predict(X_train)

## hist gradient boosting machines
hist_gradient_boosting_machine_model = HistGradientBoostingClassifier(
    class_weight='balanced', # prevents disproporionate predictions
    l2_regularization=100.0, # less overfitting, but still overfits
    max_depth=10, # negligible performance difference
    min_samples_leaf=100 # negligible performance difference
    # ,random_state=42
    )
hist_gradient_boosting_machine_model.fit(X_train, y_train)
y_predicted_test_class_probabilities_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict_proba(X_test)
y_predicted_test_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict(X_test)
y_predicted_train_class_probabilities_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict_proba(X_train)
y_predicted_train_hist_gradient_boosting_machine = hist_gradient_boosting_machine_model.predict(X_train)

## most frequent baseline model
most_frequent_model = DummyClassifier(strategy='most_frequent')
most_frequent_model.fit(X_train, y_train)
y_predicted_class_probabilities_most_frequent = most_frequent_model.predict_proba(X_test)
y_predicted_most_frequent = most_frequent_model.predict(X_test)

# proportions
college_major_categories = dataset['major_category'].unique()

y_predicted = [y_predicted_test_hist_gradient_boosting_machine, y_predicted_train_hist_gradient_boosting_machine]
y_actual = [y_test, y_train]
for i in range(len(y_predicted)):
    predicted_college_major_counts = defaultdict(int)
    for pred in y_predicted[i]:
        predicted_college_major_counts[int(pred)] += 1

    test_college_major_category_counts = defaultdict(int)

    for college_major_category in y_actual[i]:
        test_college_major_category_counts[int(college_major_category)] += 1

    print("\n# PROPORTIONS")
    print("CATEGORY    PREDICTED    ACTUAL")
    sum_of_squared_differences = 0.0
    for j in range(len(college_major_categories)):
        actual_proportion = round((test_college_major_category_counts[j] / len(y_actual[i])) * 100, 1)
        pred_proportion = round((predicted_college_major_counts[j] / len(y_actual[i])) * 100, 1)
        sum_of_squared_differences += (actual_proportion - pred_proportion)**2
        print(college_major_categories[j] + " " + str(pred_proportion) + "%     " + str(actual_proportion) + "%")

    print("\nSum of Squared Differences: " + str(round(sum_of_squared_differences, 2)))


print("\n# EVALUATION")
# print_top_k_accuracy(y_test, "Logistic Regression", number_of_top_k, "test", y_predicted_test_class_probabilities_logistic_regression)
# print_top_k_accuracy(y_train, "Logistic Regression", number_of_top_k, "train", y_predicted_train_class_probabilities_logistic_regression)
print_top_k_accuracy(y_test, "Hist Gradient Boosting Machines", number_of_top_k, "test", y_predicted_test_class_probabilities_hist_gradient_boosting_machine)
print_top_k_accuracy(y_train, "Hist Gradient Boosting Machines", number_of_top_k, "train", y_predicted_train_class_probabilities_hist_gradient_boosting_machine)
print_top_k_accuracy(y_test, "Most Frequent", number_of_top_k, "test", y_predicted_class_probabilities_most_frequent)
# print_top_1_accuracy(y_test, "Logistic Regression", "test", y_predicted_test_logistic_regression)
# print_top_1_accuracy(y_train, "Logistic Regression", "train", y_predicted_train_logistic_regression)
print_top_1_accuracy(y_test, "Hist Gradient Boosting Machine", "test", y_predicted_test_hist_gradient_boosting_machine)
print_top_1_accuracy(y_train, "Hist Gradient Boosting Machine", "train", y_predicted_train_hist_gradient_boosting_machine)
print_top_1_accuracy(y_test, "Most Frequent", "test", y_predicted_most_frequent)

# at least with Log Reg model, it seems to perform better with 0-4 likert
# 0-2 LIKERT SCALE
# Logistic Regression Test Accuracy:        0.629
# Logistic Regression Test Accuracy:        0.633

# at least with Log Reg model, it seems to perform better with no education filter
# NO EDUCATION FILTER
# Logistic Regression Top-3 Test Accuracy:        0.645
# Logistic Regression Top-1 Test Accuracy:        0.37

# at least with Log Reg model, it seems to perform better with no substring match
# no substring match
# Logistic Regression Top-3 Test Accuracy:        0.66
# Logistic Regression Top-1 Test Accuracy:        0.379


# HGBM
# # PROPORTIONS - TEST
# Sum of Squared Differences: 229.2

# # PROPORTIONS - TRAIN
# Sum of Squared Differences: 231.03

# # EVALUATION
# 0.56 - Hist Gradient Boosting Machines Top-3 test Accuracy
# 0.694 - Hist Gradient Boosting Machines Top-3 train Accuracy
# 0.285 - Hist Gradient Boosting Machine Top-1 test Accuracy
# 0.421 - Hist Gradient Boosting Machine Top-1 train Accuracy


# LOGISTIC REGRESSION
# # PROPORTIONS - TEST
# Sum of Squared Differences: 348.63

# # PROPORTIONS - TRAIN
# # Sum of Squared Differences: 341.07

# # EVALUATION
# 0.536 - Logistic Regression Top-3 test Accuracy
# 0.548 - Logistic Regression Top-3 train Accuracy
# 0.265 - Logistic Regression Top-1 test Accuracy
# 0.274 - Logistic Regression Top-1 train Accuracy

