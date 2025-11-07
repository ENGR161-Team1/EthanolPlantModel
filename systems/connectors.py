import numpy as np
import math

class Connector:
    def __init__(self, **kwargs):
        self.mass_function = kwargs.get("mass_function", None)
        self.energy_function = kwargs.get("energy_function", None)
        self.diameter = kwargs.get("diameter", 0.1)  # default diameter in meters
        self.cross_sectional_area = math.pi * (self.diameter / 2) ** 2
    
    def processDensity(self, inputs=dict()):
        input_flow = inputs.get("input_flow", 0) # input volumetric flow rate in m3/s
        input_mass = inputs.get("input_mass", 0) # input mass flow rate in kg
        return input_mass / input_flow if input_flow != 0 else 0

class Pipe(Connector):
    def __init__(self, **kwargs):
        self.length = kwargs.get("length", 1.0)      # default length in meters
        self.friction_factor = kwargs.get("friction_factor", 0.02)  # default friction factor

        super().__init__(mass_function=self.pipeMassFunction, energy_function=self.pipeEnergyFunction, diameter=kwargs.get("diameter", 0.1))
        # Additional initialization for Pipe can go here
    
    def pipeEnergyFunction(self, **kwargs):
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)
        density = self.processDensity({"input_flow": input_flow, "input_mass": input_mass})
        # For simplicity, we assume no change in composition, mass, or energy in the pipe
        energy_change = input_mass * (8 * self.friction_factor * input_flow**2) / (math.pi**2 * self.diameter**5)
        return input_energy - energy_change
    
    def pipeMassFunction(self, **kwargs):
        input_mass = kwargs.get("input_mass", 0)
        return input_mass  # No mass loss in the pipe

class Bend(Connector):
    def __init__(self, **kwargs):
        self.bend_radius = kwargs.get("bend_radius", 0.5)  # default bend radius in meters
        self.bend_factor = kwargs.get("bend_factor", 0.9)  # default bend factor

        # Additional initialization for Bend can go here
        super().__init__(mass_function=self.bendMassFunction, energy_function=self.bendEnergyFunction, diameter=kwargs.get("diameter", 0.1))

    
    def bendEnergyFunction(self, **kwargs):
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)
        # For simplicity, we assume no change in composition, mass, or energy in the bend

        if input_flow == 0 or input_mass == 0:
            return input_energy

        velocity = input_flow / (self.cross_sectional_area)
        energy_change = input_mass * (1 - self.bend_factor) * (velocity ** 2) / 2
        return input_energy - energy_change
    
    def bendMassFunction(self, **kwargs):
        input_mass = kwargs.get("input_mass", 0)
        return input_mass  # No mass loss in the bend
    

class Valve(Connector):
    def __init__(self, **kwargs):
        self.resistance_coefficient = kwargs.get("resistance_coefficient", 1.0)  # default resistance coefficient
        super().__init__(mass_function=self.valveMassFunction, energy_function=self.valveEnergyFunction)
        # Additional initialization for Valve can go here
    
    def valveEnergyFunction(self, **kwargs):
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)
        # For simplicity, we assume no change in composition, mass, or energy in the valve
        velocity = input_flow / (self.cross_sectional_area)
        energy_change = input_mass * (velocity ** 2) * self.resistance_coefficient / 2

        return input_energy - energy_change

    def valveMassFunction(self, **kwargs):
        input_mass = kwargs.get("input_mass", 0)
        return input_mass  # No mass loss in the valve