import pytest
import database

# Mocking the database collection using pytest-mock
@pytest.fixture
def mock_users_collection(mocker):
    mock_collection = mocker.MagicMock()
    mocker.patch("database.users_collection", mock_collection)
    return mock_collection

def test_register_user_new_user(mock_users_collection):
    mock_users_collection.find_one.return_value = None  # Simulate username not found
    assert database.register_user("new_user", "password") == True

def test_register_user_existing_user(mock_users_collection):
    mock_users_collection.find_one.return_value = {"username": "existing_user"}  # Simulate username found
    assert database.register_user("existing_user", "password") == False

