''' Add a lightmap to selected objects and automatically unwrap and pack the UVs. It's a very simplest Unwrap algorithm'''
import bpy

lightmapName = 'lightmap'

oldSel = bpy.context.selected_objects
oldActive = bpy.context.active_object

for obj in bpy.context.selectable_objects:

    if obj.type == 'MESH':
        if 'lightmap' not in obj.data.uv_layers:
            lightmap = obj.data.uv_layers.new()
            lightmap.name = 'lightmap'
        else:
            obj.data.uv_layers['lightmap'].active = True

        bpy.context.view_layer.objects.active = obj
        bpy.ops.uv.lightmap_pack(PREF_CONTEXT='ALL_FACES', PREF_PACK_IN_ONE=False, PREF_NEW_UVLAYER=False,
                                 PREF_APPLY_IMAGE=False, PREF_BOX_DIV=12, PREF_MARGIN_DIV=0.1)

bpy.context.view_layer.objects.active = oldActive
