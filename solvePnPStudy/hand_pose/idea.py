import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

# 핸드 이미지 위에 랜드 마크 그리기 위함
from shapely.geometry import Polygon, Point

mp_drawing = mp.solutions.drawing_utils
# 핸드 처리
mp_hands = mp.solutions.hands
# 핸드 랜드마크 표시 스타일용
drawing_styles = mp.solutions.drawing_styles

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 해상도
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(height, width)

'''
손가락 솔루션 생성
min_detection_confidence
- 손가락 감지 최소 신뢰성 0.0 - 1.0
- 1.0에 가까울수록 확실한 확률이 높은 손가락만 감지
min_tracking_confidence
- 손가락 추적 최소 신뢰성 0.0 - 1.0
- 1.0에 가까울수록 추적율이 높은 것만 감지
'''

# 3D Scatter Real-time
def animate():
    ax.clear()
    graph = ax.scatter(X,Y,Z)
    graph._offsets3d = (X, Y, Z)
    plt.pause(0.1) # 0.1초 대기
    
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

X = list()
Y = list()
Z = list()

with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    # 카메라 열려있을때까지 루프
    while cap.isOpened():
        # 카메라에서 사진 한장 얻기
        success, image = cap.read()
        # 사진을 얻어오지 못햇다면
        if not success:
            # 에러 출력 후 루프 시작으로 되돌아감
            # 카메라 로딩중일 수 있기때문에 break대신 continue로 함
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # 사진을 좌/우 반전 시킨후 BGR에서 RGB로 변환
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # 성능 향상을 위해 이미지를 쓰기 불가시켜 참조로 전달
        image.flags.writeable = False
        # 손가락 마디 검출!!
        results = hands.process(image)

        image_height, image_width, _ = image.shape

        # 다시 이미지를 쓰기 가능으로 변경
        image.flags.writeable = True
        # 이미지를 다시 RGB에서 BGR로 변경
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # hands.process에서 랜드마크를 찾았다면
        if results.multi_hand_landmarks:
            # 랜드마크 숫자 만큼 루프
            for hand_landmarks in results.multi_hand_world_landmarks:

                # # 좌표 확인
                # for ids, landmrk in enumerate(hand_landmarks.landmark):
                #     cx, cy = landmrk.x * image_width, landmrk.y * image_height
                #     print(f"<{ids}>\nx : {cx}\ny: {cy} \nz:{landmrk.z}")

                # 이미지에 랜드마크 위치마다 표시
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    drawing_styles.get_default_hand_landmarks_style(),
                    drawing_styles.get_default_hand_connections_style())
                # print(hand_landmarks.landmark)

                # palm = list()
                # for i in [0, 1, 2, 5, 9, 13, 17]:
                #     palm.append((hand_landmarks.landmark[i].x, hand_landmarks.landmark[i].y))
                print("\n-----------------------\n" + str(hand_landmarks.landmark))
                coord = list()
                X = []
                Y = []
                Z = []
                for i in range(21):
                    X.append(hand_landmarks.landmark[i].x)
                    Y.append(hand_landmarks.landmark[i].y)
                    Z.append(hand_landmarks.landmark[i].z)
                # palmPoly = Polygon(palm)
                # print(palmPoly)

                
        # 1인칭 시점에 맞추어 화면 좌우변환
        image = cv2.flip(image, 1)
        # image = cv2.putText(image, word, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 1, cv2.LINE_AA)

        # 최종 변경된 이미지를 화면에 출력
        cv2.imshow('MediaPipe Hands', image)
        cv2.waitKey(100) # 0.1초 대기, 3D Scatter 대기 시간과 동기화
        animate()
        # 5ms 대기하면서 키보드 입력 대기
        # 27 > ESC 키
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()