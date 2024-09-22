import bpy


# Operator to generate or update the UV Checker texture
class CreateUVCheckerTexture(bpy.types.Operator):
    bl_idname = "material.create_uv_checker_texture"
    bl_label = "Create UV Checker Texture"

    def execute(self, context):
        mat = context.object.active_material

        # Get resolution from custom material properties
        resolution_x = mat.uv_checker_res_x
        resolution_y = mat.uv_checker_res_y

        # Generate texture name
        texture_name = f"UVChecker_{resolution_x}x{resolution_y}"

        # Check if texture already exists
        if texture_name in bpy.data.images:
            img = bpy.data.images[texture_name]
        else:
            # Create a new UV Checker texture
            img = bpy.data.images.new(texture_name, width=resolution_x, height=resolution_y)
            img.generated_type = 'COLOR_GRID'

        # Check if material already has a node tree
        if not mat.use_nodes:
            mat.use_nodes = True

        nodes = mat.node_tree.nodes
        # Look for the existing "Simple Checker" node
        img_tex_node = nodes.get("Simple Checker")

        if not img_tex_node:
            # Create a new Image Texture node named "Simple Checker"
            img_tex_node = nodes.new(type='ShaderNodeTexImage')
            img_tex_node.name = "Simple Checker"
            img_tex_node.label = "Simple Checker"

        # Assign the new or existing UV checker image to the "Simple Checker" node
        img_tex_node.image = img

        # Set the node as the active node
        nodes.active = img_tex_node

        return {'FINISHED'}


# Panel in the Material Properties
class UVCheckerPanel(bpy.types.Panel):
    bl_label = "UV Checker Texture"
    bl_idname = "MATERIAL_PT_uv_checker"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        mat = context.object.active_material

        # Resolution inputs
        layout.prop(mat, "uv_checker_res_x", text="Resolution X")
        layout.prop(mat, "uv_checker_res_y", text="Resolution Y")

        # Create Texture Button
        layout.operator("material.create_uv_checker_texture")


def register():
    bpy.utils.register_class(CreateUVCheckerTexture)
    bpy.utils.register_class(UVCheckerPanel)

    # Add properties to the material to store the resolution
    bpy.types.Material.uv_checker_res_x = bpy.props.IntProperty(name="Resolution X", default=1024, min=1)
    bpy.types.Material.uv_checker_res_y = bpy.props.IntProperty(name="Resolution Y", default=1024, min=1)


def unregister():
    bpy.utils.unregister_class(CreateUVCheckerTexture)
    bpy.utils.unregister_class(UVCheckerPanel)

    # Remove properties
    del bpy.types.Material.uv_checker_res_x
    del bpy.types.Material.uv_checker_res_y


if __name__ == "__main__":
    register()
