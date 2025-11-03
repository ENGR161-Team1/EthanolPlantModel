class System:
    def __init__(self, name=str, inputs=list(), outputs=list(), efficiency=float=1.0, massFunction=None):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.efficiency = efficiency
        self.massFunction = massFunction
    
    def convertMass(self):
        pass
        # Placeholder for mass conversion logic
    
    def iterateInputs(self, inputValues=dict()):
        # self.inputs[key].append(inputValues[key]) for key in inputValues
        pass
        # Placeholder for iterating over inputs
    
    def display(self):
        pass
        # Placeholder for display logic

class Fermentation(System):
    def __init__(self, name = "Fermentation", efficiency=float):
        inputs = {
            "ethanol": [],
            "water": [],
            "sugar": [],
            "fiber": []
        }
        outputs = {
            "ethanol": [],
            "water": [],
            "sugar": [],
            "fiber": []
        }
        super().__init__(name, inputs, outputs, efficiency, self.ferment())
        # Additional initialization for Fermenter can go here

    
    def ferment(self, input=dict()):
        return {
            "ethanol": None,
            "water": None,
            "sugar": None,
            "fiber": None
        }
        # pass
        # Placeholder for fermentation logic
