import bpy

for obj in bpy.data.objects:
    try:
        obj.data.materials.clear()
    except:
        print("")

# for material in bpy.data.materials:
#    material.user_clear();
#    bpy.data.materials.remove(material);
