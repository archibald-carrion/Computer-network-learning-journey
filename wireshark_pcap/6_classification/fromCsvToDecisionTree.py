import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

def train_network_classifier(csv_file):
    # 1. Load the dataset
    df = pd.read_csv(csv_file)
    
    # 2. Define Features (X) and Target (y)
    # We use the stats as features and the 'label' as what we want to predict
    X = df[['mean_len', 'max_len', 'min_len', 'pkt_count']]
    y = df['label']
    
    # 3. Split into Training and Testing sets (usually 80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Initialize and Train the Decision Tree
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    
    # 5. Evaluate the model
    predictions = clf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"Model Training Complete. Accuracy: {accuracy * 100}%")
    print("\n--- Decision Tree Logic ---")
    # This shows the "If/Then" logic the model created
    tree_rules = export_text(clf, feature_names=['mean_len', 'max_len', 'min_len', 'pkt_count'])
    print(tree_rules)

if __name__ == "__main__":
    try:
        train_network_classifier("network_dataset.csv")
    except FileNotFoundError:
        print("Error: network_dataset.csv not found. Run the CSV converter script first!")
