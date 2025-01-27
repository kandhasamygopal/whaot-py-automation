import requests
from utils.config import BASE_URL , AUTH_HEADERS
from utils.helpers import json_read_credentials
import pytest

# Gmail Login API's flow
GMAIL_SIGNUP_GMAIL_CHECK = f"{BASE_URL}/user/account/check-user-exists-by-email"
NEW_GMAIL_USER_SIGNUP = f"{BASE_URL}/user/account/student-signup"
GMAIL_LOGIN = f"{BASE_URL}/user/account/login/email"

# Gmail user data stored file path
CREDENTIALS_FILE = "credentials/student_api_data.json"

# Test function for Gmail signup 
@pytest.mark.parametrize("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_gmail_user_flow(credentials):
    GMAIL_SIGNUP_Gmail = credentials["email"]["gmail_address"]
    login_type_Gmail = credentials["login_method"]["type"][0]
    phone_number = credentials["email"]["phone_number"]
    parent_name = credentials["parent_name"]
    child_name = credentials["child_name"]
    Date_of_Birth = credentials["child_dob"]
    device_Type = credentials["device_type"]
    time_zone = credentials["timezone"]
    area_code = credentials ["phone_number"]["areaCode"]
    

    payload = {"email":GMAIL_SIGNUP_Gmail}

    print("New Gmail user signup request...")

    # Step 1: Check if the gmail user is new or existing
    response = requests.post(GMAIL_SIGNUP_GMAIL_CHECK, json=payload, headers=AUTH_HEADERS)

    print(f"Gmail Signup response status: {response.status_code}")
    print(f"Gmail Signup response text: {response.text}")
    assert response.status_code == 200, f"Signup failed with status code: {response.status_code} - {response.text}"


    if  response.headers.get("Content-Type", "").startswith("application/json"):
        response_data = response.json()
        print(f"Response JSON: {response_data}")
    else:
        print("Unexpected response type")
        print(f"Response text: {response.text}")
        assert False, f"Unexpected response type: {response.headers.get('Content-Type', '')}"

    user_details = response_data.get("body", {})
    gmail_newuser = user_details.get("isNewUser", True)

# Step
    if gmail_newuser:
        
        print("New user Gmail verification completed and starting signup details...")

        # Step 3: Complete Signup
        payload_signup = {
            "name": parent_name,
            "childName": child_name,
            "dateOfBirth": Date_of_Birth,
            "loginType": login_type_Gmail,
            "deviceType": device_Type,
            "timezone": time_zone,
            "isGlobal": False,
            "phoneNumber":phone_number,
            "areaCode":area_code,
            "email": GMAIL_SIGNUP_Gmail
            
        }
        print("Starting gmail user signup flow...")
        response = requests.post(NEW_GMAIL_USER_SIGNUP, json=payload_signup, headers=AUTH_HEADERS)
        print(f"New Gmail Signup response status code: {response.status_code}")
        print(f"New Gmail Signup response text: {response.text}")
        assert response.status_code == 200, "New gmail user registration failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"
        print("Signup completed for new gmail user.")
    else:
        print("Existing gmail detected. Logging in with gmail ...")

        payload2 = {"email":GMAIL_SIGNUP_Gmail,"loginType":login_type_Gmail}

        print("Existing Gmail user signup request...")

    # Step 2: Check if the gmail user loggin
        response = requests.post(GMAIL_LOGIN, json=payload2, headers=AUTH_HEADERS)

        print(f"Existing Gmail user Signup response status: {response.status_code}")
        print(f"Existing Gmail user Signup response text: {response.text}")
        assert response.status_code == 200, f"Signup failed with status code: {response.status_code} - {response.text}"
     
        print("Existing Gmail user signup successfully...")