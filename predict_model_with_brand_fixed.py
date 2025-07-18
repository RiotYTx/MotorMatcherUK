import sys
import joblib

# Load model and encoders with error handling
try:
    model = joblib.load("car_model.pkl")
    encoders = joblib.load("feature_encoders.pkl")
    target_encoder = joblib.load("target_encoder.pkl")
except Exception as e:
    print(f"Error loading model files: {e}")
    print("The model files may be incompatible with the current scikit-learn version.")
    sys.exit(1)

# Parse command-line arguments
args = dict(arg.split("=") for arg in sys.argv[1:])

# Extract and parse input values
price = float(args.get("price", 15000))
fuel = args.get("fuel", "petrol").lower()
transmission = args.get("transmission", "manual").lower()
mileage = float(args.get("mileage", 30000))
mpg = float(args.get("mpg", 50))
engineSize = float(args.get("engineSize", 1.6))  # Optional default

# Encode categorical values using fitted encoders
try:
    fuel_encoded = encoders["fuelType"].transform([fuel])[0]
    transmission_encoded = encoders["transmission"].transform([transmission])[0]
except ValueError:
    print("Unknown fuel or transmission type.")
    sys.exit(1)

# Create input array
input_data = [[price, fuel_encoded, transmission_encoded, mileage, mpg, engineSize]]

# Predict and decode result
predicted_index = model.predict(input_data)[0]
predicted_model = target_encoder.inverse_transform([predicted_index])[0]

# Output prediction
print(predicted_model)

