import cv2, mediapipe as mp, numpy as np
from mpIdeaClasses import *

def prepareMediaPipeTools(): # 기본적인 mediapipe 도구들을 준비합니다. (중요하지 않음)
    mp_hands, mp_drawings = mp.solutions.hands, mp.solutions.drawing_utils # 손에 랜드마크를 그릴때 사용합니다.(근데 opencv로 그릴거라서 안쓰게 될 예정)
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) # 손을 추적할 모델입니다.
    return hands, mp_hands, mp_drawings

def solution(hands, mp_hands, mp_drawings, K, extended_K, calib_R_t_with_0001, dist):
    # 메인 프로세스
    camera_selection = int(input("손 촬영 카메라 선택(카메라가 1개라면 0을 입력하세요.) > "))
    cap = cv2.VideoCapture(camera_selection)
    while cap.isOpened():


        success, image = cap.read() # 한 프레임을 읽습니다.
        if success: # 프레임을 읽는데 성공했다면



            results, image, h, w, _ = Processor.processImage(hands, image) # 랜드마크 추적결과(results= 추적 좌표), 이미지의 기본 정보(이미지 픽셀별 값, 가로길이, 세로길이)를 받습니다.



            if results.multi_hand_landmarks: # 손을 찾았다면
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks): # 한손이면 i는 0, 양손이면 i는 0, 1
                    # hand_landmarks는 [노멀라이즈드랜드마크, 노멀라이즈드랜드마크, 노멀라이즈드랜드마크, ... ] 처럼 NormalizedLandmark 여러개를 담은 리스트입니다.(hand_landmark's' 이기떄문에 복수형)




                    model_points = np.float32([[l.x, l.y, l.z] for l in results.multi_hand_world_landmarks[i].landmark]) # 손 3D 좌표
                    image_points = np.float32([[l.x * w, l.y * h] for l in hand_landmarks.landmark]) # 손 2D 좌표

                    

                    # H2C에서 H곱해서 나온 C좌표를 2D이미지로 찍을때 어떤 픽셀에 찍어야 할지 리스트
                    # C2W에서 C곱해서 나온 W좌표를 2D이미지로 찍을때 어떤 픽셀에 찍어야 할지 리스트
                    # 두개를 리턴받습니다.
                    hand_to_camera_coords_to_2d, camera_to_world_coords_to_2d = MatrixHandler.getCoordinates(K, extended_K, dist, calib_R_t_with_0001, model_points, image_points)



                    # 수치적, 시각적 분석
                    image = Analyzer.analyzeResult(image_points, hand_to_camera_coords_to_2d, camera_to_world_coords_to_2d, h, w, image)
                    # mp_drawings.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS) # 사용 안해도 됨(교수님께서 말씀하심, 단순 확인용)
    




            cv2.imshow("실시간 출력", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                break
