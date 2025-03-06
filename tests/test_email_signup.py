import requests
from utils.config import BASE_URL, AUTH_HEADERS ,INVITE_CODE
from utils.helpers import read_credentials , json_read_credentials
import pytest

# Email Login Function API Endpoints
EMAIL_LOGIN = f"{BASE_URL}/user/account/check-user-exists-by-email"
REFERRAL_CODE = f"{BASE_URL}/referral-code/{INVITE_CODE}"
RESEND_OTP = f"{BASE_URL}/user/account/email-resendOtp"
OTP_VERIFICATION = f"{BASE_URL}/user/account/validate-email-otp"
NEW_USER_SIGNUP = f"{BASE_URL}/user/account/student-signup"
EMAIL_USER_LOGIN = f"{BASE_URL}/user/account/login"

#Email user data stored file path
CREDENTIALS_FILE = "credentials/student_api_data.json"

# Test Function for email signup
@pytest.mark.parametrize("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_email_user_flow(credentials):
    Email = credentials["email"]["email_address"]
    Password = credentials["email"]["password"]
    area_code = credentials ["phone_number"]["areaCode"]
    phone_number = credentials["email"]["phone_number"]
    parent_name = credentials["parent_name"]
    child_name = credentials["child_name"]
    Date_of_Birth = credentials["child_dob"]
    login_type_email = credentials["login_method"]["type"][1]
    device_Type = credentials["device_type"]
    time_zone = credentials["timezone"]
    otp_code = credentials["otp_code"]
    auth_type_signup = credentials["auth_types"]["signup"]
    is_Invite_CodeVerified = credentials ["phone_number"]["isInviteCodeVerified"]
    child_lastname = credentials["child_LastName"]
    parent_lastname = credentials["parentsLastName"]
    phone_number = credentials ["email"]["phone_number"]
    inviteCode = credentials["invite_code"]

    payload = {"email": Email ,  "isInviteCodeVerified":is_Invite_CodeVerified }
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

        # Step 3 : Verify the Invite code valid or not
        response = requests.get(REFERRAL_CODE,headers=AUTH_HEADERS)
        assert response.status_code == 200 , "Invite code validation failed"
        assert response.json().get("message") == "RESPONSE_SUCCESS" , f"Excepted 'RESPONSE_SUCCESS' but got '{response.json().get('message')}'"
        response_data = response.json()
        print(f"the data invite code data {response_data}")
        invite_code = response_data.get("body",{})

        # Step 2: Verify resend OTP for new user
        payload2= {
            
            
            "email": Email,
            "authType" : auth_type_signup
            
        }
        print(f"Resend OTP Authentication Started...")
        response = requests.post(RESEND_OTP, json=payload2, headers=AUTH_HEADERS)
        print(f"OTP Auth headers: {AUTH_HEADERS}")
        print(f"OTP response status: {response.status_code}")
        print(f"OTP response text: {response.text}")
        assert response.status_code == 200, "Resend OTP validation failed"

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
            "password":Password,
            "parentsLastName" :parent_lastname  ,
            "childLastName" : child_lastname  ,
            "phoneNumber": phone_number,
            "areaCode": area_code,
            "inviteCode" : inviteCode
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


