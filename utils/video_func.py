import cv2






def adjust_text_size(frame, match, face_location):
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (face_location[3] + 6, face_location[2] -6)
    color = (200, 200, 200)
    
    font_scale = 1.0

    thickness = 2

    cv2.putText(frame, match, org, font, font_scale, color, thickness, cv2.LINE_AA)