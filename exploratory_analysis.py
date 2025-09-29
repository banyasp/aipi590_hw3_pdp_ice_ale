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
