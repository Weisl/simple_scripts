import bpy
import bmesh


# Panel for Texel Density in the N Panel
class TEXEL_PT_Panel(bpy.types.Panel):
    bl_label = "Texel Density"
    bl_idname = "TEXEL_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texel Density"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        texel_props = scene.texel_props

        layout.prop(texel_props, "reference_texture_size", text="Reference Texture Size")
        layout.operator("mesh.calculate_texel_density", text="Calculate Texel Density")
        layout.label(text=f"Average Texel Density: {texel_props.average_texel_density:.2f} px/m²")


# Property Group to hold texel density data
class TexelProps(bpy.types.PropertyGroup):
    reference_texture_size: bpy.props.IntProperty(
        name="Reference Texture Size",
        default=1024,
        min=1,
        description="The reference texture size (e.g., 1024 for a 1024x1024 texture)"
    )

    average_texel_density: bpy.props.FloatProperty(
        name="Average Texel Density",
        default=0.0,
        description="The average texel density of the selected object"
    )


# Operator to calculate texel density
class MESH_OT_CalculateTexelDensity(bpy.types.Operator):
    bl_idname = "mesh.calculate_texel_density"
    bl_label = "Calculate Texel Density"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected")
            return {'CANCELLED'}

        # Get the reference texture size from the N panel properties
        texel_props = context.scene.texel_props
        reference_texture_size = texel_props.reference_texture_size

        # Get the mesh data and UV layer
        mesh = bmesh.new()
        mesh.from_mesh(obj.data)
        uv_layer = mesh.loops.layers.uv.verify()

        total_texel_density = 0
        face_count = 0

        for face in mesh.faces:
            face_area = face.calc_area()  # World space area in square meters

            if face_area == 0:
                continue

            # Calculate the UV area in normalized UV space (0 to 1)
            uv_area = self.calculate_uv_area(face, uv_layer)

            if uv_area == 0:
                continue

            # Calculate the scale factor: how much of the UV space (0-1) is covered
            uv_scale_factor = (uv_area / face_area) ** 0.5

            # Texel density calculation: Pixels per meter square
            texel_density = reference_texture_size * uv_scale_factor
            total_texel_density += texel_density
            face_count += 1

        # Calculate the average texel density
        if face_count > 0:
            texel_props.average_texel_density = total_texel_density / face_count
        else:
            texel_props.average_texel_density = 0.0

        # Free the bmesh data
        mesh.free()

        return {'FINISHED'}

    def calculate_uv_area(self, face, uv_layer):
        uv_coords = [loop[uv_layer].uv for loop in face.loops]
        uv_area = 0.0
        n = len(uv_coords)
        for i in range(n):
            x1, y1 = uv_coords[i]
            x2, y2 = uv_coords[(i + 1) % n]
            uv_area += x1 * y2 - x2 * y1
        return abs(uv_area) / 2.0


# Register/Unregister classes
def register():
    bpy.utils.register_class(TEXEL_PT_Panel)
    bpy.utils.register_class(TexelProps)
    bpy.utils.register_class(MESH_OT_CalculateTexelDensity)

    bpy.types.Scene.texel_props = bpy.props.PointerProperty(type=TexelProps)


def unregister():
    bpy.utils.unregister_class(TEXEL_PT_Panel)
    bpy.utils.unregister_class(TexelProps)
    bpy.utils.unregister_class(MESH_OT_CalculateTexelDensity)

    del bpy.types.Scene.texel_props


if __name__ == "__main__":
    register()
