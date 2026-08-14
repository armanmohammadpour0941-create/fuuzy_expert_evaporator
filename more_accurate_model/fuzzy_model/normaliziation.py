def normalize_scale(value, range: list[float, float, float]):
    operating_point = range[0]
    lower_bound = range[1]
    upper_bound = range[2]
    span = (upper_bound - lower_bound) / 2
    normalized_value = 5 * (value - operating_point) / span
    return normalized_value

def denormalize_scale(normal_value, range: list[float, float, float]):
    operating_point = range[0]
    lower_bound = range[1]
    upper_bound = range[2]
    span = (upper_bound - lower_bound) / 2  
    value = operating_point + ((normal_value * span) / 5)
    return value
    