import bpy

def replace_texture_file_endings():
    for material in bpy.data.materials:
        if material.node_tree:  # Check if the material has a node tree
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    image = node.image
                    if image and image.filepath.endswith('.tga'):
                        image.filepath = image.filepath.replace('.tga', '.png')
                        print(f"Updated: {image.filepath}")

replace_texture_file_endings()
