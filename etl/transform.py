# Normalize, clean, and transform the data

def transform_spells(spells_data):
    transformed_data = []

    # Iterate through the list of spells and transform each one
    for spell in spells_data:
        transformed_data.append({
            # Normalize and clean the data
            "index": spell.get("index"),
            "name": spell.get("name"),
            "level": spell.get("level"),
            "school": spell.get("school", {}).get("name"),
            "casting_time": spell.get("casting_time"),
            "range": spell.get("range"),
            "components": ", ".join(spell.get("components", [])),
            "material": spell.get("material"),
            "duration": spell.get("duration"),
            "concentration": spell.get("concentration"),
            "ritual": spell.get("ritual"),
            "description": " ".join(spell.get("desc", [])),
        })
    return transformed_data
