import pandas as pd
import pickle

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("flow_dataset.csv")

X = df[
    [
        "packet_count",
        "byte_count",
        "duration_sec",
        "duration_nsec",
        "byte_rate",
        "packet_rate",
        "avg_pkt_size"
    ]
]

y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

print(classification_report(
    y_test,
    model.predict(X_test)
))

with open("traffic_model.pkl", "wb") as f:
    pickle.dump(model, f)