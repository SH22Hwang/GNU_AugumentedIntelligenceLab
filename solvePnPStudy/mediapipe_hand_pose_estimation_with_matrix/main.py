from mpIdea import *


"""
전체적인 흐름은 다음과 같습니다.

0. 미디어파이프 기본 도구를 준비합니다.

1. calibrate() 함수로
    내부파라미터(3x3), 확장된 내부파라미터(3x4), 확장된 R|t 매트릭스, distortion(카메라 제조 오차, 사실상 없는 수준)
    을 얻습니다.
    * 현재 1회만 실행하지만, 미래에는 실시간으로 같이 돌아갈 예정입니다.

2. 기본도구와 반환받은 값을 solution함수에 넣어서 solution함수를 실행합니다.
    solution함수는 핵심 기능입니다.

3. solution 함수의 설명입니다.
    -> 이미지 읽기
    -> 손 찾기(한손일수도 두손일수도 있음)
    -> 찾은 손의 3D, 2D좌표를 통해 solvePnP도 돌려서 rvec, tvec 구하기
    -> rvec, tvec 확장행렬 구하기
    -> H2C, W2C 등등 여러 행렬 곱셈을 진행하여 최종적으로 화면 픽셀 어디에 찍을 지 좌표를 담은 리스트 2개(H2C, W2C) 받기
    -> 화면에 그리기
"""

hands, mp_hands, mp_drawings = prepareMediaPipeTools()
solution(hands, mp_hands, mp_drawings, *Calibrator.calibrate())

hands.close()

