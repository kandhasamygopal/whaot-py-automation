import requests
from utils.config import BASE_URL,AUTH_HEADERS
from utils.helpers import read_credentials
import pytest

#Test credentials file path
CREDENTIALS_FILE = "credentials/forgotpassword_credentials.csv"  

#Forgot password function API's
# EMAIL_LOGIN = f"{BASE_URL}/user/account/check-user-exists-by-email"
EMAIL_RESEND_OTP = f"{BASE_URL}/user/account/email-resendOtp"
VAILDATE_EMAIL_OTP = f"{BASE_URL}/user/account/validate-email-otp"
RESET_PASSWORD = f"{BASE_URL}/user/account/reset-password"
EMAIL_USER_LOGIN = f"{BASE_URL}/user/account/login"



#Forgot Password function
@pytest.mark.parametrize("credentials" ,read_credentials(CREDENTIALS_FILE))
def test_forgotpassword_flow(credentials):
    Email = credentials["email"]
    Password = credentials["password"]

    payload = {"email":Email,"authType":"forgot-password"}

    print("forgot password email id entered....")

    response = requests.post(EMAIL_RESEND_OTP,json=payload,headers=AUTH_HEADERS)
    print(f"forgot password auth headers: {AUTH_HEADERS}")
    print(f"Forgot Password Status code : {response.status_code}")
    print(f"Forgot password status text: {response.text}")
    assert response.status_code == 200 , f"forgot password failed with status code: {response.status_code}"

    if response.headers.get("Content-Type", "").startswith("application/json"):
        response_data = response.json()
        print(f"Response JSON: {response_data}")
    else:
        print("Unexpected response type")
        print(f"Response text: {response.text}")
        assert False, f"Unexpected response type: {response.headers.get('Content-Type', '')}"

    #Step 2 : forgot password click verify the otp
    print ("Forgot password click OTP inti....")

    payload1 = {"email":Email, "otpCode":"123456", "authType":"signup"}

    response= requests.post(VAILDATE_EMAIL_OTP,json=payload1,headers=AUTH_HEADERS)
    print(f"Email resend headers: {AUTH_HEADERS}")
    print(f"Email resend OTP Staus code : {response.status_code}")
    print(f"Email resend OTP response text : {response.text}")
    assert response.status_code == 200 , f"forgot password OTP with status code: {response.status_code}"

    # Step 3 : Reset password update process
    print("Reset password process initi....")

    payload2 = {"password":Password,"email":Email}

    response = requests.put(RESET_PASSWORD, json=payload2,headers=AUTH_HEADERS)
    print(f"Reset password headers : {AUTH_HEADERS}")
    print(f"Reset Password status_code : {response.status_code}")
    print(f"Reset password response text : {response.text}")
    assert response.status_code == 200 , f"forgot reset password with status code: {response.status_code}"

    #Step 4 : After reset password updated and login 
    print ("login intit...")

    payload3 = {"email":Email, "password":Password, "loginType": "email"}

    response = requests.post(EMAIL_USER_LOGIN,json=payload3,headers=AUTH_HEADERS)
    print(f"After login : {AUTH_HEADERS}")
    print(f"After login user response status code : {response.status_code}")
    print(f"After login user response text: {response.text}")
    assert response.status_code == 200 , f"after login status code: {response.status_code}"