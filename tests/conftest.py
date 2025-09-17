import pytest
import os
import tempfile
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_mlflow_env():
    """Mock MLflow environment variables for testing"""
    with patch.dict(os.environ, {
        'MLFLOW_TRACKING_URI': 'http://localhost:5000',
        'MODEL_NAME': 'test_model',
        'MODEL_VERSION': '1'
    }):
        yield


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
