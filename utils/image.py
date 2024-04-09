from operator import le
import os
import cv2
import typing
from typing import List
import face_recognition
from fastapi import UploadFile
from PIL import UnidentifiedImageError
from exceptions.custom_exception import BadRequestException
from utils.file import save_image_file_to_student


class ProcessImages:
    def __init__(self, images: typing.List[UploadFile]):
        self.images = images

        self.validated_images: List[ModelImage] = []

    def validate(self):
        try:
            for image in self.images:

                model_image = ModelImage(image)

                self.validated_images.append(model_image)

        except UnidentifiedImageError as e:
            raise BadRequestException(
                f"invalid image or image type: '{image.filename}'"
            )

    def get_face_encodings(self) -> typing.List:
        encodings = []

        for I in self.validated_images:

            encoding = face_recognition.face_encodings(I.image)

            if not encoding:
                raise BadRequestException(
                    f"No face found in image {I.filename}, please try another image"
                )

            encodings.append(encoding[0])

        return encodings

    def get_face_location(self, image: UploadFile):
        image = face_recognition.load_image_file(image.file)

        face_locations = face_recognition.face_locations(image)

        return face_locations

    def get_cropped_image(self, image: UploadFile):
        face_locations = self.get_face_location(image)

        top, right, bottom, left = face_locations[0]

        cropped_image = face_recognition.load_image_file(image.file)

        cropped_image = cropped_image[top:bottom, left:right]

        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

        return cropped_image


class ModelImage:
    def __init__(self, file: UploadFile) -> None:

        self.image = face_recognition.load_image_file(file.file)
        self.filename = file.filename
