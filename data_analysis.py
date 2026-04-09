"""
Data Analysis Script for Excel Datasets
Performs EDA, statistical analysis, and visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set up visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_datasets(file1_path, file2_path):
    """
    Load Excel datasets
    
    Parameters:
    - file1_path: Path to first Excel file
    - file2_path: Path to second Excel file
    
    Returns:
    - df1, df2: Loaded dataframes
    """
    try:
        df1 = pd.read_excel(file1_path)
        df2 = pd.read_excel(file2_path)
        print(f"✓ Loaded Dataset 1: {file1_path}")
        print(f"✓ Loaded Dataset 2: {file2_path}")
        return df1, df2
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None


def exploratory_data_analysis(df, dataset_name):
    """
    Perform EDA on a dataset
    """
    print(f"\n{'='*60}")
    print(f"EXPLORATORY DATA ANALYSIS - {dataset_name}")
    print(f"{'='*60}")
    
    # Basic Info
    print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn Names and Types:")
    print(df.dtypes)
    
    # Missing Values
    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values detected")
    
    # Descriptive Statistics
    print(f"\nDescriptive Statistics:")
    print(df.describe())
    
    # Data Preview
    print(f"\nFirst Few Rows:")
    print(df.head())


def statistical_analysis(df, dataset_name):
    """
    Perform statistical analysis
    """
    print(f"\n{'='*60}")
    print(f"STATISTICAL ANALYSIS - {dataset_name}")
    print(f"{'='*60}")
    
    # Numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        print(f"\nCorrelation Matrix:")
        print(df[numeric_cols].corr())
        
        # Summary statistics
        print(f"\nSummary Statistics (Numeric Columns):")
        print(df[numeric_cols].describe())
    else:
        print("No numeric columns found for statistical analysis")


def create_visualizations(df1, df2):
    """
    Create visualizations for both datasets
    """
    # Get numeric columns
    numeric_cols1 = df1.select_dtypes(include=[np.number]).columns
    numeric_cols2 = df2.select_dtypes(include=[np.number]).columns
    
    # Visualization 1: Dataset 1 Distribution
    if len(numeric_cols1) > 0:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Dataset 1 - Distributions", fontsize=16, fontweight='bold')
        
        for idx, col in enumerate(numeric_cols1[:4]):
            ax = axes[idx//2, idx%2]
            df1[col].hist(bins=30, ax=ax, color='skyblue', edgecolor='black')
            ax.set_title(f'Distribution of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('dataset1_distributions.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: dataset1_distributions.png")
        plt.close()
    
    # Visualization 2: Dataset 2 Distribution
    if len(numeric_cols2) > 0:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Dataset 2 - Distributions", fontsize=16, fontweight='bold')
        
        for idx, col in enumerate(numeric_cols2[:4]):
            ax = axes[idx//2, idx%2]
            df2[col].hist(bins=30, ax=ax, color='lightcoral', edgecolor='black')
            ax.set_title(f'Distribution of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('dataset2_distributions.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: dataset2_distributions.png")
        plt.close()
    
    # Visualization 3: Comparison if numeric columns exist
    if len(numeric_cols1) > 0 and len(numeric_cols2) > 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create comparison of first numeric column
        col1 = numeric_cols1[0]
        col2 = numeric_cols2[0]
        
        ax.hist([df1[col1], df2[col2]], bins=30, label=['Dataset 1', 'Dataset 2'], color=['skyblue', 'lightcoral'])
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.set_title('Dataset Comparison')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig('dataset_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: dataset_comparison.png")
        plt.close()


def main():
    """
    Main execution function
    """
    print("="*60)
    print("DATA ANALYSIS PIPELINE")
    print("="*60)
    
    # TODO: Update these paths to your actual Excel file locations
    file1_path = "data/dataset1.xlsx"  # Change this path
    file2_path = "data/dataset2.xlsx"  # Change this path
    
    # Load datasets
    df1, df2 = load_datasets(file1_path, file2_path)
    
    if df1 is not None and df2 is not None:
        # Perform analyses
        exploratory_data_analysis(df1, "Dataset 1")
        exploratory_data_analysis(df2, "Dataset 2")
        
        statistical_analysis(df1, "Dataset 1")
        statistical_analysis(df2, "Dataset 2")
        
        # Create visualizations
        print(f"\n{'='*60}")
        print("GENERATING VISUALIZATIONS")
        print(f"{'='*60}")
        create_visualizations(df1, df2)
        
        print("\n✓ Analysis complete! Check visualizations saved as PNG files.")
    else:
        print("Failed to load datasets. Please check file paths.")


if __name__ == "__main__":
    main()
