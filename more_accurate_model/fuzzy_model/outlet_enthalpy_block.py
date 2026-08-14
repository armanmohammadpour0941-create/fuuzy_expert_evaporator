import rule_activation as ra

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
input2_range_w_v = [50, 40, 60]
# E_w_v
output_range_w_v = [29184.44, 27000, 31370]

input1_crisp_value_w_v = 12
input2_crisp_value_w_v = 56

e_w_v = ra.calculate_fuzzy_block_output(
    input1_crisp_value_w_v,
    input2_crisp_value_w_v,
    input1_range_w_v,
    input2_range_w_v,
    output_range_w_v,
    rule_table_w_v,
)
print(e_w_v)

# E_w_b
rule_table_w_b = [
    ["NL", "NL", "NL", "NS", "NS"],
    ["NL", "NS", "NS", "NS", "Z"],
    ["NS", "Z", "Z", "Z", "PS"],
    ["Z", "PS", "PS", "PL", "PL"],
    ["PS", "PS", "PL", "PL", "PL"],
]
# w_b
input1_range_w_b = [60, 55, 65]
# T
input2_range_w_b = [50, 40, 60]
# E_w_b
output_range_w_b = [30440.22, 25800, 35000]

input1_crisp_value_w_b = 63
input2_crisp_value_w_b = 56

e_w_b = ra.calculate_fuzzy_block_output(
    input1_crisp_value_w_b,
    input2_crisp_value_w_b,
    input1_range_w_b,
    input2_range_w_b,
    output_range_w_b,
    rule_table_w_b,
)
print(e_w_b)

# E_h_out   
rule_table_h_out = [
    ["NL", "NL", "NL", "NS", "NS"],
    ["NL", "NL", "NS", "NS", "Z"],
    ["NL", "NS", "Z", "PS", "PL"],
    ["Z", "NS", "PS", "PL", "PL"],
    ["PS", "PS", "PL", "PL", "PL"],
]
# E_w_v
input1_range_h_out = [29184.44, 27000, 31370]
# E_w_b
input2_range_h_out = [30440.22, 25800, 35000]
# E_h_out
output_range_h_out = [59624.67, 53000, 66300]

input1_crisp_value_h_out = 30000
input2_crisp_value_h_out = 34000

e_h_out = ra.calculate_fuzzy_block_output(
    input1_crisp_value_h_out,
    input2_crisp_value_h_out,
    input1_range_h_out,
    input2_range_h_out,
    output_range_h_out,
    rule_table_h_out,
)
print(e_h_out)