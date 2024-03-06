def parse_voltage_description(component_description):
    voltage_value = None

    if component_description is None:
        return voltage_value

    description_parts = component_description.split(' ')
    for part in description_parts:
        if part.endswith("pV"):
            numeric_part = part.rstrip("pV")
            try:
                value = float(numeric_part)
                voltage_value = value
                break
            except ValueError:
                pass
        elif part.endswith("nV"):
            numeric_part = part.rstrip("nV")
            try:
                value = float(numeric_part)
                voltage_value = value * 1e3
                break
            except ValueError:
                pass
        elif part.endswith("uV"):
            numeric_part = part.rstrip("uV")
            try:
                value = float(numeric_part)
                voltage_value = value * 1e6
                break
            except ValueError:
                pass
        elif part.endswith("μV"):
            numeric_part = part.rstrip("μV")
            try:
                value = float(numeric_part)
                voltage_value = value * 1e6
                break
            except ValueError:
                pass
        elif part.endswith("mV"):
            numeric_part = part.rstrip("mV")
            try:
                value = float(numeric_part)
                voltage_value = value * 1e9
                break
            except ValueError:
                pass
        elif part.endswith("kV"):
            numeric_part = part.rstrip("kV")
            try:
                value = float(numeric_part)
                voltage_value = value * 1e15
                break
            except ValueError:
                pass
        elif part.endswith("MV"):
            numeric_part = part.rstrip("MV")
            try:
                value = float(numeric_part)
                voltage_value = value * 1e18
                break
            except ValueError:
                pass
        elif part.endswith('V'):
            numeric_part = part.rstrip('V')
            try:
                value = float(numeric_part)
                voltage_value = value * 1e12
                break
            except ValueError:
                pass
    return voltage_value