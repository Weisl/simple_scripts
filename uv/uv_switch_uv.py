"""Change the active UV set to the name specified in actoveUVSet at the top. """
import bpy

activeUvSet = "lightmap"

selected = bpy.context.selected_objects.copy()
for obj in selected:
    # print(instanciatedObjects)
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        uvActive = obj.data.uv_layers.active
        idx_set = obj.data.uv_layers.find(activeUvSet)
        bpy.context.object.data.uv_layers.active_index = idx_set
        bpy.context.object.data.uv_layers[idx_set].active_render = True
