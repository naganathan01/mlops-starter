import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
from src.inference import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


@patch('src.inference.model')
def test_predict_endpoint(mock_model, client):
    """Test prediction endpoint"""
    # Mock model
    mock_model.predict.return_value = np.array([1.0, 2.0])
    
    # Test data
    test_data = {
        "data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                 [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]]
    }
    
    # Mock global variables
    with patch('src.inference.model', mock_model), \
         patch('src.inference.model_version', '1'):
        
        response = client.post("/predict", json=test_data)
        
        assert response.status_code == 200
        result = response.json()
        assert "predictions" in result
        assert len(result["predictions"]) == 2
