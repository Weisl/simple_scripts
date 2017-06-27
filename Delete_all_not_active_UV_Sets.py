"""deletes all not active UV sets"""

import bpy
for obj in bpy.context.selected_objects:

    if obj.type == 'MESH':
        bpy.context.scene.objects.active = obj

        uvIndex = obj.data.uv_textures.active_index

        removeSet = []
        properUv = None

        for i, tex in enumerate(obj.data.uv_textures):
            if i != uvIndex:
                removeSet.append(tex)
            else:
                properUv = tex

        for tex in removeSet:
            bpy.context.object.data.uv_textures.active = tex
            bpy.ops.mesh.uv_texture_remove()

        if properUv is not None:
            properUv.name = "UVMap"



