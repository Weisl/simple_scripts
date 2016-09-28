# This sample script demonstrates a dynamic EnumProperty with custom icons.
# The EnumProperty is populated dynamically with thumbnails of the contents of
# a chosen directory in 'enum_previews_from_directory_items'.
# Then, the same enum is displayed with different interfaces. Note that the
# generated icon previews do not have Blender IDs, which means that they can
# not be used with UILayout templates that require IDs,
# such as template_list and template_ID_preview.
#
# Other use cases:
# - make a fixed list of enum_items instead of calculating them in a function
# - generate isolated thumbnails to use as custom icons in buttons
#   and menu items
#
# For custom icons, see the template "ui_previews_custom_icon.py".
#
# For distributable scripts, it is recommended to place the icons inside the
# script directory and access it relative to the py script file for portability:
#
#    os.path.join(os.path.dirname(__file__), "images")


import os
import bpy
from bpy.types import WindowManager
from bpy.types import Scene
from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty
    )


def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.my_previews_dir

    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]

    if directory == pcoll.my_previews_dir:
        return pcoll.my_previews

    print("Scanning directory: %s" % directory)

    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(filepath, filepath, 'IMAGE')
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.my_previews


class ImportExport(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Export panel"
    bl_idname = "OBJECT_PT_previews"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

#    ui_tab = EnumProperty(
#        items=(('MAIN', "Main", "Main basic settings"),
#            ('NAMING', "Naming", "Settings for renaming"),
#            ('GEOMETRY', "Geometries", "Geometry-related settings"),
#            ('ARMATURE', "Armatures", "Armature-related settings"),
#            ('ANIMATION', "Animation", "Animation-related settings"),
#            ),
#        name="ui_tab",
#        description="Export options categories",
#        )



    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        scene = context.scene
        
        layout.label("Export Path")      
        
        row = layout.row()
        row.prop(wm, "my_previews_dir")
        row = layout.row()
        row.operator("export.reset_dir", text = "Reset")       
        #TODO Bookmarks

        row = layout.row()
        #row.prop(self, "ui_tab"
        
        row = layout.row()
        row.prop(wm, "export_format")
        row = layout.row()
        row.prop(wm, "export_batch_mode")
                
        row = layout.row()
        row.prop(wm, "export_use_selection")
        row = layout.row()
        #row.prop(wm, "export_by_layer")
        
        
        row.prop(wm, "export_override")
        
        
        #Todo export recursive
        
        #Naming Operation 
        row = layout.row()
        row.label(text="Object Renaming")       
        
        row = layout.row()
        row.prop(wm, "export_prefix")
        row.prop(wm, "export_sufix")
        
        row = layout.row()
        row.prop(wm, "export_searchString")
        row.prop(wm, "export_replaceString")
        
        row = layout.row()
        row.label(text="Transformations")
        row = layout.row()
        row.prop(wm, "export_global_scale")
        row = layout.row()
        row.prop(wm, "export_translate_(0,0,0)")
        row = layout.row()
        row.prop(wm, "export_triangulate")
        
        format = bpy.context.window_manager.export_format  
        if format == 'obj':
            row = layout.row()
            row.label(text="Obj Specific Settings")  
        
        elif format == 'fbx': 
            row = layout.row()
            row.label(text="Fbx Specific Settings")  
        #TODO: Wirte Operator to Change things in the name

        row = layout.row()
        row.scale_y = 2.0
        
        row.operator("export.button", text = "Export")        
        
        #row = layout.row()
        #row.template_icon_view(wm, "my_previews")
        #row = layout.row()
        #row.prop(wm, "my_previews")


# We can store multiple preview collections here,
# however in this example we only store "main"

objectPositions = {}

class BUTTON_RESET_DIR(bpy.types.Operator):
    bl_idname = "export.reset_dir"
    bl_label = "Reset Directory"

    def execute(self, context):
        bpy.context.window_manager.my_previews_dir = ''
        return {'FINISHED'}

class EXPORT_BUTTON(bpy.types.Operator):
    bl_idname = "export.button"
    bl_label = "Export"
    bl_description = "Export Objects"
    #bl_options = {'UNDO', 'PRESET'}

    modifier_stack = []
    
    def execute(self, context):
  
       # get the path where the blend file is located
        basedir = bpy.context.window_manager.my_previews_dir

        if basedir == '':
            basedir = bpy.path.abspath('//')

        selection = context.selected_objects
        oldActive =   context.object
        wm = bpy.context.window_manager
    
    
    
        if wm.export_batch_mode == 'OBJECT':
            
            for obj in bpy.context.selected_objects:
                bpy.context.scene.objects.active = obj
                
                obj_location = obj.location
                
                if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'Surface':
                    # TODO Transform stuff: save transformation in variable and set transformation to 0,0,0
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select = True
                    
                    sufix = wm.export_sufix
                    prefix = wm.export_prefix   

                    exportFormat = bpy.context.window_manager.export_format

                    filepath = ""
                    filename = prefix + obj.name + sufix
                    filepath = basedir + filename + "." + exportFormat

                    print ("filepath")


                    # set Transformation to 0,0,0                
                    if bpy.context.window_manager.export_translate_000 == True:
                        
                        obj_location[0] = obj.location[0]
                        obj_location[1] = obj.location[1]
                        obj_location[2] = obj.location[2]

                        
                        print(obj_location)
                        obj.location[0] = 0
                        obj.location[1] = 0
                        obj.location[2] = 0
                        
                        print(obj_location)


                    if bpy.context.window_manager.export_triangulate == True:
                        try:
                            mod =obj.modifiers.new(name = 'Export_Triangulate', type='TRIANGULATE')
                            self.modifier_stack.append(mod)
                        except:
                            self.report({'ERROR'}, self.errorMsg)
                                                                             
                    if exportFormat == 'fbx':
                        bpy.ops.export_scene.fbx(filepath = filepath,
                            check_existing = bpy.context.window_manager.export_override, 
                            use_selection= bpy.context.window_manager.export_use_selection, 
                            global_scale=1.0)
                            
                    elif exportFormat == 'obj':
                        bpy.ops.export_scene.obj(filepath = filepath, 
                        use_selection = bpy.context.window_manager.export_use_selection,
                        global_scale=1.0)    
                            
                    # reset transformations
                    print(obj_location)                
                    obj.location[0] = obj_location[0]
                    obj.location[1] = obj_location[1]
                    obj.location[2] = obj_location[2]
                    

            for ob in selection:
                ob.select = True
            for mod in self.modifier_stack:
                bpy.ops.object.modifier_remove(modifier = mod.name)
                
            self.modifier_stack = []
            
            bpy.context.scene.objects.active == oldActive
        return {'FINISHED'}        

preview_collections = {}


def register():

    # FilePath
    WindowManager.my_previews_dir = StringProperty(
            name="Folder Path",
            subtype='DIR_PATH',
            default=""
            )

    WindowManager.my_previews = EnumProperty(
            items=enum_previews_from_directory_items,
            )

    # Settings

    WindowManager.export_format = EnumProperty(items = [('fbx', 'Fbx', "Use fbx for import and export", '', 1),('obj', 'Obj', "Use obj for import and export", '', 2)], name = 'Fileformat')

    WindowManager.export_batch_mode= EnumProperty(items = [
    ('OBJECT', 'object', "Export by object", '', 1),
    ('LAYER', 'layer', "Export by layer", '', 2),
    ('GROUP', 'group', "Export by group", '', 3),
    ('SCENE', 'scene', "Export by scene", '', 4)], name ="Batch mode")
    

    WindowManager.export_use_selection = BoolProperty(
            name="Selected Objects",
            description="Export selected objects on visible layers",
            default=True,
            )

    WindowManager.export_by_layer = BoolProperty(
            name="Export by Layer",
            description="Export every layer as a single file",
            default=False,
            )
            
    WindowManager.export_translate_000 = BoolProperty(
            name="Translate 000",
            description="Translate Objekts to 0,0,0 before exporting them",
            default=False,
            )

    WindowManager.export_triangulate = BoolProperty(
            name="Triangulate",
            description="Triangulate Object before exporting",
            default=False,
            )
            
            
    WindowManager.export_global_scale = FloatProperty(
            name="Global Scale",
            description="Global scale used for export",
            default=1.0,
            min = 0.1,
            max = 1000
            )
    
    WindowManager.export_override = BoolProperty(
            name="Override export",
            description="Override file if it already exists",
            default=True,
            )   

    WindowManager.export_prefix = StringProperty(name='Prefix')
    WindowManager.export_sufix = StringProperty(name='Sufix')

    WindowManager.export_searchString = StringProperty(name='search string')
    WindowManager.export_replaceString = StringProperty(name='replace string')


    # Note that preview collections returned by bpy.utils.previews
    # are regular Python objects - you can use them to store custom data.
    #
    # This is especially useful here, since:
    # - It avoids us regenerating the whole enum over and over.
    # - It can store enum_items' strings
    #   (remember you have to keep those strings somewhere in py,
    #   else they get freed and Blender references invalid memory!).
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()

    preview_collections["main"] = pcoll




    bpy.utils.register_class(ImportExport)
    bpy.utils.register_class(EXPORT_BUTTON)
    bpy.utils.register_class(BUTTON_RESET_DIR)

def unregister():
    from bpy.types import WindowManager

    del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    bpy.utils.unregister_class(ImportExport)
    bpy.utils.unregister_class(EXPORT_BUTTON)
    bpy.utils.unregister_class(BUTTON_RESET_DIR)

if __name__ == "__main__":
    register()
