import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 화면에 띄울 구를 생성합니다.
    height, width = frame.shape[:2]
    center = (width // 2, height // 2)
    radius = min(center) - 50
    color = (0, 255, 0)
    thickness = 2
    cv2.circle(frame, center, radius, color, thickness)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()