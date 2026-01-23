import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import pandas as pd

class SmartTrailer:
    def __init__(self, L, W, H, max_front, max_rear, wheelbase_offset):
        self.dims = (L, W, H)
        self.max_front = max_front
        self.max_rear = max_rear
        self.wb_offset = wheelbase_offset # Kingpin to center of rear bogie
        self.items = []

    def add_item(self, name, length, width, height, mass, x, y):
        # Center of Gravity assumed at center of item footprint
        cog_x = x + (length / 2)
        self.items.append({
            'name': name,
            'dims': (length, width, height),
            'pos': (x, y, 0),
            'mass': mass,
            'cog_x': cog_x
        })

    def check_physics(self):
        total_mass = sum(i['mass'] for i in self.items)
        if total_mass == 0: return 0, 0, False
        
        # Calculate combined COG relative to trailer front
        total_moment = sum(i['mass'] * i['cog_x'] for i in self.items)
        combined_cog = total_moment / total_mass
        
        # Lever principle for axle loads
        rear_load = (combined_cog / self.wb_offset) * total_mass
        front_load = total_mass - rear_load
        
        is_overloaded = (front_load > self.max_front) or (rear_load > self.max_rear)
        return front_load, rear_load, is_overloaded

    def visualize(self):
        f_load, r_load, overloaded = self.check_physics()
        fig = plt.figure(figsize=(14, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        # Color logic: Red if overloaded, Cyan if safe
        theme_color = 'red' if overloaded else 'cyan'
        edge_color = 'darkred' if overloaded else 'blue'

        # Draw Trailer Bed
        L, W, H = self.dims
        bed = [[(0,0,0), (L,0,0), (L,W,0), (0,W,0)]]
        ax.add_collection3d(Poly3DCollection(bed, color='lightgrey', alpha=0.5))

        for itm in self.items:
            x, y, z = itm['pos']
            dx, dy, dz = itm['dims']
            
            # Create cube vertices
            v = np.array([[x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],
                          [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz]])
            
            # Define the 6 faces
            faces = [[v[0],v[1],v[2],v[3]], [v[4],v[5],v[6],v[7]], [v[0],v[1],v[5],v[4]],
                     [v[2],v[3],v[7],v[6]], [v[1],v[2],v[6],v[5]], [v[4],v[7],v[3],v[0]]]
            
            ax.add_collection3d(Poly3DCollection(faces, facecolors=theme_color, 
                                                 linewidths=1, edgecolors=edge_color, alpha=0.6))
            ax.text(x, y, z+dz, itm['name'], fontsize=8)

        # Plot settings
        ax.set_xlim(0, L); ax.set_ylim(0, W); ax.set_zlim(0, H)
        status = "!!! OVERLOADED !!!" if overloaded else "LOAD SECURE"
        plt.title(f"{status}\nFront: {f_load:.0f}/{self.max_front}kg | Rear: {r_load:.0f}/{self.max_rear}kg")
        plt.show()

import numpy as np # Needed for vertex array math

# --- Execution ---
# Define trailer: 13.6m long, 12,000kg max front, 18,000kg max rear, 10.5m wheelbase
trailer = SmartTrailer(13.6, 2.4, 2.6, 12000, 18000, 10.5)

# Example: Adding heavy gensets from your CSV
trailer.add_item("GEN-001", 4.5, 2.1, 2.2, 9500, 0.5, 0.15)
trailer.add_item("GEN-002", 4.5, 2.1, 2.2, 9500, 5.5, 0.15)
# Adding this 3rd one will likely trigger the "Red" overload warning
trailer.add_item("GEN-003", 3.0, 2.1, 2.0, 6000, 10.5, 0.15)

trailer.visualize()