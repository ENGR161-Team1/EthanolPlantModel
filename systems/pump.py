from .process import Process
from .connectors import Connector
import math

class Pump():
    def __init__(self, **kwargs):
        """
        Initialize Pump.
        
        Args:
            name (str): Pump identifier (default: "Pump")
            performance_rating (float): Pump performance rating in meters (default: 0 m)
            cost (float): Cost in USD per m³/s of flow rate (default: 0)
            efficiency (float): Pump efficiency as fraction 0-1 (default: 1.0)
            opening_diameter (float): Inlet/outlet opening diameter in meters (default: 0.1 m)
        """
        self.name = kwargs.get("name", "Pump")
        self.performance_rating = kwargs.get("performance_rating", 0)  # in m
        self.cost = kwargs.get("cost", 0)  # in USD per m3/sec of flow rate
        self.efficiency = kwargs.get("efficiency", 1.0)  # fraction (0 to 1)
        opening_diameter = kwargs.get("opening_diameter", 0.1)  # in meters
        self.cross_sectional_area = math.pi * (opening_diameter / 2) ** 2  # in m²

    def pump_process(self, **kwargs):
        """
        Pump process: increases pressure/velocity of fluid based on pump efficiency.
        
        Calculates output flow rate and power consumption based on input volumetric flow,
        fluid composition (which determines density), and pump efficiency.
        
        Args:
            input_volume_flow (float): Inlet volumetric flow rate in m³/s
            input_composition (dict): Component volume fractions with keys:
                "ethanol", "water", "sugar", "fiber"
        
        Returns:
            tuple: (output_mass_flow, output_volumetric_flow, power_consumed)
                - output_mass_flow (float): Mass flow rate at pump outlet in kg/s
                - output_volumetric_flow (float): Volumetric flow rate at pump outlet in m³/s
                - power_consumed (float): Mechanical power consumed by pump in Watts
        """
        input_volume_flow = kwargs.get("input_volume_flow", 0)  # in m³/s
        input_composition = kwargs.get("input_composition", {})  # component volume fractions
        
        # Normalize composition fractions
        for component in input_composition:
            input_composition[component] = input_composition.get(component, 0)
        
        # Calculate solution density as weighted average of component densities (kg/m³)
        input_density = (
            input_composition.get("ethanol", 0) * Process.DENSITY_ETHANOL +
            input_composition.get("water", 0) * Process.DENSITY_WATER +
            input_composition.get("sugar", 0) * Process.DENSITY_SUGAR +
            input_composition.get("fiber", 0) * Process.DENSITY_FIBER
        )
        
        # Calculate mass flow rate: mass_flow = volumetric_flow × density
        input_mass_flow = input_volume_flow * input_density

        # Calculate inlet velocity and kinetic energy
        input_velocity = input_volume_flow / self.cross_sectional_area  # in m/s
        input_kinetic_energy = input_mass_flow * (input_velocity ** 2) / 2  # in Watts
        
        # Energy added by pump: efficiency determines fraction of input kinetic energy transferred
        energy_added = input_kinetic_energy * self.efficiency  # in Watts
        power_consumed = input_kinetic_energy + energy_added  # in Watts

        # Calculate output flow using energy balance at outlet
        output_volumetric_flow = (2 * energy_added * self.cross_sectional_area**2 / input_density) ** (1 / 3) if input_density != 0 else 0
        output_mass_flow = output_volumetric_flow * input_density  # in kg/s

        return output_mass_flow, output_volumetric_flow, power_consumed
