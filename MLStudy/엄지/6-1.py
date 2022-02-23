import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# 1번
data_loc = 'https://github.com/dknife/ML/raw/main/data/'
df = pd.read_csv(data_loc+'nonlinear.csv')

plt.scatter(df['x'], df['y'])

# 2번
from sklearn.preprocessing import PolynomialFeatures

X = df['x'].to_numpy()
y = df['y'].to_numpy()
X = X.reshape(-1, 1)  # 하나씩 재배열
feature_cubic = PolynomialFeatures(degree = 3)
X_3 = feature_cubic.fit_transform(X)

# 3번
lin_model = LinearRegression()
domain = np.linspace(0, 1, 100).reshape(-1, 1)  # 입력은 2차원 벡터로 변형

# 4번
lin_model.fit(X_3, y)
domain_3 = feature_cubic.fit_transform(domain)
predictions = lin_model.predict(domain_3)
plt.scatter(df['x'], df['y'])
plt.scatter(domain, predictions, color='r')
