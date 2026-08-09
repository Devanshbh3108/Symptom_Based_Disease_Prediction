import pickle
from pathlib import Path

import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ================== LOAD DATA ==================
data_path = Path("realistic_dataset_no_covid.csv")
if not data_path.exists():
    data_path = Path(r"C:\Users\HP\Downloads\synthetic_health_data.csv")

df = pd.read_csv(data_path)

# ================== SPLIT FEATURES & LABEL ==================
X = df.drop("disease", axis=1)
y = df["disease"]

# ================== ENCODE LABEL ==================
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ================== TRAIN-TEST SPLIT ==================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ================== MODEL ==================
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.08,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="mlogloss",
    random_state=42,
)

# ================== TRAIN ==================
model.fit(X_train, y_train)

# ================== EVALUATE ==================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# ================== SAVE FILES (FOR YOUR APP) ==================
pickle.dump(model, open("symptom_disease_model.pkl", "wb"))
pickle.dump(le, open("disease_label_encoder.pkl", "wb"))
pickle.dump(list(X.columns), open("symptom_features.pkl", "wb"))

print("\nModel and files saved successfully!")
