import numpy as np
import matplotlib.pyplot as plt

U = np.random.rand(2,3)   # 연결강도 U
W = np.random.rand(3,2)   # 연결강도 W
learning_rate = 1.0       # 학습률

def sigmoid(v):
  return 1 / (1+np.exp(-v))

def derivative_sigmoid(v):
  s = sigmoid(v)
  return s*(1-s)

input = np.zeros(2)

h_sum, h_out, h_deriv = np.zeros(3), np.zeros(3), np.zeros(3)
h_error, h_delta = np.zeros(3), np.zeros(3)

yy_error, y_delta = np.zeros(2), np.zeros(2)
y_error, h_delta = np.zeros(2), np.zeros(2)

def forward_xh(x):
  global input, h_sum, h_out, h_deriv
  input = x
  h_sum = U.T.dot(input)
  h_out = sigmoid(h_sum)
  h_deriv = derivative_sigmoid(h_sum)

def forward_hy():
  global y_sum, y_out, y_deriv
  y_sum = W.T.dot(h_out)
  y_out = sigmoid(y_sum)
  y_deriv = derivative_sigmoid(y_sum)

def compute_error(target):
  return y_out - target

def backward_y(error):
  global y_error, y_delta, W
  y_error = error
  y_delta = y_deriv * y_error
  dW = - learning_rate * np.outer(h_out, y_delta)
  W = W + dW

def backward_h():
  global h_error, h_delta, U
  h_error = W.dot(y_delta)
  h_delta = h_deriv * h_error
  dU = - learning_rate * np.outer(input, h_delta)
  U = U + dU

def train(x, target):
  forward_xh(x)
  forward_hy()
  e = compute_error(target)
  backward_y(e)
  backward_h()
  return e**2

loss = []

for i in range(1000):
  e_accum=0
  true = np.array([1,0])
  false = np.array([0,1])
  e_accum += train(np.array([0,0]), false)
  e_accum += train(np.array([0,1]), true)
  e_accum += train(np.array([1,1]), false)
  e_accum += train(np.array([1,0]), true)
  loss.append(e_accum)

plt.plot(loss)
plt.ylabel('loss')
plt.xlabel('training')
plt.show()

def test(X):
  y_hat = []
  for x in X:
    forward_xh(x)
    forward_hy()
    y_hat.append(y_out)
  return y_hat

test(np.array([[0,0], [0,1], [1,0], [1,1]]))
