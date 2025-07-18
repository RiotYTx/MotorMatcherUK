import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import glob

# Find your cleaned dataset
csv_files = glob.glob("*.csv")
for f in csv_files:
    print("Found CSV file:", f)

# Adjust this if you know the file name for sure:
df = pd.read_csv("final_cleaned_data.csv")  # Replace with your actual final cleaned file name

# Drop missing values
if "tax(£)" in df.columns:
    df.drop(columns=["tax(£)"], inplace=True)

df = df.dropna()

# Normalize text columns to lowercase
df["fuelType"] = df["fuelType"].str.lower()
df["transmission"] = df["transmission"].str.lower()

# Encode fuel and transmission
encoders = {}
for col in ["fuelType", "transmission"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le


# Encode model name
target_encoder = LabelEncoder()
df["model_encoded"] = target_encoder.fit_transform(df["model"])

# Select features and target
features = ["price", "fuelType", "transmission", "mileage", "mpg", "engineSize"]
X = df[features]
y = df["model_encoded"]

# Train/test split (optional)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Save all files
joblib.dump(model, "car_model.pkl")
joblib.dump(encoders, "feature_encoders.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")

print("✅ Model trained and saved in current Replit environment.")

