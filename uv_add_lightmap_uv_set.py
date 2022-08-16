"""deletes all not active UV sets"""
import bpy

selected = bpy.context.selected_objects.copy()
instanciatedObjects = []

for obj in selected:
    # print(instanciatedObjects)
    if obj.type == 'MESH':
        if obj.data not in instanciatedObjects:
            instanciatedObjects.append(obj.data)
            bpy.context.view_layer.objects.active = obj
            uvActive = obj.data.uv_layers.active
            texSetList = list(obj.data.uv_layers)
            idx_set = len(texSetList)


            if "lightmap" not in obj.data.uv_layers:
                bpy.ops.mesh.uv_texture_add()
                bpy.context.object.data.uv_layers.active_index = idx_set
                bpy.context.object.data.uv_layers[idx_set].name = "lightmap"
