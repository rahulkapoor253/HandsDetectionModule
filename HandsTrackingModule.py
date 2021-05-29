import cv2
import mediapipe as mp
import time


class HandDetector():

    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, track_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence

        self.mpHands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.detection_confidence, self.track_confidence)

    def find_hands(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        # we get landmark {
        #   x: 0.6321582794189453
        #   y: 0.42400041222572327
        #   z: -0.1402321755886078
        # }
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

        return image

    def find_position(self, image, hand_num=0):
        landmarks_list = []

        if self.results.multi_hand_landmarks:
           # print(f"total hands are {len(self.results.multi_hand_landmarks)}")
            if hand_num == 0:
                selected_hand = self.results.multi_hand_landmarks[hand_num]

                for id, lm in enumerate(selected_hand.landmark):
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * h), int(lm.y * w)
                    landmarks_list.append([id, cx, cy])

            elif hand_num == 1 and len(self.results.multi_hand_landmarks) > 1:
                selected_hand = self.results.multi_hand_landmarks[hand_num]

                for id, lm in enumerate(selected_hand.landmark):
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * h), int(lm.y * w)
                    landmarks_list.append([id, cx, cy])

        return landmarks_list


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

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


if __name__ == "__main__":
    main()
