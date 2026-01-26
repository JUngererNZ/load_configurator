import pandas as pd
import matplotlib.pyplot as plt
from Integrated_Load_Configurator_Visualizer import SmartTrailer  # Adjust import if needed
import os
import sys
import tempfile

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
    
    # 3. Simple Heuristic Packing Logic (Distribute 19 items across 3 trailers)
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
            y=0.15  # Offset from trailer edge
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
    # Prompt for XLSX file
    xlsx_file = input("Enter the path to your .xlsx file (or press Enter for current dir search): ").strip()
    if not xlsx_file:
        # Auto-find .xlsx in current dir
        xlsx_files = [f for f in os.listdir('.') if f.lower().endswith('.xlsx')]
        if xlsx_files:
            xlsx_file = xlsx_files[0]  # Use first found
            print(f"Using first found XLSX: {xlsx_file}")
        else:
            print("No .xlsx found. Place your file and re-run.")
            sys.exit(1)
    
    if not os.path.exists(xlsx_file):
        print(f"File not found: {xlsx_file}")
        sys.exit(1)
    
    # Convert XLSX Sheet1 to temp CSV (skiprows handled in pipeline)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as temp_csv:
        temp_csv_path = temp_csv.name
        df_temp = pd.read_excel(xlsx_file, sheet_name='Sheet1')
        df_temp.to_csv(temp_csv_path, index=False)
        print(f"Converted {xlsx_file} (Sheet1) to temp CSV: {temp_csv_path}")
    
    # Run pipeline
    run_transport_pipeline(temp_csv_path)
    
    # Cleanup temp file
    os.unlink(temp_csv_path)
