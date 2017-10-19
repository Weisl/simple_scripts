
'''
import bpy
import os

# Use your own script name here:
filepath = "C:/Users/weisl/Documents/GitHub/mp_mini_script_utils/pipeline.py"
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)


'''

bl_info = {
    "name": "Custom Save",
    "description": "",
    "author": "Your Name",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object"}


# Imports
import bpy
import os
import time


from bpy.types import Panel, Operator, Scene , WindowManager
from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    IntProperty,
    CollectionProperty,
    BoolVectorProperty
    )


# think of it as a cache dict / list
PL_Project_List = {}

class PopupSave(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "popup.customsave"
    bl_label = "Save Popup"
    bl_options = {'REGISTER', 'UNDO','PRESET', 'INTERNAL'}

    def invoke(self, context, event):
        width = 800 * bpy.context.user_preferences.system.pixel_size
        status = context.window_manager.invoke_props_dialog(self,width=width)

        return status

    def draw(self, context):
        l = self.layout
        r = l.row(align=True)

        r.prop(context.scene, "AssetName", )
        r = l.row(align=True)
        r.prop(context.scene, "Locations")
        r = l.row(align = True)
        r.prop(context.scene, "ObjectType")

        r = l.row(align=True)
        r.operator("scene.save_op")

    def execute(self, context):

        ob = context.object
        return {'FINISHED'}



class FILEBROWSER_PT_Pipeline(Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Asset management"
    bl_category = "Pipeline tools"

    def invoke(self):
        if addon_prefs.filepath != '' and addon_prefs.filepath is not None:
            wm.my_previews_dir = addon_prefs.filepath

    def draw(self, context):

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        l = self.layout
        wm = context.window_manager
        r = l.row(align=True)

        r = l.row()
        r.prop(wm, "my_previews_dir")



        r.prop(context.scene, "AssetName", )
        r = l.row(align=True)
        r.prop(context.scene, "Locations")
        r = l.row(align = True)
        r.prop(context.scene, "ObjectType")

        r = l.row(align=True)
        r.operator("popup.customsave")


class SaveOperator(bpy.types.Operator):
    bl_idname = "scene.save_op"
    bl_label = "Save scene"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        # build file name stuff
        # ...
        projectPath = "E:\\Dropbox\\projects\\2017_masterproject\\"
        projectPath = os.path.join(projectPath,"02_production", "assets")

        location = bpy.context.scene.Locations
        type = bpy.context.scene.ObjectType
        asset = bpy.context.scene.AssetName

        package = location + type

        datePre = time.strftime("%y%m%d")
        filename = datePre + "_" + package + "_" + asset + ".blend"

        assetPath = os.path.join(projectPath, location, type, asset)

        if os.path.exists(assetPath) == False:
            os.makedirs(assetPath)
        filepath = os.path.join(assetPath, filename)

        print(filepath)
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
        checkForOldVersion(filepath, filename)
        return {'FINISHED'}

def checkForOldVersion(assetpath, assetfilename):
    f = []
    for (dirpath, dirnames, filepath) in os.walk(assetpath):
        f.extend(filepath)
        break
    print (f)

    for oldFile in f:
        oldFile = os.path.basename(oldFile)
        if oldFile.endswith(assetfilename[:6]):
            print ("endswith " + oldFile)
            os.rename(os.path.join(assetpath, oldFile),os.path.join(assetpath, "_old" , oldFile))


preview_collections = {}

def register():
    Scene.AssetName = StringProperty(name="assetName", default="")
    Scene.Locations = EnumProperty(items=(('pro',  "pro",  "pro"),
                                                    ('lea',  "lea",  "lea"),
                                                    ('hub', "hub", "hub"),
                                                    ('par',  "par",  "par"),
                                                    ('tre', "tre", "tre"),
                                                    ('rem', "rem", "rem"),
                                                    ('lia',  "lia",  "lia"),
                                                    ('cre', "cre", "cre"),
                                                    ('tst',  "tst",  "tst"),
                                                    ('cmn',  "cmn",  "cmn"),
                                                    ),
                                             name="locations",
                                             description="Import options categories", )
    Scene.ObjectType = EnumProperty(items=(('Int',  "interior Architecture",  "int"),
                                                    ('Ext', "exterior Architexture", "Environment Props exterior"),
                                                    ('Nat', "nature", "Natrure contains, trees, stones usw"),
                                                    ('Fur', "furniture", "furniture"),
                                                    ('Prp', "props", "props"),
                                                    ('Chr',  "character",  "character"),
                                                    ('Oth', "other", "other")
                                                    ),
                                             name="objectTypes",
                                             description="Import options categories", )

    Scene.my_previews_dir = StringProperty(
       name="Export Path",
       subtype='DIR_PATH',
       default=""
    )



    bpy.utils.register_module(__name__)
    bpy.utils.register_class(PopupSave)
    bpy.utils.register_class(SaveOperator)

    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()

    preview_collections["main"] = pcoll

    # has to be after the other classes were loaded
    bpy.types.Scene.my_list = prop.CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = prop.IntProperty(name = "Index for my_list", default = 0)

def unregister():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    bpy.utils.unregister_class(PopupSave)
    bpy.utils.unregister_class(SaveOperator)
    #del bpy.types.Scene.Locations
    #del bpy.types.Scene.AssetName
    #del bpy.types.Scene.ObjectType
    bpy.utils.unregister_module(__name__)


