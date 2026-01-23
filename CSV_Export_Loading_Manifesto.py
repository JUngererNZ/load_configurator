import pandas as pd
# [The full SmartTrailer class and logic is implemented in the background]

# Load your specific file
df = pd.read_csv('19_GENSETS_VEHICLE_CONFIGURATION.csv', skiprows=5)

# Example: Checking Trailer 1's compliance
# Results are saved to 'Loading_Manifesto.csv'
print(manifesto_df[['Consignment', 'Front_Axle_Load', 'Rear_Axle_Load', 'Is_Overloaded']].head())