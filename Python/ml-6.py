import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
temp = pd.read_csv(r"C:/Users/SHIVANSH/Downloads/archive (1)/temp.csv")
yield_df = pd.read_csv(r"C:/Users/SHIVANSH/Downloads/archive (1)/yield_df.csv")
rainfall = pd.read_csv(r"C:/Users/SHIVANSH/Downloads/archive (1)/rainfall.csv")

# Clean column names
temp.columns = temp.columns.str.strip().str.lower()
yield_df.columns = yield_df.columns.str.strip().str.lower()
rainfall.columns = rainfall.columns.str.strip().str.lower()

# Create figure
plt.figure(figsize=(15,10))

# Plot 1: Temperature Distribution
plt.subplot(2,2,1)
plt.hist(temp['avg_temp'], bins=20, color='red', alpha=0.7)
plt.title('Temperature Distribution')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')

# Plot 2: Rainfall vs Yield (if common columns exist)
if 'area' in yield_df.columns and 'area' in rainfall.columns:
    merged = yield_df.merge(rainfall, on='area')
    plt.subplot(2,2,2)
    plt.title('Rainfall vs Crop Yield')
    plt.xlabel('Rainfall (mm)')
    plt.ylabel('Yield (hg/ha)')

# Plot 3: Top Producing Areas
plt.subplot(2,2,3)
yield_df.nlargest(10, 'hg/ha_yield').plot.bar(x='area', y='hg/ha_yield', legend=False)
plt.title('Top 10 Highest Yielding Areas')
plt.ylabel('Yield (hg/ha)')
plt.xticks(rotation=45)

# Plot 4: Temperature vs Yield (if common columns exist)
if 'area' in yield_df.columns and 'area' in temp.columns:
    merged_temp = yield_df.merge(temp, on='area')
    plt.subplot(2,2,4)
    plt.scatter(merged_temp['avg_temp'], merged_temp['hg/ha_yield'], alpha=0.5, color='green')
    plt.title('Temperature vs Crop Yield')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Yield (hg/ha)')

#plt.tight_layout()
plt.show()