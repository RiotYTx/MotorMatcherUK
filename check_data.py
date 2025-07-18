import pandas as pd

df = pd.read_csv("final_cleaned_data.csv")
print("Shape:", df.shape)
print("First few rows:\n", df.head())
