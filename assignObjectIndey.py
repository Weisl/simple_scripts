import bpy



#for obj in bpy.data.objects:
#    obj.pass_index = 0

for obj in bpy.context.selected_objects:
    obj.pass_index = 1
