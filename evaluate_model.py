import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# 1) Load your cleaned data and drop NAs
df = pd.read_csv("final_cleaned_data.csv")
df.dropna(inplace=True)

# 2) Load model + encoders
model          = joblib.load("car_model.pkl")
encoders       = joblib.load("feature_encoders.pkl")
target_encoder = joblib.load("target_encoder.pkl")

# 3) Normalize text & encode *into the original column names*
df["fuelType"]     = df["fuelType"].str.lower().str.strip()
df["transmission"] = df["transmission"].str.lower().str.strip()
df["brand"]        = df["brand"].str.lower().str.strip()
df["model"]        = df["model"].str.strip()

df["fuelType"]     = encoders["fuelType"].transform(df["fuelType"])
df["transmission"] = encoders["transmission"].transform(df["transmission"])
df["brand"]        = encoders["brand"].transform(df["brand"])
df["model_enc"]    = target_encoder.transform(df["model"])

# 4) Prepare X, y and do a train/test split
features = ["price","fuelType","transmission","mileage","mpg","engineSize","brand"]
X = df[features]
y = df["model_enc"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5) Predict & print classification report
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()
print("\n===== Classification Report =====")
print(report_df.to_string())

# 6) Confusion matrix
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(8,6))
im = ax.imshow(cm, cmap="Blues")
ax.set_title("Confusion Matrix")
ax.set_xlabel("Predicted label index")
ax.set_ylabel("True label index")
fig.colorbar(im, ax=ax)
plt.tight_layout()
plt.savefig("confusion_matrix.png")
print("\nSaved confusion matrix to confusion_matrix.png")
