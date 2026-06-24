import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt


def train_evaluate(X, y, feature_names, label_encoder):
    """Train a Random Forest classifier and evaluate on a held-out test set."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    rf.fit(X_train_scaled, y_train)
    y_pred = rf.predict(X_test_scaled)

    results = {
        'accuracy': accuracy_score(y_test, y_pred),
        'macro_f1': f1_score(y_test, y_pred, average='macro'),
        'classification_report': classification_report(y_test, y_pred, target_names=label_encoder.classes_),
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'model': rf,
        'scaler': scaler,
    }

    print("\n--- Random Forest Performance ---")
    print(f"Accuracy: {results['accuracy']:.4f}")
    print(f"Macro F1-Score: {results['macro_f1']:.4f}")
    print("\nClassification Report:")
    print(results['classification_report'])
    print("\nUnique classes in y_test:", np.unique(y_test))
    print("Unique classes in y_pred:", np.unique(y_pred))

    plt.figure(figsize=(20, 16))
    all_classes = label_encoder.classes_
    conf_matrix = confusion_matrix(y_test, y_pred, labels=range(len(all_classes)))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=conf_matrix,
        display_labels=all_classes
    )
    disp.plot(cmap='Blues', xticks_rotation='vertical')
    plt.title("Confusion Matrix - Random Forest", fontsize=20)
    plt.xticks(fontsize=8, rotation=90)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

    return results, X_train_scaled, X_test_scaled
