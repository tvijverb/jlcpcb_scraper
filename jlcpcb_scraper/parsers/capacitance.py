def parse_capacitance_description(component_description):
    capacitance_value = None
    if component_description is None:
        return capacitance_value
    description_parts = component_description.split(' ')
    for part in description_parts:
        if part.endswith("pF"):
            numeric_part = part.rstrip("pF")
            try:
                value = float(numeric_part)
                capacitance_value = value
                break
            except ValueError:
                pass
        elif part.endswith("nF"):
            numeric_part = part.rstrip("nF")
            try:
                value = float(numeric_part)
                capacitance_value = value * 1000.0
                break
            except ValueError:
                pass
        elif part.endswith("uF") or part.endswith("µF"):
            numeric_part = part.rstrip("uF").rstrip("µF")
            try:
                value = float(numeric_part)
                capacitance_value = value * 1000000.0
                break
            except ValueError:
                pass
        elif part.endswith("mF"):
            numeric_part = part.rstrip("mF")
            try:
                value = float(numeric_part)
                capacitance_value = value * 1000000000.0
                break
            except ValueError:
                pass
        elif part.endswith("kF"):
            numeric_part = part.rstrip("kF")
            try:
                value = float(numeric_part)
                capacitance_value = value * 1000000000000000.0
                break
            except ValueError:
                pass
        elif part.endswith("MF"):
            numeric_part = part.rstrip("MF")
            try:
                value = float(numeric_part)
                capacitance_value = value * 1000000000000000000.0
                break
            except ValueError:
                pass
        elif part.endswith('F'):
            numeric_part = part.rstrip('F')
            try:
                value = float(numeric_part)
                capacitance_value = value * 1000000000000.0
                break
            except ValueError:
                pass
    return capacitance_value