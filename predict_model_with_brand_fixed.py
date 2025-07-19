import sys
import joblib

# Load model and encoders
model = joblib.load("car_model.pkl")
encoders = joblib.load("feature_encoders.pkl")
target_encoder = joblib.load("target_encoder.pkl")

# Parse command-line arguments
args = dict(arg.split("=") for arg in sys.argv[1:])

# Read and clean inputs
price = float(args.get("price", 15000))
fuel = args.get("fuel", "petrol").lower().strip()
trans = args.get("transmission", "manual").lower().strip()
mileage = float(args.get("mileage", 30000))
mpg = float(args.get("mpg", 50))
engine = float(args.get("engineSize", 1.6))
brand = args.get("brand", "any").lower().strip()

# Encode inputs
try:
    fuel_encoded = encoders["fuelType"].transform([fuel])[0]
    trans_encoded = encoders["transmission"].transform([trans])[0]

    if brand == "any":
        # Use fallback brand if user doesn't specify
        fallback_brand = "ford"
        brand_encoded = encoders["brand"].transform([fallback_brand])[0]
    else:
        brand_encoded = encoders["brand"].transform([brand])[0]

except Exception as e:
    print(f"Encoding error: {e}")
    sys.exit(1)

# Prepare input for prediction
input_data = [[price, fuel_encoded, trans_encoded, mileage, mpg, engine, brand_encoded]]

# Predict
try:
    predicted_index = model.predict(input_data)[0]
    predicted_model = target_encoder.inverse_transform([predicted_index])[0]
    print(predicted_model)
except Exception as e:
    print(f"Prediction error: {e}")
    sys.exit(1)
