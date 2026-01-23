import pandas as pd
import numpy as np
import itertools
from Integrated_Load_Configurator_Visualizer import SmartTrailer

def optimize_trailer_load(trailer_id, items_to_pack):
    """
    Tries different permutations of items to find the best axle balance.
    """
    best_config = None
    lowest_imbalance = float('inf')
    
    # To keep it fast, we test a sample of permutations if there are many items
    import random
    iterations = 50 
    
    for _ in range(iterations):
        random.shuffle(items_to_pack)
        
        # Create a test trailer
        test_t = SmartTrailer(trailer_id, 13.6, 2.4, 2.6, 12000, 18000, 10.5)
        current_x = 0.2
        
        for item in items_to_pack:
            test_t.add_item(
                name=item['Consignment'],
                length=item['LENGTH'], width=item['WIDTH'], height=item['HEIGHT'],
                mass=item['MASS_KG'], x=current_x, y=0.15
            )
            current_x += item['LENGTH'] + 0.2 # Add gap
            
        f_load, r_load, is_overloaded = test_t.check_physics()
        
        # We want the ratio of front/rear load to be as balanced as possible
        # or at least well within the limits.
        imbalance = abs(f_load - r_load)
        
        if not is_overloaded and imbalance < lowest_imbalance:
            lowest_imbalance = imbalance
            best_config = test_t
            
    return best_config

def run_optimized_pipeline(input_csv):
    print("--- Starting Auto-Optimized Load Pipeline ---")
    df = pd.read_csv(input_csv, skiprows=5).dropna(subset=['ORDER NUMBER'])
    df['MASS_KG'] = df['MASS'] * 1000
    df['Consignment'] = df['ORDER NUMBER'] + "-" + df['CONSIGNMENT']
    
    # Group items into 3 batches
    all_items = df.to_dict('records')
    batches = [all_items[0:6], all_items[6:13], all_items[13:19]]
    
    optimized_trailers = []
    for i, batch in enumerate(batches):
        print(f"Optimizing Trailer {i+1}...")
        best_t = optimize_trailer_load(f"Trailer_{i+1}", batch)
        if best_t:
            optimized_trailers.append(best_t)
            best_t.visualize()
        else:
            print(f"Warning: Could not find a legal configuration for Trailer {i+1}")

    # Export Logic remains the same...
    print("--- Optimization Complete ---")

if __name__ == "__main__":
    run_optimized_pipeline('19 GENSETS VEHICLE CONFIGURATION.xlsx - Sheet1.csv')