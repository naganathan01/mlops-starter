#!/usr/bin/env python3
"""
Model registration script
"""

import os
import argparse
import mlflow
from mlflow.tracking import MlflowClient


def register_model(run_id, model_name, stage="Staging"):
    """Register model from MLflow run"""
    
    mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000')
    mlflow.set_tracking_uri(mlflow_uri)
    
    client = MlflowClient()
    
    # Get model URI
    model_uri = f"runs:/{run_id}/model"
    
    # Register model
    model_version = mlflow.register_model(
        model_uri=model_uri,
        name=model_name
    )
    
    print(f"Model registered: {model_name} version {model_version.version}")
    
    # Transition to specified stage
    if stage:
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage=stage
        )
        print(f"Model transitioned to {stage} stage")
    
    return model_version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True, help='MLflow run ID')
    parser.add_argument('--model-name', default='random_forest_regressor')
    parser.add_argument('--stage', default='Staging')
    args = parser.parse_args()
    
    model_version = register_model(args.run_id, args.model_name, args.stage)
    print(f"Successfully registered model version: {model_version.version}")


if __name__ == "__main__":
    main()
