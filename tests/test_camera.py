import cv2
import queue
import threading
from models.detect import detect_humans


# Function to capture frames
def capture_frames(video, frame_queue):
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame_queue.put(frame)

# Function for frame processing (e.g., object detection)
def process_frames(frame_queue):
    while True:
        frame = frame_queue.get()
        (humans, _) = detect_humans(frame)
        for (x, y, w, h) in humans:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow("Video Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord("w"):
            break

# Create VideoCapture object
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Could not start the camera")
    exit()

# Create a queue to pass frames between capture and processing threads
frame_queue = queue.Queue()

# Create threads for capture and processing
capture_thread = threading.Thread(target=capture_frames, args=(video, frame_queue))
process_thread = threading.Thread(target=process_frames, args=(frame_queue,))

# Start the threads
capture_thread.start()
process_thread.start()

# Wait for threads to finish
capture_thread.join()
process_thread.join()

# Release the VideoCapture
video.release()
cv2.destroyAllWindows()



































# import cv2
# import imutils
# import threading
# import numpy as np
# from models.detect import detect_humans




# video = cv2.VideoCapture(0)


# if not video.isOpened():

#     print("Could not start the camera")
#     exit()



# while True:
#     ret, frame = video.read()


#     if not ret:
#         print("could not read frames")

#         break

#     (humans, _) = detect_humans(frame)

#     for (x, y, w, h) in humans: 
#         cv2.rectangle(frame, (x, y),  (x + w, y + h),  (0, 0, 255), 2) 


#     cv2.imshow("Video Capture", frame)


#     if cv2.waitKey(1) & 0xFF == ord("w"):
#         break


# video.release()
# cv2.destroyAllWindows()