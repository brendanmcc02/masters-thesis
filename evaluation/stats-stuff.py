import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

file_path = "../college-course-recommender-system/user-evaluation-metrics.tsv" 
df = pd.read_csv(file_path, sep='\t')


# fig, axes = plt.subplots(2, 4, figsize=(20, 10))
# axes = axes.flatten()

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


metrics = ["Diversity", "Trust", "Precision", "Serendipity"]
results = []

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
        "shapiro-wilk p-value": shapiro_p,
        "T-test/wilcoxon P-value": round(p_value, 4),
        "Cohen's d": round(cohen_d, 2),
        "Effect Size": "Large" if abs(cohen_d) >= 0.8 else "Medium" if abs(cohen_d) >= 0.5 else "Small"
    })

# Convert to DataFrame for a clean summary table
results_df = pd.DataFrame(results)

# Export for your thesis appendix
results_df.to_csv("statistical_results.csv", index=False)

# visualise cohen effect
df_plot = results_df.copy()

# 2. Assign colors based on sign (Blue for positive, Red for negative)
df_plot['color'] = ['#3498db' if x >= 0 else '#e74c3c' for x in df_plot["Cohen's d"]]

plt.figure(figsize=(10, 6))

# 3. Create the bar chart
bars = plt.bar(df_plot["Metric"], df_plot["Cohen's d"], color=df_plot['color'])

for i, bar in enumerate(bars):
    yval = bar.get_height()
    # Determine vertical offset: positive values go up, negative go down
    offset = 0.05 if yval >= 0 else -0.05
    va = 'bottom' if yval >= 0 else 'top'
    
    plt.text(bar.get_x() + bar.get_width()/2, yval + offset, 
             f'd = {yval:.2f}', 
             ha='center', va=va, fontweight='bold', fontsize=10)

# 4. Add threshold lines and annotations
# Cohen's standard thresholds: 0.2 (Small), 0.5 (Medium), 0.8 (Large)
thresholds = [0.2, 0.5, 0.8]
labels = ["Small", "Medium", "Large"]

for t, label in zip(thresholds, labels):
    # Positive thresholds
    plt.axhline(y=t, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    plt.text(len(metrics)-0.4, t + 0.02, label, color='gray', fontsize=9, fontweight='bold')

# 5. Final Styling
plt.axhline(0, color='black', linewidth=1.2) # Baseline at zero
plt.ylabel("Cohen's d (Effect Size)")
plt.title("Cohen's d Effect Size across Evaluation Metrics", fontweight='bold', pad=20)
plt.grid(axis='y', linestyle=':', alpha=0.3)

# Adjust y-limit to ensure all labels and bars are visible
max_val = max(abs(df_plot["Cohen's d"]).max(), 0.9)
plt.ylim(0, max_val + 0.2)

plt.tight_layout()
plt.show()