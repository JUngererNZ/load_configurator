# Conceptual Master Script
from load_configurator import Packer
from Axle_Load_Calculation import PhysicsEngine
from CSV_Export_Loading_Manifesto import Exporter

# 1. Pack items
packed_data = Packer.solve('gensets.csv')

# 2. Check Weights
if PhysicsEngine.is_legal(packed_data):
    # 3. If safe, export and plot
    Exporter.generate_manifest(packed_data)
    print("Configuration successful. Manifesto generated.")
else:
    print("Warning: Load is illegal! Adjusting positions...")