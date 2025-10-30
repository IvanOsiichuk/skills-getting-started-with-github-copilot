import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

def test_root_redirect(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200  # The response is successful

def test_get_activities(client: TestClient):
    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json() == activities

def test_signup_for_activity_success(client: TestClient):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    
    # Ensure student is not already signed up
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]

def test_signup_for_activity_already_registered(client: TestClient):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered student
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}

def test_signup_for_nonexistent_activity(client: TestClient):
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_unregister_from_activity_success(client: TestClient):
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"  # Known participant
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_registered(client: TestClient):
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not registered for this activity"}

def test_unregister_from_nonexistent_activity(client: TestClient):
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}