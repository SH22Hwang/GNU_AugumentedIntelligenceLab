import numpy as np
W, b = np.array([0, 0]), 0.0
learning_rate = 0.01

def activation(s):
  if s > 0: return 1
  elif s < 0: return -1
  return 0

def out(x):
  return activation (W.dot(x) + b)

def predict(inputs):
  outputs = []
  for x in inputs:
    outputs.append (out(x))
  return outputs

def train(x0, x1, target):
  global W, b
  X = np.array([x0, x1])
  y = out(X)

  ### 예측이 맞으면 아무것도 X
  if target == y: return False  # 가중치 변경X 반환
  ### 예측이 틀리면 학습 실시
  print('가중치 수정 전 target: {} y:{} b:{} W:{}'.format(target, y, b, W))
  W = W + learning_rate * X * target
  b = b + learning_rate * 1 * target
  print('가중치 수정 전 target: {} y:{} b:{} W:{}'.format(target, y, b, W))
  return True

### AND 구현
adjusted = 0
for i in range(100):
  adjusted += train(-1, -1, -1)   # 훈련 데이터 1
  adjusted += train(-1, 1, -1)    # 훈련 데이터 2
  adjusted += train(1, -1, -1)     # 훈련 데이터 3
  adjusted += train(1, 1, 1)      # 훈련 데이터 4
  print('iteration --------------', i)
  if not adjusted: break
  adjusted = 0
  
X = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
yhat = predict(X)
print('x0 x1  y')
for i in range(len(X)):
  print('{0:2d} {1:2d} {2:2d}'.format(X[i][0], X[i][1], yhat[i]))
  
### NAND 구현
adjusted = 0
for i in range(100):
  adjusted += train(-1, -1, -1)   # 훈련 데이터 1
  adjusted += train(-1, 1, 1)    # 훈련 데이터 2
  adjusted += train(1, -1, 1)     # 훈련 데이터 3
  adjusted += train(1, 1, -1)      # 훈련 데이터 4
  print('iteration --------------', i)
  if not adjusted: break
  adjusted = 0
  
X = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
yhat = predict(X)
print('x0 x1  y')
for i in range(len(X)):
  print('{0:2d} {1:2d} {2:2d}'.format(X[i][0], X[i][1], yhat[i]))
  
