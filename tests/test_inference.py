import pytest
from unittest.mock import patch
import pandas as pd
import numpy as np
import asyncio
from src.train import load_data, train_model


def test_load_data():
    """Test data loading function"""
    df = load_data("dummy_path")
    assert isinstance(df, pd.DataFrame)
    assert 'target' in df.columns
    assert len(df) == 1000


def test_train_model():
    """Test model training"""
    np.random.seed(42)
    data = np.random.randn(100, 10)
    df = pd.DataFrame(data, columns=[f"feature_{i}" for i in range(10)])
    df['target'] = np.sum(data[:, :3], axis=1)
    
    params = {'n_estimators': 10, 'max_depth': 5}
    model, X_test, y_pred, metrics = train_model(df, params)
    
    assert model is not None
    assert len(y_pred) > 0
    assert 'mse' in metrics
    assert 'mae' in metrics
    assert 'r2' in metrics


def test_basic_inference_import():
    """Test that inference module imports correctly"""
    from src import inference
    assert inference.app is not None


@patch('src.inference.model', None)  
def test_health_check():
    """Test health check function"""
    from src.inference import health_check
    result = asyncio.run(health_check())
    assert result["status"] == "healthy"
    assert "model_loaded" in result
