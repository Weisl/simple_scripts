import bpy
import os


def parse_preset_file(preset_path):
    """Parse the preset file to extract properties and their values."""
    properties = {}

    if not os.path.exists(preset_path):
        print(f"Preset file not found: {preset_path}")
        return properties

    with open(preset_path, 'r') as preset_file:
        for line in preset_file:
            line = line.strip()
            if line.startswith("op."):
                try:
                    # Extract the property name and value
                    prop_name, prop_value = line[3:].split(" = ", 1)
                    # Evaluate the value if it's not a string
                    if prop_value.startswith(("'", '"')):
                        properties[prop_name] = prop_value.strip("'\"")
                    else:
                        properties[prop_name] = eval(prop_value)
                except Exception as e:
                    print(f"Error parsing line: {line} -> {e}")
    return properties


def assign_preset_to_exporter(properties, exporter):
    """Apply parsed properties to the exporter."""
    for prop_name, prop_value in properties.items():
        try:
            if hasattr(exporter.export_properties, prop_name):
                setattr(exporter.export_properties, prop_name, prop_value)
                print(f"Applied {prop_name} = {prop_value}")
            else:
                print(f"Exporter property '{prop_name}' not found.")
        except Exception as e:
            print(f"Error setting property '{prop_name}': {e}")


# Define the preset file path
preset_path = r"C:\Users\weisl\AppData\Roaming\Blender Foundation\Blender\4.3\scripts\presets\operator\export_scene.fbx\a7.py"

# Get the current scene and collection
scene = bpy.context.scene
collection = bpy.context.collection

# Ensure the collection has exporters
if hasattr(collection, "exporters") and len(collection.exporters) > 0:
    exporter = collection.exporters[0]

    # Parse the preset file
    preset_properties = parse_preset_file(preset_path)

    # Apply the properties to the exporter
    assign_preset_to_exporter(preset_properties, exporter)
else:
    print("No exporters found in the current collection.")
