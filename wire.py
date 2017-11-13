import bpy

for ob in bpy.context.selected_objects:
    bpy.context.scene.objects.active = ob
    try:
        bpy.context.object.draw_type = 'WIRE'
    except:
        pass