"""show wire of all objects"""
import bpy
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH' or obj.type == 'CURCVE' or obj.type == 'SURFACE':
        bpy.context.scene.objects.active = obj
        bpy.context.object.show_wire = False
