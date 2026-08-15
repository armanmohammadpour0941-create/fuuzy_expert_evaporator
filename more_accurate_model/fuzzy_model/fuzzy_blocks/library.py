from dataclasses import dataclass


@dataclass(frozen=True)
class InferenceResult:
    crisp: float
    normalized: float
    dominant_label: str
    
@dataclass(frozen=True)
class FuzzyStepResult:
    level: float
    salintiy: float
    temperature: float
    d_level: float
    level_update: float
    salt_balance: float
    d_salinity: float
    salinity_update: float
    inlet_energy: float
    outlet_energy: float
    energy_balance: float
    d_temperature: float
    temperature_update: float
    