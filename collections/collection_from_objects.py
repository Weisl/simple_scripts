"""Create s collection for each selected object and set the instance offset to the object origin"""
import bpy

for ob in bpy.context.selected_objects:
    myCol = bpy.data.collections.new(ob.name)
    bpy.context.scene.collection.children.link(myCol)
    myCol.objects.link(ob)

    myCol.instance_offset[0] = ob.location[0]
    myCol.instance_offset[1] = ob.location[1]
    myCol.instance_offset[2] = ob.location[2]
