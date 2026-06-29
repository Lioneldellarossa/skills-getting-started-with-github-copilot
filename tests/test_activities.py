def test_get_activities_returns_all_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    activities = response.json()
    assert len(activities) == 9
    assert "Chess Club" in activities


def test_get_activities_returns_expected_activity_shape(client):
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    activities = response.json()
    chess_club = activities["Chess Club"]
    assert set(chess_club.keys()) == expected_keys
    assert isinstance(chess_club["participants"], list)