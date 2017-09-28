''' stupid UV Lightpacker, if no uV set exists it creates on, otherwise it uses an existing one'''
import bpy

oldSel = bpy.context.selected_objects
oldActive = bpy.context.active_object

lightmapName = 'lightmap'

for obj in bpy.context.selectable_objects:
    bpy.context.scene.objects.active = obj
    if obj.type == 'MESH':
        if 'lightmap' not in obj.data.uv_textures:
            bpy.ops.mesh.uv_texture_add()
            lightmap = obj.data.uv_textures.active
            lightmap.name = 'lightmap'
        else:
            bpy.context.active_object.data.uv_textures['lightmap'].active = True

        bpy.ops.uv.lightmap_pack(PREF_CONTEXT='ALL_FACES', PREF_PACK_IN_ONE=False, PREF_NEW_UVLAYER=False,
                                 PREF_APPLY_IMAGE=False, PREF_BOX_DIV=12, PREF_MARGIN_DIV=0.1)

bpy.context.scene.objects.active = oldActive