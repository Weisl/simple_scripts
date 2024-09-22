import bmesh
import bpy
import gpu
from gpu_extras.batch import batch_for_shader

# Draw handler reference
draw_handler = None


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

        layout.operator("mesh.calculate_texel_density", text="Calculate Texel Density")
        layout.label(text=f"Average Texel Density: {texel_props.average_texel_density:.2f} px/m²")

        layout.separator()
        layout.prop(context.scene, "show_texel_density_overlay", text="Texel Density Overlay")
        layout.operator("texel.update_overlay", text="Update Overlay")
        layout.operator("texel.remove_overlay", text="Remove Overlay")

        layout.separator()
        layout.label(text="Material Properties:")
        for material in bpy.data.materials:
            row = layout.row()
            row.prop(material, "texture_size", text=f"{material.name} Texture Size")


# Property Group to hold texel density data
class TexelProps(bpy.types.PropertyGroup):
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

        texel_props = context.scene.texel_props

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

            # Get the material assigned to this face
            material_index = face.material_index
            if material_index < len(obj.data.materials):
                material = obj.data.materials[material_index]
                texture_size = material.texture_size if material else 1024  # Default to 1024 if no material
            else:
                texture_size = 1024

            uv_scale_factor = (uv_area / face_area) ** 0.5

            # Texel density calculation: Pixels per meter square
            texel_density = texture_size * uv_scale_factor
            total_texel_density += texel_density
            face_count += 1

        # Calculate the average texel density
        if face_count > 0:
            texel_props.average_texel_density = total_texel_density / face_count
        else:
            texel_props.average_texel_density = 0.0

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


# Toggle Texel Density Overlay in Viewport
def toggle_texel_density_overlay(self, context):
    if context.scene.show_texel_density_overlay:
        register_draw_handler()
    else:
        unregister_draw_handler()


def draw_texel_density_overlay():
    context = bpy.context  # Access the global context
    texel_props = context.scene.texel_props

    for obj in context.selected_objects:
        if obj.type != 'MESH':
            continue

        mesh = bmesh.new()
        mesh.from_mesh(obj.data)
        uv_layer = mesh.loops.layers.uv.verify()

        # Create a shader for drawing
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        gpu.state.blend_set('ALPHA')

        # Get object transformation matrix
        obj_matrix = obj.matrix_world

        for face in mesh.faces:
            face_area = face.calc_area()  # World space area in square meters

            if face_area == 0:
                continue

            uv_area = calculate_uv_area(face, uv_layer)
            if uv_area == 0:
                continue

            # Get the material assigned to this face
            material_index = face.material_index
            if material_index < len(obj.data.materials):
                material = obj.data.materials[material_index]
                texture_size = material.texture_size if material else 1024  # Default to 1024 if no material
            else:
                texture_size = 1024

            # Calculate the texel density
            texel_density = texture_size * (uv_area / face_area) ** 0.5

            # Determine the color based on texel density
            if texel_density == texture_size:
                color = (0.0, 1.0, 0.0, 0.3)  # Green for exact match
            elif texel_density > texture_size:
                color = (1.0, 0.0, 0.0, 0.3)  # Red for higher density
            else:
                color = (0.0, 0.0, 1.0, 0.3)  # Blue for lower density

            # Triangulate the face for correct rendering using bmesh.ops.triangulate
            geom = [face]
            bmesh.ops.triangulate(mesh, faces=geom)

            for tri_face in geom:
                vertices = [obj_matrix @ loop.vert.co for loop in tri_face.loops]
                batch = batch_for_shader(shader, 'TRIS', {"pos": vertices})
                shader.bind()
                shader.uniform_float("color", color)
                batch.draw(shader)

        mesh.free()
        gpu.state.blend_set('NONE')


def calculate_uv_area(face, uv_layer):
    uv_coords = [loop[uv_layer].uv for loop in face.loops]
    uv_area = 0.0
    n = len(uv_coords)
    for i in range(n):
        x1, y1 = uv_coords[i]
        x2, y2 = uv_coords[(i + 1) % n]
        uv_area += x1 * y2 - x2 * y1
    return abs(uv_area) / 2.0


# Register the draw handler
def register_draw_handler():
    global draw_handler
    if draw_handler is None:
        draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            draw_texel_density_overlay, (), 'WINDOW', 'POST_VIEW')
        print("Draw handler registered.")


# Unregister the draw handler
def unregister_draw_handler():
    global draw_handler
    if draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
        draw_handler = None
        print("Draw handler unregistered.")


# Operator to update the overlay
class TEXEL_OT_UpdateOverlay(bpy.types.Operator):
    bl_idname = "texel.update_overlay"
    bl_label = "Update Overlay"

    def execute(self, context):
        unregister_draw_handler()  # Ensure the old handler is removed
        register_draw_handler()
        return {'FINISHED'}


# Operator to remove the overlay
class TEXEL_OT_RemoveOverlay(bpy.types.Operator):
    bl_idname = "texel.remove_overlay"
    bl_label = "Remove Overlay"

    def execute(self, context):
        unregister_draw_handler()
        return {'FINISHED'}


# Register/Unregister classes
def register():
    bpy.utils.register_class(TEXEL_PT_Panel)
    bpy.utils.register_class(TexelProps)
    bpy.utils.register_class(MESH_OT_CalculateTexelDensity)
    bpy.utils.register_class(TEXEL_OT_UpdateOverlay)
    bpy.utils.register_class(TEXEL_OT_RemoveOverlay)

    bpy.types.Material.texture_size = bpy.props.IntProperty(
        name="Texture Size",
        default=1024,
        min=1,
        description="The texture size (e.g., 1024 for a 1024x1024 texture)"
    )

    bpy.types.Scene.texel_props = bpy.props.PointerProperty(type=TexelProps)
    bpy.types.Scene.show_texel_density_overlay = bpy.props.BoolProperty(
        name="Texel Density Overlay",
        default=False,
        update=toggle_texel_density_overlay,
    )


def unregister():
    bpy.utils.unregister_class(TEXEL_PT_Panel)
    bpy.utils.unregister_class(TexelProps)
    bpy.utils.unregister_class(MESH_OT_CalculateTexelDensity)
    bpy.utils.unregister_class(TEXEL_OT_UpdateOverlay)
    bpy.utils.unregister_class(TEXEL_OT_RemoveOverlay)

    del bpy.types.Scene.texel_props
    del bpy.types.Scene.show_texel_density_overlay
    del bpy.types.Material.texture_size

    unregister_draw_handler()


if __name__ == "__main__":
    register()
