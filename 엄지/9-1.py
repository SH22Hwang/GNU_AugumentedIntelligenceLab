import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

url = 'https://github.com/dknife/ML/raw/main/data/image/david.png'
img = mpimg.imread(url)

plt.imshow(img)  # 아래는 david.png 뿐 아니라 book.png도 로드한 결과임

img.shape

# 책에는 아래 URL이 없으나 그림은 나타나 있음
url = 'https://github.com/dknife/ML/raw/main/data/image/book.png'
img = mpimg.imread(url)

plt.imshow(img)  # 아래는 david.png 뿐 아니라 book.png도 로드한 결과임.

# 다비드 그림을 사용하자
url = 'https://github.com/dknife/ML/raw/main/data/image/david.png'
img = mpimg.imread(url)

def padding(image, p_size):    # 넘파이의 pad 함수를 이용한 패딩 구현
    padded_img = np.pad(
                   array = image,
                   pad_width = ((p_size,p_size), (p_size,p_size), (0,0)),
                   mode = 'constant', constant_values = 0)
    return padded_img
  
padded = padding(img, 2)
plt.imshow(padded)
padded.shape

box_filter = np.array(
   [[1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]])

def apply_filter(small_region, filter) :
    conv = np.multiply(small_region, filter)
    return np.sum(conv)
  
def convolution(img, filter):
   r, c, channels = img.shape
   rp, cp = filter.shape
   th_r, th_c = (rp-1)//2 , (cp-1)//2
  
   start = np.array([ th_r, th_c ])
   end = np.array([r, c]) - start
   print(start, end, rp, cp)
   conv_img = np.zeros( (r - th_r*2, c - th_c*2, channels) )

   for channel in range(channels):
       for i in range(start[0], end[0]):
           for j in range(start[1], end[1]):
               conv_img[i-th_r, j-th_c, channel] = apply_filter(
                       img[i-th_r:i+th_r+1, j-th_c:j+th_c+1, channel], 
                       filter)
   return conv_img

conv_img = convolution(padded, box_filter)
plt.imshow(conv_img)

laplacian = np.array(
   [[1, 0, 1],
    [0, -4, 0],
    [1, 0, 1],    ])
conv_img = convolution(padded, laplacian)
plt.imshow(conv_img)

unknown = np.random.rand(3, 3)

conv_img = convolution(padded, unknown)
np.clip(conv_img, 0, 255)
plt.imshow(conv_img)
