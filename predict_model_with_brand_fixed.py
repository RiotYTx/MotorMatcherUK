import sys
import joblib
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Load model and encoders
model = joblib.load("car_model.pkl")
encoders = joblib.load("feature_encoders.pkl")
model_encoder = joblib.load("model_encoder.pkl")

# Build brand-model mapping
brand_model_map = {}
csv_dir = Path("car_data")
for file in csv_dir.glob("*.csv"):
    brand = file.stem.lower()
    try:
        df = pd.read_csv(file)
        if "model" in df.columns:
            for model_name in df["model"].unique():
                brand_model_map.setdefault(brand, set()).add(model_name)
    except:
        continue

# Parse arguments
args = dict(arg.split("=") for arg in sys.argv[1:])
year = int(args.get("year", 2019))
price = float(args.get("price", 15000))
transmission = args.get("transmission", "manual").lower()
mileage = float(args.get("mileage", 30000))
fuel = args.get("fuel", "petrol").lower()
tax = float(args.get("tax", 150))
mpg = float(args.get("mpg", 55))
engineSize = float(args.get("engineSize", 1.4))
brand = args.get("brand", "").lower()

# Encode categorical features
try:
    transmission_encoded = encoders["transmission"].transform([transmission])[0]
    fuel_encoded = encoders["fuelType"].transform([fuel])[0]
except:
    print("Encoding error")
    sys.exit(1)

# Prepare input features
X_input = np.array([[year, price, transmission_encoded, mileage, fuel_encoded, tax, mpg, engineSize]])

# Predict probabilities
probs = model.predict_proba(X_input)[0]
top_idx = np.argsort(probs)[::-1]

# Try to match prediction to selected brand
for idx in top_idx:
    predicted_model = model_encoder.inverse_transform([idx])[0]
    if not brand or predicted_model in brand_model_map.get(brand, []):
        print(predicted_model)
        break
else:
    # Fallback to top predicted model even if brand doesn't match
    fallback_model = model_encoder.inverse_transform([top_idx[0]])[0]
    print(fallback_model)
