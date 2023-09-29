import os
import cv2
import datetime
import threading
import numpy as np
import face_recognition
from .model import get_model, SecurityModel
from .video import adjust_text_size
from .storage import handle_upload







class Camera():

    cap = cv2.VideoCapture(0)
    video_writer = None

    FRAME_THICKNESS = 5


    def __init__(self):
        self.armed = False
        self.camera_thread = None
        self.camera_loc = 0
        self.class_list = SecurityModel.get_class_dict(os.path.join(os.getcwd(), "models/class_dict.json"))
        self.model = get_model(os.path.join(os.getcwd(), "models/tf_face_model.h5"))

        print("Camera has started...")

    def arm(self):

        # Arm Camera and Initialize Camera Thread
        if not self.armed and not self.camera_thread:

            self.camera_thread = threading.Thread(target=self.run)


        self.camera_thread.start()
        self.armed = True

    def disarm(self):

        # Disarm Camera and Initialize Camera Thread
        
        self.camera_thread = None
        self.armed = False
        print("Camera is disarmed")

    def run(self):

        
        Camera.cap = cv2.VideoCapture(0)

        none_detected_counter = 0

        recording = False

        if self.armed:
            print("Camera is armed")

        while self.armed:


            success, frame = self.cap.read()

            if not success:
                break


            locations = face_recognition.face_locations(frame)

            scaled_cropped_grayscale_image = None

            if locations:

                none_detected_counter = 0


                for face_location in locations:

                    top, right, bottom, left = face_location

                    cropped_face = frame[top:bottom, left:right]
            

                    grayscale_image = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)


                    scaled_cropped_grayscale_image = cv2.resize(grayscale_image, (40, 40))

                    prediction = self.model.predict(np.array([scaled_cropped_grayscale_image]))

                    FRAME_THICKNESS = 5

                    color = (0, 200, 0)

                    match_id =  self.class_list[np.argmax(prediction)]
                    
                    cv2.rectangle(frame, (left, top), (right, bottom), color, FRAME_THICKNESS)
                    
                    adjust_text_size(frame, match_id, face_location)

                    # firstname, lastname, is_blacklisted = next(((user.firstname, user.lastname, user.is_blacklisted) for user in all_users if str(user.id) == match_id), None)


                if not recording:
        
                    recording = True

                    now = datetime.datetime.now()
                    
                    recording_name = now.strftime("%Y-%m-%d__%H-%M-%S")

                    # time_of_detection = now.strftime("%Y-%m-%d %I:%M%p")

                    time_of_detection = now

                    fourcc = cv2.VideoWriter_fourcc(*'XVID')

                    recording_path = os.path.join(os.getcwd(), f"videos/{recording_name}.avi")
                
                    self.video_writer = cv2.VideoWriter(recording_path, fourcc, 5.0, (640, 480))

                self.video_writer.write(frame)

            else:
                none_detected_counter += 1    # Increment the counter

                if recording and none_detected_counter >= 50:    # If after 50 frames the person is not detected, stop recording and release the video write

                    recording = False
                    self.video_writer.release()
                    self.video_writer = None


                    upload_thread = threading.Thread(target=handle_upload, 
                        args=(
                            recording_name, 
                            recording_path, 
                            self.camera_loc, 
                            "Wisdom Dakoh", 
                            time_of_detection
                        )
                    )

                    upload_thread.start()

                

        if self.video_writer is not None:

                self.video_writer.release()

                self.video_writer = None

            






