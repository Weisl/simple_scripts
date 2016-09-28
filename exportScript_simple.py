import bpy


# get the path where the blend file is located
basedir = bpy.path.abspath('//')
selection = bpy.context.selected_objects

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        # TODO Transform stuff: save transformation in variable and set transformation to 0,0,0
        
        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True
        
        bpy.ops.export_scene.fbx(filepath = basedir + obj.name + '.fbx', check_existing=True, use_selection=True, global_scale=1.0)


for ob in selection:
    ob.select = True