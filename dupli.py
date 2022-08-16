
import bpy

selectedObjects = list(bpy.context.selected_objects)


for obj in selectedObjects:
    me = obj.data
    me_copy = me.copy()

    ob = bpy.data.objects.new(obj.name + "_copy", me_copy)
    ob.location = obj.location

    scene = bpy.context.scene
    scene.objects.link(ob)
    scene.update()