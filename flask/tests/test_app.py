import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the Health Check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert b"healthy" in response.data

def test_system_status(client):
    """Test the New Feature (System Status)"""
    response = client.get('/api/system')
    assert response.status_code == 200
    data = response.get_json()
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert data["status"] == "online"
