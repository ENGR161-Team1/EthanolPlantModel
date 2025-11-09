# API Reference

This document provides detailed API documentation for all classes and methods in the Ethanol Plant Model.

## Process Class

The base class for all process systems.

### Initialization Parameters

```python
Process(
    name: str = "Process",
    efficiency: float = 1.0,
    massFlowFunction: callable = None,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    cost_per_flow: float = 0
)
```

**Parameters:**
- `name` (str): Name of the process
- `efficiency` (float): Process efficiency (0.0 to 1.0)
- `massFlowFunction` (callable): Custom function for processing mass flows
- `power_consumption_rate` (float): Power consumption rate (default: 0)
- `power_consumption_unit` (str): Unit for power consumption. Options:
  - `"kWh/day"` (default): Kilowatt-hours per day
  - `"kWh/hour"` or `"kW"`: Kilowatts
  - `"W"`: Watts
- `cost_per_flow` (float): Cost per unit volumetric flow rate in $/m³/s (default: 0)

**Attributes:**
- `power_log` (dict): Dictionary tracking power consumption with keys:
  - `power_consumption_rate`: List of power rates (W)
  - `energy_consumed`: List of energy consumed in each interval (J)
  - `interval`: List of time intervals (s)
- `input_log` (dict): Logged input data
- `output_log` (dict): Logged output data

#### consumption_log (dict)
Unified tracking of power, energy, and cost consumption:
- `power_consumption_rate` (list): Power consumption at each time step (W)
- `energy_consumed` (list): Energy consumed in each interval (J)
- `interval` (list): Time interval for each measurement (s)
- `cost_per_unit_flow` (list): Cost per unit flow at each time step ($/m³/s)
- `cost_incurred` (list): Cost incurred for processing each flow ($)

### Methods

#### `processMassFlow()`

Process mass flow rate inputs through the system.

```python
processMassFlow(
    inputs: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_mass: float = None,
    store_inputs: bool = False,
    store_outputs: bool = False,
    store_cost: bool = False
) -> dict
```

**Parameters:**
- `inputs` (dict): Input mass flows for each component
- `input_type` (str): Format of inputs - "amount", "composition", or "full"
- `output_type` (str): Format of outputs - "amount", "composition", or "full"
- `total_mass` (float): Total mass flow rate (required for composition inputs)
- `store_inputs` (bool): Whether to log input values (default: False)
- `store_outputs` (bool): Whether to log output values (default: False)
- `store_cost` (bool): Whether to log cost data (default: False)

**Returns:**
- dict: Processed outputs in the format specified by output_type

**Example:**
```python
result = processor.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True,
    store_cost=True  # Enable cost tracking
)
```

#### `processVolumetricFlow()`

Process volumetric flow rate inputs through the system.

```python
processVolumetricFlow(
    inputs: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_flow: float = None,
    store_inputs: bool = False,
    store_outputs: bool = False,
    store_cost: bool = False
) -> dict
```

**Parameters:**
- `inputs` (dict): Input volumetric flows for each component
- `input_type` (str): Format of inputs - "amount", "composition", or "full"
- `output_type` (str): Format of outputs - "amount", "composition", or "full"
- `total_flow` (float): Total volumetric flow rate (required for composition inputs)
- `store_inputs` (bool): Whether to log input values (default: False)
- `store_outputs` (bool): Whether to log output values (default: False)
- `store_cost` (bool): Whether to log cost data (default: False)

**Returns:**
- dict: Processed volumetric flow outputs in the format specified by output_type

**Example:**
```python
result = processor.processVolumetricFlow(
    inputs={"ethanol": 0, "water": 0.1, "sugar": 0.03, "fiber": 0.008},
    input_type="amount",
    output_type="full",
    store_outputs=True,
    store_cost=True  # Enable cost tracking
)
```

#### `processPowerConsumption()`

Calculate energy consumed over a time interval based on power consumption rate.

```python
processPowerConsumption(
    store_energy: bool = False,
    interval: float = 1
) -> float
```

**Parameters:**
- `store_energy` (bool): Whether to log power and energy data (default: False)
- `interval` (float): Time interval in seconds (default: 1)

**Returns:**
- float: Energy consumed in the interval (Joules)

**Example:**
```python
# Calculate energy over 60 seconds and log it
energy = processor.processPowerConsumption(store_energy=True, interval=60)
print(f"Energy consumed: {energy} J")

# Access logged data
print(f"Power rate: {processor.power_log['power_consumption_rate'][-1]} W")
print(f"Energy: {processor.power_log['energy_consumed'][-1]} J")
print(f"Interval: {processor.power_log['interval'][-1]} s")
```

#### `iterateMassFlowInputs()`

Process multiple sets of mass flow rate inputs in batch.

```python
iterateMassFlowInputs(
    inputValues: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_mass_flow_list: list = None
) -> None
```

**Parameters:**
- `inputValues` (dict): Dictionary of component lists
- `input_type` (str): Input data type ("amount", "composition", or "full")
- `output_type` (str): Output data type ("amount", "composition", or "full")
- `total_mass_flow_list` (list): List of total mass flows (for composition inputs)

**Note:** Results are automatically stored in logs

#### `iterateVolumetricFlowInputs()`

Process multiple sets of volumetric flow rate inputs in batch.

```python
iterateVolumetricFlowInputs(
    inputValues: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_volumetric_flow_list: list = None
) -> None
```

**Parameters:** Same as `iterateMassFlowInputs()` but for volumetric flow rates

#### `volumetricToMass()`

Convert volumetric flow rates to mass flow rates.

```python
volumetricToMass(
    inputs: dict,
    mode: str = "amount",
    total_flow: float = None
) -> dict
```

#### `massToVolumetric()`

Convert mass flow rates to volumetric flow rates.

```python
massToVolumetric(
    inputs: dict,
    mode: str = "amount",
    total_mass: float = None
) -> dict
```

## Processor Classes

All processor classes inherit from `Process` and accept the same initialization parameters.

### Fermentation

Converts sugar to ethanol (51% stoichiometric yield).

```python
Fermentation(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Fermentation"
)
```

**Process:** `sugar → ethanol (51%) + unconverted sugar`

### Filtration

Removes fiber from the mixture.

```python
Filtration(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Filtration"
)
```

**Process:** `fiber → removed fiber + remaining fiber`

### Distillation

Separates ethanol from impurities.

```python
Distillation(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Distillation"
)
```

**Process:** At perfect efficiency (1.0), outputs pure ethanol. Lower efficiency adds proportional impurities.

### Dehydration

Removes water from the mixture.

```python
Dehydration(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Dehydration"
)
```

**Process:** `water → removed water + remaining water`

## Connector Class

Base class for fluid transport components.

### Initialization Parameters

```python
Connector(
    name: str = "Connector",
    length: float = 1.0,
    diameter: float = 0.1,
    roughness: float = 0.0001,
    bend_angle: float = 0,
    bend_radius: float = None,
    resistance_coefficient: float = 0
)
```

### Connector Types

#### Pipe

Straight pipe with friction losses.

```python
Pipe(length: float, diameter: float, roughness: float = 0.0001)
```

#### Bend

Pipe bend with direction change losses.

```python
Bend(
    diameter: float,
    bend_angle: float,
    bend_radius: float = None,
    roughness: float = 0.0001
)
```

#### Valve

Flow control valve with adjustable resistance.

```python
Valve(diameter: float, resistance_coefficient: float)
```

### Methods

#### `processFlow()`

Calculate output flow considering energy losses.

```python
processFlow(inputs: dict, store_inputs: bool = False, store_outputs: bool = False) -> dict
```

**Parameters:**
- `inputs` (dict): Input flow rates and compositions
- `store_inputs` (bool): Whether to log inputs
- `store_outputs` (bool): Whether to log outputs

**Returns:**
- dict: Output flow rates and compositions after energy losses

---

## Complete Example

```python
from systems.processors import Fermentation, Filtration

# Create processes with power consumption
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,  # 50 kWh/day
    power_consumption_unit="kWh/day"
)

filter = Filtration(
    efficiency=0.98,
    power_consumption_rate=2,  # 2 kW
    power_consumption_unit="kW"
)

# Process with logging
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True
)

# Track energy consumption
energy = fermenter.processPowerConsumption(store_energy=True, interval=3600)  # 1 hour
print(f"Energy consumed: {energy/3600000:.2f} kWh")
```
