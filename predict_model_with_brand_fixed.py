# predict_model_with_brand_fixed.py

import sys
import joblib

# Load model and encoders
model = joblib.load("car_model.pkl")
encoders = joblib.load("feature_encoders.pkl")
target_encoder = joblib.load("target_encoder.pkl")

# Parse command-line arguments
args = dict(arg.split("=") for arg in sys.argv[1:])

# Get inputs
price = float(args.get("price", 15000))
fuel = args.get("fuel", "petrol").lower()
trans = args.get("transmission", "manual").lower()
mileage = float(args.get("mileage", 30000))
mpg = float(args.get("mpg", 50))
engine = float(args.get("engineSize", 1.6))

#print("Received args:", args)
#print("Parsed:", price, fuel, trans, mileage, mpg, engine)

# Encode
try:
    fuel_encoded = encoders["fuelType"].transform([fuel])[0]
    trans_encoded = encoders["transmission"].transform([trans])[0]
except Exception as e:
    print("Encoding error:", e)
    sys.exit(1)

#print("Encoded inputs:", fuel_encoded, trans_encoded)

# Predict
input_data = [[price, fuel_encoded, trans_encoded, mileage, mpg, engine]]
predicted_index = model.predict(input_data)[0]
predicted_model = target_encoder.inverse_transform([predicted_index])[0]

# Output
print(predicted_model)
