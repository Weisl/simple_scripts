import bpy
active_object = bpy.context.active_object 

if active_object.type == 'CAMERA':
    bpy.context.scene.camera = bpy.data.objects[active_object.name]
