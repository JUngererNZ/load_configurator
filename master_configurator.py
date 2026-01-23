import pandas as pd
import matplotlib.pyplot as plt
from Integrated_Load_Configurator_Visualizer import SmartTrailer
import os

def run_transport_pipeline(input_csv):
    print("--- Starting Load Configuration Pipeline ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv(input_csv, skiprows=5)
        df = df.dropna(subset=['ORDER NUMBER'])
        df['MASS_KG'] = df['MASS'] * 1000  # Convert tonnes to kg
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 2. Initialize Trailers (Using standard European flatbed specs)
    # L=13.6m, W=2.4m, H=2.6m | Max Front=12t, Max Rear=18t, Wheelbase=10.5m
    trailers = [
        SmartTrailer("Trailer_A", 13.6, 2.4, 2.6, 12000, 18000, 10.5),
        SmartTrailer("Trailer_B", 13.6, 2.4, 2.6, 12000, 18000, 10.5),
        SmartTrailer("Trailer_C", 13.6, 2.4, 2.6, 12000, 18000, 10.5)
    ]

    # 3. Simple Heuristic Packing Logic
    # (Distribute 19 items across 3 trailers)
    items_list = df.to_dict('records')
    for i, item in enumerate(items_list):
        # Determine which trailer to use
        t_idx = i // 7 if i < 14 else 2 
        target_trailer = trailers[t_idx]
        
        # Calculate X position (simplified: place one after another with 0.2m gap)
        current_x_offset = sum(itm['dims'][0] for itm in target_trailer.items) + (len(target_trailer.items) * 0.2)
        
        target_trailer.add_item(
            name=f"{item['ORDER NUMBER']}-{item['CONSIGNMENT']}",
            length=item['LENGTH'],
            width=item['WIDTH'],
            height=item['HEIGHT'],
            mass=item['MASS_KG'],
            x=current_x_offset,
            y=0.15 # Offset from trailer edge
        )

    # 4. Validate Physics and Generate Outputs
    manifest_data = []
    
    for t in trailers:
        f_load, r_load, is_overloaded = t.check_physics()
        status = "FAIL - OVERLOADED" if is_overloaded else "PASS - SECURE"
        print(f"Checking {t.trailer_id}: {status} (F: {f_load:.0f}kg, R: {r_load:.0f}kg)")
        
        # Generate 3D Plot
        t.visualize() 
        
        # Collect data for Manifesto
        for itm in t.items:
            manifest_data.append({
                'Trailer': t.trailer_id,
                'Consignment': itm['name'],
                'X_Pos_Meters': itm['pos'][0],
                'Mass_KG': itm['mass'],
                'Front_Axle_Load': f_load,
                'Rear_Axle_Load': r_load,
                'Safety_Status': status
            })

    # 5. Export Final Manifesto
    manifesto_df = pd.DataFrame(manifest_data)
    manifesto_df.to_csv('FINAL_LOADING_MANIFESTO.csv', index=False)
    print("--- Pipeline Complete: FINAL_LOADING_MANIFESTO.csv generated ---")

if __name__ == "__main__":
    run_transport_pipeline('19 GENSETS VEHICLE CONFIGURATION.xlsx - Sheet1.csv')