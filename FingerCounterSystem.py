import cv2
import time
import HandsTrackingModule as htm

cTime = 0
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, 650)
cap.set(4, 450)

detector = htm.HandDetector()
fingerTipIds = [4, 8, 12, 16, 20]

while True:
    ret_val, image = cap.read()

    ret_image = detector.find_hands(image)
    lms_list = detector.find_position(ret_image)

    if len(lms_list) > 0:
        fingers = []

        # for thumb scenario will be different -> for left hand
        if lms_list[4][1] < lms_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for i in range(1, 5):
            if lms_list[fingerTipIds[i]][2] < lms_list[fingerTipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        if totalFingers == 0:
            totalFingers = 6
        print(totalFingers)

        cv2.putText(ret_image, str(totalFingers), (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(ret_image, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, cv2.COLOR_GRAY2BGR555)
    cv2.imshow("frame", ret_image)
    cv2.waitKey(1)