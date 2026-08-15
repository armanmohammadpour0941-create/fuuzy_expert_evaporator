import rule_activation as ra

rule_table = [
    ["Z",  "NS", "NL", "NL", "NL"],
    ["PS", "Z",  "NS", "NS", "NL"],
    ["PL", "PS", "Z",  "NS", "NL"],
    ["PL", "PS", "PS", "Z",  "NS"],
    ["PL", "PL", "PL", "PS", "Z"]
]

# E_s
input1_range = [0, -100, 100]
# level
input2_range = [0.11, 0, 0.22]
# dx/dt
output_range = [0, -10, 10]

input1_crisp_value = 39
input2_crisp_value = 0.15

dx_dt = ra.calculate_fuzzy_block_output(
    input1_crisp_value,
    input2_crisp_value,
    input1_range,
    input2_range,
    output_range,
    rule_table,
)
print(dx_dt)

