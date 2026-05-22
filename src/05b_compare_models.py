import os
import joblib
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.impute import SimpleImputer

# --------------------------------------------------
# Resolve project root
# --------------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_dir = os.path.join(project_root, "models")

# --------------------------------------------------
# Load data
# --------------------------------------------------
print("Loading data...")
X_train = joblib.load(os.path.join(models_dir, "xtrain.pkl"))
y_train = joblib.load(os.path.join(models_dir, "ytrain.pkl"))
X_test = joblib.load(os.path.join(models_dir, "X_test.pkl"))
y_test = joblib.load(os.path.join(models_dir, "y_test.pkl"))

print(f"Loaded {X_train.shape[0]} training samples and {X_test.shape[0]} test samples.\n")

print("Imputing any missing values (NaNs)...")
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)
print("Imputation complete.\n")

# --------------------------------------------------
# Define Intrusion Detection Models
# --------------------------------------------------
# Note: Using LinearSVC instead of standard SVC for performance on large datasets.
# MLPClassifier acts as a basic Neural Network.
models = {
    "Random Forest": RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "SVM (Linear)": LinearSVC(random_state=42, max_iter=2000, dual=False),
    "Neural Network": MLPClassifier(hidden_layer_sizes=(50,), max_iter=200, random_state=42)
}

results = {}

# --------------------------------------------------
# Train and Evaluate Models
# --------------------------------------------------
for name, model in models.items():
    print(f"--- Training {name} ---")
    start_time = time.time()
    
    # Train
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    train_time = time.time() - start_time
    
    results[name] = {
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-Score": f1,
        "Time (s)": train_time
    }
    print(f"{name} Evaluation Complete in {train_time:.2f}s.\n")

# --------------------------------------------------
# Compare Results
# --------------------------------------------------
print("=========================================================================================")
print("                               INTRUSION DETECTION SYSTEMS COMPARISON")
print("=========================================================================================")
print(f"{'Model':<18} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'Time(s)':<8}")
print("-" * 89)
for name, metrics in results.items():
    print(f"{name:<18} | {metrics['Accuracy']:<10.4f} | {metrics['Precision']:<10.4f} | {metrics['Recall']:<10.4f} | {metrics['F1-Score']:<10.4f} | {metrics['Time (s)']:<8.2f}")
print("=========================================================================================\n")

print("--- Key Contributions of Techniques ---")
print("1. Data Preprocessing (Scaling/Encoding) : Improves data quality and accuracy.")
print("2. Random Forest (Ensemble Learning)     : High detection accuracy.")
print("3. SVM (Classification)                  : Robust intrusion detection.")
print("4. Decision Tree (Supervised Learning)   : Fast and interpretable model.")
print("5. Neural Networks (Deep Learning)       : Handles complex network patterns.")
