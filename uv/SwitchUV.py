"""deletes all not active UV sets"""
import bpy

selected = bpy.context.selected_objects.copy()
activeUvSet = "map1"
activeUvSet = "lightmap"

for obj in selected:
    # print(instanciatedObjects)
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        uvActive = obj.data.uv_layers.active
        idx_set = obj.data.uv_layers.find(activeUvSet)
        bpy.context.object.data.uv_layers.active_index = idx_set
        bpy.context.object.data.uv_layers[idx_set].active_render = True
