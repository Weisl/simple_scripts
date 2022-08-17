import bpy
selected = bpy.context.selected_objects.copy()
activeOb = bpy.context.view_layer.objects.active

dataList = []
multiDataList = {}

for obj in selected:
    if obj.data not in dataList and obj.data.users:
        multiDataList.append(obj)

        grpExists = False
        for grp in bpy.data.collections:
            if grp.name == grpName:
                grpExists = True

    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)

    if bpy.context.view_layer.objects.active is not None:
        grpName = bpy.context.active_object.name + "_grp"


    if grpExists == False:
        bpy.ops.collection.create(name=grpName)
        bpy.ops.object.group_link(group=grpName)

    bpy.context.view_layer.objects.active = activeOb