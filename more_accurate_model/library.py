def normalize(value, operating_point, max_deviation_percentage):
    max_deviation = operating_point * max_deviation_percentage / 100.0
    return (value - operating_point) / max_deviation


