import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from more_accurate_model.fuzzy_model import rule_activation as ra


def enthalpy_balance(e_h_in, e_h_out):
    rule_table = [
        ["Z", "NS", "NL", "NL", "NL"],
        ["PS", "Z", "NS", "NL", "NL"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["PL", "PL", "PS", "Z", "NS"],
        ["PL", "PL", "PL", "PS", "Z"],
    ]

    # E_h_in
    input1_range = [60670.99, 0, 120000]
    # E_h_out
    input2_range = [59624.67, 0, 119250]
    #E_h
    output_range = [0, -1000, 1000]

    input1_crisp_value = e_h_in
    input2_crisp_value = e_h_out
    e_h = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return e_h