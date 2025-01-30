import requests
import json
import pytest
from utils.config import BASE_URL,AUTH_HEADERS
from utils.helpers import read_credentials ,json_read_credentials


# Sunbscription Booking API's function
USER_LOGIN = f"{BASE_URL}/user/account/check-user-exists-by-phone"
OTP_VERIFICATION = f"{BASE_URL}/user/account/validate-phone-otp"
PHONE_LOGIN = f"{BASE_URL}/user/account/student-signup"
FREE_TRAIL = f"{BASE_URL}/enable-free-trail"
SUBSCRIPTION_ENROLL = f"{BASE_URL}/subscription-booking/enroll"

#Test credentials file path
CREDENTIALS_FILE = "credentials/student_api_data.json"

@pytest.fixture(scope="module")
def user_data():
    """Fixture to read user credentials from JSON."""
    return read_credentials(CREDENTIALS_FILE)

@pytest.fixture(scope="module")
def create_user():
    """Fixture to store user details after creation."""
    return {}

@pytest.fixture(scope="module")
def Existing_user():
    """Fixture to store user details after creation."""
    return {}

# Test Function
@pytest.mark.parametrize("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_user_flow(credentials,create_user,Existing_user):
    # Step 1: Check if this user is new or existing
    area_code = credentials["phone_number"]["areaCode"]
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

    payload = {"areaCode":area_code,"phoneNumber":phone_number} 
    (f"creating new user signup request...")
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
        print("New user detected. Redirected to signup flow...")

        # Step 2: Verify OTP for new user
        payload2= {
            "phoneNumber": phone_number,
            "areaCode": area_code,
            "otpCode": otp_code,  # Replace with dynamic OTP if applicable
            "authType": authType_signup,
        }
        print(f"OTP Authentication Started...")
        response = requests.post(OTP_VERIFICATION, json=payload2, headers=AUTH_HEADERS)
        print(f"OTP Auth headers: {AUTH_HEADERS}")
        print(f"OTP response status: {response.status_code}")
        print(f"OTP response text: {response.text}")
        assert response.status_code == 200, "OTP validation failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"

        # Step 3: Test new user signup
        payload3 = {
            "name": parent_name,
            "childName": child_name,
            "dateOfBirth": Date_of_Birth,
            "loginType": login_type_phone_number,
            "deviceType": device_Type,
            "timezone": time_zone,
            "isGlobal": False,
            "phoneNumber": phone_number,
            "areaCode": area_code,
        }
        print(f"New user signup flow started...")
        response = requests.post(PHONE_LOGIN, json=payload3, headers=AUTH_HEADERS)
        print(f"New user Auth headers: {AUTH_HEADERS}")
        print(f"New user Signup response status: {response.status_code}")
        print(f"New User Signup response text: {response.text}")
        assert response.status_code == 200, "Signup failed"
        assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"

        
        response_data = response.json()
        assert response_data.get("message") == "Success" , f"unexpected response message:{response_data}"
    
        User_details = response_data.get("body",{}).get("user",{})
        User_id = User_details.get("_id")
        token = User_details.get("token")

        assert User_id # user_ID not found in response
        assert token #Token not found in response

    # Store the UserID and token for later use
        create_user[phone_number] = {"user_id":User_id,"token":token}
        print("New user signup completed successfully.")


    else:
        print("Existing user detected. Logging in...")

        # Step 2: Verify OTP for existing user
        payload4 = {
            "phoneNumber": phone_number,
            "areaCode": area_code,
            "otpCode": otp_code,  # Replace with dynamic OTP if applicable
            "authType": authType_login,
        }
        print(f"If Existing user login started...")
        response = requests.post(OTP_VERIFICATION, json=payload4, headers=AUTH_HEADERS)
        print(f"Existing user Auth headers: {AUTH_HEADERS}")
        print(f"Existing user Signup response status: {response.status_code}")
        print(f"Existing user Signup response text: {response.text}")
        assert response.status_code == 200, f"Expected 'Success' but got '{response.json().get('message')}'"

        is_verified = response.json().get("body", {}).get("isVerified", False)
        assert is_verified, "User verification failed"
       

        response_data = response.json()
        assert response_data.get("message") == "Success" , f"unexpected response message:{response_data}"
    
        Existing_User_details = response_data.get("body",{}).get("user",{})
        Existing_User_id = Existing_User_details.get("_id")
        Existing_user_token = Existing_User_details.get("token")

        assert Existing_User_id # user_ID not found in response
        assert Existing_user_token #Token not found in response

        # Store the Existing UserID and token for later use
        Existing_user[phone_number] = {"user_id":Existing_User_id,"token":Existing_user_token}
        print("Existing user login completed successfully.")

# Free trail enabled for new created user
@pytest.mark.parametrize ("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_free_trail_enabled(credentials,create_user,Existing_user):
 
 print("Test to create new user booking free trail enabled using store credentials...")

 phone_number = credentials["phone_number"]["phone_number"]
 user_info = create_user.get(phone_number) or Existing_user.get(phone_number)
 assert user_info , f"No Stored data found for {credentials['phone_number']['phone_number']}"
 token = user_info["token"]

 assert token # No token for user free trail enabled function

 headers = {"Authorization" : f"Bearer {token}"}

 reponse = requests.put(FREE_TRAIL,headers=headers)
 print(f"free trail response auth : {reponse.headers}")
 print(f"free trail enabled status: {reponse.status_code}")
 print(f"free trail response text : {reponse.text}")
 reponse.status_code == 200 , f"falied to free trail enabled : {reponse.text}"

 print("New user free trail option enabled succesfully enabled..")

# New free trail user after enroll the new class

@pytest.mark.parametrize ("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_subscribtion_enroll(credentials,create_user,Existing_user):   
   print("New user enroll the new class...")
   phone_number = credentials['phone_number']['phone_number']
   assignment_id = credentials["assignment_id"]

   payload = {
           "assignmentId": assignment_id
   }
   print(f"Print the class assignmentId : {assignment_id}")
   user_info = create_user.get(phone_number) or Existing_user.get(phone_number)
   assert user_info , f"No stored data found for {credentials['phone_number']['phone_number']}"
   token = user_info["token"]
   headers = {"Authorization" : f"Bearer {token}"}

   response =requests.post(SUBSCRIPTION_ENROLL,json=payload,headers=headers)
   print(f"Subscription enroll : {headers}")
   print(f"Subscription enrolled response status : {response.status_code}")
   print(f"Subscribtion enroll response text : {response.text}")
   assert response.status_code == 200 , f"failed to subscribrtion enrolled: {response.text}"

   print("Subscribtion enroll success...")


