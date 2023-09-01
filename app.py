import cv2
import threading
import numpy



hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
                   


image = cv2.imread("./images/image_5.jpg")

video = cv2.VideoCapture(0)




if not video.isOpened():

    print("Could not start the camera")
    exit()



while True:
    ret, frame = video.read()


    if not ret:
        print("could not read frames")

        break

    cv2.imshow("Video Capture", frame)


    if cv2.waitKey(1) & 0xFF == ord("w"):
        break


video.release()
cv2.destroyAllWindows()