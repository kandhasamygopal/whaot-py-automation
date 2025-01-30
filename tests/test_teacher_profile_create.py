import requests
import pytest
from utils.config import BASE_URL , ADMIN_AUTH_HEADERS
from utils.helpers import json_read_credentials


# Test API's function teacher profile create
TEACHER_CREATE_API = f"{BASE_URL}/admin/teacher/create"


# Teacher profile create data stored file location
CREDENTIALS_FILE = "credentials/teacher_create_api_data.json"


# Test function for teacher create profile create
@pytest.mark.parametrize("credentials",json_read_credentials(CREDENTIALS_FILE))
def test_teacher_profile_create_flow(credentials):
    
    teacher_name = credentials["name"]
    area_code = credentials["areaCode"]
    phone_number = credentials["phoneNumber"]
    teacher_email = credentials["email"]
    timezone = credentials["timezone"]
    address_details = credentials["addressDetails"]["address"]
    about_me = credentials["aboutMe"]
    langu_ages = credentials["languages"]
    teacher_picture = credentials["picture"]
    teacher_introVideosrc = credentials["introVideoSrc"]
    teacher_qualification = credentials["qualification"]
    teacher_studentTaught = credentials["studentsTaught"]
    teacher_experience = credentials["experience"]
    teacher_profile_url = credentials["teacherProfileUrl"]
    teacher_panNumber = credentials["panNumber"]
    teacher_panImage = credentials["panImage"]
    teacher_introVideo = credentials["introVideo"]
    subscription_availability = [
                                   {
                                       "dayOfWeek": b["dayOfWeek"],
                                        "timeSlots" :[
                                        {
                                            "startTime":t["startTime"],
                                            "endTime" : t["endTime"]
                                        } for t in b["timeSlots"]
                                      ]                                  
                              } for b in credentials ["subscriptionAvailability"]
                               ]
    
    perHour_Rate = credentials ["perHourRate"] 
    bio_graphy        = credentials ["bio"]   
    
                      
    class_Preferences = [
                            
                        {
                          "classId": class_pref["classId"],
                          "className":class_pref ["className"],
                             "levels": [
                                 {
                                    "levelId":level["levelId"],
                                    "levelName":level["levelName"],
                                 
                                    "modules": [
                                           {
                                            "moduleId": module["moduleId"],
                                            "moduleName":module["moduleName"]
                                            }  for module in level["modules"]                        
                                               ]
                            } for level in class_pref["levels"]                 
                                         ]        
                                } for class_pref in credentials["classPreferences"]
                        ]    
    payload = {

    "name": teacher_name ,
    "areaCode": area_code ,
    "phoneNumber": phone_number,
    "email": teacher_email,
    "timezone":timezone,
    "addressDetails":address_details,
    "aboutMe": about_me,
    "languages": langu_ages,
    "picture": teacher_picture,
    "introVideoSrc": teacher_introVideosrc,
    "qualification": teacher_qualification,
    "studentsTaught": teacher_studentTaught,
    "experience": teacher_experience,
    "teacherProfileUrl": teacher_profile_url,
    "panNumber": teacher_panNumber,
    "panImage": teacher_panImage,
    "introVideo": teacher_introVideo,
    "subscriptionAvailability": subscription_availability,
    "perHourRate":perHour_Rate ,
     "bio" : bio_graphy ,
    "classPreferences": class_Preferences       
    
           }
    
    print("Teacher profile creates payload JSON file data inti......")

    response = requests.post(TEACHER_CREATE_API,json=payload,headers = ADMIN_AUTH_HEADERS)
    print(f"Teacher profile create API response status: {response.status_code}")
    print(f"Teacher profile create API response text: {response.text}")
    assert response.status_code == 200 , "Teacher profile registration failed"
    assert response.json().get("message") == "Success" , f"Expected 'Success' but got '{response.json().get('message')}'"
    print("Teacher profile created Successfully")




















    
    
      
      
  
    