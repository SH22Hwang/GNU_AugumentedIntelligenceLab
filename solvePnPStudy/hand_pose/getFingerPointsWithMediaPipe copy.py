import cv2
import mediapipe as mp

main_points = []
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        results = hands.process(image)
        image_height, image_width, _ = image.shape
        image.flags.writeable = True

        a = results.multi_hand_landmarks
        if a:
            for hand_landmarks in a:
                for ids, landmrk in enumerate(hand_landmarks.landmark):
                    cx, cy = landmrk.x * image_width, landmrk.y * image_height
                    if ids == 0: main_points.append([cx, cy])
                    if ids == 4: main_points.append([cx, cy])
                    if ids == 8: main_points.append([cx, cy])
                    if ids == 12: main_points.append([cx, cy])
                    if ids == 16: main_points.append([cx, cy])
                    if ids == 20: main_points.append([cx, cy])
            cap.release()


