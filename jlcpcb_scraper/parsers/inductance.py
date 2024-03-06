def parse_inductance_description(component_description):
    inductance_value = None
    if component_description is None:
        return inductance_value
    description_parts = component_description.split(' ')
    for part in description_parts:
        if part.endswith("pH"):
            numeric_part = part.rstrip("pH")
            try:
                value = float(numeric_part)
                inductance_value = value
                break
            except ValueError:
                pass
        elif part.endswith("nH"):
            numeric_part = part.rstrip("nH")
            try:
                value = float(numeric_part)
                inductance_value = value * 1_000
                break
            except ValueError:
                pass
        elif part.endswith("uH"):
            numeric_part = part.rstrip("uH")
            try:
                value = float(numeric_part)
                inductance_value = value * 1_000_000
                break
            except ValueError:
                pass
        elif part.endswith("µH"):
            numeric_part = part.rstrip("µH")
            try:
                value = float(numeric_part)
                inductance_value = value * 1_000_000
                break
            except ValueError:
                pass
        elif part.endswith("mH"):
            numeric_part = part.rstrip("mH")
            try:
                value = float(numeric_part)
                inductance_value = value * 1_000_000_000
                break
            except ValueError:
                pass
        elif part.endswith("kH"):
            numeric_part = part.rstrip("kH")
            try:
                value = float(numeric_part)
                inductance_value = value * 1_000_000_000_000
                break
            except ValueError:
                pass
        elif part.endswith("MH"):
            numeric_part = part.rstrip("MH")
            try:
                value = float(numeric_part)
                inductance_value = value * 1_000_000_000_000_000
                break
            except ValueError:
                pass
        elif part.endswith('H'):
            numeric_part = part.rstrip('H')
            try:
                value = float(numeric_part)
                inductance_value = value * 1_000_000_000_000_000_000
                break
            except ValueError:
                pass
    return inductance_value