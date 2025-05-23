# Normalize, clean, and transform the data

def transform_spells(spells_data):
    transformed_data = []

    # Iterate through the list of spells and transform each one
    for spell in spells_data:
        # Extract classes nested list and flatten to a comma-separated string
        classes = spell.get("classes", [])
        class_names = ", ".join(cls.get("name", "") for cls in classes)


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
            "classes": class_names,
            "higher_level": " ".join(spell.get("higher_level", [])),
            "subclasses": ", ".join(s["name"] for s in spell.get("subclasses", [])),
        })
    return transformed_data
