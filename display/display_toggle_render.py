"""Toggle only render view"""
import bpy

if bpy.context.space_data.show_only_render == True:
    bpy.context.space_data.show_only_render = False
if bpy.context.space_data.show_only_render == False:
    bpy.context.space_data.show_only_render = True
