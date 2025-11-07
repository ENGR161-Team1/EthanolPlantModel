# Ethanol Plant Model

## Overview
This project contains a model of an ethanol production plant, developed as part of ENGR-16100 coursework. The model simulates the complete production pipeline from raw materials to high-purity ethanol through mass balance calculations and process efficiency modeling.

## Description
The model simulates four key stages of ethanol production:

1. **Fermentation**: Converts sugar into ethanol using a biochemical process
   - Theoretical maximum conversion: 51% of sugar mass to ethanol
   - Configurable efficiency parameter (0.0 to 1.0)
   - Preserves water and fiber content through the process

2. **Filtration**: Removes solid particles and fiber content
   - Efficiency-based fiber removal
   - Passes ethanol, water, and sugar through unchanged

3. **Distillation**: Separates and concentrates ethanol
   - Exploits differences in boiling points
   - Some carry-over of non-ethanol components based on efficiency

4. **Dehydration**: Removes remaining water content
   - Produces high-purity ethanol
   - Efficiency-based water removal

### Mass Balance Tracking
The model tracks four components throughout the process:
- **Ethanol**: Product concentration
- **Water**: Solvent and byproduct
- **Sugar**: Raw material and residual
- **Fiber**: Solid waste material

Each `System` class maintains input and output histories for all components, enabling detailed analysis and visualization of the production process.

## Features
- Mass balance calculations for each process stage
- Configurable efficiency parameters for realistic simulations
- Built-in visualization using Matplotlib with GTK4 backend
- Iterative processing of multiple input batches
- Component tracking across the entire production pipeline

## Dependencies
- Python >= 3.10
- NumPy
- Matplotlib
- PyGObject (GTK4 bindings)

## Installation

### Using pip
```bash
# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel

# Install system dependencies (Ubuntu/Debian)
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection

# Install Python package
pip install .
```

### Using uv (Faster Alternative)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel

# Install system dependencies (Ubuntu/Debian)
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection

# Install using uv
uv pip install .
```

## Usage

### Basic Example
```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration

# Initialize systems with efficiency values (0.0 to 1.0)
fermenter = Fermentation(efficiency=0.85)    # 85% sugar conversion
filter_system = Filtration(efficiency=0.90)  # 90% fiber removal
distiller = Distillation(efficiency=0.80)    # 80% separation efficiency
dehydrator = Dehydration(efficiency=0.95)    # 95% water removal

# Configure input parameters (single batch)
input_values = {
    "ethanol": [0],      # Initial ethanol: 0 kg
    "water": [3000],     # Water: 3000 kg
    "sugar": [1000],     # Sugar: 1000 kg
    "fiber": [100]       # Fiber: 100 kg
}

# Process through the production pipeline
fermented = fermenter.iterateInputs(input_values)
filtered = filter_system.iterateInputs(fermented)
distilled = distiller.iterateInputs(filtered)
final_output = dehydrator.iterateInputs(distilled)

# Display results
print(f"Final ethanol: {final_output['ethanol'][-1]:.2f} kg")
print(f"Final water: {final_output['water'][-1]:.2f} kg")
print(f"Residual sugar: {final_output['sugar'][-1]:.2f} kg")
print(f"Residual fiber: {final_output['fiber'][-1]:.2f} kg")
```

### Visualization Example
```python
# Visualize the relationship between input sugar and output ethanol
fermenter.display(input="sugar", output="ethanol")

# Visualize water content through distillation
distiller.display(input="water", output="ethanol")
```

### Multiple Batch Processing
```python
# Process multiple batches with varying inputs
multi_batch_inputs = {
    "ethanol": [0, 0, 0],
    "water": [2500, 3000, 3500],
    "sugar": [800, 1000, 1200],
    "fiber": [80, 100, 120]
}

# Process all batches through the system
results = fermenter.iterateInputs(multi_batch_inputs)
# Each component list will contain results for all three batches
```

## System Components

### System (Base Class)
The base class for all process systems, providing:
- Input/output tracking for all components
- Mass function execution via `massFunction`
- Batch iteration capabilities with `iterateInputs()`
- Visualization with `display()`

### Fermentation
- **Input**: Sugar, water, fiber
- **Output**: Ethanol (51% × sugar × efficiency), unconverted sugar, water, fiber
- **Efficiency effect**: Determines sugar conversion rate

### Filtration
- **Input**: All components from fermentation
- **Output**: Ethanol, water, sugar pass through; fiber reduced by efficiency
- **Efficiency effect**: Determines fiber removal rate

### Distillation
- **Input**: All components from filtration
- **Output**: Concentrated ethanol with some carry-over impurities
- **Efficiency effect**: Determines purity of separation

### Dehydration
- **Input**: All components from distillation
- **Output**: High-purity ethanol with reduced water content
- **Efficiency effect**: Determines water removal rate

## Project Structure
```
EthanolPlantModel/
├── systems/
│   └── processes.py    # Core system components
├── LICENSE
├── README.md
└── pyproject.toml
```

## API Reference

### System Methods
- `iterateInputs(inputValues: dict) -> dict`: Process input batches and return outputs
- `display(input: str, output: str)`: Visualize input vs output relationship
- `convertMass()`: Placeholder for future mass conversion logic

### Process-Specific Methods
- `Fermentation.ferment(input: dict) -> dict`: Execute fermentation mass balance
- `Filtration.filter(input: dict) -> dict`: Execute filtration mass balance
- `Distillation.distill(input: dict) -> dict`: Execute distillation mass balance
- `Dehydration.dehydrate(input: dict) -> dict`: Execute dehydration mass balance

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Team Members
- **Advay R. Chandra** - chand289@purdue.edu
- **Karley J. Hammond** - hammon88@purdue.edu
- **Samuel M. Razor** - razor@purdue.edu
- **Katherine E. Hampton** - hampto64@purdue.edu

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
Developed as part of ENGR-16100 coursework at Purdue University.
