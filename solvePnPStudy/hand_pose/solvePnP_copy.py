import numpy as np
import cv2
import mediapipe as mp


def getHandCoordinates():
    main_points = []
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6) as hands:
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
                        if ids == 0:
                            main_points.append([cx, cy])
                        if ids == 4:
                            main_points.append([cx, cy])
                        if ids == 8:
                            main_points.append([cx, cy])
                        if ids == 12:
                            main_points.append([cx, cy])
                        if ids == 16:
                            main_points.append([cx, cy])
                        if ids == 20:
                            main_points.append([cx, cy])
                cap.release()
    return main_points


def getInnerMatrixOfCalibrationedCamera():
    """캘리브레이션 하기"""
    # 체스보드 코너 포인트를 계산할 체스보드 이미지 파일 경로
    chessboard_img_path = 'image2.jpg'

    # 체스보드 가로, 세로 코너 포인트 개수
    chessboard_size = (10, 7)

    # 체스보드 패턴에서의 3D 좌표 생성
    object_points = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    object_points[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # 저장된 이미지에서 체스보드 코너 포인트 검출
    img = cv2.imread(chessboard_img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # 내부 매개변수 및 왜곡 계수 계산
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([object_points], [corners], gray.shape[::-1], None, None)
    return ret, mtx, dist, rvecs, tvecs


main_points = getHandCoordinates()  # 손목, 엄지->소지 까지
ret, matrix, distortion, rvecs, tvecs = getInnerMatrixOfCalibrationedCamera()

# solvePnP 함수에 label으로 사용할 3D 좌표 생성
object_points = np.array(
    [[3 / 6, 7 / 8, 0], [1 / 6, 3 / 8, 0], [2 / 6, 2 / 8, 0], [3 / 6, 1 / 8, 0], [4 / 6, 2 / 8, 0], [5 / 6, 3 / 8, 0]],
    np.float32)  # 손 3D 좌표 임의로 정하기
img_points = np.array(main_points)  # 손 2D 좌표
ret, rvecs, tvecs = cv2.solvePnP(object_points, img_points, matrix, distortion)

# 결과 출력
print("Rotation Vector:\n", rvecs)
print("Translation Vector:\n", tvecs)
