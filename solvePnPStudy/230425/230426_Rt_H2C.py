""" solvePnP Hand to world

프로젝트 이름: 손 으로하는증강현실은뭐든지잘해
참가자: 이민재, 황승현, 이수원
주제: 단안카메라 증강현실 구현 및 상용화 기술 연구

1. 3D 공간에 물체 구현. K[R|t]w2c
    1. [R|t]w2c의 역함수 [R|t]c2w 구함.
    2. [R|t]c2w에 [P]c(물체의 카메라 상의 좌표 곱하면 [P]w(현실의 좌표) 나옴.
2. Hand의 공간좌표 구현. K[R|t]h2c
   1. [R|t]h2c에 [P]h(손의 좌표) 곱하면 [p]c(카메라 상의 좌표) 나옴
3. [P]w와 [P]h 2개가 같은 곳에 있으면 증강현실 구현 완료

해야할 일:
this file>> [R|t]h2c(solvePnP Hand to world)의 작동 시간 측정.

결과 (소요시간)
평균: 0.015020 sec
최대: 0.046875 sec

- OpenGL로 월드에 구 띄우기
- 역함수 구하기.
- 걸리는 시간 측정하기

"""


import cv2
import numpy as np
import mediapipe as mp

import time

time_meas_array = np.zeros(shape=1)

mp_hands = mp.solutions.hands

""" 캘리브레이션 """
SIZE = (15, 10)
img = cv2.imread('./images/calibrationImage.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
object_points = np.zeros((1, SIZE[0] * SIZE[1], 3), np.float32)
object_points[0,:,:2] = np.mgrid[0:SIZE[0], 0:SIZE[1]].T.reshape(-1, 2)
ret, corners = cv2.findChessboardCorners(gray,SIZE, None)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([object_points], [corners], gray.shape[::-1], None, None)


""" 늘 해오던 카메라 읽어들이기 """
cap = cv2.VideoCapture(0) # 0번 irium, 1번 맥 캠
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        start = time.process_time()
        ret, image = cap.read()
        if not ret: continue
        
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image) # results
        h, w, d = image.shape
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                world_landmarks = results.multi_hand_world_landmarks[i]

                # baby_finger_tip = hand_landmarks.landmark[20]
                # 시간 측정 시작:

                model_points = np.float32([[l.x, l.y, l.z] for l in world_landmarks.landmark])
                image_points = np.float32([[l.x * w, l.y * h] for l in hand_landmarks.landmark])
                success, rvecs, tvecs, = cv2.solvePnP(model_points, image_points, mtx, dist, flags=cv2.SOLVEPNP_EPNP)


                # 3D Bounding Box 그리기
                if success:
                    bb_3d_world = np.float32([[ 0.06,  0.06,  0.06],
                                            [ 0.06, -0.06,  0.06],
                                            [-0.06, -0.06,  0.06],
                                            [-0.06,  0.06,  0.06],
                                            [ 0.06,  0.06, -0.06],
                                            [ 0.06, -0.06, -0.06],
                                            [-0.06, -0.06, -0.06],
                                            [-0.06,  0.06, -0.06]])
                    
                    # 3D Bounding Box 꼭지점의 2D 좌표
                    bb_2d, _ = cv2.projectPoints(bb_3d_world, rvecs, tvecs, mtx, dist)
                    bb_2d = np.int32(bb_2d).reshape(-1, 2)
                    
                    # 3D Bounding Box 그리기
                    # x_min, x_max, y_min, y_max: 큐브가 화면 안에 그려지도록 제한하는 변수
                    x_min, y_min = np.min(bb_2d, axis=0)
                    x_max, y_max = np.max(bb_2d, axis=0)
                    x_min, x_max = max(0, x_min), min(w, x_max)
                    y_min, y_max = max(0, y_min), min(h, y_max)
                    
                    # 큐브 그리기
                    line_width = 2

                    # 회전각(rvec)을 이용하여 회전 변환 행렬(rotation matrix)을 구하고,
                    # 이를 이용하여 큐브 꼭지점의 위치를 회전시킨다.
                    rotation_matrix, _ = cv2.Rodrigues(rvecs)
                    bb_3d_world_rotated = np.matmul(bb_3d_world, rotation_matrix.T)

                    # 이동 벡터(tvec)를 이용하여 큐브 꼭지점을 이동시킨다.
                    bb_3d_world_rotated_translated = bb_3d_world_rotated + np.transpose(tvecs)

                    bb_2d_rotated, _ = cv2.projectPoints(bb_3d_world_rotated_translated, np.zeros((3,1)), np.zeros((3,1)), mtx, dist)
                    bb_2d_rotated = np.int32(bb_2d_rotated).reshape(-1, 2)

                    for i, j in [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]:
                        pt1 = (int(bb_2d_rotated[i][0]), int(bb_2d_rotated[i][1]))
                        pt2 = (int(bb_2d_rotated[j][0]), int(bb_2d_rotated[j][1]))
                        cube_color = (0, 255, 0)
                        cv2.line(image, pt1, pt2, cube_color, line_width)

                # 시간측정 종료
                end = time.process_time()
                # print(f"{int(round(end - start))} ms")
                print(f"{end - start} sec")
                time_meas_array = np.append(time_meas_array, end - start)
                    
        cv2.imshow('output', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            print(f"소요시간:\n"
                  f"평균: {np.mean(time_meas_array):.6f} sec\n"
                  f"최대: {np.max(time_meas_array):.6f} sec\n")
            break