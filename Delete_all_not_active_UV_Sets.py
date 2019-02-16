"""deletes all not active UV sets"""
import bpy

selected = bpy.context.selected_objects.copy()

for obj in selected:

    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        uvActive = obj.data.uv_textures.active
        texSetList = list(obj.data.uv_textures)

        for tex in texSetList:
            if tex != uvActive:
                try:
                    obj.data.uv_textures.remove(tex)
                    print ("Deleted %s on object %s" % (str(tex), obj.name))

                except Exception:
                    print ("couldn't delete textuteset %s on object %s" % (str(tex), obj.name))
            else:
                print ("LOL")



