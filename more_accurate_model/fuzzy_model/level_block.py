import rule_activation as ra

rule_table = [
    ["Z", "PS", "NL", "NS", "NL"],
    ["PS", "Z", "NS", "NS", "NL"],
    ["PL", "PS", "Z", "NS", "NL"],
    ["PL", "PL", "PS", "Z", "NS"],
    ["PL", "PL", "PL", "PS", "Z"],
]

input1_range = [70, 60, 80]
input2_range = [70, 60, 80]
output_range = [0, -5, 5]

input1_crisp_value = 74.5
input2_crisp_value = 68.7

dl_dt = ra.calculate_fuzzy_block_output(
    input1_crisp_value,
    input2_crisp_value,
    input1_range,
    input2_range,
    output_range,
    rule_table,
)
print(dl_dt)