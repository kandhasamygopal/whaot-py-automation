import requests
import json
import pytest
from utils.config import BASE_URL,AUTH_HEADERS
from utils.helpers import read_credentials ,json_read_credentials


# Sunbscription Booking API's function
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

#Test function for booking API's enroll and unroll
@pytest.mark.parametrize("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_new_user_created(credentials,create_user):
    area_code = credentials["areacode"]
    phone_number = credentials["phonenumber"]
    parent_name = credentials["parentName"]
    child_name = credentials["childName"]
    Date_of_Birth = credentials["DOB"]
    login_Type_phone_number = credentials["loginType_phoneNumber"]
    device_Type = credentials["deviceType"]
    time_zone = credentials["timezone"]
    # otp_code = credentials["otpCode"]
    # auth_Type = credentials["authType"]


    payload = {
            "name": parent_name,
            "childName": child_name,
            "dateOfBirth": Date_of_Birth,
            "loginType": login_Type_phone_number,
            "deviceType": device_Type,
            "timezone": time_zone,
            "isGlobal": False,
            "phoneNumber": phone_number,
            "areaCode": area_code,
        }
    print(f"New PhoneNumber user detected signup data uploading...")
    response = requests.post(PHONE_LOGIN,json=payload,headers=AUTH_HEADERS)
    print(f"New PhoneNumber user Auth: {AUTH_HEADERS}")
    print(f"NewPhoneNumber Status: {response.status_code}")
    print(f"NewPhoneNumber text:{response.text}")
    print(f"NewPhoneNumber headers: {response.headers}")
    assert response.status_code == 200 , f"Failed to create user: {response.text}"
    assert response.json().get("message") == "Success", f"expect 'Success' but got '{response.json().get('message')}'"

    print("New PhoneNumber user Signup completed.....")

    response_data = response.json()
    assert response_data.get("message") == "Success" , f"unexpected response message:{response_data}"
    
    User_details = response_data.get("body",{}).get("user",{})
    User_id = User_details.get("_id")
    token = User_details.get("token")

    assert User_id # user_ID not found in response
    assert token #Token not found in response

    # Store the UserID and token for later use
    create_user[credentials["phonenumber"]] = {"user_id":User_id,"token":token}

# Free trail enabled for new created user
@pytest.mark.parametrize ("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_free_trail_enabled(credentials,create_user):
 
 print("Test to create new user booking free trail enabled using store credentials...")

 user_info = create_user.get(credentials["phonenumber"])
 assert user_info , f"No Stored data found for {credentials['phonenumber']}"
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
def test_subscribtion_enroll(credentials,create_user):   
   print("New user enroll the new class...")
   assignment_id = credentials["assignmentid"]

   payload = {
           "assignmentId": assignment_id
   }
   user_info = create_user.get(credentials["phonenumber"])
   assert user_info , f"No stored data found for {credentials["phonenumber"]}"
   token = user_info["token"]
   headers = {"Authorization" : f"Bearer {token}"}

   print("New user enroll the new class using assignment id")
   response =requests.post(SUBSCRIPTION_ENROLL,json=payload,headers=headers)
   print(f"Subscription enroll : {headers}")
   print(f"Subscription enrolled response status : {response.status_code}")
   print(f"Subscribtion enroll response text : {response.text}")
   assert response.status_code == 200 , f"failed to subscribrtion enrolled: {response.text}"


