import cv2
import time
import HandsTrackingModule as htm

cTime = 0
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, 700)
cap.set(4, 550)

detector = htm.HandDetector()
fingerTipIds = [4, 8, 12, 16, 20]


def get_fingers(mylist):
    fingers = []

    if mylist[1][1] < mylist[17][1]:
        # for thumb scenario will be different -> for left hand
        if mylist[4][1] < mylist[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    else:
        # for thumb scenario will be different -> for right hand
        if mylist[4][1] > mylist[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    for i in range(1, 5):
        if mylist[fingerTipIds[i]][2] < mylist[fingerTipIds[i] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)


while True:
    ret_val, image = cap.read()

    ret_image = detector.find_hands(image)
    lms_list1 = detector.find_position(ret_image, hand_num=0)
    lms_list2 = detector.find_position(ret_image, hand_num=1)

    res_count = 0
    if len(lms_list1) > 0:
        res_count += get_fingers(lms_list1)

    if len(lms_list2) > 0:
        res_count += get_fingers(lms_list2)

    print(res_count)
    cv2.putText(ret_image, str(res_count), (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(ret_image, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, cv2.COLOR_GRAY2BGR555)
    cv2.imshow("frame", ret_image)
    cv2.waitKey(1)