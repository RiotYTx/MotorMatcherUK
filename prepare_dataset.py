# prepare_dataset.py
import pandas as pd
import glob
import os
import sys

# 1) Find all CSVs except any existing final_cleaned_data.csv
csv_files = [f for f in glob.glob("*.csv") if os.path.basename(f) != "final_cleaned_data.csv"]
print("🔍 CSV files found to combine:", csv_files)

if not csv_files:
    print("❌ No CSV files to process. Are your brand CSVs in the same folder as this script?")
    sys.exit(1)

dfs = []
for file in csv_files:
    try:
        df = pd.read_csv(file)
        print(f"   • Loaded {file} — shape: {df.shape}")
    except Exception as e:
        print(f"❌ Failed to read {file}: {e}")
        continue

    # 2) Derive brand from filename
    brand = os.path.splitext(os.path.basename(file))[0].lower()
    df["brand"] = brand
    dfs.append(df)

if not dfs:
    print("❌ No DataFrames successfully loaded; aborting.")
    sys.exit(1)

# 3) Concatenate
combined = pd.concat(dfs, ignore_index=True)
print("➕ Combined DataFrame shape before cleaning:", combined.shape)

# 4) Drop unwanted column if present
if "tax(£)" in combined.columns:
    combined.drop(columns=["tax(£)"], inplace=True)
    print("🗑️ Dropped tax(£) column")

# 5) Drop any rows with missing values
before = combined.shape[0]
combined.dropna(inplace=True)
after = combined.shape[0]
print(f"🧹 Dropped {before - after} rows with missing data → shape now {combined.shape}")

# 6) Save
combined.to_csv("final_cleaned_data.csv", index=False)
print("✅ Saved final_cleaned_data.csv with shape:", combined.shape)
