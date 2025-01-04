import requests
import json
import uuid

#Booking API
BOOKING_API = "https://api-staging.whaot.com/class/group/book"

# Example token
AUTH_TOKEN = "9ab6c59281c57b7db7929f978255788d8514da143bc63a00ebeae4b2fc2b2ee510dbf97b8c59e669fb91228bab3793003ac4eb017cbb28ddef569210c546d369d28f0dac13b446655e140fd61837df12878cd6a16e66c570d7f9dbc984ab7c09ff51d98087dc9f126d4b3c58ebe6ca2a6c0042079f03d5b8fdb95426cc4169e45bea6f7aca8a561517c1285867c57785bfdeb556f2e31dc86e28dd0e644f34736dd2a8cac23a23b4f5917f86c699d29d0439696f5e491ccd8fe04a6fd4b28ab30c9ace6f9143dff350b0eaf56d9e4822b4899bf89a940e5f5d34c28337294bd835d0c24c755b65f60fd6ac5ccc19982b4b364b6374a3397313e39c166658e6a7e5c2a1610a528f8269c29956ff28cddb0c88cb9ccffeeac52a5ddb1ce9eabb3e197262a9622c29e1fd128cf948f2902987380081a2647469bfef96c52c7fc1b15daf6252a286a8bcbea722e72b8dbde7bd0c9d5d98b8578142d0db806234c6b7"

#Razorpay Credentials
RAZORPAY_PREFERENCES_API = "https://api.razorpay.com/v2/standard_checkout/preferences"
RAZORPAY_KEY = "rzp_test_HZVGvRzMAmxJ0A"
RAZORPAY_SECRET = "your_test_key_secret"
RAZORPAY_SESSION_TOKEN = "C83844A3D5D1517E92FA0F1C3A79A6E2B57169397775D8DFB7000C0671E6A80A0B9D1083E182CBB968D78024A1807161A5628BCF1A8F1EB253D2825054B693FABAB394C35DF59ECA0E2A6A0A1984A50C9B3DE3B66302E13A5206700CDABD8C50009C9E71E8AAE974"
RAZORPAY_AUTH = (RAZORPAY_KEY,RAZORPAY_SECRET)

#Booking Payload
BOOKING_PAYLOAD = {
    "useWallet": False,
    "classId": "66cc697e93933d001181581a",
    "slots": [
        {
            "from": "2025-01-04T11:30:00.000Z",
            "to": "2025-01-04T13:30:00.000Z",
            "toActual": "2025-01-04T13:30:00.000Z",
            "zoneSelected": {"from": "05:00 PM", "to": "07:00 PM"}
        },
        {
            "from": "2025-01-05T11:30:00.000Z",
            "to": "2025-01-05T13:30:00.000Z",
            "toActual": "2025-01-05T13:30:00.000Z",
            "zoneSelected": {"from": "05:00 PM", "to": "07:00 PM"}
        }
    ],
    "coupon": [],
    "paymentGateway": "razorpay",
    "currency": "INR",
    "timezoneId": "652d2ab14eeb65744d58b772",
    "isSubscription": False,
    "planId": ""
}

#Razorpay preferences pay 
def generate_razorpay_payload():
    try:
        print("Starting Razorpay payload generation...")
        device_id = str(uuid.uuid4())
        print(f"Generated device Id: {device_id}")

        payload= {
               "query": [
                   {"resource": "checkout_version_config"},
                   {"resource": "merchant"},
                   {"resource": "merchant_features"},
                   {"resource": "downtime"},
                   {"resource": "customer"},
                   {"resource": "customer_tokens"},
                   {"resource": "truecaller"},
                   {"resource": "methods"},
                   {"resource": "experiments"},
                   {"resource": "offers"},
                   {"resource": "checkout_config"},
                   {"resource": "order"},
                   {"resource": "invoice"}
                    ],
                "query_params": {
                   "device_id": device_id,
                   "amount": 28253,  # Replace with the actual amount in paise
                 "currency": "INR",
                "order_id": "order_Pexodwr2Y8WZlf"
                 },
                       "action": "get"
                       }
        print("Payload succesfully Generated")
        print(f"Payload Details:/n{json.dumps(payload, indent=4)}")
        return payload

    except Exception as e :
        print(f"Error generating razorpay payload : {e}")
    return None



#Step1: book the class
def book_class():
    try:
        print("Booking class intiate...")
        headers = {
            "Authorization" : f"Bearer {AUTH_TOKEN}",
            "Content-type" : "application/json"
        }
        response=requests.post(BOOKING_API, json=BOOKING_PAYLOAD,headers=headers)

        if response.status_code == 200:
                print("booked class successfully.")
                return response.json()
        else:
                print(f"Failed to book the class: {response.status_code}-{response.text}")
                return None
        
    except Exception as e :
      print(f"Error to booking class:{e}")
      return None



#Step 2: Get Razorpay Preferences
def get_razorpay_preferences(payload):
    try:
          print("Generating Fetch razorpay preferences...")

          headers = {
               "Authorziation" : f"Bearer {RAZORPAY_SESSION_TOKEN}" ,
               "Content-type"  : "application/json"
          }
          
          response=  requests.post(RAZORPAY_PREFERENCES_API,json=payload,headers=headers,auth=RAZORPAY_AUTH)
          if response.status_code== 200 :
            print("Razorpay preferences fetch successfully.")
            return response.json()
          else:
            print(f"falied to fetch razorpay preferences : {response.status_code}-{response.text}")
            return None

    except Exception as e :
        print(f"Error fetch rezorpay prferences: {e}")
        return None


#Manin Function
if __name__ == "__main__" :
  
   #Book the class
   booking_response = book_class()

   if not booking_response:
     print("Class booking Failed.Exiting..")
     exit()

    # Generate Razorpay payload
   razorpay_payload = generate_razorpay_payload()
   if not razorpay_payload:
        print("Failed to generate Razorpay payload. Exiting...")
        exit()

   #Get Razorpay Preferences
   razorpay_preferences = get_razorpay_preferences(razorpay_payload)
   if not razorpay_preferences:
    print("Failed to fetch rezorpay preferences.Exiting..")
    exit()

    print("Booking and payment setup completed Successfully")
   

