# solvePnP 스터디

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
