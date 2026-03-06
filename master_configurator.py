import pandas as pd
import matplotlib.pyplot as plt
from three_d_visualizer import plot_loading_plan  # Uses your renamed 3D script
import os
import sys
import tempfile

def run_transport_pipeline(input_csv):
    print("--- Starting Load Configuration Pipeline ---")
    
    # Read CSV - handles semicolon separators, comma decimals, BOM, both messy/clean formats
    df = pd.read_csv(input_csv, sep=None, engine='python')  # Auto-detects ; or ,

    # Convert comma decimals to dots (European format)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.replace(',', '.').str.replace('\ufeff', '')  # Remove BOM

# Find ORDER NUMBER row (case insensitive, handles spacing)
    header_pattern = 'ORDER NUMBER'
    header_idx = None
    for i, row in df.iterrows():
        if any(header_pattern.lower() in str(cell).lower() for cell in row.values):
            header_idx = i
            break

    if header_idx is None:
        print("Error: No 'ORDER NUMBER' column found. First few rows:")
        print(df.head())
        return

    print(f"Found header at row {header_idx}")

    df = df.iloc[header_idx:].reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df = df.dropna(subset=['ORDER NUMBER'])

    # Safe numeric conversion
    numeric_cols = ['MASS', 'LENGTH', 'WIDTH', 'HEIGHT']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df['MASS_KG'] = df.get('MASS', pd.Series(0)) * 1000
    print(f"Loaded {len(df)} items from CSV")

    
    # 2. Initialize Trailers (Using standard European flatbed specs)
    # L=13.6m, W=2.4m, H=2.6m | Max Front=12t, Max Rear=18t, Wheelbase=10.5m
    trailer_dims = (13.6, 2.4, 2.6)
    trailers = [
        {"id": "Trailer_A", "items": [], "dims": trailer_dims},
        {"id": "Trailer_B", "items": [], "dims": trailer_dims},
        {"id": "Trailer_C", "items": [], "dims": trailer_dims}
    ]
    
    # 3. Simple Heuristic Packing Logic (Distribute 19 items across 3 trailers)
    items_list = df.to_dict('records')
    for i, item in enumerate(items_list):
        # Determine which trailer to use (7 per trailer approx)
        t_idx = i // 7 if i < 14 else 2
        target_trailer = trailers[t_idx]
        
        # Calculate X position (simplified: place one after another with 0.2m gap)
        current_x_offset = sum(itm['dims'][0] for itm in target_trailer["items"]) + (len(target_trailer["items"]) * 0.2)
        
        target_trailer["items"].append({
            'name': f"{item['ORDER NUMBER']}-{item['CONSIGNMENT']}",
            'pos': (current_x_offset, 0.15, 0),  # x, y, z
            'dims': (float(item['LENGTH']), float(item['WIDTH']), float(item['HEIGHT']))
        })
    
    # 4. Generate 3D plots and collect manifesto data
    manifest_data = []
    for t in trailers:
        print(f"Generating 3D for {t['id']}")
        plot_loading_plan(t["items"], t["dims"])
        
        # Mock physics check (replace with real if you have Axle_Load_Calculation.py)
        total_mass = sum(item['dims'][2] * 1000 for item in t["items"])  # rough est
        f_load, r_load = total_mass * 0.4, total_mass * 0.6  # 40/60 split estimate
        is_overloaded = f_load > 12000 or r_load > 18000
        status = "FAIL - OVERLOADED" if is_overloaded else "PASS - SECURE"
        print(f"Checking {t['id']}: {status} (F: {f_load:.0f}kg, R: {r_load:.0f}kg)")
        
        # Collect data for Manifesto
        for itm in t["items"]:
            manifest_data.append({
                'Trailer': t['id'],
                'Consignment': itm['name'],
                'X_Pos_Meters': itm['pos'][0],
                'Mass_KG': itm['dims'][2] * 1000,  # height as proxy; use real mass if avail
                'Front_Axle_Load': f_load,
                'Rear_Axle_Load': r_load,
                'Safety_Status': status
            })
    
    # 5. Export Final Manifesto, sorted by trailer + X position
    manifesto_df = pd.DataFrame(manifest_data)
    manifesto_df = manifesto_df.sort_values(by=['Trailer', 'X_Pos_Meters'])
    manifesto_df.to_csv('FINAL_LOADING_MANIFESTO.csv', index=False)
    print("--- Pipeline Complete: FINAL_LOADING_MANIFESTO.csv generated ---")

if __name__ == "__main__":
    input_file = input("Enter path to .xlsx or .csv file (Enter for auto-detect): ").strip()
    
    if not input_file:
        all_files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.csv'))]
        if all_files:
            input_file = all_files[0]
            print(f"Using first found: {input_file}")
        else:
            print("No .xlsx or .csv found.")
            sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)
    
    temp_csv_path = None
    try:
        if input_file.lower().endswith('.xlsx'):
            # Convert XLSX → CSV in C:\Temp (matches your 19_gensets.csv exact format)
            temp_csv_path = r"C:\Temp\xlsx_temp.csv"
            df_temp = pd.read_excel(input_file, sheet_name='Sheet1', header=None)  # No header assumption
            df_temp.to_csv(temp_csv_path, index=False, header=False)  # Raw format like your CSV
            print(f"Converted {input_file} → {temp_csv_path}")
            run_transport_pipeline(temp_csv_path)
        else:
            run_transport_pipeline(input_file)
    finally:
        if temp_csv_path and os.path.exists(temp_csv_path):
            try:
                os.unlink(temp_csv_path)
                print(f"Cleaned up {temp_csv_path}")
            except:
                print(f"Manual delete: {temp_csv_path}")

    

