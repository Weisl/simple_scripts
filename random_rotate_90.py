import bpy 
import random

old_selected_objects = bpy.context.selected_objects

for obj in bpy.context.selected_objects:
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj
    obj.select = True
    
    random_number = random.randint(0,4)
    rotation_angle = random_number * 1.5708
    bpy.ops.transform.rotate(value = rotation_angle, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False,       proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=28.1024)


bpy.ops.object.select_all(action='DESELECT')
for obj in old_selected_objects:
    obj.select = True
        