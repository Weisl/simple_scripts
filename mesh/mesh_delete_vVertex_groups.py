"""deletes all vertex groups"""
import bpy

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for vGroup in obj.vertex_groups:
            obj.vertex_groups.remove(vGroup)
