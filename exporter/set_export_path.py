import bpy
import os


def get_active_collection():
    # Try to get the active collection from the context
    active_collection = bpy.context.collection

    if active_collection:
        print(f"Active collection: {active_collection.name}")
        return active_collection
    else:
        print("No active collection found.")
        return None


def add_custom_exporter_to_collection(collection_name, exporter_name):
    # Get the collection
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Error: Collection '{collection_name}' not found.")
        return None

    # Check if the custom exporter property already exists
    for exporter in collection.exporters:
        if exporter.name == 'FBX':
            print(f"Custom exporter '{exporter_name}' already exists in the collection.")
        return exporter


def set_exporter_path(collection_name, exporter, A, B):
    # Get the current Blender file directory
    blend_filepath = bpy.data.filepath
    blend_dir = os.path.dirname(blend_filepath)

    # Ensure the Blender file is saved
    if not blend_filepath:
        print("Error: Save the Blender file before running the script.")
        return

    # Create the export path with the collection name as the file name
    export_name = collection_name + ".fbx"
    export_path = os.path.join(blend_dir, export_name)

    # Replace part of the path if A is found
    if A in export_path:
        export_path = export_path.replace(A, B)

    exporter.export_properties.filepath = export_path

    # Print the export path for debugging
    print(f"Set export path to: {export_path}")


active_collection = get_active_collection()

if active_collection:
    collection_name = active_collection.name  # Replace with your collection name
    exporter_name = "IO_FH_fbx"
    A = "workdata"
    B = "sourcedata"

    # Add custom exporter to collection
    exporter = add_custom_exporter_to_collection(collection_name, exporter_name)
    exporter
    # Set the export path
    if exporter:
        set_exporter_path(collection_name, exporter, A, B)
