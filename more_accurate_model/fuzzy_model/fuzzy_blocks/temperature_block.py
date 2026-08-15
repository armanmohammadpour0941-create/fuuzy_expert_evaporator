import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from more_accurate_model.fuzzy_model import rule_activation as ra


def temperature_derivative(e_h, l):
    rule_table = [
        ["Z", "NS", "NS", "NL", "NL"],
        ["PS", "Z", "NS", "NS","NL"],
        ["PL", "PS", "Z", "NS", "NL"],
        ["PL", "PS", "PS", "Z", "NS"],
        ["PL", "PL", "PS", "PS", "Z"]
    ]

    # E_h
    input1_range = [0, -1000, 1000]
    # level
    input2_range = [0.11, 0, 0.22]
    # dT/dt
    output_range = [0, -100, 100]

    input1_crisp_value = e_h
    input2_crisp_value = l

    dT_dt = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return dT_dt

