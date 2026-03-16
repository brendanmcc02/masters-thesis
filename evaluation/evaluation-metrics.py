import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

eval_metrics = pd.read_csv("../college-course-recommender-system/user-evaluation-metrics.tsv", sep='\t')

data = {
    "Actual Diversity Mean": round(eval_metrics["Actual Diversity"].mean(), 2),
    "Baseline Diversity Mean": round(eval_metrics["Baseline Diversity"].mean(), 2),
    "Actual Trust Mean": round(eval_metrics["Actual Trust"].mean(), 2),
    "Baseline Trust Mean": round(eval_metrics["Baseline Trust"].mean(), 2),
    "Actual Precision Mean": round(eval_metrics["Actual Precision"].mean(), 2),
    "Baseline Precision Mean": round(eval_metrics["Baseline Precision"].mean(), 2),
    "Actual Recall Mean": round(eval_metrics["Actual Recall"].mean(), 2),
    "Baseline Recall Mean": round(eval_metrics["Baseline Recall"].mean(), 2),
    "Actual F1 Mean" : round(eval_metrics["Actual F1 Score"].mean(), 2),
    "Baseline F1 Mean" : round(eval_metrics["Baseline F1 Score"].mean(), 2),
    "Actual Novelty Mean": round(eval_metrics["Actual Novelty"].mean(), 2),
    "Baseline Novelty Mean": round(eval_metrics["Baseline Novelty"].mean(), 2),
    "Actual Serendipity Mean": round(eval_metrics["Actual Serendipity"].mean(), 2),
    "Baseline Serendipity Mean": round(eval_metrics["Baseline Serendipity"].mean(), 2)
}

# 1. Objective Metrics (Y-axis 0 to 1)
objective_metrics = ['Precision', 'Recall', 'F1 Score', 'Novelty', 'Serendipity']
actual_obj = [data["Actual Precision Mean"], data["Actual Recall Mean"], data["Actual F1 Mean"], data["Actual Novelty Mean"], data["Actual Serendipity Mean"]]
baseline_obj = [data["Baseline Precision Mean"], data["Baseline Recall Mean"], data["Baseline F1 Mean"], data["Baseline Novelty Mean"], data["Baseline Serendipity Mean"]]

# 2. User-Perceived Metrics (Y-axis 1 to 5)
user_metrics = ['Diversity', 'Trust']
actual_user = [data["Actual Diversity Mean"], data["Actual Trust Mean"]]
baseline_user = [data["Baseline Diversity Mean"], data["Baseline Trust Mean"]]

# Style settings
width = 0.35
blue_color = '#3498db'
red_color = '#e74c3c'

fig1, ax1 = plt.subplots(figsize=(8, 6))
x1 = np.arange(len(objective_metrics))
ax1.bar(x1 - width/2, actual_obj, width, label='Actual', color=blue_color)
ax1.bar(x1 + width/2, baseline_obj, width, label='Baseline', color=red_color)
ax1.set_title('Objective Metrics Comparison', fontweight='bold', pad=15)
ax1.set_ylim(0, 1)
ax1.set_xticks(x1)
ax1.set_xticklabels(objective_metrics)
ax1.set_xlabel("Objective Metrics")
ax1.set_ylabel("Metric Score")
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('objective_metrics_plot.png')

fig2, ax2 = plt.subplots(figsize=(6, 6))
x2 = np.arange(len(user_metrics))
ax2.bar(x2 - width/2, actual_user, width, label='Actual', color=blue_color)
ax2.bar(x2 + width/2, baseline_user, width, label='Baseline', color=red_color)
ax2.set_title('User-Perceived Metrics Comparison', fontweight='bold', pad=15)
ax2.set_ylim(1, 5)
ax2.set_xticks(x2)
ax2.set_xticklabels(user_metrics)
ax2.set_xlabel("User-perceived Metrics")
ax2.set_ylabel("Metric Score")
ax2.legend()
ax2.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('user_perceived_metrics_plot.png')