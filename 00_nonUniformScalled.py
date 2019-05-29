"""select all objects that use modifier (except Triangulate and Weighted Normals)"""
import bpy

selected = bpy.context.selected_objects.copy()
new_selection = []

for obj in selected:
    bpy.context.view_layer.objects.active = obj

    if obj.scale is ((1.0, 1.0, 1.0)):
        new_selection.append(obj)

bpy.ops.object.select_all(action='DESELECT')

for ob in new_selection:
    ob.select_set(True)