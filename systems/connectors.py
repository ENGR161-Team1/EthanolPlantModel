import numpy as np
import math

class Connector:
    def __init__(self, **kwargs):
        self.mass_function = kwargs.get("mass_function", None)
        self.energy_function = kwargs.get("energy_function", None)
    
    def processDensity(self, inputs=dict()):
        input_flow = inputs.get("input_flow", 0) # input volumetric flow rate in m3/s
        input_mass = inputs.get("input_mass", 0) # input mass flow rate in kg
        return input_mass / input_flow if input_flow != 0 else 0

class Pipe(Connector):
    def __init__(self, **kwargs):
        self.diameter = kwargs.get("diameter", 0.1)  # default diameter in meters
        self.length = kwargs.get("length", 1.0)      # default length in meters
        self.friction_factor = kwargs.get("friction_factor", 0.02)  # default friction factor

        super().__init__(mass_function=self.pipeMassFunction, energy_function=self.pipeEnergyFunction)
        # Additional initialization for Pipe can go here
    
    def pipeEnergyFunction(self, **kwargs):
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)
        interval = kwargs.get("interval", 1.0)
        density = self.processDensity({"input_flow": input_flow, "input_mass": input_mass})
        # For simplicity, we assume no change in composition, mass, or energy in the pipe
        energy_change = density * interval * (8 * self.friction_factor * input_flow**3) / (math.pi**2 * self.diameter**5)
        return input_energy - energy_change
    
    def pipeMassFunction(self, **kwargs):
        pass

class Bend(Connector):
    def __init__(self, **kwargs):
        self.bend_radius = kwargs.get("bend_radius", 0.5)  # default bend radius in meters
        bend_factor = kwargs.get("bend_factor", 0.9)  # default bend factor
        # Additional initialization for Bend can go here
        super().__init__(mass_function=self.bendMassFunction, energy_function=self.bendEnergyFunction)

    
    def bendEnergyFunction(self, **kwargs):
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)
        interval = kwargs.get("interval", 1.0)
        density = self.processDensity({"input_flow": input_flow, "input_mass": input_mass})
        # For simplicity, we assume no change in composition, mass, or energy in the bend

        velocity = input_flow / ((math.pi / 4) * (self.bend_radius ** 2))
        energy_change = density * interval * (1 - self.bend_factor) * (velocity ** 2) / 2
        return input_energy - energy_change
    
    def bendMassFunction(self, **kwargs):
        pass

    

"""
class Valve(Connector):
    def __init__(self):
        super().__init__(connectorFunction=self.valve_function)
        # Additional initialization for Valve can go here

    
    def valve_function(self, input=dict()):
        return input
        # pass
"""