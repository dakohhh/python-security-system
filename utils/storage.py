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
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


import os
from pprint import pprint
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
from typing import Union, Any

load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


class Upload:
    def __init__(self, private_name, file_name):
        self.private_name = private_name

        self.file_name = file_name

    def handle_upload(self, file: Union[str, Any]) -> dict:

        metadata = cloudinary.uploader.upload_large(
            file,
            resource_type="video",
            public_id=f"{self.private_name}/{self.file_name}",
            chunk_size=6000000,
            eager=[
                {"width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
                {
                    "width": 160,
                    "height": 100,
                    "crop": "crop",
                    "gravity": "south",
                    "audio_codec": "none",
                },
            ],
            eager_async=True,
        )

        return metadata

    async def handle_delete(self):
        public_ids = [f"{self.private_name}/{self.file_name}"]

        image_delete_result = cloudinary.api.delete_resources(
            public_ids, resource_type="image", type="upload"
        )

        return image_delete_result


class SecurityUpload(Upload):
    private_name = "chowgoo"

    def __init__(self, file_name: str):
        super().__init__(self.private_name, file_name)







def handle_log(
    recording_name,
    current_recording_path: str,
    camera,
    detected_user,
    time_of_detection,
):
    metadata = cloudinary.uploader.upload_large(
        current_recording_path,
        resource_type="video",
        public_id=f"python_security/{recording_name}",
        chunk_size=6000000,
        eager=[
            {"width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
            {
                "width": 160,
                "height": 100,
                "crop": "crop",
                "gravity": "south",
                "audio_codec": "none",
            },
        ],
        eager_async=True,
    )

    if metadata:
        save_metadata_to_database(recording_name, metadata["url"], time_of_detection)

        notify_request(camera, metadata["url"], detected_user, time_of_detection)

        os.remove(current_recording_path)


