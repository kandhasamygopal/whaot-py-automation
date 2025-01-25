import requests
from utils.config import BASE_URL, AUTH_HEADERS
from utils.helpers import read_credentials , json_read_credentials
import pytest

# Email Login Function API Endpoints
EMAIL_LOGIN = f"{BASE_URL}/user/account/check-user-exists-by-email"
OTP_VERIFICATION = f"{BASE_URL}/user/account/validate-email-otp"
NEW_USER_SIGNUP = f"{BASE_URL}/user/account/student-signup"
EMAIL_USER_LOGIN = f"{BASE_URL}/user/account/login"

#Email user data stored file path
CREDENTIALS_FILE = "credentials/student_api_data.json"

# Test Function
@pytest.mark.parametrize("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_email_user_flow(credentials):
    Email = credentials["email"]
    Password = credentials["password"]
    area_code = credentials["areacode"]
    phone_number = credentials["phonenumber"]
    parent_name = credentials["parentName"]
    child_name = credentials["childName"]
    Date_of_Birth = credentials["DOB"]
    login_type_email = credentials["loginType_email"]
    device_Type = credentials["deviceType"]
    time_zone = credentials["timezone"]
    otp_code = credentials["otpCode"]
    auth_type_signup = credentials["authType_signup"]

    payload = {"email": Email}
    print("New email user signup request...")

    # Step 1: Check if the email user is new or existing
    response = requests.post(EMAIL_LOGIN, json=payload, headers=AUTH_HEADERS)

    print(f"Signup response status: {response.status_code}")
    print(f"Signup response text: {response.text}")
    assert response.status_code == 200, f"Signup failed with status code: {response.status_code}"

    if response.headers.get("Content-Type", "").startswith("application/json"):
        response_data = response.json()
        print(f"Response JSON: {response_data}")
    else:
        print("Unexpected response type")
        print(f"Response text: {response.text}")
        assert False, f"Unexpected response type: {response.headers.get('Content-Type', '')}"

    user_details = response_data.get("body", {})
    email_newuser = user_details.get("isNewUser", True)

    if email_newuser:
        print("New user detected. Starting email verification...")

        # Step 2: Validate OTP
        payload_otp = {
            "email": Email,
            "otpCode": otp_code,  # Replace with dynamic OTP if applicable
            "authType": auth_type_signup
        }
        print("OTP Authentication started...")
        response = requests.post(OTP_VERIFICATION, json=payload_otp, headers=AUTH_HEADERS)
        print(f"OTP response status code: {response.status_code}")
        print(f"OTP response text: {response.text}")
        assert response.status_code == 200, "OTP validation failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"

        # Step 3: Complete Signup
        payload_signup = {
            "name": parent_name,
            "childName": child_name,
            "dateOfBirth": Date_of_Birth,
            "loginType": login_type_email,
            "deviceType": device_Type,
            "timezone": time_zone,
            "isGlobal": False,
            "phoneNumber":phone_number,
            "areaCode":area_code,
            "email":Email,
            "password":Password
        }
        print("Starting email user signup flow...")
        response = requests.post(NEW_USER_SIGNUP, json=payload_signup, headers=AUTH_HEADERS)
        print(f"Signup response status code: {response.status_code}")
        print(f"Signup response text: {response.text}")
        assert response.status_code == 200, "New email user registration failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"
        print("Signup completed for new email user.")
    else:
        print("Existing email detected. Logging in with email and password...")

    # Step 2: Login
        payload_login = {"email": Email, "password": Password, "loginType": login_type_email}
        response = requests.post(EMAIL_USER_LOGIN, json=payload_login, headers=AUTH_HEADERS)
        print(f"Login response status code: {response.status_code}")
        print(f"Login response text: {response.text}")
        assert response.status_code == 200, "Email login failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"

        print("Existing user detected so  user login  to email & Password")


