# solvePnP Hand to world

참가자: 이수원, 이민재, 황승현

## 주제

단안카메라 증강현실 구현 및 상용화 기술 연구

1. 3D 공간에 물체 구현. K[R|t]w2c
   1. [R|t]w2c의 역함수 [R|t]c2w 구함.
   2. [R|t]c2w에 [P]c(물체의 카메라 상의 좌표 곱하면 [P]w(현실의 좌표) 나옴.
2. Hand의 공간좌표 구현. K[R|t]h2c
   1. [R|t]h2c에 [P]h(손의 좌표) 곱하면 [p]c(카메라 상의 좌표) 나옴
3. [P]w와 [P]h 2개가 같은 곳에 있으면 증강현실 구현 완료

## 해야할 일

- OpenGL로 월드에 구 띄우기
- 역함수 구하기.
- 걸리는 시간 측정하기

-----

2023-04-26 기준 폐기

## 참가자

- 황승현

- 김상현

- 이민재

## 개설 목적

3D Hand Pose 과제 수행

## 우리의 목표

- Mediapipe의 가상 손 위치와 현재 카메라의 위치를 동기화 시켜, 실세계의 손 위치(좌표) 추출

- 2023-04-05(수) 4시에 하는 과제 회의 전까지 solvePnP 공부

## solvePnP란?

- OpenCV에서 perspective n point문제를 푸는 메소드

- 카메라의 위치와 방향을 알아낼 때 쓰는 것

- perspective n point란?
  
  - 영상을 획득한 카메라의 위치 및 방향 (camera pose)을 알아내는 것

## 교재

1. 다크 프로그래머 solvePnP 함수 사용법과 Rodrigues 표현법
   https://darkpgmr.tistory.com/99

2. ArUco Marker Detection 구현 및 Pose Estimation
   https://webnautes.tistory.com/1040

3. Computer vision : algorithms and applications / Richard Szeliski.
- 기타 교재
  
  - OpenCV docs Perspective-n-Point (PnP) pose computation
      https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html
  
  - 컴퓨터비전 특강: ORB SLAM #2 Solve PnP
      [HGU SW 중심대, 한동대 SW중심대학 사업단] https://www.youtube.com/watch?v=tDfAbqQQO0o
  
  - `E`pipolar Geometry, SolvePnP, MonoSLAM*에 관한 설명...
      https://www.youtube.com/watch?v=dVZ7G4fYv50

# 
