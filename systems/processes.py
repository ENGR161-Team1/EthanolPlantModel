import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("gtk4agg")

class System:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "System")
        self.input_log = {
            "mass": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }
            },
            "flow": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }
            }
        }
        self.output_log = {
            "mass": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                },
            },
            "flow": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                },
            }
        }
        self.efficiency = kwargs.get("efficiency", 1.0)
        self.massFunction = kwargs.get("massFunction", None)
        self.densityWater = 997  # kg/m^3
        self.densityEthanol = 789  # kg/m^3
        self.densitySugar = 1590  # kg/m^3
        self.densityFiber = 1311  # kg/m^3

    def flowToMass(self, **kwargs):
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_flow = kwargs.get("total_flow", None)
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
        if mode == "amount":
            mass_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_inputs[component] = inputs[component] * self.densityEthanol
                elif component == "water":
                    mass_inputs[component] = inputs[component] * self.densityWater
                elif component == "sugar":
                    mass_inputs[component] = inputs[component] * self.densitySugar
                elif component == "fiber":
                    mass_inputs[component] = inputs[component] * self.densityFiber
                elif component == "total":
                    mass_inputs[component] = inputs[component] * (
                        self.densityEthanol + self.densityWater + self.densitySugar + self.densityFiber
                    )  # Simplified total density calculation
                else:
                    raise ValueError(f"Unknown component: {component}")
            return mass_inputs
        else:  # composition
            if total_flow is None:
                raise ValueError("total_flow must be provided when mode is 'composition'")
            mass_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_inputs[component] = inputs[component] * total_flow * self.densityEthanol
                elif component == "water":
                    mass_inputs[component] = inputs[component] * total_flow * self.densityWater
                elif component == "sugar":
                    mass_inputs[component] = inputs[component] * total_flow * self.densitySugar
                elif component == "fiber":
                    mass_inputs[component] = inputs[component] * total_flow * self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            mass_inputs["total"] = sum(mass_inputs[component] for component in mass_inputs)
            return mass_inputs
            
    
    def massToFlow(self, **kwargs):
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_mass = kwargs.get("total_mass", None)
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
        if mode == "amount":
            flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    flow_inputs[component] = inputs[component] / self.densityEthanol
                elif component == "water":
                    flow_inputs[component] = inputs[component] / self.densityWater
                elif component == "sugar":
                    flow_inputs[component] = inputs[component] / self.densitySugar
                elif component == "fiber":
                    flow_inputs[component] = inputs[component] / self.densityFiber
                elif component == "total":
                    flow_inputs[component] = inputs[component] / (
                        self.densityEthanol + self.densityWater + self.densitySugar + self.densityFiber
                    )  # Simplified total density calculation
                else:
                    raise ValueError(f"Unknown component: {component}")
            return flow_inputs
        else:  # composition
            if total_mass is None:
                raise ValueError("total_mass must be provided when mode is 'composition'")
            flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    flow_inputs[component] = inputs[component] * total_mass / self.densityEthanol
                elif component == "water":
                    flow_inputs[component] = inputs[component] * total_mass / self.densityWater
                elif component == "sugar":
                    flow_inputs[component] = inputs[component] * total_mass / self.densitySugar
                elif component == "fiber":
                    flow_inputs[component] = inputs[component] * total_mass / self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            flow_inputs["total"] = sum(flow_inputs[component] for component in flow_inputs)
            return flow_inputs

    
    def processMass(self, **kwargs):
        # Process mass inputs and return outputs based on specified types
        # Extract parameters from kwargs
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_mass = kwargs.get("total_mass", None)

        # Asking whether to store inputs and outputs into the system logs
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)
        
        # Validate inputs
        if not inputs:
            raise ValueError("No inputs provided for processing")
        elif input_type not in ["amount", "composition", "full"] or output_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type and output_type must be either 'amount', 'composition', or 'full'")
        elif store_outputs and not output_type == "full":
            raise ValueError("store_outputs can only be True when output_type is 'full'")
        elif input_type == "composition" and any(key not in inputs for key in ["ethanol", "water", "sugar", "fiber"]):
            raise ValueError("All components must be provided when input_type is 'composition'")
        
        # Fill missing inputs with zeros for amount input_type
        if input_type == "amount" and any(key not in inputs for key in ["ethanol", "water", "sugar", "fiber"]):
            for key in ["ethanol", "water", "sugar", "fiber"]:
                if key not in inputs or inputs[key] is None:
                    inputs[key] = 0.0
        
        # Convert inputs to amounts if necessary
        if input_type == "composition":
            if total_mass is None:
                raise ValueError("total_mass must be provided when input_type is 'composition'")
            if total_mass <= 0:
                raise ValueError("total_mass must be greater than zero")
            if any(key not in inputs for key in ["ethanol", "water", "sugar", "fiber"]):
                raise ValueError("All components must be provided when input_type is 'composition'")
            input_amounts = {key: inputs[key] * total_mass for key in inputs}
            if store_inputs:
                for key in input_amounts:
                    self.input_log["mass"]["amount"][key].append(input_amounts[key])
                    self.input_log["mass"]["composition"][key].append(inputs[key])
                self.input_log["mass"]["amount"]["total"].append(total_mass)
        elif input_type == "amount":
            if any(key not in inputs for key in ["ethanol", "water", "sugar", "fiber"]):
                for key in ["ethanol", "water", "sugar", "fiber"]:
                    if key not in inputs or inputs[key] is None:
                        inputs[key] = 0.0
            input_amounts = inputs
            if store_inputs:
                input_total = sum(input_amounts.values())
                if input_total <= 0:
                    raise ValueError("Total input amount must be greater than zero to store composition")
                for key in input_amounts:
                    self.input_log["mass"]["amount"][key].append(input_amounts[key])
                    self.input_log["mass"]["composition"][key].append(input_amounts[key] / input_total if input_total > 0 else 0)
                self.input_log["mass"]["amount"]["total"].append(input_total)
        else:  # full
            input_amounts = inputs["amount"]
            if "amount" not in inputs or "composition" not in inputs:
                raise ValueError("Both 'amount' and 'composition' must be provided when input_type is 'full'")
            if store_inputs:
                for key in input_amounts:
                    self.input_log["mass"]["amount"][key].append(input_amounts[key])
                    self.input_log["mass"]["composition"][key].append(inputs["composition"][key])
                self.input_log["mass"]["amount"]["total"].append(sum(input_amounts.values())) 
        
        # Process inputs through massFunction
        output_amounts = self.massFunction(input_amounts) if self.massFunction else input_amounts

        # Calculate total output and format output based on output_type
        output_total = sum(output_amounts.values())
        if output_type == "amount":
            output_amounts["total"] = output_total
            return output_amounts
        else: 
            if output_total <= 0:
                raise ValueError("Total output amount must be greater than zero to calculate composition")
            output_composition = {key: output_amounts[key] / output_total for key in output_amounts}
            if output_type == "composition":
                return output_composition
            else:  # full
                output_composition = {key: output_amounts[key] / output_total for key in output_amounts}
                if store_outputs:
                    for key in output_amounts:
                        self.output_log["mass"]["amount"][key].append(output_amounts[key])
                        self.output_log["mass"]["composition"][key].append(output_composition[key])
                    self.output_log["mass"]["amount"]["total"].append(output_total)
                output_amounts["total"] = output_total
                outputs = {
                    "amount": output_amounts,
                    "composition": output_composition
                }
                return outputs
    

    def processFlow(self, **kwargs):
        # Convert flow inputs to mass, process them, and convert outputs back to flow
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_flow = kwargs.get("total_flow", None)
        store_inputs = kwargs.get("store_inputs", False)

        # Convert flow inputs to mass inputs
        if input_type == "full":
            mass_inputs = {
                "amount": self.flowToMass(inputs=inputs["amount"], mode="amount"),
                "composition": self.flowToMass(inputs=inputs["composition"], mode="composition", total_flow=total_flow)
            }
            if store_inputs:
                for key in mass_inputs["amount"]:
                    self.input_log["flow"]["amount"][key].append(inputs["amount"][key])
                    self.input_log["flow"]["composition"][key].append(inputs["composition"][key])
                self.input_log["flow"]["amount"]["total"].append(total_flow)
        elif input_type == "amount":
            mass_inputs = self.flowToMass(inputs=inputs, mode="amount")
            if store_inputs:
                for key in mass_inputs:
                    self.input_log["flow"]["amount"][key].append(inputs[key])
                self.input_log["flow"]["amount"]["total"].append(sum(inputs.values()))
        elif input_type == "composition":
            if total_flow is None:
                raise ValueError("total_flow must be provided when input_type is 'composition'")
            mass_inputs = self.flowToMass(inputs=inputs, mode="composition", total_flow=total_flow)
            if store_inputs:
                for key in inputs:
                    self.input_log["flow"]["composition"][key].append(inputs[key])
                self.input_log["flow"]["amount"]["total"].append(total_flow)
        else:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")

    def iterateInputs(self, inputValues=dict(), **kwargs):
        # Appends input values to the inputs dictionary
        for key in inputValues:
            self.input_log[key] += inputValues[key]

        # Process each set of inputs and appends to outputs
        for i in range(len(inputValues["ethanol"])):
            input_dict = {key: inputValues[key][i] for key in inputValues}
            output_dict = self.massFunction(input_dict)
            for key in self.output_log:
                self.output_log[key].append(output_dict[key])

        return self.output_log 
    
    def display(self, input=str, output=str):
        plt.plot(self.input_log[input], self.output_log[output], linestyle='--', marker='o')
        plt.title(f"{self.name} System: {input} vs {output}")
        plt.xlabel(f"Input {input} (units)")
        plt.ylabel(f"Output {output} (units)")
        plt.grid(True)
        plt.show()


class Fermentation(System):
    def __init__(self, efficiency=float):
        super().__init__("Fermentation", efficiency, self.ferment)
        # Additional initialization for Fermenter can go here

    
    def ferment(self, input=dict()):
        return {
            "ethanol": 0.51 * input["sugar"] * self.efficiency if input.get("sugar") is not None else None, 
            "water": input["water"] if input.get("water") is not None and input.get("sugar") is not None else None,
            "sugar": (1 - self.efficiency) * input["sugar"] if input.get("sugar") is not None else None,
            "fiber": input["fiber"] if input.get("fiber") is not None else None
        }
        # pass

class Filtration(System):
    def __init__(self, efficiency=float):
        super().__init__(name = "Filtration", efficiency = efficiency, massFunction = self.filter)
        # Additional initialization for Filter can go here

    
    def filter(self, input=dict()):
        return {
            "ethanol": input["ethanol"] if input.get("ethanol") is not None else None, 
            "water": input["water"] if input.get("water") is not None else None,
            "sugar": input["sugar"] if input.get("sugar") is not None else None,
            "fiber": (1 - self.efficiency) * input["fiber"] if input.get("fiber") is not None else None
        }

class Distillation(System):
    def __init__(self, efficiency=float):
        super().__init__(name = "Distillation", efficiency = efficiency, massFunction = self.distill)
        # Additional initialization for Distiller can go here

    
    def distill(self, input=dict()):
        if None in [input.get("ethanol"), input.get("water"), input.get("sugar"), input.get("fiber")]:
            return {
                "ethanol": None,
                "water": None,
                "sugar": None,
                "fiber": None
            }
        distill_inefficiency = (1 / self.efficiency) - 1
        in_nonEthanol = input["water"] + input["sugar"] + input["fiber"]
        return {
            "ethanol": input["ethanol"],
            "water": (input["water"] * input["ethanol"] * distill_inefficiency) / in_nonEthanol, 
            "sugar": (input["sugar"] * input["ethanol"] * distill_inefficiency) / in_nonEthanol,
            "fiber": (input["fiber"] * input["ethanol"] * distill_inefficiency) / in_nonEthanol
        }

class Dehydration(System):
    def __init__(self, efficiency=float):
        super().__init__(name = "Dehydration", efficiency = efficiency, massFunction = self.dehydrate)
        # Additional initialization for Dehydrator can go here

    
    def dehydrate(self, input=dict()):
        if None in [input.get("ethanol"), input.get("water"), input.get("sugar"), input.get("fiber")]:
            return {
                "ethanol": None,
                "water": None,
                "sugar": None,
                "fiber": None
            }
        return {
            "ethanol": input["ethanol"], 
            "water": input["water"] * (1 - self.efficiency),
            "sugar": input["sugar"],
            "fiber": input["fiber"],
        }