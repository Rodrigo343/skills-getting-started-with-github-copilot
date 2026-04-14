def test_get_activities(client):
    # Arrange: No specific setup needed as activities are predefined

    # Act: Make a GET request to /activities
    response = client.get("/activities")

    # Assert: Check status code and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data  # Example activity
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_success(client):
    # Arrange: Choose an activity and a new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make a POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]


def test_signup_for_activity_duplicate(client):
    # Arrange: Sign up first, then try again with same email
    activity_name = "Programming Class"
    email = "duplicatestudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})  # First signup

    # Act: Attempt duplicate signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up" in data["detail"]


def test_remove_participant_success(client):
    # Arrange: Sign up a participant first
    activity_name = "Gym Class"
    email = "removestudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Make a DELETE request to remove the participant
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Removed {email} from {activity_name}" in data["message"]


def test_remove_participant_not_found(client):
    # Arrange: Choose an activity and an email not signed up
    activity_name = "Basketball Team"
    email = "nonexistent@mergington.edu"

    # Act: Attempt to remove a non-existent participant
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]