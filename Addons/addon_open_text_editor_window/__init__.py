bl_info = {
    "name": "Error Text Window Demo",
    "blender": (3, 0, 0),
    "category": "Development",
    "author": "Your Name",
    "version": (1, 0, 5),
    "description": "Opens a new compact Blender window with a Text Editor displaying an error message.",
}

import bpy

class ShowErrorTextOperator(bpy.types.Operator):
    """Opens a new Blender window with a minimal Text Editor displaying an error message"""
    bl_idname = "wm.show_error_text"
    bl_label = "Show Error in New Window"

    message: bpy.props.StringProperty(name="Message", default="An error occurred!")

    def execute(self, context):
        # Create or get the text block
        text_name = "Error_Log"
        if text_name in bpy.data.texts:
            text_block = bpy.data.texts[text_name]
            text_block.clear()  # Clear existing text
        else:
            text_block = bpy.data.texts.new(name=text_name)

        # Write the error message
        text_block.write(f"--- ERROR MESSAGE ---\n{self.message}\n\nDetails:\n(Add more details here...)")

        # Open a new Blender window
        bpy.ops.wm.window_new()

        # Get the newly opened window
        new_window = bpy.context.window_manager.windows[-1]
        new_screen = new_window.screen

        # Change the entire layout to a minimal workspace
        for area in new_screen.areas:
            area.type = 'TEXT_EDITOR'  # Convert the entire area into a Text Editor
            area.spaces.active.text = text_block  # Assign the error message text block
            break  # Stop after modifying the first available area

        # Hide unnecessary panels where possible
        for area in new_screen.areas:
            if area.type == 'TEXT_EDITOR':
                for region in area.regions:
                    if region.type in {'UI', 'TOOLS', 'HEADER'}:
                        region.tag_redraw()  # Attempt to hide UI elements
                break  # Stop after modifying the first found Text Editor

        return {'FINISHED'}

class ERRORTEXT_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the N-Panel"""
    bl_label = "Error Text"
    bl_idname = "ERRORTEXT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Error Text"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.show_error_text", text="Open Error Log").message = "Something went wrong!"

# Register / Unregister
classes = [ShowErrorTextOperator, ERRORTEXT_PT_Panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
