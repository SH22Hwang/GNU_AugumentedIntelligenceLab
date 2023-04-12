import cv2
import numpy as np
import mediapipe as mp

N = 1
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
cap = cv2.VideoCapture(1)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, image = cap.read()
        if not ret: continue
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image) # results
        h, w, d = image.shape
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        

        """ multi hand world 랑 multi hand 담기 """
        object_points, image_points = [], []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_world_landmarks:
                for i in range(21):
                    obj_x = hand_landmarks.landmark[i].x
                    obj_y = hand_landmarks.landmark[i].y
                    obj_z = hand_landmarks.landmark[i].z
                    object_points.append([obj_x, obj_y, obj_z])
            
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(21):
                    img_x = int(hand_landmarks.landmark[i].x * w)
                    img_y = int(hand_landmarks.landmark[i].y * h)
                    image_points.append([img_x, img_y])


        """ 손 전체를 인식 할 때만( >= 21) """
        ret, rvecs, tvecs = None, None, None
        if len(object_points) >= 21 and len(image_points) >= 21:        
            object_points, image_points = np.array(object_points, np.float32), np.array(image_points, np.float32)
            ret, rvecs, tvecs = cv2.solvePnP(object_points, image_points, mtx, dist)

            # box_points = np.array([[0, 0, 0], [0, h, 0], [w, h, 0], [w, 0, 0], [0, 0, d], [0, h, d], [w, h, d], [w, 0, d]], np.float32)
            box_points = np.array([[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]], np.float32)
            # 3D 포인트를 2D 이미지 상의 좌표로 변환
            img_points, _ = cv2.projectPoints(box_points, rvecs, tvecs, mtx, dist)

            # 변환된 좌표를 이용하여 3D Bounding Box 그리기
            img_points = np.int32(img_points).reshape(-1, 2)
            for point in img_points:
                x, y = point
                if 0 <= x <= w and 0 <= y <= h:
                    cv2.drawContours(image, [img_points[:4]], -1, (0, 255, 0), 3) # 밑면
                    cv2.drawContours(image, [img_points[4:]], -1, (0, 255, 0), 3) # 윗면
                    for i in range(4):
                        cv2.drawContours(image, [np.array([img_points[i], img_points[i+4]])], -1, (0, 255, 0), 3) # 모서리
                        cv2.imshow('output', image)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cap.release()
                            cv2.destroyAllWindows()
                            break