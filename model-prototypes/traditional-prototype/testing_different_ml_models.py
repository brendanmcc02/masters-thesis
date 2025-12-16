import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import top_k_accuracy_score, accuracy_score
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from collections import defaultdict

def print_top_k_accuracy_metric(y_actual, model_name, number_of_top_k, train_or_test_label, y_predicted_class_probabilities):
    print(str(round(top_k_accuracy_score(y_actual, y_predicted_class_probabilities, k=number_of_top_k), 3)) + " - " + model_name + " Top-" + str(number_of_top_k) + " " + train_or_test_label + " Accuracy")

def print_top_1_accuracy_metric(y_actual, model_name, train_or_test_label, y_predicted):
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
    X, y, test_size=0.2, stratify=y, random_state=42
)

## hist gradient boosting machines (HGBM)
# testing the following hyperparameters with different configuration, and it resulted in neglibile improvements:
# * max_iter
# * max_depth
# * min_samples_leaf
# a note on `max_leaf_nodes=None`:
# * it overfits like crazy (~0.9 top-3 train set performance), BUT
# * significant improvement on top-3 unseen test set performance (~+0.04)
# * AND significant reduction in sum of squared differences (~30.0 vs ~250 previously)
#   * this might seem like an improvement,
#   * BUT it puts more bias towards psych & business (combined ~40% of the dataset)
#   * see metrics for `default` and `None` hyperparameter values for `max_leaf_nodes`
# max_leaf_nodes=default:
# ```
# major_category            PREDICTED   ACTUAL
# business                  11.8%       16.4%
# psychology & social work  11.6%       22.8%
# Sum of Squared Differences: 234.57

# 0.568 - Hist Gradient Boosting Machines Top-3 test Accuracy
# 0.682 - Hist Gradient Boosting Machines Top-3 train Accuracy
# 0.288 - Hist Gradient Boosting Machine Top-1 test Accuracy
# 0.409 - Hist Gradient Boosting Machine Top-1 train Accuracy
# ```
# max_leaf_nodes=None:
# ```
# major_category            PREDICTED   ACTUAL
# business                  17.9%       16.4%
# psychology & social work  19.5%       22.8%
# Sum of Squared Differences: 34.24

# 0.606 - Hist Gradient Boosting Machines Top-3 test Accuracy
# 0.952 - Hist Gradient Boosting Machines Top-3 train Accuracy
# 0.319 - Hist Gradient Boosting Machine Top-1 test Accuracy
# 0.875 - Hist Gradient Boosting Machine Top-1 train Accuracy
# ```
hist_gradient_boosting_machines_model = HistGradientBoostingClassifier(
    class_weight='balanced', # prevents disproporionate predictions
    l2_regularization=1.0, # less overfitting & improves performance. still overfits on the whole.
    # max_leaf_nodes=None, # see notes above
    random_state=42
    )
hist_gradient_boosting_machines_model.fit(X_train, y_train)
y_predicted_test_class_probabilities_hist_gradient_boosting_machines = hist_gradient_boosting_machines_model.predict_proba(X_test)
y_predicted_test_hist_gradient_boosting_machines = hist_gradient_boosting_machines_model.predict(X_test)
y_predicted_train_class_probabilities_hist_gradient_boosting_machines = hist_gradient_boosting_machines_model.predict_proba(X_train)
y_predicted_train_hist_gradient_boosting_machines = hist_gradient_boosting_machines_model.predict(X_train)

## most frequent baseline model
most_frequent_baseline_model = DummyClassifier(strategy='most_frequent')
most_frequent_baseline_model.fit(X_train, y_train)
y_predicted_class_probabilities_most_frequent = most_frequent_baseline_model.predict_proba(X_test)
y_predicted_most_frequent = most_frequent_baseline_model.predict(X_test)

# proportions
print("\n# EVALUATION")
college_major_categories = dataset['major_category'].unique()

predicted_college_major_counts = defaultdict(int)
for pred in y_predicted_test_hist_gradient_boosting_machines:
    predicted_college_major_counts[int(pred)] += 1

test_college_major_category_counts = defaultdict(int)

for college_major_category in y_test:
    test_college_major_category_counts[int(college_major_category)] += 1

print("\n## PROPORTIONS")
print("CATEGORY    PREDICTED    ACTUAL")
sum_of_squared_differences = 0.0
for j in range(len(college_major_categories)):
    actual_proportion = round((test_college_major_category_counts[j] / len(y_test)) * 100, 1)
    pred_proportion = round((predicted_college_major_counts[j] / len(y_test)) * 100, 1)
    sum_of_squared_differences += (actual_proportion - pred_proportion)**2
    print(college_major_categories[j] + " " + str(pred_proportion) + "%     " + str(actual_proportion) + "%")

print("\nSum of Squared Differences: " + str(round(sum_of_squared_differences, 2)))

print("\n## ACCURACY METRICS")
print_top_k_accuracy_metric(y_test, "Hist Gradient Boosting Machines", number_of_top_k, "test", y_predicted_test_class_probabilities_hist_gradient_boosting_machines)
print_top_k_accuracy_metric(y_train, "Hist Gradient Boosting Machines", number_of_top_k, "train", y_predicted_train_class_probabilities_hist_gradient_boosting_machines)
# print_top_k_accuracy_metric(y_test, "Most Frequent Baseline", number_of_top_k, "test", y_predicted_class_probabilities_most_frequent)
print_top_1_accuracy_metric(y_test, "Hist Gradient Boosting Machines", "test", y_predicted_test_hist_gradient_boosting_machines)
print_top_1_accuracy_metric(y_train, "Hist Gradient Boosting Machines", "train", y_predicted_train_hist_gradient_boosting_machines)
# print_top_1_accuracy_metric(y_test, "Most Frequent Baseline", "test", y_predicted_most_frequent)

# 0-2 LIKERT SCALE (0-4 has better performance)
# 0.629 - Logistic Regression Test Accuracy
# 0.633 - Logistic Regression Test Accuracy
# 0.566 - Hist Gradient Boosting Machines Top-3 test Accuracy
# 0.937 - Hist Gradient Boosting Machines Top-3 train Accuracy
# 0.281 - Hist Gradient Boosting Machine Top-1 test Accuracy
# 0.831 - Hist Gradient Boosting Machine Top-1 train Accuracy

# NO EDUCATION FILTER (better performance with no education filter)
# 0.645 - Logistic Regression Top-3 Test Accuracy
# 0.37  - Logistic Regression Top-1 Test Accuracy
# 0.566 - Hist Gradient Boosting Machines Top-3 test Accuracy
# 0.937 - Hist Gradient Boosting Machines Top-3 train Accuracy
# 0.281 - Hist Gradient Boosting Machine Top-1 test Accuracy
# 0.831 - Hist Gradient Boosting Machine Top-1 train Accuracy


# at least with Log Reg model, it seems to perform better with no substring match
# no substring match
# Logistic Regression Top-3 Test Accuracy:        0.66
# Logistic Regression Top-1 Test Accuracy:        0.379


# HGBM - max_leaf_nodes=None, l2_regularization=1.0, class_weight='balanced'
# Sum of Squared Differences (test): 34.24
# Sum of Squared Differences (train): 16.41

# 0.606 - Hist Gradient Boosting Machines Top-3 test Accuracy
# 0.952 - Hist Gradient Boosting Machines Top-3 train Accuracy
# 0.319 - Hist Gradient Boosting Machine Top-1 test Accuracy
# 0.875 - Hist Gradient Boosting Machine Top-1 train Accuracy

