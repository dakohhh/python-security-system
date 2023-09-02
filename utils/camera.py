import os
import cv2
import datetime
import numpy as np
import threading
import face_recognition
# from utils.video_func import adjust_text_size
from model import get_model



class Camera():

    cap = cv2.VideoCapture(0)
    video_writer = None


    def __init__(self):
        self.armed = False
        self.camera_thread = None
        self.model = get_model(os.path.join(os.getcwd(), "tf_face_model.h5"))

    def arm(self):
        # start camera thread
        if not self.armed and not self.camera_thread:

            self.camera_thread = threading.Thread(target=self.run)


        self.camera_thread.start()
        self.armed = True

    def disarm(self):
        
        self.camera_thread = None
        self.armed = False
        print("Camera is diarmed")

    def run(self):

        
        Camera.cap = cv2.VideoCapture(0)

        none_detected_counter = 0

        recording = False

        if self.armed:
            print("Camera has Started...")

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

                    print(prediction)


                if not recording:
        
                    recording = True

                    now = datetime.datetime.now()
                    today_date = now.strftime("%d-%m-%y-%H-%M-%S")

                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                
                    self.video_writer = cv2.VideoWriter(f'{today_date}.avi', fourcc, 5.0, (640, 480))

                self.video_writer.write(frame)

            else:
                none_detected_counter += 1

                if recording and none_detected_counter >= 50:

                    recording = False
                    self.video_writer.release()
                    self.video_writer = None
                

        if self.video_writer is not None:

                self.video_writer.release()

                self.video_writer = None





                

        

                



            
        

    

    


camera = Camera()

camera.arm()



    








# async def detect_faces(all_users):

#     global model

#     global class_list

#     model = await model

#     class_list = await class_list

#     FRAME_THICKNESS = 5

#     camera = cv2.VideoCapture(0)

#     while True:
#         success, frame = camera.read()

#         if not success:
#             break

#         locations = face_recognition.face_locations(frame)
    
#         for face_location in locations:

#             top, right, bottom, left = face_location

#             cropped_face = frame[top:bottom, left:right]


#             grayscale_image = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)


#             scaled_cropped_grayscale_image = cv2.resize(grayscale_image, (40, 40))

#             prediction = model.predict(np.array([scaled_cropped_grayscale_image]))

#             match_id =  class_list[np.argmax(prediction)]

#             firstname, lastname, is_blacklisted = next(((user.firstname, user.lastname, user.is_blacklisted) for user in all_users if str(user.id) == match_id), None)

#             match = f"{firstname} {lastname}"

#             color = [0, 255, 0]

#             cv2.rectangle(frame, (left, top), (right, bottom), color, FRAME_THICKNESS)

#             adjust_text_size(frame, match, face_location, IS_KNOWN)



#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     camera.release()