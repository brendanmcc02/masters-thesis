import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

file_path = "../college-course-recommender-system/user-evaluation-metrics.tsv" 
df = pd.read_csv(file_path, sep='\t')

columns_to_drop = ["Actual Recall", "Baseline Recall", "Actual Recall", "Baseline Recall", "Actual F1 Score", "Baseline F1 Score", "Actual Novelty", "Baseline Novelty", "Feedback", "Timestamp Part 1", "Timestamp Part 2"]
filtered_df = df.drop(columns=columns_to_drop)
filtered_df.to_csv("filtered-eval-metrics.tsv")

# metrics = ["Diversity", "Trust", "Precision", "Serendipity"]
# results = []

# for m in metrics:
#     # Extract columns based on your naming convention
#     actual = df[f"Actual {m}"]
#     baseline = df[f"Baseline {m}"]
#     differences = actual - baseline
    
#     # 1. Shapiro-Wilk Test for Normality
#     _, shapiro_p = stats.shapiro(differences)

#     if shapiro_p >= 0.05:
#         _, p_value = stats.ttest_rel(actual, baseline)
#         effect_size = np.mean(differences) / np.std(differences, ddof=1)
#     else:
#         _, p_value = stats.wilcoxon(actual, baseline)
        
#         # Calculate Matched-Pairs Rank Biserial Correlation (r_rb)
#         # 1. Get the absolute differences and exclude zeros (standard for Wilcoxon)
#         differences = differences[differences != 0]
        
#         if len(differences) == 0:
#             effect_size = 0.0
#         else:
#             # 2. Rank the absolute differences
#             ranks = stats.rankdata(np.abs(differences))
            
#             # 3. Sum the ranks for positive and negative differences
#             pos_ranks = np.sum(ranks[differences > 0])
#             neg_ranks = np.sum(ranks[differences < 0])
#             total_ranks = pos_ranks + neg_ranks
            
#             # 4. Calculate r_rb
#             effect_size = (pos_ranks - neg_ranks) / total_ranks

#     results.append({
#         "Metric": m,
#         "is normally distributed?": shapiro_p >= 0.05,
#         "shapiro-wilk p-value": shapiro_p,
#         "T-test/wilcoxon P-value": round(p_value, 4),
#         "effect_size": round(effect_size, 2),
#     })

# # Convert to DataFrame for a clean summary table
# results_df = pd.DataFrame(results)

# # Export for your thesis appendix
# results_df.to_csv("statistical_results.csv", index=False)

# # visualise cohen effect
# df_plot = results_df[results_df["is normally distributed?"] == True].copy()

# # 2. Assign colors based on sign (Blue for positive, Red for negative)
# df_plot['color'] = ['#3498db' if x >= 0 else '#e74c3c' for x in df_plot["effect_size"]]

# plt.figure(figsize=(10, 6))

# # 3. Create the bar chart
# bars = plt.bar(df_plot["Metric"], df_plot["effect_size"], color=df_plot['color'])

# for i, bar in enumerate(bars):
#     yval = bar.get_height()
#     # Determine vertical offset: positive values go up, negative go down
#     offset = 0.05 if yval >= 0 else -0.05
#     va = 'bottom' if yval >= 0 else 'top'
    
#     plt.text(bar.get_x() + bar.get_width()/2, yval + offset, 
#              f'd = {yval:.2f}', 
#              ha='center', va=va, fontweight='bold', fontsize=10)

# # 4. Add threshold lines and annotations
# # Cohen's standard thresholds: 0.2 (Small), 0.5 (Medium), 0.8 (Large)
# thresholds = [0.2, 0.5, 0.8]
# labels = ["Small", "Medium", "Large"]

# for t, label in zip(thresholds, labels):
#     # Positive thresholds
#     plt.axhline(y=t, color='gray', linestyle='--', linewidth=1, alpha=0.6)
#     plt.text(len(metrics)-1-0.4, t + 0.02, label, color='gray', fontsize=9, fontweight='bold')

# # 5. Final Styling
# plt.axhline(0, color='black', linewidth=1.2) # Baseline at zero
# plt.ylabel("Cohen's d (Effect Size)")
# plt.title("Cohen's d Effect Size across Normally Distributed Evaluation Metrics", fontweight='bold', pad=20)
# plt.grid(axis='y', linestyle=':', alpha=0.3)

# # Adjust y-limit to ensure all labels and bars are visible
# max_val = max(abs(df_plot["effect_size"]).max(), 0.9)
# plt.ylim(0, max_val + 0.2)

# plt.tight_layout()
# plt.show()