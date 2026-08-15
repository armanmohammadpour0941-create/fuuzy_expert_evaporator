import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from more_accurate_model.fuzzy_model import rule_activation as ra


def level_update(dl_dt, last_l):
    rule_table = [
        ["NL", "NL", "NL", "NS", "Z"],
        ["NL", "NS", "NS", "Z", "PS"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["NS", "Z", "PS", "PL", "PL"],
        ["Z", "PS", "PL", "PL", "PL"],
    ]
    # dl/dt
    input1_range = [0, -100, 100]
    # L(k-1)
    input2_range = [0.11, 0, 0.22]
    # L(k)
    output_range = [0.11, 0, 0.22]

    input1_crisp_value = dl_dt
    input2_crisp_value = last_l

    l = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
        'som'
    )
    return l

