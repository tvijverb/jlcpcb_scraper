def parse_dielectric_description(component_description):
    dielectric_value = None
    if component_description is None:
        return dielectric_value
    
    if "C0G" in component_description:
        dielectric_value = "C0G"
    elif "X7R" in component_description:
        dielectric_value = "X7R"
    elif "X5R" in component_description:
        dielectric_value = "X5R"
    elif "Y5V" in component_description:
        dielectric_value = "Y5V"
    
    return dielectric_value