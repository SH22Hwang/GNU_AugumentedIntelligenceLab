import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

iris = load_iris()
X, y = iris.data, iris.target
dec_tree = DecisionTreeClassifier(max_depth=3, criterion='entropy')
dec_tree.fit(X, y)

export_graphviz(
    dec_tree,
    out_file=('./dec_tree_for_iris.dot'),
    feature_names=iris.feature_names,
)

!dot -Tjpg dec_tree_for_iris.dot -o dec_tree_for_iris.jpg

dec_tree_img = plt.imread('./dec_tree_for_iris.jpg')
plt.figure(num=None, figsize=(12,8), dpi=80, facecolor='w', edgecolor='k')
plt.imshow(dec_tree_img)
