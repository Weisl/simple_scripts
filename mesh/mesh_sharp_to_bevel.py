


"Converts Sharp Edges to Bevels"
import bpy
import bmesh

selected = bpy.context.selected_objects.copy()

for obj in selected:
    bpy.context.view_layer.objects.active = obj

    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    edgeBevelWeight = bm.edges.layers.bevel_weight.verify()
    sharpEdge = bm.edges.layers.bevel_weight.verify()

    for edge in bm.edges:
        if edge.select:
            if edge.smooth == False:
                edge.smooth == True
                edge[edgeBevelWeight] = 1.0

    bmesh.update_edit_mesh(me, False, False)
