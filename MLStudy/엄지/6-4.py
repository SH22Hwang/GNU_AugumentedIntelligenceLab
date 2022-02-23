import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from yellowbrick.contrib.classifier import DecisionViz

data_loc = 'https://github.com/dknife/ML/raw/main/data/'
df = pd.read_csv(data_loc+'twisted_data.csv')
print(df.tail(5))

df_positive = df[df['y']>0]
df_negative = df[df['y']==0]

plt.scatter(df_positive['x1'], df_positive['x2'], color='r')
plt.scatter(df_negative['x1'], df_negative['x2'], color='g')

X = df[['x1', 'x2']].to_numpy()
y = df['y']

polynomial_svm_clf = Pipeline([
                               ("scaler", StandardScaler()),
                               ("poly_features", PolynomialFeatures(degree=5)),
                               ("svm_clf", LinearSVC(C=1, loss="hinge"))
])

polynomial_svm_clf.fit(X, y)
viz = DecisionViz(polynomial_svm_clf, title="polynomial feature SVM")
viz.fit(X, y)
viz.draw(X, y)
