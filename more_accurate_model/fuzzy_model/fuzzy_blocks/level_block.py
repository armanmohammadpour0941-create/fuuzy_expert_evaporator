import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from more_accurate_model.fuzzy_model import rule_activation as ra


def level_derivative(i_w_in, w_v, w_b):
    rule_table = [
        ["Z", "PS", "NL", "NS", "NL"],
        ["PS", "Z", "NS", "NS", "NL"],
        ["PL", "PS", "Z", "NS", "NL"],
        ["PL", "PL", "PS", "Z", "NS"],
        ["PL", "PL", "PL", "PS", "Z"],
    ]

    # I_w_in
    input1_range = [70, 60, 80]
    # I_w_out
    input2_range = [70, 60, 80]
    #dl/dt
    output_range = [0, -5, 5]

    input1_crisp_value = i_w_in
    input2_crisp_value = w_v + w_b

    dl_dt = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return dl_dt
