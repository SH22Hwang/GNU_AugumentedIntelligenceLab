import cv2
import numpy as np
import mediapipe as mp

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

                baby_finger_tip = hand_landmarks.landmark[20]
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
        cv2.imshow('output', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break