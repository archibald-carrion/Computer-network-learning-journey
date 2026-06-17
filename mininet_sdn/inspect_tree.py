import pickle
from sklearn import tree

with open("traffic_model.pkl", "rb") as f:
    model = pickle.load(f)

print(tree.export_text(model))