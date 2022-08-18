"""Deselect all objects with a 'WEIGTHED_NORMAL' modifier and keep sharp enabled"""
import bpy

selected = bpy.context.selected_objects.copy()
new_selection = []

for obj in selected:
    modifiers = obj.modifiers

    if len(obj.modifiers) > 0:
        for mod in obj.modifiers:
            if mod.type == 'WEIGHTED_NORMAL' and mod.keep_sharp == False:
                new_selection.append(obj)

bpy.ops.object.select_all(action='DESELECT')

for ob in new_selection:
    ob.select_set(True)
