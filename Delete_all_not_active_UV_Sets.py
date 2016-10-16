import bpy
for obj in bpy.context.selected_objects:
    
    if obj.type == 'MESH':
        bpy.context.scene.objects.active = obj
        for tex in obj.data.uv_textures:
            if tex.active_render == False:

                bpy.context.object.data.uv_textures.active = tex
                bpy.ops.mesh.uv_texture_remove()
                
            else: 
                tex.name = "UVMap"

        bpy.context.object.data.active_index = 0


