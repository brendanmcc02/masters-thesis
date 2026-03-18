import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

file_path = "../college-course-recommender-system/user-evaluation-metrics.tsv" 
df = pd.read_csv(file_path, sep='\t')

metrics = ["Diversity", "Trust", "Precision", "Recall", "F1 Score", "Novelty", "Serendipity"]
results = []

fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()

# for i, metric in enumerate(metrics):
#     difference = df[f"Actual {metric}"] - df[f"Baseline {metric}"]
    
#     # Plot histogram and KDE (Kernel Density Estimate)
#     sns.histplot(difference, kde=True, ax=axes[i], color='skyblue', stat="density")
    
#     # Overlay a perfect normal distribution curve for comparison
#     mu, std = difference.mean(), difference.std()
#     x = np.linspace(difference.min(), difference.max(), 100)
#     p = stats.norm.pdf(x, mu, std)
#     axes[i].plot(x, p, 'r', linewidth=2, label='Normal Curve')
    
#     axes[i].set_title(f"{metric} Differences")
#     axes[i].legend()


# plt.show()
for m in metrics:
    # Extract columns based on your naming convention
    actual = df[f"Actual {m}"]
    baseline = df[f"Baseline {m}"]
    differences = actual - baseline
    
    # 1. Shapiro-Wilk Test for Normality
    _, shapiro_p = stats.shapiro(differences)

    if shapiro_p >= 0.05:
        _, p_value = stats.ttest_rel(actual, baseline)
    else:
        _, p_value = stats.wilcoxon(actual, baseline)

    # 4. Cohen's d (Effect Size)
    cohen_d = np.mean(differences) / np.std(differences, ddof=1)
    
    results.append({
        "Metric": m,
        "is normally distributed?": shapiro_p >= 0.05,
        "T-test/wilcoxon P-value": round(p_value, 4),
        "Cohen's d": round(cohen_d, 2),
        "Effect Size": "Large" if abs(cohen_d) >= 0.8 else "Medium" if abs(cohen_d) >= 0.5 else "Small"
    })

# Convert to DataFrame for a clean summary table
results_df = pd.DataFrame(results)
print(results_df)

# Export for your thesis appendix
results_df.to_csv("statistical_results.csv", index=False)