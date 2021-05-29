import cv2
import time
import HandsTrackingModule as htm


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()

while True:
    retval, image = cap.read()
    ret_image = detector.find_hands(image)
    lms_list = detector.find_position(ret_image)
    if len(lms_list) > 0:
        print(lms_list[4]) # pointer to thumb

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(ret_image, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, cv2.COLOR_GRAY2BGR555)
    cv2.imshow("frame", ret_image)
    cv2.waitKey(1)