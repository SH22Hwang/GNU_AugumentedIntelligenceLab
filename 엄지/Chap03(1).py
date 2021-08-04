# 3.1 setting
import numpy as np
import random

randArray = np.random.randint(0,9,(10000,10000))

randArrayPlus = randArray + 1

## check
print(randArray, '\n')
print(randArrayPlus)

for i in range(0, 10, 2):
  randArray[i] = 0

for i in range(1, 10, 2):
  randArray[i][1::2] = 0

randArray
