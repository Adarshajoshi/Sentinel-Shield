from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_mask_endpoint():
    response = client.post(
        "/mask",
        json={"prompt": "Contact me at 123-456-7890", "session_id": "api_test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "masked_text" in data
    assert "[PHONE_NUMBER" in data["masked_text"]

def test_api_invalid_request():
    """Does the API correctly fail if the prompt is missing?"""
    response = client.post("/mask", json={"session_id": "bad_req"})
    # FastAPI should automatically return 422 Unprocessable Entity
    assert response.status_code == 422