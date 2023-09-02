import cv2
import imutils






def detect_humans(image):

    hog = cv2.HOGDescriptor()

    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    (humans, _) = hog.detectMultiScale(image,  winStride=(5, 5), padding=(3, 3), scale=1.21)
    
    return (humans, _)




def detect_from_image():

    image = cv2.imread("./images/image_7.jpg")


    image = imutils.resize(image, width=min(500, image.shape[1])) 


    (humans, _) = detect_humans(image)

    print('Human Detected : ', len(humans))

    for (x, y, w, h) in humans: 
        cv2.rectangle(image, (x, y),  (x + w, y + h),  (0, 0, 255), 2) 



    cv2.imshow("Image", image)


    cv2.waitKey(0) 

    cv2.destroyAllWindows()