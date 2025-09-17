#!/usr/bin/env python3
"""
Training script for MLOps starter project
"""

import os
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature


def load_data(data_path):
    """Load training data"""
    # For demo purposes, generate synthetic data
    # In practice, load your actual dataset
    np.random.seed(42)
    n_samples = 1000
    n_features = 10
    
    X = np.random.randn(n_samples, n_features)
    y = np.sum(X[:, :3], axis=1) + np.random.randn(n_samples) * 0.1
    
    feature_names = [f"feature_{i}" for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    return df


def train_model(df, params):
    """Train the model"""
    # Prepare data
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=params['n_estimators'],
        max_depth=params['max_depth'],
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return model, X_test, y_pred, {'mse': mse, 'mae': mae, 'r2': r2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', default='data/train.csv')
    parser.add_argument('--n-estimators', type=int, default=100)
    parser.add_argument('--max-depth', type=int, default=10)
    args = parser.parse_args()
    
    params = {
        'n_estimators': args.n_estimators,
        'max_depth': args.max_depth
    }
    
    # Set MLflow tracking URI
    mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000')
    mlflow.set_tracking_uri(mlflow_uri)
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(params)
        
        # Load data
        df = load_data(args.data_path)
        
        # Train model
        model, X_test, y_pred, metrics = train_model(df, params)
        
        # Log metrics
        mlflow.log_metrics(metrics)
        
        # Create model signature
        signature = infer_signature(X_test, y_pred)
        
        # Log model
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            registered_model_name="random_forest_regressor"
        )
        
        print(f"Model metrics: {metrics}")
        print(f"Model logged to MLflow with run ID: {mlflow.active_run().info.run_id}")


if __name__ == "__main__":
    main()
