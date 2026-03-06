# 🚛 Load Configurator

A comprehensive Python-based load configurator for optimizing cargo placement on trailers, specifically designed for heavy equipment like gensets.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Concepts](#technical-concepts)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This toolset automates the transformation of client bulk orders into physically balanced, 3D-mapped loading plans for multiple trailers. It ensures road-legal configurations by optimizing weight distribution and center of gravity calculations.

## ✨ Features

- **3D Load Visualization**: Interactive 3D representations of cargo placement
- **Weight Distribution Analysis**: Calculates front/rear axle loads and center of gravity
- **Auto-Optimization**: Iterative algorithm to find optimal load configurations
- **Multi-Trailer Support**: Handles loading plans for multiple trailers
- **CSV Export**: Generates final loading manifests for operational use
- **Safety Validation**: Ensures configurations meet legal weight limits

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/load_configurator.git
   cd load_configurator
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have Python 3.8+ installed

## 💻 Usage

### Quick Start (Recommended)

1. Place your client spreadsheet (e.g., `19_GENSETS.csv`) in the project folder
2. Run the master configurator:
   ```bash
   python master_configurator.py
   ```
3. The script will:
   - Iterate 50+ times to find the best balance
   - Display 3D layouts for all trailers
   - Generate `FINAL_LOADING_MANIFESTO.csv`

### Modular Workflow (Development/Debugging)

For detailed control over the process:

1. **Test 3D packing**: `python load_configurator.py`
2. **Verify weight calculations**: `python Axle_Load_Calculation.py`
3. **View combined results**: `python Integrated_Load_Configurator_Visualizer.py`
4. **Export final data**: `python CSV_Export_Loading_Manifesto.py`

## 🔬 Technical Concepts

### Understanding the Physics

When heavy equipment is loaded, weight distribution is critical:

- **Front (Kingpin) Load**: Weight on truck's drive axles
  - Too high: Can damage fifth wheel
  - Too low: Reduces steering traction

- **Rear Axle Load**: Weight on trailer wheels
  - Most common cause of DOT/Roadside fines when exceeded

- **Center of Gravity (CoG)**: Balance point of total weight
  - Auto-Optimizer moves CoG to ideal "sweet spot"
  - Usually slightly forward of trailer center

### Key Metrics in Final Report

| Column | Meaning | Action if High/Red |
|--------|---------|-------------------|
| **X_Pos_Meters** | Front position of genset | Measure from front trailer bulkhead |
| **Front_Axle_Load** | Weight on truck | If >12,000kg, move unit further back |
| **Rear_Axle_Load** | Weight on trailer wheels | If >18,000kg, move unit further forward |
| **Safety_Status** | Overall legal check | **PASS** = Good to go, **FAIL** = Do not load |

## 📁 File Structure

```
load_configurator/
├── README.md                    # This file
├── master_configurator.py       # Main orchestrator script
├── load_configurator.py         # 3D packing logic
├── Axle_Load_Calculation.py     # Weight distribution math
├── Integrated_Load_Configurator_Visualizer.py  # 3D visualization
├── CSV_Export_Loading_Manifesto.py  # Data export
├── Auto-Optimizer.py            # Optimization algorithms
├── three_d_visualizer.py        # 3D plotting utilities
├── run_all.py                   # Batch processing script
├── user_guide.md                # Detailed user documentation
├── requirements.txt             # Python dependencies
├── LICENSE                      # License file
├── *.csv                        # Client data files (excluded from git)
├── *.xlsx                       # Configuration files (excluded from git)
└── images/                      # Documentation images
```

## 🛠️ Troubleshooting

- **"Fail - Overloaded"**: Items too heavy for 3 trailers or specific mix too dense
  - Consider using 4th trailer or higher-capacity axles
  
- **Units overlapping in 3D**: Inaccurate dimensions in CSV
  - Verify `LENGTH` and `WIDTH` values include protrusions (exhaust pipes, control panels)
  
- **Red colors in plot**: Optimizer couldn't find safe configuration
  - **Do not load** - configuration is unsafe

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or support, please refer to the [User Guide](user_guide.md) or create an issue in this repository.
