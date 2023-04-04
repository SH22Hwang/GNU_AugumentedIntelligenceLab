import numpy as np
import cv2

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

# solvePnP 함수에 입력으로 사용할 3D 좌표 생성
object_points = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]], np.float32)

# 이미지에서 각 포인트에 해당하는 2D 좌표 계산
img_points = cv2.projectPoints(object_points, rvecs[0], tvecs[0], mtx, dist)[0]

# solvePnP 함수 호출을 위한 매개변수 설정
ret, rvecs, tvecs = cv2.solvePnP(object_points, img_points, mtx, dist)

# 결과 출력
print("Rotation Vector:\n", rvecs)
print("Translation Vector:\n", tvecs)
