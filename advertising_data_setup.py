"""
Advertising Dataset Setup for XAI Analysis
==========================================

This module loads and prepares the advertising dataset for explainable AI analysis.
The dataset contains advertising spend data for TV, Radio, and Newspaper media,
with Sales as the target variable to predict.

Dataset: advertising.csv
- Features: TV, Radio, Newspaper (advertising spend in thousands)
- Target: Sales (in thousands of units)
- Task: Regression (predicting continuous sales values)
"""

import pandas as pd
import numpy as np
import xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

def load_advertising_data(data_path='advertising.csv'):
    """
    Load the advertising dataset from CSV file.
    
    Parameters:
    -----------
    data_path : str
        Path to the advertising.csv file
        
    Returns:
    --------
    tuple: (X, y) where X is features DataFrame and y is target Series
    """
    # Check if file exists
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found: {data_path}")
    
    # Load the dataset
    print(f"📊 Loading advertising dataset from: {data_path}")
    df = pd.read_csv(data_path)
    
    # Remove any empty rows
    df = df.dropna()
    
    print(f"✅ Dataset loaded successfully!")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    
    # Separate features and target
    feature_columns = ['TV', 'Radio', 'Newspaper']
    target_column = 'Sales'
    
    X = df[feature_columns].copy()
    y = df[target_column].copy()
    
    return X, y

def setup_advertising_model(data_path='advertising.csv', test_size=0.3, random_state=42):
    """
    Complete setup for advertising dataset: load data, split, and train model.
    
    Parameters:
    -----------
    data_path : str
        Path to the advertising.csv file
    test_size : float
        Proportion of dataset to use for testing (default: 0.3)
    random_state : int
        Random seed for reproducibility (default: 42)
        
    Returns:
    --------
    dict: Dictionary containing all necessary components:
        - 'X': Full feature DataFrame
        - 'y': Full target Series  
        - 'X_train': Training features
        - 'X_test': Test features
        - 'y_train': Training target
        - 'y_test': Test target
        - 'model': Trained XGBoost model
        - 'feature_names': List of feature names
    """
    
    print("🚀 Setting up Advertising Dataset for XAI Analysis")
    print("=" * 60)
    
    # Load data
    X, y = load_advertising_data(data_path)
    
    # Display basic dataset info
    print(f"\n📈 Dataset Overview:")
    print(f"   Features: {list(X.columns)}")
    print(f"   Target: Sales")
    print(f"   Samples: {len(X)}")
    print(f"   Task: Regression (predicting sales from advertising spend)")
    
    # Show data types and basic statistics
    print(f"\n📋 Feature Information:")
    for col in X.columns:
        print(f"   {col}: {X[col].dtype} | Range: {X[col].min():.1f} - {X[col].max():.1f}")
    
    print(f"\n🎯 Target Information:")
    print(f"   Sales: {y.dtype} | Range: {y.min():.1f} - {y.max():.1f}")
    
    # Train-test split
    print(f"\n✂️ Splitting data (test_size={test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Test set: {X_test.shape[0]} samples")
    
    # Train XGBoost model
    print(f"\n🤖 Training XGBoost Regressor...")
    model = xgboost.XGBRegressor(
        random_state=random_state,
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    
    print(f"\n📊 Model Performance:")
    print(f"   Training RMSE: {train_rmse:.2f}")
    print(f"   Test RMSE: {test_rmse:.2f}")
    print(f"   Training R²: {train_r2:.3f}")
    print(f"   Test R²: {test_r2:.3f}")
    
    if test_r2 > 0.7:
        print(f"   ✅ Good model performance (R² > 0.7)")
    elif test_r2 > 0.5:
        print(f"   ⚠️ Moderate model performance (R² > 0.5)")
    else:
        print(f"   ❌ Poor model performance (R² < 0.5)")
    
    print(f"\n🎉 Setup complete! Ready for XAI analysis.")
    
    # Return all components
    return {
        'X': X,
        'y': y,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'model': model,
        'feature_names': list(X.columns),
        'target_name': 'Sales',
        'task_type': 'regression'
    }

def display_sample_data(data_dict, n_samples=5):
    """
    Display sample data for inspection.
    
    Parameters:
    -----------
    data_dict : dict
        Dictionary returned from setup_advertising_model()
    n_samples : int
        Number of samples to display
    """
    print(f"\n🔍 Sample Data (first {n_samples} rows):")
    print("=" * 50)
    
    sample_data = pd.concat([
        data_dict['X'].head(n_samples),
        data_dict['y'].head(n_samples)
    ], axis=1)
    
    print(sample_data.to_string(index=False))
    
    print(f"\n💡 Interpretation:")
    print(f"   - TV, Radio, Newspaper: Advertising spend (in thousands $)")
    print(f"   - Sales: Product sales (in thousands of units)")
    print(f"   - Goal: Predict sales based on advertising investment")

if __name__ == "__main__":
    # Example usage
    try:
        # Setup the advertising dataset
        advertising_data = setup_advertising_model(
            data_path='advertising.csv',
            test_size=0.3,
            random_state=42
        )
        
        # Display sample data
        display_sample_data(advertising_data)
        
        # Quick feature importance check
        print(f"\n🔥 Feature Importance (from XGBoost):")
        print("=" * 40)
        feature_importance = advertising_data['model'].feature_importances_
        for i, (feature, importance) in enumerate(zip(advertising_data['feature_names'], feature_importance)):
            print(f"   {i+1}. {feature}: {importance:.3f}")
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Make sure 'advertising.csv' is in the current directory.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
