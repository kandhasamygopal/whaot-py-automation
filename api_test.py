import csv
import requests
import os

# CSV Inputs
CSV_FILE_PATH = r"C:\Users\user\Downloads\user_student.csv"

# Verify the file path
print(f"CSV file path: {CSV_FILE_PATH}")

# API Endpoints
SIGNUP_API = "https://api-staging.whaot.com/user/account/student-signup"
DELETE_API = "https://api-staging.whaot.com/user/account/delete"

# Common Parameters
COMMON_PARAMS = {
    "areaCode": "+91",
    "deviceType": "web",
    "loginType": "phoneNumber",
    "isGlobal": False,
    "timezone": "652d2ab14eeb65744d58b772",
}

# Authentication Token
BEARER_TOKEN = "9ab6c59281c57b7db7929f978255788d8514da143bc63a00ebeae4b2fc2b2ee5eff7381e83f789cd67373135ca906ba72926c5dfc7146bad2d2438af4d2584bab2d9f7c1f5ba9a74c25a8781df72dfa339c872670df2261256f9a4c3d8d8317a410cdb7c24fb83aa6403a74afeeba8f92370d5672b842c89d2f5d9a84f1d4e2c92a8f5737d368609b14f60a7e0dfcac4d946b618f82f002c41ac04aab135d986"
AUTH_HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "content-type": "application/json",
}

# Function to create a user
def create_user(data):
    print(f"Creating user with data: {data}")
    try:
        response = requests.post(SIGNUP_API, json=data, headers=AUTH_HEADERS)
        print(f"Create User Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            print("User created successfully:", response.json())
            user_details = response.json().get("body", {}).get("user", {})
            user_id = user_details.get("_id")
            token = user_details.get("token")
            return user_id, token
        else:
            print(f"Failed to create user: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print(f"Error in create_user: {e}")
        return None, None

# Function to delete a user
def delete_user(user_id, token):
    print(f"Deleting user ID: {user_id}")
    delete_url = f"{DELETE_API}?accountDetailId={user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.delete(delete_url, headers=headers)
        print(f"Delete User Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            print(f"User deleted successfully: {user_id}")
        else:
            print(f"Failed to delete user {user_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error in delete_user: {e}")

# Main execution
def main():
    try:
        if not os.path.exists(CSV_FILE_PATH):
            print(f"Error: CSV file not found at {CSV_FILE_PATH}")
            return

        with open(CSV_FILE_PATH, "r") as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)
            if not rows:
                print("CSV file is empty.")
                return
            
            for row in rows:
                # Map CSV fields to API keys
                  user_data = {
                      **COMMON_PARAMS,
                     "name": row.get("Name"),  # Map 'Name' from CSV to 'name'
                    "phoneNumber": row.get("phoneNumber")  # Ensure phoneNumber is passed correctly
                }
                  print(f"Payload for API request: {user_data}")

                # Create a user
            user_id, token = create_user(user_data)

                # Optionally delete the user
            if user_id and token:
                    delete_user(user_id, token)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
