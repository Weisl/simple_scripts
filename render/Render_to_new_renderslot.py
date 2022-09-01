'''Automatically render to a new render slot. Change used_renderslots to define how many render slots should be used '''

import bpy
from bpy.app.handlers import persistent

used_renderslots = 7

@persistent
def PostRender(self):
    bpy.data.images['Render Result'].render_slots.active_index += 1
    bpy.data.images['Render Result'].render_slots.active_index %= used_renderslots


bpy.app.handlers.render_complete.append(PostRender)
