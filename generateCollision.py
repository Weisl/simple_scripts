import bpy

allObjects = bpy.data.objects
selectedObjects = bpy.context.selected_objects.copy()


for obj in selectedObjects:
    parName = obj.parent.name
    #coordinates = obj.bound_box

    i = 1
    beginning = ('%02d' % i)
    newName = "UBX_" + parName + "_clone_" + beginning
    while (newName in allObjects):
        beginning = ('%02d' % i)
        newName = "UBX_" + parName + "_" + beginning
        i = i + 1

    obj.name = newName
    obj.draw_type = 'WIRE'
