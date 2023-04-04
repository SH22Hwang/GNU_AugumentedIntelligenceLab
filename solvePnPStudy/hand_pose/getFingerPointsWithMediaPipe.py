import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(1)
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
            print("=======================================")
            b = list(results.multi_handedness)
            for i, hand_landmarks in enumerate(a):
                added_text = "왼손" if b[i].classification[0].label == 'Left' else "오른손"
                for ids, landmrk in enumerate(hand_landmarks.landmark):
                    cx, cy = landmrk.x * image_width, landmrk.y * image_height
                    if ids == 0: print (added_text + "손목: [%dpx, %dpx]" % (int(cx), int(cy)))
                    if ids == 4: print (added_text + "엄지: [%dpx, %dpx]" % (int(cx), int(cy)))
                    if ids == 8: print (added_text + "검지: [%dpx, %dpx]" % (int(cx), int(cy)))
                    if ids == 12: print (added_text + "중지: [%dpx, %dpx]" % (int(cx), int(cy)))
                    if ids == 16: print (added_text + "약지: [%dpx, %dpx]" % (int(cx), int(cy)))
                    if ids == 20: print (added_text + "소지: [%dpx, %dpx]" % (int(cx), int(cy)))
                    

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()