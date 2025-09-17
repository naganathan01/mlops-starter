#!/usr/bin/env python3
"""
Model inference service
"""

import os
from fastapi import FastAPI, HTTPException
import pandas as pd
import mlflow
import mlflow.sklearn
from pydantic import BaseModel
from typing import List
import uvicorn


app = FastAPI(title="MLOps Model Server", version="1.0.0")

# Global model variable
model = None
model_version = None


class PredictionRequest(BaseModel):
    data: List[List[float]]
    feature_names: List[str] = None


class PredictionResponse(BaseModel):
    predictions: List[float]
    model_version: str


def load_model():
    """Load model from MLflow"""
    global model, model_version

    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    model_name = os.getenv("MODEL_NAME", "random_forest_regressor")
    version = os.getenv("MODEL_VERSION", "latest")

    mlflow.set_tracking_uri(mlflow_uri)

    try:
        if version == "latest":
            model_uri = f"models:/{model_name}/Latest"
        else:
            model_uri = f"models:/{model_name}/{version}"

        model = mlflow.sklearn.load_model(model_uri)
        model_version = version
        print(f"Model loaded successfully: {model_uri}")

    except Exception as e:
        print(f"Error loading model: {e}")
        raise


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready", "model_version": model_version}


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make predictions"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert to DataFrame
        if request.feature_names:
            df = pd.DataFrame(request.data, columns=request.feature_names)
        else:
            df = pd.DataFrame(request.data)

        # Make predictions
        predictions = model.predict(df)

        return PredictionResponse(
            predictions=predictions.tolist(), model_version=model_version
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.get("/model-info")
async def get_model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "model_version": model_version,
        "model_type": type(model).__name__,
        "feature_count": getattr(model, "n_features_in_", "unknown"),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
