import bpy
import blf
import bpy_extras


class CameraLockGizmoButtons:
    """Persistent Camera Lock Gizmo with Buttons"""
    _handle = None
    _button_lock = None
    _button_unlock = None

    @staticmethod
    def is_camera_location_locked(camera):
        """Check if the camera's location is locked"""
        return any(camera.lock_location)

    @staticmethod
    def draw_buttons(context):
        """Draw lock and unlock buttons in the camera view"""
        region = context.region
        space_data = context.space_data

        # Ensure we are in the camera view
        if space_data.region_3d.view_perspective != 'CAMERA':
            return

        scene = context.scene
        camera = scene.camera

        if not camera:
            return

        # Button text and colors
        lock_icon = "🔒 Lock"
        unlock_icon = "🔓 Unlock"
        color_button = (0.3, 0.3, 0.3, 1.0)  # Button background color
        color_text = (1.0, 1.0, 1.0, 1.0)   # Text color

        # Button positions and sizes
        region_width = region.width
        region_height = region.height
        button_width = 100
        button_height = 30

        lock_button_x = region_width // 2 - 110
        unlock_button_x = region_width // 2 + 10
        button_y = region_height // 2 - 50

        # Store button bounds for click detection
        CameraLockGizmoButtons._button_lock = (lock_button_x, button_y, button_width, button_height)
        CameraLockGizmoButtons._button_unlock = (unlock_button_x, button_y, button_width, button_height)

        # Draw Lock Button
        font_id = 0  # Default font
        blf.color(font_id, *color_text)
        blf.position(font_id, lock_button_x + 10, button_y + 5, 0)
        blf.size(font_id, 16)
        blf.draw(font_id, lock_icon)

        # Draw Unlock Button
        blf.position(font_id, unlock_button_x + 10, button_y + 5, 0)
        blf.draw(font_id, unlock_icon)

    @staticmethod
    def handle_click(context, event):
        """Handle mouse click events"""
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            mouse_x, mouse_y = event.mouse_region_x, event.mouse_region_y

            # Check if the click is within the lock button
            if CameraLockGizmoButtons._button_lock:
                x, y, w, h = CameraLockGizmoButtons._button_lock
                if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                    # Lock the camera
                    if context.scene.camera:
                        context.scene.camera.lock_location = (True, True, True)
                    return {'RUNNING_MODAL'}

            # Check if the click is within the unlock button
            if CameraLockGizmoButtons._button_unlock:
                x, y, w, h = CameraLockGizmoButtons._button_unlock
                if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                    # Unlock the camera
                    if context.scene.camera:
                        context.scene.camera.lock_location = (False, False, False)
                    return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    @staticmethod
    def add_draw_handler():
        """Add the draw handler for the gizmo"""
        if CameraLockGizmoButtons._handle is None:
            CameraLockGizmoButtons._handle = bpy.types.SpaceView3D.draw_handler_add(
                CameraLockGizmoButtons.draw_buttons, (bpy.context,), 'WINDOW', 'POST_PIXEL'
            )

    @staticmethod
    def remove_draw_handler():
        """Remove the draw handler"""
        if CameraLockGizmoButtons._handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(CameraLockGizmoButtons._handle, 'WINDOW')
            CameraLockGizmoButtons._handle = None


class GizmoButtonsModalOperator(bpy.types.Operator):
    """Interactive Lock/Unlock Buttons"""
    bl_idname = "view3d.camera_lock_buttons"
    bl_label = "Camera Lock Buttons"
    _running = False

    def modal(self, context, event):
        if event.type == 'ESC':
            CameraLockGizmoButtons.remove_draw_handler()
            self._running = False
            return {'CANCELLED'}

        # Pass click events to the handler
        return CameraLockGizmoButtons.handle_click(context, event)

    def invoke(self, context, event):
        if not self._running:
            CameraLockGizmoButtons.add_draw_handler()
            context.window_manager.modal_handler_add(self)
            self._running = True
            return {'RUNNING_MODAL'}
        else:
            CameraLockGizmoButtons.remove_draw_handler()
            self._running = False
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(GizmoButtonsModalOperator)


def unregister():
    CameraLockGizmoButtons.remove_draw_handler()
    bpy.utils.unregister_class(GizmoButtonsModalOperator)


if __name__ == "__main__":
    register()
    bpy.ops.view3d.camera_lock_buttons('INVOKE_DEFAULT')
