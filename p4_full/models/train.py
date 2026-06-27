import pandas as pd
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('./data/dataset.csv')
X = df[['pkt_rate','avg_pkt_size','flow_duration']]
y = df['class']

clf = DecisionTreeClassifier(max_depth=3)
clf.fit(X,y)

print("Feature importance:", clf.feature_importances_)
print("Rules:")
from sklearn import tree
print(tree.export_text(clf))
