import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

# Remove old artifacts
for f in ("car_model.pkl","feature_encoders.pkl","target_encoder.pkl"):
    if os.path.exists(f): os.remove(f)

# Load the merged CSV (with real brand column)
df = pd.read_csv("final_cleaned_data.csv")
df.dropna(inplace=True)
if "tax(£)" in df.columns:
    df.drop(columns=["tax(£)"], inplace=True)

# Normalize text
df["fuelType"]     = df["fuelType"].str.lower().str.strip()
df["transmission"] = df["transmission"].str.lower().str.strip()
df["model"]        = df["model"].str.strip()
df["brand"]        = df["brand"].str.lower().str.strip()

# Encode categorical features
encoders = {}
for col in ["fuelType","transmission","brand"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

print("🔑 Encoded brands:", encoders["brand"].classes_)

# Encode target
target_encoder = LabelEncoder()
df["model_encoded"] = target_encoder.fit_transform(df["model"])
print("🛞 Encoded models:", target_encoder.classes_[:10], "...")

# Features & target
features = ["price","fuelType","transmission","mileage","mpg","engineSize","brand"]
X = df[features]
y = df["model_encoded"]

# Train/test
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

# Train & save
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
joblib.dump(model, "car_model.pkl")
joblib.dump(encoders, "feature_encoders.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")

print("✅ Retrained model with correct brand encoding.")
