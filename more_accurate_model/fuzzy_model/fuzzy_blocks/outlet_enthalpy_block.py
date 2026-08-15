import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from more_accurate_model.fuzzy_model import rule_activation as ra


def outlet_energy(w_v, w_b, temperature):
    rule_table_w_v = [
        ["NL", "NL", "NL", "NS", "Z"],
        ["NL", "NS", "NS", "Z", "PS"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["NS", "Z", "PS", "PL", "PL"],
        ["Z", "PS", "PL", "PL", "PL"],
    ]
    # w_v
    input1_range_w_v = [10, 5, 15]
    # T
    input2_range_w_v = [50, 10, 90]
    # E_w_v
    output_range_w_v = [29184.44, 0, 58370]

    input1_crisp_value_w_v = w_v
    input2_crisp_value_w_v = temperature

    e_w_v = ra.calculate_fuzzy_block_output(
        input1_crisp_value_w_v,
        input2_crisp_value_w_v,
        input1_range_w_v,
        input2_range_w_v,
        output_range_w_v,
        rule_table_w_v,
    )

    # E_w_b
    rule_table_w_b = [
        ["NL", "NL", "NL", "NS", "NS"],
        ["NL", "NS", "NS", "NS", "Z"],
        ["NS", "Z", "Z", "Z", "PS"],
        ["Z", "PS", "PS", "PL", "PL"],
        ["PS", "PS", "PL", "PL", "PL"],
    ]
    # w_b
    input1_range_w_b = [60, 0, 120]
    # T
    input2_range_w_b = [50, 10, 90]
    # E_w_b
    output_range_w_b = [30440.22, 0, 60880]

    input1_crisp_value_w_b = w_b
    input2_crisp_value_w_b = temperature

    e_w_b = ra.calculate_fuzzy_block_output(
        input1_crisp_value_w_b,
        input2_crisp_value_w_b,
        input1_range_w_b,
        input2_range_w_b,
        output_range_w_b,
        rule_table_w_b,
    )
    
    # E_h_out   
    rule_table_h_out = [
        ["NL", "NL", "NL", "NS", "NS"],
        ["NL", "NL", "NS", "NS", "Z"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["Z", "NS", "PS", "PL", "PL"],
        ["PS", "PS", "PL", "PL", "PL"],
    ]
    # E_w_v
    input1_range_h_out = [29184.44, 0, 58370]
    # E_w_b
    input2_range_h_out = [30440.22, 0, 60880]
    # E_h_out
    output_range_h_out = [59624.67, 0, 119250]

    input1_crisp_value_h_out = e_w_v
    input2_crisp_value_h_out = e_w_b

    e_h_out = ra.calculate_fuzzy_block_output(
        input1_crisp_value_h_out,
        input2_crisp_value_h_out,
        input1_range_h_out,
        input2_range_h_out,
        output_range_h_out,
        rule_table_h_out,
    )
    return e_h_out