import cv2
import numpy as np

def clickEvent(event, x, y, flags, params): # 수동 점 찍기
    if event == cv2.EVENT_LBUTTONDOWN:
        image_points.append([x, y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' + str(y), (x,y), font, 1, (255, 0, 0), 2)
        cv2.imshow('image', img)


""" 캘리브레이션 """
SIZE = (15, 10)
img = cv2.imread('./images/calibrationImage.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
object_points = np.zeros((1, SIZE[0] * SIZE[1], 3), np.float32)
object_points[0,:,:2] = np.mgrid[0:SIZE[0], 0:SIZE[1]].T.reshape(-1, 2)
ret, corners = cv2.findChessboardCorners(gray, SIZE, None)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([object_points], [corners], gray.shape[::-1], None, None)


""" image_points를 직접 찍은 후 solvePnP 실행 """
N = 1
object_points = np.array([[0, 0, 0], [N, 0, 0], [N, N, 0], [0, N, 0], [0, 0, N], [N, 0, N], [0, N, N]], np.float32) # 0, 1, 2, 3, 4, 5, 7 (6 없음)
image_points = []
img = cv2.imread('./images/cubeImage.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('image', img)
cv2.setMouseCallback('image', clickEvent)

if cv2.waitKey(0) & 0xFF == 27:
    cv2.destroyAllWindows()

image_points = np.array(image_points, np.float32)
ret, rvecs, tvecs = cv2.solvePnP(object_points, image_points, mtx, dist)

""" solvePnP를 통해 얻은 결과로 예상할 수 없던 6번 점의 이미지 포인트 얻기 """
missing_point_object = np.array([N, N, N], np.float32)
missing_point_image, _ = cv2.projectPoints(missing_point_object, rvecs, tvecs, mtx, dist)
new_x, new_y = missing_point_image.squeeze()[:2]
image_points = np.insert(image_points, 6, [int(new_x), int(new_y)], axis=0)


""" 공간인척 하는 2D 이미지에게 큐브 그려주기 """
cv2_image = cv2.imread('./images/cubeImage.jpg', cv2.IMREAD_COLOR)
drawing_image = cv2_image.copy()
for p1_idx, p2_idx in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]:
    p1, p2 = image_points[p1_idx].astype(np.int32), image_points[p2_idx].astype(np.int32)
    cv2.line(drawing_image, p1, p2, (0,0,255), thickness=4, lineType=cv2.LINE_AA)
cv2.imshow("Space", drawing_image)

if cv2.waitKey(0) & 0xFF == 27:
    cv2.destroyAllWindows()

"""손 큐브 그리는 코드 추가 필요"""