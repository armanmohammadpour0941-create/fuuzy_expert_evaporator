from more_accurate_model import thermo as th


def outlet_energy(w_v, w_f, w_bin, level, salinity, temperature, params):

    brine_temperature = temperature + th.bpe(temperature, salinity)
    brine_density = th.calculate_liquid_density(brine_temperature, salinity)
    vapor_density = th.calculate_vapor_density(temperature)
    brine_mass = brine_density * params.A_s * level
    vapor_mass = vapor_density * params.A_s * (params.H - level)
    total_mass = brine_mass + vapor_mass
    vapor_fraction = vapor_mass / total_mass

    brine_enthalpy = th.calculate_liquid_water_enthalpy(brine_temperature)
    vapor_enthalpy = th.calculate_vapor_water_enthalpy(temperature)
    mixture_enthalpy = (
        vapor_fraction * vapor_enthalpy
        + (1.0 - vapor_fraction) * brine_enthalpy
    )

    return (
        (w_f + w_bin) * mixture_enthalpy
        + w_v * (mixture_enthalpy - brine_enthalpy)
    )
