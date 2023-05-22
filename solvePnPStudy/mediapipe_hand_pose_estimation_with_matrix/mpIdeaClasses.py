import cv2, numpy as np

class Calibrator:
    def getCalibratedResult(camera_selection):
        while True:
            SIZE = tuple(map(int, input("체스보드 사이즈 입력 (ex. 9 7) > ").split()))
            img = None
            if camera_selection == -1: img = cv2.imread("./images/calibrationImage.jpg")
            else:
                cap = cv2.VideoCapture(camera_selection)
                while cap.isOpened():
                    success, img = cap.read()
                    if success:
                        img = cv2.flip(img, 1)
                        cv2.imshow("캘리브레이션 캡쳐(Press Q to capture an image.)", img)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            cap.release()
                            cv2.destroyAllWindows()
                            break

            # 체크보드 코너 찾기
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            object_points = np.zeros((1, SIZE[0] * SIZE[1], 3), np.float32)
            object_points[0, :, :2] = np.mgrid[0 : SIZE[0], 0 : SIZE[1]].T.reshape(-1, 2)

            success, corners = cv2.findChessboardCorners(gray, SIZE, None)
            if success: return cv2.calibrateCamera([object_points], [corners], gray.shape[::-1], None, None)
            print("코너 찾기 실패(재촬영 시도 or 체크보드의 가로세로 코너 개수 확인 필요)")
            
    def calibrate():
        # 캘리브레이션
        camera_selection = int(input("캘리브레이션 카메라 선택(-1: use ImageFile, 0: Irium Webcam, 1: MacBook Camera) > "))
        _, K, dist, calib_rvecs, calib_tvecs = Calibrator.getCalibratedResult(camera_selection)
        extended_K, calib_R_t_with_0001 = MatrixHandler.extendMatrix("K", K), MatrixHandler.extendMatrix("[R|t]", calib_rvecs[0], calib_tvecs[0]) # calibration의 rvec, tvec은 return 될 때 사이즈 1짜리 튜플로 나와서 [0]을 해줘야 순수한 벡터가 나온다.
        return K, extended_K, calib_R_t_with_0001, dist
    
class MatrixHandler:
    def extendMatrix(mode, *matrices):
        if mode == "[R|t]":
            rvecs, tvecs = matrices
            R, _ = cv2.Rodrigues(rvecs)
            col_tvec = np.array([tvecs[0], tvecs[1], tvecs[2]])
            R_t = np.append(R, col_tvec, axis=1)
            R_t_with_0001 = np.append(R_t, [np.array([0, 0, 0, 1])], axis=0)
            return R_t_with_0001
        elif mode == "K":
            return np.append(matrices[0], np.array([[0], [0], [0]]), axis=1)
    
    def scaleLastElementAs1(matrix):
        for line in matrix:
            line /= line[2]
        
        return matrix

    def getMultipleMatricesAndCoords(K, extended_K, dist, calib_R_t_with_0001, model_points, image_points):
        # H2C
        success, solvepnp_rvecs, solvepnp_tvecs = cv2.solvePnP(model_points, image_points, K, dist, flags=cv2.SOLVEPNP_EPNP)
        H2C_MATRIX = MatrixHandler.extendMatrix("[R|t]", solvepnp_rvecs, solvepnp_tvecs)

        # H2C * H -> C
        hand_to_camera_coords = [H2C_MATRIX @ np.array([X, Y, Z, 1]) for X, Y, Z in model_points]
    
        # W2C from calib_rvecs, calib_tvecs
        W2C_MATRIX = calib_R_t_with_0001

        # W2C -> C2W
        C2W_MATRIX = np.linalg.inv(W2C_MATRIX)

        # C2W * C -> W
        camera_to_world_coords = [C2W_MATRIX @ np.array([X, Y, Z, 1]) for X, Y, Z, _ in hand_to_camera_coords]

        # W2C * W -> C
        world_to_camera_coords = [W2C_MATRIX @ np.array([X, Y, Z, 1]) for X, Y, Z, _ in camera_to_world_coords]


        # 3D -> 2D
        hand_to_camera_coords_to_2d = [extended_K @ h2c_3d_coords for h2c_3d_coords in hand_to_camera_coords]
        world_to_camera_coords_to_2d = [extended_K @ w2c_3d_coords for w2c_3d_coords in world_to_camera_coords]

        return MatrixHandler.scaleLastElementAs1(hand_to_camera_coords_to_2d), \
               MatrixHandler.scaleLastElementAs1(world_to_camera_coords_to_2d)

class Analyzer:
    def analyzeResult(image_points, hand_to_camera_coords_to_2d, world_to_camera_coords_to_2d, h, w, image=None):
        ## 수치적 분석
        for i in range(21):
            print("-------------------------------------------------------")
            mp_x, mp_y = image_points[i]
            h2c_x, h2c_y, _ = hand_to_camera_coords_to_2d[i]
            w2c_x, w2c_y, _ = world_to_camera_coords_to_2d[i]

            print("MP  Point %d: [%.7f, %.7f]" % (i+1, mp_x, mp_y))
            print("H2C Point %d: [%.7f, %.7f]" % (i+1, h2c_x, h2c_y))
            print("W2C Point %d: [%.7f, %.7f]" % (i+1, w2c_x, w2c_y))
            # print("비율 대조 %.10f vs %.10f" % (h2c_x / h2c_y, w2c_x / w2c_y))
            # print("비율 차이 절댓값: %.10f" % abs(h2c_x / h2c_y - w2c_x / w2c_y))


        ## 시각적 분석
        # 1. H2C와 W2C 원(circle) 그리기
        for i in range(21):
            h2c_x, h2c_y, _ = map(int, hand_to_camera_coords_to_2d[i])
            w2c_x, w2c_y, _ = map(int, world_to_camera_coords_to_2d[i])
            image = cv2.circle(image, (h2c_x, h2c_y), 6, (0, 255, 0), 2)

            # if w2c_x == 0:
            #     continue
            # ratio = h2c_x / w2c_x
            # new_x, new_y = w2c_x * ratio, w2c_y * ratio
            # if 0 <= new_x <= w and 0 <= new_y <= h:
            #     image = cv2.circle(image, [*map(int, (new_x, new_y))], 10, (255, 0, 0), 2)

            if 0 <= h2c_x <= w and 0 <= h2c_y <= h and 0 <= w2c_x <= w and 0 <= w2c_y <= h:
                image = cv2.circle(image, [*map(int, (h2c_x, h2c_y))], 6, (0, 255, 0), 2)
                image = cv2.circle(image, [*map(int, (w2c_x, w2c_y))], 10, (255, 0, 0), 2)
        
        # 2. H2C와 W2C 의 관절 사이 선분(line) 그리기
        for start, end in [(1, 2), (2, 3), (3, 4), \
                            (5, 6), (6, 7), (7, 8), \
                            (9, 10), (10, 11), (11, 12), \
                            (13, 14), (14, 15), (15, 16), \
                            (17, 18), (18, 19), (19, 20), \
                            (0, 1), (0, 5), (0, 17), \
                            (5, 9), (9, 13), (13, 17)]:
            
            # H2C
            h2c_1_x, h2c_1_y, _ = map(int, hand_to_camera_coords_to_2d[start])
            h2c_2_x, h2c_2_y, _ = map(int, hand_to_camera_coords_to_2d[end])

            if 0 <= h2c_1_x <= w and 0 <= h2c_2_x <= w and 0 <= h2c_1_y <= h and 0 <= h2c_2_y <= h:
                image = cv2.line(image, (h2c_1_x, h2c_1_y), (h2c_2_x, h2c_2_y), (0, 255, 0), 2)

            # W2C
            w2c_1_x, w2c_1_y, _ = world_to_camera_coords_to_2d[start]
            w2c_2_x, w2c_2_y, _ = world_to_camera_coords_to_2d[end]
            ratio_1, ratio_2 = h2c_1_x / w2c_1_x, h2c_2_x / w2c_2_x

            new_1_x, new_1_y = int(w2c_1_x * ratio_1), int(w2c_1_y * ratio_1)
            new_2_x, new_2_y = int(w2c_2_x * ratio_2), int(w2c_2_y * ratio_2)

            if 0 <= new_1_x <= w and 0 <= new_2_x <= w and 0 <= new_1_y <= h and 0 <= new_2_y <= h:
                image = cv2.line(image, (new_1_x, new_1_y), (new_2_x, new_2_y), (255, 0, 0), 2)

        return image

class Processor:
    def processImage(hands, image):
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        h, w, d = image.shape
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return results, image, h, w, d