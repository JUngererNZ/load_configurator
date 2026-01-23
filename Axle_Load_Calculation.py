import pandas as pd

class TrailerLoad:
    def __init__(self, length, max_payload, wheelbase_offset):
        self.length = length
        self.max_payload = max_payload
        self.wheelbase_offset = wheelbase_offset # Distance from kingpin to center of rear bogie
        self.items = []

    def add_item(self, weight, length, x_pos):
        # x_pos is the distance from the front of the trailer to the front of the item
        item_cog = x_pos + (length / 2)
        self.items.append({'weight': weight, 'cog': item_cog})

    def calculate_distribution(self):
        total_mass = sum(i['weight'] for i in self.items)
        if total_mass == 0: return 0, 0
        
        # Calculate moment relative to the front (Kingpin area)
        total_moment = sum(i['weight'] * i['cog'] for i in self.items)
        combined_cog = total_moment / total_mass
        
        # Estimate weight on rear axles (Simplified lever principle)
        rear_load = (combined_cog / self.wheelbase_offset) * total_mass
        front_load = total_mass - rear_load
        
        return front_load, rear_load, combined_cog

# Example Usage
trailer = TrailerLoad(length=13.6, max_payload=28000, wheelbase_offset=10.5)
# Adding a 8000kg Genset 2 meters from the front
trailer.add_item(weight=8000, length=4.5, x_pos=2.0)

f_load, r_load, cog = trailer.calculate_distribution()
print(f"Front Load: {f_load:.2f}kg | Rear Load: {r_load:.2f}kg | COG: {cog:.2f}m")