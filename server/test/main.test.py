import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch
from server.service.vision import detect

# Import the app from your FastAPI code (assuming the app is in a file named `main.py`)
from main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def mock_detect():
    """Mock the detect function to avoid actual detection during testing."""
    with patch("service.vision.detect") as mock:
        yield mock

def test_test_endpoint(client):
    """Test the /test endpoint."""
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Test is working!"}

def test_websocket_endpoint(client, mock_detect):
    """Test the /ws WebSocket endpoint."""
    mock_detect.return_value = '{"message": "Detection successful"}'
    
    with client.websocket_connect("/ws") as websocket:
        # Send a base64 image string (simulated for testing)
        websocket.send_text("data:image/jpg;base64,valid_image_data")
        
        # Receive the detection response from the WebSocket
        response = websocket.receive_text()
        assert response == '{"message": "Detection successful"}'
        
        # Ensure the detect function was called with the correct arguments
        mock_detect.assert_called_once_with("data:image/jpg;base64,valid_image_data")

def test_invalid_image_websocket(client, mock_detect):
    """Test the /ws WebSocket endpoint with invalid image input."""
    mock_detect.return_value = '[]'
    
    with client.websocket_connect("/ws") as websocket:
        # Send an invalid base64 image string
        websocket.send_text("data:image/jpg;base64,invalid_data")
        
        # Receive the detection response from the WebSocket
        response = websocket.receive_text()
        assert response == '[]'  # Should return an empty list for invalid input
