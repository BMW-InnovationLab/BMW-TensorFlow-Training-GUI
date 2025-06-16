"""Shared pytest fixtures and configuration for all tests."""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any

import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide a mock configuration dictionary."""
    return {
        "api_version": "v1",
        "host": "localhost",
        "port": 8080,
        "debug": True,
        "log_level": "DEBUG",
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "test_db",
            "user": "test_user",
            "password": "test_password"
        },
        "redis": {
            "host": "localhost",
            "port": 6379,
            "db": 0
        },
        "model_config": {
            "batch_size": 32,
            "epochs": 10,
            "learning_rate": 0.001
        }
    }


@pytest.fixture
def mock_logger() -> Mock:
    """Provide a mock logger."""
    logger = Mock()
    logger.debug = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.exception = Mock()
    return logger


@pytest.fixture
def sample_image_path(temp_dir: Path) -> Path:
    """Create a sample image file path."""
    image_path = temp_dir / "sample_image.jpg"
    image_path.write_bytes(b"fake image content")
    return image_path


@pytest.fixture
def sample_model_path(temp_dir: Path) -> Path:
    """Create a sample model file path."""
    model_path = temp_dir / "sample_model.h5"
    model_path.write_bytes(b"fake model content")
    return model_path


@pytest.fixture
def mock_request() -> Mock:
    """Provide a mock HTTP request object."""
    request = Mock()
    request.method = "GET"
    request.path = "/api/v1/test"
    request.headers = {"Content-Type": "application/json"}
    request.json = Mock(return_value={})
    request.args = {}
    request.files = {}
    return request


@pytest.fixture
def mock_response() -> Mock:
    """Provide a mock HTTP response object."""
    response = Mock()
    response.status_code = 200
    response.json = Mock(return_value={})
    response.text = ""
    return response


@pytest.fixture
def sample_training_data() -> Dict[str, Any]:
    """Provide sample training data structure."""
    return {
        "dataset_name": "test_dataset",
        "images": [
            {"id": 1, "path": "/data/image1.jpg", "label": "cat"},
            {"id": 2, "path": "/data/image2.jpg", "label": "dog"}
        ],
        "labels": ["cat", "dog", "bird"],
        "split_ratio": {"train": 0.8, "val": 0.1, "test": 0.1}
    }


@pytest.fixture
def sample_inference_data() -> Dict[str, Any]:
    """Provide sample inference data structure."""
    return {
        "image_path": "/data/test_image.jpg",
        "model_name": "test_model",
        "confidence_threshold": 0.5,
        "max_detections": 10
    }


@pytest.fixture
def mock_docker_client() -> Mock:
    """Provide a mock Docker client."""
    client = Mock()
    client.containers = Mock()
    client.images = Mock()
    client.networks = Mock()
    client.volumes = Mock()
    return client


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_database_connection() -> Mock:
    """Provide a mock database connection."""
    connection = Mock()
    connection.execute = Mock(return_value=Mock())
    connection.commit = Mock()
    connection.rollback = Mock()
    connection.close = Mock()
    return connection


@pytest.fixture
def async_mock():
    """Create an async mock object."""
    return MagicMock(__aenter__=MagicMock(return_value=None),
                     __aexit__=MagicMock(return_value=None))


@pytest.fixture
def mock_file_upload() -> Dict[str, Any]:
    """Provide a mock file upload object."""
    return {
        "filename": "test_file.txt",
        "content_type": "text/plain",
        "data": b"test file content"
    }


def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "requires_gpu: mark test as requiring GPU"
    )
    config.addinivalue_line(
        "markers", "requires_docker: mark test as requiring Docker"
    )
    config.addinivalue_line(
        "markers", "requires_network: mark test as requiring network access"
    )