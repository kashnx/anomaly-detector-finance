import pandas as pd

# Load the dataset
df = pd.read_csv('../data/Financials.csv')  # Adjust path if needed

# 1. Preview the first few rows
print("🔹 First 5 rows:")
print(df.head(), "\n")

# 2. Display column names
print("🔹 Columns:")
print(df.columns, "\n")

# 3. Check data types
print("🔹 Data types:")
print(df.dtypes, "\n")

# 4. Convert 'Date' column to datetime if present
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    print(f"✅ Converted 'Date' column to datetime. Invalid dates: {df['Date'].isnull().sum()}\n")
else:
    print("⚠️ 'Date' column not found.\n")

# 5. Check for missing values
print("🔹 Missing values per column:")
print(df.isnull().sum(), "\n")

# 6. Show summary statistics for numeric columns
print("🔹 Summary statistics:")
print(df.describe())
