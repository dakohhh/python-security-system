import os
from typing import List
import cv2
from datetime import datetime
import threading
import numpy as np
import face_recognition
from client import send_notify_request
from database.schema import UniversityMember
from utils.interface import CreateLog
from repository.logs import LogsRepository
from utils.func import threshold_compare
from utils.notifications import notify_users_by_phone


class Camera:
    cap = cv2.VideoCapture(0)

    video_writer = None

    FRAME_THICKNESS = 5

    def __init__(self, members):
        self.armed = False
        self.members: List[UniversityMember] = members
        self.camera_thread = None
        self.camera_loc = 0

        self.threshold = 60

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

            unknown_faces_image_encodings = face_recognition.face_encodings(frame)

            if unknown_faces_image_encodings:
                none_detected_counter = 0

                for (
                    unknown_face_encoding
                ) in (
                    unknown_faces_image_encodings
                ):  # Iterate over each of the encoded faces detected on frame:
                    for member in self.members:
                        results = face_recognition.compare_faces(
                            np.array(member.encodings), unknown_face_encoding
                        )

                        if threshold_compare(results) >= self.threshold:
                            # Log Time of detection for member

                            print("Member detected")

                            now = datetime.now()

                            log = CreateLog(member, str(self.camera_loc), False, now)

                            # create_log_thread = threading.Thread(target=LogsRepository.create_log, args=(log, ))

                            # create_log_thread.start()

                            # Start recording if not already recording
                            if not recording:
                                recording = True
                                recording_name = (
                                    now.strftime("%Y-%m-%d__%H-%M-%S") + "_member.avi"
                                )
                                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                                recording_path = os.path.join(
                                    os.getcwd(), "recordings", recording_name
                                )
                                self.video_writer = cv2.VideoWriter(
                                    recording_path, fourcc, 5.0, (640, 480)
                                )

                            self.video_writer.write(frame)

                        else:
                            print("Unkwnown detected")

                            # Log Time of detection for unkwnown person

                            now = datetime.now()

                            log = CreateLog(None, str(self.camera_loc), True, now)

                            # Start recording if not already recording
                            if not recording:
                                recording = True
                                recording_name = (
                                    now.strftime("%Y-%m-%d__%H-%M-%S") + "_unknown.avi"
                                )
                                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                                recording_path = os.path.join(
                                    os.getcwd(), "recordings", recording_name
                                )
                                self.video_writer = cv2.VideoWriter(
                                    recording_path, fourcc, 5.0, (640, 480)
                                )

                            self.video_writer.write(frame)

            elif recording:
                none_detected_counter += 1  # Increment the counter

                if (
                    none_detected_counter >= 50
                ):  # Stop recording after 50 frames without detection
                    print("Recording stopped")

                    print(log)

                    recording = False
                    self.video_writer.release()
                    self.video_writer = None

                    create_log_thread = threading.Thread(
                        target=LogsRepository.create_log, args=(log,)
                    )

                    create_log_thread.start()

                    if log.is_unknown:
                        # Send notification Thread Request

                        print("sending unknown log")

                        notification_thread = threading.Thread(
                            target=send_notify_request,
                            args=(str(self.camera_loc), str(log.time_of_detection)),
                        )

                        notification_thread.start()
