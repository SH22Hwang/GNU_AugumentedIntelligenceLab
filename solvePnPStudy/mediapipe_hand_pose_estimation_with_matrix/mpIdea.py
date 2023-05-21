import cv2, mediapipe as mp, numpy as np
from mpIdeaClasses import *

def prepareMediaPipeTools():
    mp_hands, mp_drawings = mp.solutions.hands, mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    return hands, mp_hands, mp_drawings

def solution(hands, mp_hands, mp_drawings, K, extended_K, calib_R_t_with_0001, dist):
    # 메인 프로세스
    camera_selection = int(input("손 촬영 카메라 선택(0: Irium Webcam, 1: MacBook Camera) > "))
    cap = cv2.VideoCapture(camera_selection)
    while cap.isOpened():
        success, image = cap.read()
        if success:
            results, image, h, w, _ = Processor.processImage(hands, image)
            if results.multi_hand_landmarks:
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    model_points = np.float32([[l.x, l.y, l.z] for l in results.multi_hand_world_landmarks[i].landmark])
                    image_points = np.float32([[l.x * w, l.y * h] for l in hand_landmarks.landmark])

                    hand_to_camera_coords_to_2d, camera_to_world_coords_to_2d = MatrixHandler.getMultipleMatricesAndCoords(K, extended_K, dist, calib_R_t_with_0001, model_points, image_points)

                    # 수치적, 시각적 분석
                    image = Analyzer.analyzeResult(image_points, hand_to_camera_coords_to_2d, camera_to_world_coords_to_2d, h, w, image)
                    mp_drawings.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS) 
    

            cv2.imshow("실시간 출력", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                break
