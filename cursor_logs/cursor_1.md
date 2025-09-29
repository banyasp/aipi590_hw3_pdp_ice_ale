# Preliminary exploratory data analysis
_Exported on 9/29/2025 at 11:25:54 EDT from Cursor (1.7.12)_

---

**User**

write code to do a preliminary exploratory analysis of the dataset. determine the amount of correlation between features.  

---

**Cursor**

I'll help you create a preliminary exploratory analysis of the dataset with correlation analysis. Let me first examine the current notebook and understand what dataset we're working with.

I can see you're working with the advertising dataset and need to perform preliminary exploratory analysis in your notebook. Looking at cell 8, I'll add comprehensive exploratory analysis code that includes correlation analysis between features.

```plaintext
# here

->

import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

print("📊 PRELIMINARY EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# Load the raw dataset for exploration
df = pd.read_csv('../advertising.csv')

print("\n🔍 DATASET OVERVIEW")
print("-" * 30)
print(f"Dataset Shape: {df.shape}")
print(f"Features: {list(df.columns)}")
print(f"Data Types:\n{df.dtypes}")
print(f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

# Check for missing values
print(f"\n🚫 MISSING VALUES")
print("-" * 20)
missing_counts = df.isnull().sum()
missing_percentages = (missing_counts / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing_counts,
    'Missing Percentage': missing_percentages
})
print(missing_df[missing_df['Missing Count'] > 0])
if missing_df['Missing Count'].sum() == 0:
    print("✅ No missing values found!")

# Basic statistical summary
print(f"\n📈 DESCRIPTIVE STATISTICS")
print("-" * 30)
print(df.describe().round(2))

# Check for potential outliers using IQR method
print(f"\n🎯 OUTLIER DETECTION (IQR Method)")
print("-" * 40)
outlier_summary = []
for col in df.columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary.append({
        'Feature': col,
        'Outliers': len(outliers),
        'Percentage': f"{(len(outliers)/len(df))*100:.1f}%",
        'Range': f"[{df[col].min():.1f}, {df[col].max():.1f}]"
    })

outlier_df = pd.DataFrame(outlier_summary)
print(outlier_df)

# Distribution Analysis
print(f"\n📊 DISTRIBUTION VISUALIZATION")
print("-" * 35)

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Distribution Analysis of Features', fontsize=16, fontweight='bold')

# Plot distributions
for i, column in enumerate(df.columns):
    row = i // 2
    col = i % 2
    
    # Histogram with KDE
    axes[row, col].hist(df[column], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[row, col].axvline(df[column].mean(), color='red', linestyle='--', 
                          label=f'Mean: {df[column].mean():.2f}')
    axes[row, col].axvline(df[column].median(), color='green', linestyle='--', 
                          label=f'Median: {df[column].median():.2f}')
    axes[row, col].set_title(f'{column} Distribution')
    axes[row, col].set_xlabel(column)
    axes[row, col].set_ylabel('Frequency')
    axes[row, col].legend()
    axes[row, col].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Correlation Analysis - The Key Focus
print(f"\n🔗 CORRELATION ANALYSIS")
print("=" * 40)

# Calculate different types of correlations
pearson_corr = df.corr(method='pearson')
spearman_corr = df.corr(method='spearman')

print("📊 PEARSON CORRELATION MATRIX")
print("-" * 35)
print(pearson_corr.round(3))

print(f"\n📊 SPEARMAN CORRELATION MATRIX")
print("-" * 35)
print(spearman_corr.round(3))

# Correlation interpretation function
def interpret_correlation(r):
    r_abs = abs(r)
    if r_abs >= 0.8:
        strength = "Very Strong"
    elif r_abs >= 0.6:
        strength = "Strong"
    elif r_abs >= 0.4:
        strength = "Moderate"
    elif r_abs >= 0.2:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    direction = "Positive" if r >= 0 else "Negative"
    return f"{direction} {strength}"

# Detailed correlation analysis
print(f"\n🔍 DETAILED CORRELATION ANALYSIS")
print("-" * 45)

feature_pairs = []
for i in range(len(df.columns)):
    for j in range(i+1, len(df.columns)):
        col1, col2 = df.columns[i], df.columns[j]
        pearson_r = pearson_corr.loc[col1, col2]
        spearman_r = spearman_corr.loc[col1, col2]
        
        feature_pairs.append({
            'Feature Pair': f"{col1} vs {col2}",
            'Pearson r': round(pearson_r, 3),
            'Pearson Interpretation': interpret_correlation(pearson_r),
            'Spearman r': round(spearman_r, 3),
            'Spearman Interpretation': interpret_correlation(spearman_r)
        })

correlation_summary = pd.DataFrame(feature_pairs)
print(correlation_summary.to_string(index=False))

# Visual correlation analysis
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Pearson correlation heatmap
sns.heatmap(pearson_corr, annot=True, cmap='RdBu_r', center=0, 
            square=True, fmt='.3f', cbar_kws={'label': 'Correlation Coefficient'},
            ax=axes[0])
axes[0].set_title('Pearson Correlation Heatmap', fontsize=14, fontweight='bold')

# Spearman correlation heatmap  
sns.heatmap(spearman_corr, annot=True, cmap='RdBu_r', center=0,
            square=True, fmt='.3f', cbar_kws={'label': 'Correlation Coefficient'},
            ax=axes[1])
axes[1].set_title('Spearman Correlation Heatmap', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

# Pairwise scatter plots
print(f"\n📈 PAIRWISE RELATIONSHIP VISUALIZATION")
print("-" * 45)

# Create pair plot
fig = plt.figure(figsize=(12, 10))
fig.suptitle('Pairwise Feature Relationships', fontsize=16, fontweight='bold')

# Create scatter plots for all feature combinations
feature_names = df.columns
n_features = len(feature_names)

for i in range(n_features):
    for j in range(n_features):
        plt.subplot(n_features, n_features, i * n_features + j + 1)
        
        if i == j:
            # Diagonal: histogram
            plt.hist(df[feature_names[i]], bins=15, alpha=0.7, color='lightblue')
            plt.title(f'{feature_names[i]}')
        else:
            # Off-diagonal: scatter plot
            plt.scatter(df[feature_names[j]], df[feature_names[i]], alpha=0.6)
            
            # Add correlation coefficient
            corr = pearson_corr.loc[feature_names[i], feature_names[j]]
            plt.text(0.05, 0.95, f'r={corr:.3f}', transform=plt.gca().transAxes,
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.xlabel(feature_names[j])
            plt.ylabel(feature_names[i])

plt.tight_layout()
plt.show()

# Feature importance for target variable (Sales)
print(f"\n🎯 FEATURE IMPORTANCE FOR TARGET (SALES)")
print("-" * 50)

target_correlations = pearson_corr['Sales'].drop('Sales').sort_values(key=abs, ascending=False)
print("Features ranked by correlation with Sales:")
for feature, corr in target_correlations.items():
    print(f"  • {feature:<12}: {corr:>6.3f} ({interpret_correlation(corr)})")

# Summary insights
print(f"\n💡 KEY INSIGHTS")
print("=" * 30)

# Find highest correlation pairs (excluding self-correlation)
corr_values = []
for i in range(len(pearson_corr.columns)):
    for j in range(i+1, len(pearson_corr.columns)):
        corr_values.append((
            pearson_corr.columns[i], 
            pearson_corr.columns[j], 
            abs(pearson_corr.iloc[i, j])
        ))

corr_values.sort(key=lambda x: x[2], reverse=True)

print(f"🔴 Highest correlation between features:")
top_corr = corr_values[0]
if 'Sales' not in [top_corr[0], top_corr[1]]:  # Feature-feature correlation
    print(f"   {top_corr[0]} ↔ {top_corr[1]}: {pearson_corr.loc[top_corr[0], top_corr[1]]:.3f}")
    if abs(pearson_corr.loc[top_corr[0], top_corr[1]]) > 0.7:
        print("   ⚠️  HIGH CORRELATION: May cause multicollinearity issues")
    elif abs(pearson_corr.loc[top_corr[0], top_corr[1]]) > 0.4:
        print("   ⚡ MODERATE CORRELATION: Monitor for potential interactions")

print(f"\n🎯 Best predictor of Sales: {target_correlations.index[0]} (r={target_correlations.iloc[0]:.3f})")
print(f"🎯 Weakest predictor of Sales: {target_correlations.index[-1]} (r={target_correlations.iloc[-1]:.3f})")

# Check for potential multicollinearity
print(f"\n⚠️  MULTICOLLINEARITY CHECK")
print("-" * 35)
high_corr_pairs = [(name1, name2, corr) for name1, name2, corr in corr_values 
                   if corr > 0.7 and 'Sales' not in [name1, name2]]

if high_corr_pairs:
    print("High correlation pairs found (|r| > 0.7):")
    for name1, name2, corr in high_corr_pairs:
        actual_corr = pearson_corr.loc[name1, name2]
        print(f"  • {name1} ↔ {name2}: {actual_corr:.3f}")
    print("  💡 Consider feature selection or regularization techniques")
else:
    print("✅ No high multicollinearity detected between features")

print(f"\n🏁 Exploratory Analysis Complete!")
print("Ready to proceed with PDP, ICE, and ALE analysis...")
```

Perfect! I've added comprehensive exploratory analysis code to your notebook that will thoroughly examine the advertising dataset and determine correlations between features. The code includes:

## 🔍 **Key Analysis Components Added:**

1. **Dataset Overview** - Basic information about shape, data types, and memory usage
2. **Data Quality Check** - Missing values and outlier detection using IQR method
3. **Descriptive Statistics** - Summary statistics for all features
4. **Distribution Analysis** - Histograms showing the distribution of each feature with mean/median lines

## 🔗 **Correlation Analysis (Main Focus):**
- **Pearson & Spearman correlation matrices** - Different correlation methods to capture linear and non-linear relationships
- **Detailed correlation interpretation** - Automatic classification of correlation strength (Very Strong, Strong, Moderate, Weak, Very Weak)
- **Visual correlation heatmaps** - Side-by-side comparison of Pearson and Spearman correlations
- **Pairwise scatter plots** - Visual representation of all feature relationships with correlation coefficients
- **Feature ranking** - Features ordered by correlation with the target variable (Sales)
- **Multicollinearity check** - Identifies potential issues with highly correlated features

## 💡 **Key Insights Generated:**
- Identifies the strongest predictor of Sales
- Highlights potential multicollinearity issues
- Provides actionable recommendations for model building
- Prepares the foundation for understanding PDP/ICE/ALE plot results

The analysis will help you understand how features relate to each other and to the target variable, which is crucial for interpreting the explainability plots (PDP, ICE, ALE) that follow in your notebook. This correlation analysis will particularly help explain any differences you see between PDP and ALE plots, as ALE plots handle feature correlations differently than PDP plots.

Run this cell to get a complete picture of your dataset's structure and feature relationships! [[memory:8851887]]

---

**User**

put that code in a seperate python file that can be called by a function in the notebook. here was your code: 

---

**Cursor**

I'll create a separate Python file for the exploratory analysis code and then update the notebook to call it as a function. This is great for code organization!

```python
"""
Exploratory Data Analysis Module for Advertising Dataset
========================================================

This module provides comprehensive exploratory analysis functionality
including correlation analysis, distribution visualization, and data quality checks.

Author: Generated for AIPI 590 XAI Assignment
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')


def run_exploratory_analysis(data_path='../advertising.csv', show_plots=True):
    """
    Perform comprehensive exploratory data analysis on the advertising dataset.
    
    Parameters:
    -----------
    data_path : str, optional
        Path to the CSV data file (default: '../advertising.csv')
    show_plots : bool, optional
        Whether to display plots (default: True)
    
    Returns:
    --------
    dict : Dictionary containing analysis results including:
        - 'dataset': The loaded DataFrame
        - 'correlations': Dictionary with Pearson and Spearman correlation matrices
        - 'target_correlations': Series of feature correlations with target variable
        - 'outlier_summary': DataFrame with outlier information
        - 'summary_stats': DataFrame with descriptive statistics
        - 'insights': Dictionary with key findings
    """
    
    print("📊 PRELIMINARY EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    
    # Load the raw dataset for exploration
    df = pd.read_csv(data_path)
    
    print("\n🔍 DATASET OVERVIEW")
    print("-" * 30)
    print(f"Dataset Shape: {df.shape}")
    print(f"Features: {list(df.columns)}")
    print(f"Data Types:\n{df.dtypes}")
    print(f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # Check for missing values
    print(f"\n🚫 MISSING VALUES")
    print("-" * 20)
    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percentages
    })
    print(missing_df[missing_df['Missing Count'] > 0])
    if missing_df['Missing Count'].sum() == 0:
        print("✅ No missing values found!")
    
    # Basic statistical summary
    print(f"\n📈 DESCRIPTIVE STATISTICS")
    print("-" * 30)
    summary_stats = df.describe().round(2)
    print(summary_stats)
    
    # Check for potential outliers using IQR method
    print(f"\n🎯 OUTLIER DETECTION (IQR Method)")
    print("-" * 40)
    outlier_summary = []
    for col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_summary.append({
            'Feature': col,
            'Outliers': len(outliers),
            'Percentage': f"{(len(outliers)/len(df))*100:.1f}%",
            'Range': f"[{df[col].min():.1f}, {df[col].max():.1f}]"
        })
    
    outlier_df = pd.DataFrame(outlier_summary)
    print(outlier_df)
    
    # Distribution Analysis
    if show_plots:
        print(f"\n📊 DISTRIBUTION VISUALIZATION")
        print("-" * 35)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Distribution Analysis of Features', fontsize=16, fontweight='bold')
        
        # Plot distributions
        for i, column in enumerate(df.columns):
            row = i // 2
            col = i % 2
            
            # Histogram with KDE
            axes[row, col].hist(df[column], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            axes[row, col].axvline(df[column].mean(), color='red', linestyle='--', 
                                  label=f'Mean: {df[column].mean():.2f}')
            axes[row, col].axvline(df[column].median(), color='green', linestyle='--', 
                                  label=f'Median: {df[column].median():.2f}')
            axes[row, col].set_title(f'{column} Distribution')
            axes[row, col].set_xlabel(column)
            axes[row, col].set_ylabel('Frequency')
            axes[row, col].legend()
            axes[row, col].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    # Correlation Analysis - The Key Focus
    print(f"\n🔗 CORRELATION ANALYSIS")
    print("=" * 40)
    
    # Calculate different types of correlations
    pearson_corr = df.corr(method='pearson')
    spearman_corr = df.corr(method='spearman')
    
    print("📊 PEARSON CORRELATION MATRIX")
    print("-" * 35)
    print(pearson_corr.round(3))
    
    print(f"\n📊 SPEARMAN CORRELATION MATRIX")
    print("-" * 35)
    print(spearman_corr.round(3))
    
    # Correlation interpretation function
    def interpret_correlation(r):
        r_abs = abs(r)
        if r_abs >= 0.8:
            strength = "Very Strong"
        elif r_abs >= 0.6:
            strength = "Strong"
        elif r_abs >= 0.4:
            strength = "Moderate"
        elif r_abs >= 0.2:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        direction = "Positive" if r >= 0 else "Negative"
        return f"{direction} {strength}"
    
    # Detailed correlation analysis
    print(f"\n🔍 DETAILED CORRELATION ANALYSIS")
    print("-" * 45)
    
    feature_pairs = []
    for i in range(len(df.columns)):
        for j in range(i+1, len(df.columns)):
            col1, col2 = df.columns[i], df.columns[j]
            pearson_r = pearson_corr.loc[col1, col2]
            spearman_r = spearman_corr.loc[col1, col2]
            
            feature_pairs.append({
                'Feature Pair': f"{col1} vs {col2}",
                'Pearson r': round(pearson_r, 3),
                'Pearson Interpretation': interpret_correlation(pearson_r),
                'Spearman r': round(spearman_r, 3),
                'Spearman Interpretation': interpret_correlation(spearman_r)
            })
    
    correlation_summary = pd.DataFrame(feature_pairs)
    print(correlation_summary.to_string(index=False))
    
    # Visual correlation analysis
    if show_plots:
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Pearson correlation heatmap
        sns.heatmap(pearson_corr, annot=True, cmap='RdBu_r', center=0, 
                    square=True, fmt='.3f', cbar_kws={'label': 'Correlation Coefficient'},
                    ax=axes[0])
        axes[0].set_title('Pearson Correlation Heatmap', fontsize=14, fontweight='bold')
        
        # Spearman correlation heatmap  
        sns.heatmap(spearman_corr, annot=True, cmap='RdBu_r', center=0,
                    square=True, fmt='.3f', cbar_kws={'label': 'Correlation Coefficient'},
                    ax=axes[1])
        axes[1].set_title('Spearman Correlation Heatmap', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        # Pairwise scatter plots
        print(f"\n📈 PAIRWISE RELATIONSHIP VISUALIZATION")
        print("-" * 45)
        
        # Create pair plot
        fig = plt.figure(figsize=(12, 10))
        fig.suptitle('Pairwise Feature Relationships', fontsize=16, fontweight='bold')
        
        # Create scatter plots for all feature combinations
        feature_names = df.columns
        n_features = len(feature_names)
        
        for i in range(n_features):
            for j in range(n_features):
                plt.subplot(n_features, n_features, i * n_features + j + 1)
                
                if i == j:
                    # Diagonal: histogram
                    plt.hist(df[feature_names[i]], bins=15, alpha=0.7, color='lightblue')
                    plt.title(f'{feature_names[i]}')
                else:
                    # Off-diagonal: scatter plot
                    plt.scatter(df[feature_names[j]], df[feature_names[i]], alpha=0.6)
                    
                    # Add correlation coefficient
                    corr = pearson_corr.loc[feature_names[i], feature_names[j]]
                    plt.text(0.05, 0.95, f'r={corr:.3f}', transform=plt.gca().transAxes,
                            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                    
                    plt.xlabel(feature_names[j])
                    plt.ylabel(feature_names[i])
        
        plt.tight_layout()
        plt.show()
    
    # Feature importance for target variable (Sales)
    print(f"\n🎯 FEATURE IMPORTANCE FOR TARGET (SALES)")
    print("-" * 50)
    
    target_correlations = pearson_corr['Sales'].drop('Sales').sort_values(key=abs, ascending=False)
    print("Features ranked by correlation with Sales:")
    for feature, corr in target_correlations.items():
        print(f"  • {feature:<12}: {corr:>6.3f} ({interpret_correlation(corr)})")
    
    # Summary insights
    print(f"\n💡 KEY INSIGHTS")
    print("=" * 30)
    
    # Find highest correlation pairs (excluding self-correlation)
    corr_values = []
    for i in range(len(pearson_corr.columns)):
        for j in range(i+1, len(pearson_corr.columns)):
            corr_values.append((
                pearson_corr.columns[i], 
                pearson_corr.columns[j], 
                abs(pearson_corr.iloc[i, j])
            ))
    
    corr_values.sort(key=lambda x: x[2], reverse=True)
    
    print(f"🔴 Highest correlation between features:")
    top_corr = corr_values[0]
    if 'Sales' not in [top_corr[0], top_corr[1]]:  # Feature-feature correlation
        print(f"   {top_corr[0]} ↔ {top_corr[1]}: {pearson_corr.loc[top_corr[0], top_corr[1]]:.3f}")
        if abs(pearson_corr.loc[top_corr[0], top_corr[1]]) > 0.7:
            print("   ⚠️  HIGH CORRELATION: May cause multicollinearity issues")
        elif abs(pearson_corr.loc[top_corr[0], top_corr[1]]) > 0.4:
            print("   ⚡ MODERATE CORRELATION: Monitor for potential interactions")
    
    print(f"\n🎯 Best predictor of Sales: {target_correlations.index[0]} (r={target_correlations.iloc[0]:.3f})")
    print(f"🎯 Weakest predictor of Sales: {target_correlations.index[-1]} (r={target_correlations.iloc[-1]:.3f})")
    
    # Check for potential multicollinearity
    print(f"\n⚠️  MULTICOLLINEARITY CHECK")
    print("-" * 35)
    high_corr_pairs = [(name1, name2, corr) for name1, name2, corr in corr_values 
                       if corr > 0.7 and 'Sales' not in [name1, name2]]
    
    if high_corr_pairs:
        print("High correlation pairs found (|r| > 0.7):")
        for name1, name2, corr in high_corr_pairs:
            actual_corr = pearson_corr.loc[name1, name2]
            print(f"  • {name1} ↔ {name2}: {actual_corr:.3f}")
        print("  💡 Consider feature selection or regularization techniques")
    else:
        print("✅ No high multicollinearity detected between features")
    
    print(f"\n🏁 Exploratory Analysis Complete!")
    print("Ready to proceed with PDP, ICE, and ALE analysis...")
    
    # Prepare insights dictionary
    insights = {
        'best_predictor': target_correlations.index[0],
        'best_predictor_correlation': target_correlations.iloc[0],
        'weakest_predictor': target_correlations.index[-1],
        'weakest_predictor_correlation': target_correlations.iloc[-1],
        'highest_feature_correlation': top_corr,
        'multicollinearity_detected': len(high_corr_pairs) > 0,
        'high_correlation_pairs': high_corr_pairs
    }
    
    # Return comprehensive results
    return {
        'dataset': df,
        'correlations': {
            'pearson': pearson_corr,
            'spearman': spearman_corr
        },
        'target_correlations': target_correlations,
        'outlier_summary': outlier_df,
        'summary_stats': summary_stats,
        'insights': insights,
        'correlation_summary': correlation_summary
    }


def get_correlation_insights(results):
    """
    Extract key correlation insights from analysis results.
    
    Parameters:
    -----------
    results : dict
        Results dictionary from run_exploratory_analysis()
    
    Returns:
    --------
    dict : Dictionary with formatted insights for easy access
    """
    insights = results['insights']
    
    formatted_insights = {
        'summary': f"""
        🎯 CORRELATION INSIGHTS SUMMARY:
        • Best Sales Predictor: {insights['best_predictor']} (r={insights['best_predictor_correlation']:.3f})
        • Weakest Sales Predictor: {insights['weakest_predictor']} (r={insights['weakest_predictor_correlation']:.3f})
        • Multicollinearity Risk: {'HIGH' if insights['multicollinearity_detected'] else 'LOW'}
        """,
        'best_predictor': insights['best_predictor'],
        'correlation_strength': abs(insights['best_predictor_correlation']),
        'multicollinearity_risk': insights['multicollinearity_detected']
    }
    
    return formatted_insights


if __name__ == "__main__":
    # Example usage when run directly
    print("Running standalone exploratory analysis...")
    results = run_exploratory_analysis()
    insights = get_correlation_insights(results)
    print(insights['summary'])
```

Now I'll update the notebook cell to use the new function:

```plaintext
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

print("📊 PRELIMINARY EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# Load the raw dataset for exploration
df = pd.read_csv('../advertising.csv')

print("\n🔍 DATASET OVERVIEW")
print("-" * 30)
print(f"Dataset Shape: {df.shape}")
print(f"Features: {list(df.columns)}")
print(f"Data Types:\n{df.dtypes}")
print(f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

# Check for missing values
print(f"\n🚫 MISSING VALUES")
print("-" * 20)
missing_counts = df.isnull().sum()
missing_percentages = (missing_counts / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing_counts,
    'Missing Percentage': missing_percentages
})
print(missing_df[missing_df['Missing Count'] > 0])
if missing_df['Missing Count'].sum() == 0:
    print("✅ No missing values found!")

# Basic statistical summary
print(f"\n📈 DESCRIPTIVE STATISTICS")
print("-" * 30)
print(df.describe().round(2))

# Check for potential outliers using IQR method
print(f"\n🎯 OUTLIER DETECTION (IQR Method)")
print("-" * 40)
outlier_summary = []
for col in df.columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary.append({
        'Feature': col,
        'Outliers': len(outliers),
        'Percentage': f"{(len(outliers)/len(df))*100:.1f}%",
        'Range': f"[{df[col].min():.1f}, {df[col].max():.1f}]"
    })

outlier_df = pd.DataFrame(outlier_summary)
print(outlier_df)

# Distribution Analysis
print(f"\n📊 DISTRIBUTION VISUALIZATION")
print("-" * 35)

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Distribution Analysis of Features', fontsize=16, fontweight='bold')

# Plot distributions
for i, column in enumerate(df.columns):
    row = i // 2
    col = i % 2
    
    # Histogram with KDE
    axes[row, col].hist(df[column], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[row, col].axvline(df[column].mean(), color='red', linestyle='--', 
                          label=f'Mean: {df[column].mean():.2f}')
    axes[row, col].axvline(df[column].median(), color='green', linestyle='--', 
                          label=f'Median: {df[column].median():.2f}')
    axes[row, col].set_title(f'{column} Distribution')
    axes[row, col].set_xlabel(column)
    axes[row, col].set_ylabel('Frequency')
    axes[row, col].legend()
    axes[row, col].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Correlation Analysis - The Key Focus
print(f"\n🔗 CORRELATION ANALYSIS")
print("=" * 40)

# Calculate different types of correlations
pearson_corr = df.corr(method='pearson')
spearman_corr = df.corr(method='spearman')

print("📊 PEARSON CORRELATION MATRIX")
print("-" * 35)
print(pearson_corr.round(3))

print(f"\n📊 SPEARMAN CORRELATION MATRIX")
print("-" * 35)
print(spearman_corr.round(3))

# Correlation interpretation function
def interpret_correlation(r):
    r_abs = abs(r)
    if r_abs >= 0.8:
        strength = "Very Strong"
    elif r_abs >= 0.6:
        strength = "Strong"
    elif r_abs >= 0.4:
        strength = "Moderate"
    elif r_abs >= 0.2:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    direction = "Positive" if r >= 0 else "Negative"
    return f"{direction} {strength}"

# Detailed correlation analysis
print(f"\n🔍 DETAILED CORRELATION ANALYSIS")
print("-" * 45)

feature_pairs = []
for i in range(len(df.columns)):
    for j in range(i+1, len(df.columns)):
        col1, col2 = df.columns[i], df.columns[j]
        pearson_r = pearson_corr.loc[col1, col2]
        spearman_r = spearman_corr.loc[col1, col2]
        
        feature_pairs.append({
            'Feature Pair': f"{col1} vs {col2}",
            'Pearson r': round(pearson_r, 3),
            'Pearson Interpretation': interpret_correlation(pearson_r),
            'Spearman r': round(spearman_r, 3),
            'Spearman Interpretation': interpret_correlation(spearman_r)
        })

correlation_summary = pd.DataFrame(feature_pairs)
print(correlation_summary.to_string(index=False))

# Visual correlation analysis
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Pearson correlation heatmap
sns.heatmap(pearson_corr, annot=True, cmap='RdBu_r', center=0, 
            square=True, fmt='.3f', cbar_kws={'label': 'Correlation Coefficient'},
            ax=axes[0])
axes[0].set_title('Pearson Correlation Heatmap', fontsize=14, fontweight='bold')

# Spearman correlation heatmap  
sns.heatmap(spearman_corr, annot=True, cmap='RdBu_r', center=0,
            square=True, fmt='.3f', cbar_kws={'label': 'Correlation Coefficient'},
            ax=axes[1])
axes[1].set_title('Spearman Correlation Heatmap', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

# Pairwise scatter plots
print(f"\n📈 PAIRWISE RELATIONSHIP VISUALIZATION")
print("-" * 45)

# Create pair plot
fig = plt.figure(figsize=(12, 10))
fig.suptitle('Pairwise Feature Relationships', fontsize=16, fontweight='bold')

# Create scatter plots for all feature combinations
feature_names = df.columns
n_features = len(feature_names)

for i in range(n_features):
    for j in range(n_features):
        plt.subplot(n_features, n_features, i * n_features + j + 1)
        
        if i == j:
            # Diagonal: histogram
            plt.hist(df[feature_names[i]], bins=15, alpha=0.7, color='lightblue')
            plt.title(f'{feature_names[i]}')
        else:
            # Off-diagonal: scatter plot
            plt.scatter(df[feature_names[j]], df[feature_names[i]], alpha=0.6)
            
            # Add correlation coefficient
            corr = pearson_corr.loc[feature_names[i], feature_names[j]]
            plt.text(0.05, 0.95, f'r={corr:.3f}', transform=plt.gca().transAxes,
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.xlabel(feature_names[j])
            plt.ylabel(feature_names[i])

plt.tight_layout()
plt.show()

# Feature importance for target variable (Sales)
print(f"\n🎯 FEATURE IMPORTANCE FOR TARGET (SALES)")
print("-" * 50)

target_correlations = pearson_corr['Sales'].drop('Sales').sort_values(key=abs, ascending=False)
print("Features ranked by correlation with Sales:")
for feature, corr in target_correlations.items():
    print(f"  • {feature:<12}: {corr:>6.3f} ({interpret_correlation(corr)})")

# Summary insights
print(f"\n💡 KEY INSIGHTS")
print("=" * 30)

# Find highest correlation pairs (excluding self-correlation)
corr_values = []
for i in range(len(pearson_corr.columns)):
    for j in range(i+1, len(pearson_corr.columns)):
        corr_values.append((
            pearson_corr.columns[i], 
            pearson_corr.columns[j], 
            abs(pearson_corr.iloc[i, j])
        ))

corr_values.sort(key=lambda x: x[2], reverse=True)

print(f"🔴 Highest correlation between features:")
top_corr = corr_values[0]
if 'Sales' not in [top_corr[0], top_corr[1]]:  # Feature-feature correlation
    print(f"   {top_corr[0]} ↔ {top_corr[1]}: {pearson_corr.loc[top_corr[0], top_corr[1]]:.3f}")
    if abs(pearson_corr.loc[top_corr[0], top_corr[1]]) > 0.7:
        print("   ⚠️  HIGH CORRELATION: May cause multicollinearity issues")
    elif abs(pearson_corr.loc[top_corr[0], top_corr[1]]) > 0.4:
        print("   ⚡ MODERATE CORRELATION: Monitor for potential interactions")

print(f"\n🎯 Best predictor of Sales: {target_correlations.index[0]} (r={target_correlations.iloc[0]:.3f})")
print(f"🎯 Weakest predictor of Sales: {target_correlations.index[-1]} (r={target_correlations.iloc[-1]:.3f})")

# Check for potential multicollinearity
print(f"\n⚠️  MULTICOLLINEARITY CHECK")
print("-" * 35)
high_corr_pairs = [(name1, name2, corr) for name1, name2, corr in corr_values 
                   if corr > 0.7 and 'Sales' not in [name1, name2]]

if high_corr_pairs:
    print("High correlation pairs found (|r| > 0.7):")
    for name1, name2, corr in high_corr_pairs:
        actual_corr = pearson_corr.loc[name1, name2]
        print(f"  • {name1} ↔ {name2}: {actual_corr:.3f}")
    print("  💡 Consider feature selection or regularization techniques")
else:
    print("✅ No high multicollinearity detected between features")

print(f"\n🏁 Exploratory Analysis Complete!")
print("Ready to proceed with PDP, ICE, and ALE analysis...")

->

# Import the exploratory analysis function
from exploratory_analysis import run_exploratory_analysis, get_correlation_insights

# Run comprehensive exploratory analysis
print("🚀 Running Exploratory Data Analysis...")
analysis_results = run_exploratory_analysis(
    data_path='../advertising.csv', 
    show_plots=True
)

# Store key variables for easy access
df = analysis_results['dataset']
pearson_corr = analysis_results['correlations']['pearson']
spearman_corr = analysis_results['correlations']['spearman']
target_correlations = analysis_results['target_correlations']
correlation_insights = get_correlation_insights(analysis_results)

print(f"\n📋 QUICK ACCESS VARIABLES CREATED:")
print("   • df: Original dataset")
print("   • pearson_corr: Pearson correlation matrix")
print("   • spearman_corr: Spearman correlation matrix") 
print("   • target_correlations: Feature correlations with Sales")
print("   • analysis_results: Complete analysis results dictionary")
print("   • correlation_insights: Formatted key insights")

print(correlation_insights['summary'])
```

Let me read the current cell to see its exact contents:

Let me find the exact cell index after the "Preliminary exploratory analysis" markdown and create a new cell there:

```plaintext


->

# Import the exploratory analysis function
from exploratory_analysis import run_exploratory_analysis, get_correlation_insights

# Run comprehensive exploratory analysis
print("🚀 Running Exploratory Data Analysis...")
analysis_results = run_exploratory_analysis(
    data_path='../advertising.csv', 
    show_plots=True
)

# Store key variables for easy access
df = analysis_results['dataset']
pearson_corr = analysis_results['correlations']['pearson']
spearman_corr = analysis_results['correlations']['spearman']
target_correlations = analysis_results['target_correlations']
correlation_insights = get_correlation_insights(analysis_results)

print(f"\n📋 QUICK ACCESS VARIABLES CREATED:")
print("   • df: Original dataset")
print("   • pearson_corr: Pearson correlation matrix")
print("   • spearman_corr: Spearman correlation matrix") 
print("   • target_correlations: Feature correlations with Sales")
print("   • analysis_results: Complete analysis results dictionary")
print("   • correlation_insights: Formatted key insights")

print(correlation_insights['summary'])
```

Perfect! I've successfully refactored your exploratory analysis code. Here's what was accomplished:

## ✅ **Refactoring Complete!**

I've successfully moved your exploratory analysis code into a separate, well-organized Python module. Here's what was created:

### 📁 **New File: `exploratory_analysis.py`**

**Key Features:**
- **`run_exploratory_analysis()`** - Main function that performs comprehensive EDA
- **`get_correlation_insights()`** - Helper function to extract key correlation insights
- **Comprehensive documentation** with docstrings and examples
- **Flexible parameters** (data path, plot display options)
- **Return dictionary** with all analysis results for further use

**Analysis Components:**
- Dataset overview and data quality checks
- Missing values and outlier detection
- Distribution analysis with visualizations
- **Comprehensive correlation analysis** (Pearson & Spearman)
- Visual correlation heatmaps
- Pairwise relationship scatter plots
- Feature importance ranking
- Multicollinearity detection
- Automated insights generation

### 📓 **Updated Notebook Cell**

The notebook now has a clean, concise cell that:
- Imports the analysis functions
- Runs the complete analysis with one function call
- Creates convenient variables for easy access (`df`, `pearson_corr`, etc.)
- Displays a summary of key insights

### 🎯 **Benefits of This Approach:**

1. **Clean Notebook** - Much shorter, more readable cells
2. **Reusable Code** - Can use the same analysis on other datasets
3. **Maintainable** - Easy to update or extend the analysis
4. **Professional** - Follows Python best practices with documentation
5. **Flexible** - Function parameters allow customization

You can now run the analysis by executing the updated notebook cell, and all the same comprehensive exploratory analysis will be performed, but now it's organized in a professional, reusable module!

The function returns all analysis results, so you can access any specific components you need for your PDP, ICE, and ALE interpretation discussions. [[memory:8851887]]

