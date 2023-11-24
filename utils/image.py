import os
import cv2 as cv
import typing
import face_recognition
from fastapi import UploadFile
from PIL import UnidentifiedImageError
from exceptions.custom_exception import BadRequestException
from utils.file import save_image_file_to_student




class ModelImage():

    def __init__(self, images:typing.List[UploadFile]):

        self.images = images


    def validate_images(self):
            
        try:
            for img in self.images:

                image = face_recognition.load_image_file(img.file)

        except UnidentifiedImageError as e:

            raise BadRequestException(f"invalid image or image type: '{img.filename}'")
        
    
        
    def get_face_location(self, image:UploadFile):

        image = face_recognition.load_image_file(image.file)

        face_locations = face_recognition.face_locations(image)

        return face_locations
    


    def get_cropped_image(self, image:UploadFile):

        face_locations = self.get_face_location(image)

        top, right, bottom, left = face_locations[0]

        cropped_image = face_recognition.load_image_file(image.file)

        cropped_image = cropped_image[top:bottom, left:right]

        cropped_image = cv.cvtColor(cropped_image, cv.COLOR_BGR2RGB)


        return cropped_image


    def save_cropped_images(self, student_id:str):

        for img in self.images:

            cropped_image = self.get_cropped_image(img)

            file_path_for_student = os.path.join(os.getcwd(), f"static/data/{student_id}")

            os.makedirs(file_path_for_student, exist_ok=True)

            save_image_file_to_student(cropped_image, file_path_for_student)




    