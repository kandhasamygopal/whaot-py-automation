import requests
import json  # Ensure JSON library is imported
from utils.config import BASE_URL, AUTH_HEADERS , INVITE_CODE
from utils.helpers import read_credentials , json_read_credentials
import pytest

# API Endpoints
USER_LOGIN = f"{BASE_URL}/user/account/check-user-exists-by-phone"
REFERRAL_CODE = f"{BASE_URL}/referral-code/{INVITE_CODE}"
RESEND_OTP = f"{BASE_URL}/user/account/resendOtp"
OTP_VERIFICATION = f"{BASE_URL}/user/account/validate-phone-otp"
NEW_USER_SIGNUP = f"{BASE_URL}/user/account/student-signup"

#Test credentials file path
CREDENTIALS_FILE = "credentials/student_api_data.json" 

# Test Function
@pytest.mark.parametrize("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_user_flow(credentials):
    # Step 1: Check if this user is new or existing
    area_Code = credentials["phone_number"]["areaCode"]
    phone_number = credentials["phone_number"]["phone_number"]
    otp_code = credentials["otp_code"]
    authType_signup = credentials["auth_types"]["signup"]
    parent_name = credentials["parent_name"]
    child_name = credentials["child_name"]
    Date_of_Birth = credentials["child_dob"]
    login_type_phone_number = credentials["login_method"]["type"][2]
    device_Type = credentials["device_type"]
    time_zone = credentials["timezone"]
    authType_login = credentials["auth_types"]["login"]
    is_Invite_CodeVerified = credentials ["phone_number"]["isInviteCodeVerified"]
    child_lastname = credentials["child_LastName"]
    parent_lastname = credentials["parentsLastName"]
    email_address = credentials ["email"]["email_address"]
    inviteCode = credentials["invite_code"]

    payload = {"areaCode":area_Code,"phoneNumber":phone_number , "isInviteCodeVerified":is_Invite_CodeVerified} 
    (f"ending new user signup request...")
    response = requests.post(USER_LOGIN, json=payload, headers=AUTH_HEADERS)  # Fixed issue here
    print(f"API end point:{USER_LOGIN}")
    print(f"Auth headers: {AUTH_HEADERS}")
    print(f"Signup response status: {response.status_code}")
    print(f"Signup response text: {response.text}")
    print(f"Response headers: {response.headers}")
    assert response.status_code == 200,  f"Signup failed with status code {response.status_code}"
    

    # Check if response is JSON
    if response.headers.get("Content-Type", "").startswith("application/json"):
      response_data = response.json()
      print(f"Response JSON: {response_data}")
    # Process the JSON response
    else:
        print("Unexpected response type:")
        print(response.text)  # Debugging purposes
        print(f"response headers: {response.headers}")
        assert False, f"API returned an unexpected response type: {response.headers.get('Content-Type', '')}"


    # Proceed with processing the JSON response
    user_details = response_data.get("body", {})
    is_new_user = user_details.get("isNewUser", True)


    if is_new_user:
        print("New user detected. Redirected to INVITE CODE enter screen...")

        # Step 3 : Verify the Invite code valid or not
        response = requests.get(REFERRAL_CODE,headers=AUTH_HEADERS)
        assert response.status_code == 200 , "Invite code validation failed"
        assert response.json().get("message") == "RESPONSE_SUCCESS" , f"Excepted 'RESPONSE_SUCCESS' but got '{response.json().get('message')}'"
        response_data = response.json()
        print(f"the data invite code data {response_data}")
        invite_code = response_data.get("body",{})

        # Step 2: Verify resend OTP for new user
        payload2= {
            
            "areaCode": area_Code,
            "phoneNumber": phone_number,
            "deviceType" : device_Type
            
        }
        print(f"Resend OTP Authentication Started...")
        response = requests.post(RESEND_OTP, json=payload2, headers=AUTH_HEADERS)
        print(f"OTP Auth headers: {AUTH_HEADERS}")
        print(f"OTP response status: {response.status_code}")
        print(f"OTP response text: {response.text}")
        assert response.status_code == 200, "Resend OTP validation failed"
        

        # Step 4: Test new user validate phone OTP
        payload5 = {
            
            "areaCode" : area_Code ,
            "authType" : authType_signup ,
            "otpCode"  : otp_code , # Replace OTP dynamic code paste here
            "phoneNumber" : phone_number    
        }
        print(f"OTP Verification Authentication Started...")
        response = requests.post(OTP_VERIFICATION, json=payload5, headers=AUTH_HEADERS)
        print(f"OTP Auth headers: {AUTH_HEADERS}")
        print(f"OTP response status: {response.status_code}")
        print(f"OTP response text: {response.text}")
        assert response.status_code == 200, "OTP verification validation failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"
        is_verified = response.json().get("body", {}).get("isVerified", True)
        assert is_verified, "new user verification failed"
        print("New user signup flow started")

        # Step 3: Test new user signup
        payload3 = {
            "name": parent_name,
            "childFirstName": child_name,
            "dateOfBirth": Date_of_Birth,
            "loginType": login_type_phone_number,
            "deviceType": device_Type,
            "timezone": time_zone,
            "isGlobal": False,
            "parentsLastName" :parent_lastname  ,
            "childLastName" : child_lastname  ,
            "phoneNumber": phone_number,
            "areaCode": area_Code,
            "email" : email_address  ,
            "inviteCode" : inviteCode
        }
        print(f"New user signup flow started...")
        response = requests.post(NEW_USER_SIGNUP, json=payload3, headers=AUTH_HEADERS)
        print(f"New user Auth headers: {AUTH_HEADERS}")
        print(f"New user Signup response status: {response.status_code}")
        print(f"New User Signup response text: {response.text}")
        assert response.status_code == 200, "Signup failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"

        print("Signup completed for new user.")

    else:
        print("Existing user detected. Logging in...")

        # Step 2: Verify OTP for existing user
        payload4 = {
            "phoneNumber": phone_number,
            "areaCode": area_Code,
            "otpCode": otp_code,  # Replace with dynamic OTP if applicable
            "authType": authType_login,
        }
        print(f"If Existing user login started...")
        response = requests.post(OTP_VERIFICATION, json=payload4, headers=AUTH_HEADERS)
        print(f"Existing user Auth headers: {AUTH_HEADERS}")
        print(f"Existing user Signup response status: {response.status_code}")
        print(f"Existing user Signup response text: {response.text}")
        assert response.status_code == 200, f"Expected 'Success' but got '{response.json().get('message')}'"
        print(f"Signup failed with response: {response.text}")

        is_verified = response.json().get("body", {}).get("isVerified", False)
        assert is_verified, "User verification failed"
        print("Login successful for existing user.")
