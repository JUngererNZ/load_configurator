This **User Guide** serves as the standard operating procedure (SOP) for your transport team. It explains not just how to run the code, but how to interpret the technical physics data to ensure every load is road-legal.

---

# 🚛 Genset Load Configurator: User Guide

This toolset automates the transformation of a client bulk order into a physically balanced, 3D-mapped loading plan for three trailers.

## 1. Technical Concepts: Understanding the Physics

When heavy gensets are loaded, the weight is distributed between two points: the **Kingpin** (front) and the **Rear Axle Group**.

* **Front (Kingpin) Load:** The weight pressing down on the truck's drive axles. If this is too high, it can damage the truck's fifth wheel. If it's too low, the truck loses steering traction.
* **Rear Axle Load:** The weight pressing down on the trailer's wheels. Exceeding this limit is the most common cause of DOT/Roadside fines.
* **Center of Gravity (CoG):** The point where the total weight of all items is balanced. The **Auto-Optimizer** shuffles items to move this CoG to the ideal "sweet spot" (usually slightly forward of the trailer center).

---

## 2. Sequence of Operations (Manual vs. One-Click)

### Option A: The "One-Click" Workflow (Recommended)

Use this for daily operations to get an optimized result immediately.

1. Place the client spreadsheet (e.g., `19_GENSETS.csv`) in the folder.
2. Run the **`master_configurator.py`**.
3. **The script will:**
* Iterate 50+ times to find the best balance.
* Pop up 3D windows showing the layout for Trailer A, B, and C.
* Generate the `FINAL_LOADING_MANIFESTO.csv`.



### Option B: The Modular Workflow (Development/Debugging)

If you need to change specific parts of the logic, run the scripts in this order:

1. **`load_configurator.py`**: Test the 3D packing fit only.
2. **`Axle_Load_Calculation.py`**: Verify the weight math.
3. **`Integrated_Load_Configurator_Visualizer.py`**: View the combined 3D result.
4. **`CSV_Export_Loading_Manifesto.py`**: Save the final data.

---

## 3. Interpreting the Final Report

Open the `FINAL_LOADING_MANIFESTO.csv`. Pay close attention to these columns:

| Column | Meaning | Action if High/Red |
| --- | --- | --- |
| **X_Pos_Meters** | Where the front of the genset should sit. | Measure from the front trailer bulkhead. |
| **Front_Axle_Load** | Weight on the truck. | If >12,000kg, move a unit further back. |
| **Rear_Axle_Load** | Weight on trailer wheels. | If >18,000kg, move a unit further forward. |
| **Safety_Status** | Overall legal check. | **PASS** = Good to go. **FAIL** = Do not load. |

---

## 4. Troubleshooting

* **"Fail - Overloaded" appears:** This means the 19 items are too heavy for 3 trailers, or the specific mix of items is too dense. Consider using a 4th trailer or higher-capacity axles.
* **Units overlapping in 3D:** Ensure the `LENGTH` and `WIDTH` values in your CSV are accurate (including any protruding exhaust pipes or control panels).
* **Red Colors in Plot:** This is a visual warning that the optimizer could not find a safe configuration. **Do not give these instructions to the driver.**

---

**This completes the setup for your load configurator.**

Is there anything else I can assist with? For example, would you like me to help you create a **PDF template** version of the loading manifesto so it looks like an official shipping document?