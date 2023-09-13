import os
import json
import asyncio
import requests
import threading 
from pprint import pprint
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api
from database.schema import Recordings
from dotenv import load_dotenv

load_dotenv()




cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),

  api_key = os.getenv("CLOUDINARY_API_KEY"), 

  api_secret = os.getenv("CLOUDINARY_API_SECRET"),

  secure = True
)




def handle_upload(recording_name, current_recording_path:str, camera, detected_user, time_of_detection):
      

	metadata = cloudinary.uploader.upload_large(current_recording_path, 
		resource_type = "video",
		public_id = f"python_security/{recording_name}",
		chunk_size = 6000000,
		eager = [
			{ "width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
			{ "width": 160, "height": 100, "crop": "crop", "gravity": "south",
				"audio_codec": "none"}],
		eager_async = True,
	)

	if metadata:
		save_metadata_to_database(recording_name, metadata["url"], time_of_detection)


		notify_request(camera, metadata["url"], detected_user, time_of_detection)



		os.remove(current_recording_path)
	

    



def save_metadata_to_database(recording_name:str, url:str, time_of_detection:datetime):

    recording = Recordings(name=recording_name, url=url, time_of_detection=time_of_detection)

    recording.save()



def notify_request(camera:int, metadata_url:str, detected_user:str, time_of_detection:datetime):

	url = "http://127.0.0.1:8000/user/notify"


	payload = json.dumps({
		"camera": camera,
		"link": metadata_url,
		"detected_user": detected_user,
		"time_of_detection": time_of_detection.strftime("%Y-%m-%d %I:%M%p")
	})


	response = requests.request("POST", url, data=payload)

	print("Request")




async def handle_delete(name:str):

	public_ids = [
		"python_security/2023-09-13__09-28-48", 
		"python_security/2023-09-13__09-25-38"
	]

	result = cloudinary.api.delete_resources(public_ids, resource_type="video", type="upload")

	print(result)


