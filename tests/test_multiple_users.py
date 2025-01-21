import pytest
import requests
from utils.helpers import read_credentials
from utils.config import BASE_URL, AUTH_HEADERS

# CSV Inputs
CREDENTIALS_FILE = "credentials/multiple_users.csv"

# API Endpoints
SIGNUP_API = f"{BASE_URL}/user/account/student-signup"
DELETE_API = f"{BASE_URL}/user/account/delete"

@pytest.fixture(scope="module")
def user_data():
    """Fixture to read user credentials from CSV."""
    return read_credentials(CREDENTIALS_FILE)

@pytest.fixture(scope="module")
def created_users():
    """Fixture to store user details after creation."""
    return {}

@pytest.mark.parametrize("credentials", read_credentials(CREDENTIALS_FILE))
def test_create_user(credentials, created_users):
    """Test to create a new user and store credentials for deletion."""
    print(f"Creating user with credentials: {credentials}")

    payload = {
        "name": credentials["name"],
        "childName": "ram",
        "dateOfBirth": "1994-03-11",
        "loginType": "phoneNumber",
        "deviceType": "web",
        "timezone": "652d2ab14eeb65744d58b772",
        "isGlobal": False,
        "phoneNumber": credentials["phonenumber"],
        "areaCode": "+91",
    }

    response = requests.post(SIGNUP_API, json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200, f"Failed to create user: {response.text}"

    response_data = response.json()
    assert response_data.get("message") == "Success", f"Unexpected response message: {response_data}"

    user_details = response_data.get("body", {}).get("user", {})
    user_id = user_details.get("_id")
    token = user_details.get("token")

    assert user_id, "User ID not found in response"
    assert token, "Token not found in response"

    # Store the user ID and token for later use
    created_users[credentials["phonenumber"]] = {"user_id": user_id, "token": token}

@pytest.mark.parametrize("credentials", read_credentials(CREDENTIALS_FILE))
def test_delete_user(credentials, created_users):
    """Test to delete the created user using stored credentials."""
    user_info = created_users.get(credentials["phonenumber"])
    
    assert user_info, f"No stored data found for {credentials['phonenumber']}"
    user_id = user_info["user_id"]
    token = user_info["token"]

    assert user_id, "No user ID found for deletion"
    assert token, "No token found for deletion"

    delete_url = f"{DELETE_API}?accountDetailId={user_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(delete_url, headers=headers)
    assert response.status_code == 200, f"Failed to delete user: {response.text}"
