import requests
from utils.config import BASE_URL ,ADMIN_AUTH_HEADERS
from utils.helpers import json_read_credentials
import pytest


# Admin panel class create API's
UPLOAD_IMAGE_API = f"{BASE_URL}/user/upload/images"
UPLOAD_VIDEOS_API = f"{BASE_URL}/user/upload/videos"
CLASS_CREATE_API= f"{BASE_URL}/subscription-class/create"

# Class-create-api-data store data file location
CREDENTIALS_FILE = "credentials/class_create_api_data.json"

#Test function for class create 
@pytest.mark.parametrize("credentials" , json_read_credentials(CREDENTIALS_FILE))
def test_for_class_create (credentials):
    class_Type = credentials["classType"]
    class_Title = credentials["classTitle"]
    Tag_line = credentials["tagLine"]
    class_url = credentials["classUrl"]
    category_id = credentials["category"]["_id"]
    category_name = credentials["category"]["name"]
    language = credentials["languages"]
    hash_Tag = credentials["hashTag"]
    Class_Theme = credentials["classTheme"]
    dashboard_card_Theme = credentials["dashboardCardTheme"]
    heading_color = credentials["headingColor"]
    text_color = credentials["textColor"]
    tag_Line_color = credentials["tagLineColor"]
    aeroplane_color = credentials["aeroplaneColor"]
    rating_details = credentials["ratingDetails"]["noOfRatings"]
    students_Enrolled_count = credentials["studentsEnrolledCount"]
    whatYou_Will_learn = credentials["whatYouWillLearn"]
    des_cription = credentials["description"]
    class_cover_Image = credentials["classCoverImage"]["attachmentId"]
    dashboard_card_Image = credentials["dashboardCardImage"]["attachmentId"]
    class_Image = credentials["classImages"]
    class_videos = credentials["classVideos"]
    dashboard_key_points = credentials["dashboardKeyPoints"]
    class_key_points = credentials["classKeyPoints"]
    batches = [
              {
                 "batchName": b["batchName"],
                 "status": b["status"],
                 "timings": [
              {
                "dayOfWeek": t["dayOfWeek"],
                "startTime": t["startTime"],
                "endTime": t["endTime"]
            } for t in b["timings"]
            ],
            "capacity": b["capacity"],  # Accessing capacity within each batch
            "durationInSeconds": b["durationInSeconds"] # Fetching duration directly from JSON
            } for b in credentials["batches"] 
            ]
   
    curriculum = [
                 {
                  "name": level["name"],
                  "minAge": level["minAge"],
                  "maxAge": level["maxAge"],
                  "totalChapterCount": level["totalChapterCount"],
               "modules": [
            {
                "name": module["name"],
                "moduleTitleBgColor": module["moduleTitleBgColor"],
                "moduleBgColor": module["moduleBgColor"],
                "chapters": [
                    {"name": chapter["name"], "description": chapter["description"]}
                    for chapter in module["chapters"]
                ]
            } for module in level["modules"]
        ]
    } for level in credentials["curriculum"]["levels"]
             ]
  
    chapter_names = credentials["chapterNames"]

    payload = {
    "classType": class_Type,
    "classTitle": class_Title,
    "tagLine": Tag_line,
    "classUrl": class_url,
    "category": [{"_id": category_id, "name": category_name}],
    "languages": language,
    "hashTag": hash_Tag,
    "classTheme": Class_Theme,
    "dashboardCardTheme": dashboard_card_Theme,
    "headingColor": heading_color,
    "textColor": text_color,
    "tagLineColor": tag_Line_color,
    "aeroplaneColor": aeroplane_color,
    "ratingDetails": {
        "rating": 4.9,
        "noOfRatings": rating_details
    },
    "studentsEnrolledCount": students_Enrolled_count,
    "whatYouWillLearn": whatYou_Will_learn,
    "description": des_cription,
    "classCoverImage": {
        "url": "https://whaot-dev-static.s3.ap-south-1.amazonaws.com/static/images/2025/1/28/b5991f8d-b7b6-4d99-a515-5fa1b5356f2d.jpg",
        "attachmentId": class_cover_Image
    },
    "dashboardCardImage": {
        "url": "https://whaot-dev-static.s3.ap-south-1.amazonaws.com/static/images/2025/1/28/33008168-d91d-4d86-b4d5-00e517de9678.jpg",
        "attachmentId": dashboard_card_Image
    },
    "classImages": class_Image,
    "classVideos": class_videos,
    "dashboardKeyPoints": dashboard_key_points,
    "classKeyPoints": class_key_points,
    "batches": batches,
    "curriculum": {
        "levels": curriculum
            
    },
     
    "chapterNames": chapter_names
}

    
    print("Class create API payload upload function started...")
    response = requests.post(CLASS_CREATE_API, json=payload, headers=ADMIN_AUTH_HEADERS)
    print(f"Class create API response status: {response.status_code}")
    print(f"Class create API response text: {response.text}")
    assert response.status_code == 200, "Class creation failed"
    assert response.json().get("message") == "Success", f"Expected 'Success' but got '{response.json().get('message')}'"
    print("New Class created successfully")
