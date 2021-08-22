import numpy as np

W, b = np.array([0.5, 0.5]), -0.7

def perceptron(x1, x2):
  x = np.array([x1, x2])
  tmp = np.sum( W * x ) + b
  if tmp <= 0:  return -1
  else: return 1
  
print('=== 퍼셉트론으로 구현한 AND 게이트 ===')
for xs in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
  y = perceptron(xs[0], xs[1])
  print(xs, ':', y)
  
W, b = np.array([0.7, 0.7]), .5

print('=== 퍼셉트론으로 구현한 OR 게이트 ===')
for xs in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
  y = perceptron(xs[0], xs[1])
  print(xs, ':', y)
