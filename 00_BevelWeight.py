"Sets all bevels weights to 0"
import bpy
import bmesh

selected = bpy.context.selected_objects.copy()

for obj in selected:
    bpy.context.view_layer.objects.active = obj

    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    cl = bm.edges.layers.bevel_weight.verify()

    for edge in bm.edges:
        if edge.select:
            edge[cl] = 0.0

    bmesh.update_edit_mesh(me, False, False)
