def parse_current_description(component_description):
    current_value = None

    if component_description is None:
        return current_value

    description_parts = component_description.split(' ')
    for part in description_parts:
        if part.endswith("pA"):
            numeric_part = part.rstrip("pA")
            try:
                value = float(numeric_part)
                current_value = value
                break
            except ValueError:
                pass
        elif part.endswith("nA"):
            numeric_part = part.rstrip("nA")
            try:
                value = float(numeric_part)
                current_value = value * 1e3
                break
            except ValueError:
                pass
        elif part.endswith("uA"):
            numeric_part = part.rstrip("uA")
            try:
                value = float(numeric_part)
                current_value = value * 1e6
                break
            except ValueError:
                pass
        elif part.endswith("μA"):
            numeric_part = part.rstrip("μA")
            try:
                value = float(numeric_part)
                current_value = value * 1e6
                break
            except ValueError:
                pass
        elif part.endswith("mA"):
            numeric_part = part.rstrip("mA")
            try:
                value = float(numeric_part)
                current_value = value * 1e9
                break
            except ValueError:
                pass
        elif part.endswith("kA"):
            numeric_part = part.rstrip("kA")
            try:
                value = float(numeric_part)
                current_value = value * 1e15
                break
            except ValueError:
                pass
        elif part.endswith("MA"):
            numeric_part = part.rstrip("MA")
            try:
                value = float(numeric_part)
                current_value = value * 1e18
                break
            except ValueError:
                pass
        elif part.endswith('A'):
            numeric_part = part.rstrip('A')
            try:
                value = float(numeric_part)
                current_value = value * 1e12
                break
            except ValueError:
                pass

    return current_value