import rule_activation as ra

rule_table = [
    ["NL", "NL", "NL", "NS", "Z"],
    ["NL", "NS", "NS", "Z", "PS"],
    ["NL", "NS", "Z", "PS", "PL"],
    ["NS", "Z", "PS", "PL", "PL"],
    ["Z", "PS", "PL", "PL", "PL"],
]
# dl/dt
input1_range = [0, -10, 10]
# L(k-1)
input2_range = [0.11, 0, 0.22]
# L(k)
output_range = [0.11, 0, 0.22]

input1_crisp_value = 1.5
input2_crisp_value = 0.09

l = ra.calculate_fuzzy_block_output(
    input1_crisp_value,
    input2_crisp_value,
    input1_range,
    input2_range,
    output_range,
    rule_table,
)
print(l)

