import csv
import requests
import os
import time
import schedule  # Import the schedule library for scheduling tasks

# CSV Inputs
CSV_FILE_PATH = r"C:\Users\user\Downloads\user_student.csv"
REPORT_FILE_PATH = r"C:\Users\user\Downloads\user_report.csv"  
PDF_REPORT_FOLDER = r"C:\Users\user\Downloads"  #delete the pdf folder automatically

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
           # print("User created successfully:", response.json())
            user_details = response.json().get("body", {}).get("user", {})
            user_id = user_details.get("_id")
            token = user_details.get("token")
            return user_id, token ,"Success", None
        else:
           # print(f"Failed to create user: {response.status_code} - {response.text}")
            return None, None,"Failed", response.text
    except Exception as e:
        #print(f"Error in create_user: {e}")
        return None, None , "Failed" ,str(e)

# Function to delete a user
def delete_user(user_id, token):
    print(f"Deleting user ID: {user_id}")
    delete_url = f"{DELETE_API}?accountDetailId={user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.delete(delete_url, headers=headers)
        if response.status_code == 200:
            return "Success", None
        else:
            return "Failed", response.text
    except Exception as e:
       return "Failed" , str(e)
       
# Main execution
def main():
    try:
        if not os.path.exists(CSV_FILE_PATH):
            print(f"Error: CSV file not found at {
                CSV_FILE_PATH}")
            return

        report_data = []
        with open(CSV_FILE_PATH, "r") as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            if not rows:
                print("CSV file is empty.")
                return
            
            for index, row in enumerate(rows, start=1):
                 print(f"\nProcessing user {index}: {row}")

                # Map CSV fields to API keys
                 user_data = {**COMMON_PARAMS, **row}
            #print(f"Payload for API request: {user_data}")
                 

                # Create a user
                 user_id, token,create_status,create_error = create_user(user_data)

                # Delete the user if created successfully
                 if user_id and token:
                           delete_status,delete_error = delete_user(user_id, token)
                 else:
                           delete_status, delete_error = "Not Attempted", "Creation Failed"

             # log the report data
                 report_data.append({
                        
                         "Name": row.get("name",""),
                         "phoneNumber" : row.get("phoneNumber",""),
                         "User ID" : user_id or "NA",
                         "Creation Status" : create_status,
                         "Creation Error" :  create_error,
                         "Deletion Status" : delete_status,
                         "Deletion Error"  : delete_error,
                            })


    # Wrirte the report to the csv

        with open (REPORT_FILE_PATH , "w" , newline="") as report_file:

         fieldnames = ["Name" , "phoneNumber" , "User ID","Creation Status" , "Creation Error" , "Deletion Status" , "Deletion Error"]
         writer = csv.DictWriter(report_file, fieldnames=fieldnames)
         writer.writeheader()
         writer.writerows(report_data)
        print(f"Report  Generated successfully at : {REPORT_FILE_PATH}")

        # Waiting 10 minutes before deleteing the report
        print("waiting 10 minutes before deleting the report file...")
        time.sleep(600) # Wait for 600 seconds(10 Minutes)

        if os.path.exists(REPORT_FILE_PATH):
            os.remove(REPORT_FILE_PATH)
            print(f"Report file {REPORT_FILE_PATH} deleted successfully.")

    


    except FileNotFoundError :
        print(f"Error : CSV file not found at {CSV_FILE_PATH}")

    except requests.RequestException as e :
        print(f"Error during API Call: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the script daliy to run at a specfic time
def schedule_tasks():
    schedule.every().day.at("10.00").do(main) #Run at 9.00 AM
    schedule.every().day.at("18.00").do(main) #Run at 6.00 PM

    print("Scheduler started. Waiting for the schedule tasks..")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
