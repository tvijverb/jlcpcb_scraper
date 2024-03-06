def parse_resistance_description(component_description):
    resistance_value = None

    if component_description is None:
        return resistance_value

    description_parts = component_description.split(' ')
    for part in description_parts:
        if part.endswith("pΩ"):
            numeric_part = part.rstrip("pΩ")
            try:
                value = float(numeric_part)
                resistance_value = value * 1e-12
                break
            except ValueError:
                pass
        elif part.endswith("nΩ"):
            numeric_part = part.rstrip("nΩ")
            try:
                value = float(numeric_part)
                resistance_value = value * 1e-9
                break
            except ValueError:
                pass
        elif part.endswith("uΩ") or part.endswith("μΩ"):
            numeric_part = part.rstrip("uΩ").rstrip("μΩ")
            try:
                value = float(numeric_part)
                resistance_value = value * 1e-6
                break
            except ValueError:
                pass
        elif part.endswith("mΩ"):
            numeric_part = part.rstrip("mΩ")
            try:
                value = float(numeric_part)
                resistance_value = value * 1e-3
                break
            except ValueError:
                pass
        elif part.endswith("kΩ"):
            numeric_part = part.rstrip("kΩ")
            try:
                value = float(numeric_part)
                resistance_value = value * 1e3
                break
            except ValueError:
                pass
        elif part.endswith("MΩ"):
            numeric_part = part.rstrip("MΩ")
            try:
                value = float(numeric_part)
                resistance_value = value * 1e6
                break
            except ValueError:
                pass
        elif part.endswith('Ω'):
            numeric_part = part.rstrip('Ω')
            try:
                value = float(numeric_part)
                resistance_value = value
                break
            except ValueError:
                pass

    return resistance_value