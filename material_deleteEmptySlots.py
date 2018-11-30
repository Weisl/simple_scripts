import bpy

c = bpy.context

for obj in c.selected_objects:
    if obj.type == 'MESH':
        c.scene.objects.active = obj
        materialList = list(obj.material_slots)
        deleteList = []
        
        counter = 0
        
        for mat in materialList:
            if mat.material == None:
                counter = counter + 1
        for i in range(counter):
            idx = obj.material_slots.find('')
            bpy.context.object.active_material_index = idx
            bpy.ops.object.material_slot_remove()

            

        
            




    
            