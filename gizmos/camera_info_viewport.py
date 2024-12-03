import bpy
import blf


class CameraInfoOverlay:
    """Persistent Camera Info Overlay"""
    _handle = None

    @staticmethod
    def is_camera_location_locked(camera):
        """Check if the camera's location is locked"""
        return any(camera.lock_location)

    @staticmethod
    def draw_overlay(context):
        """Draw camera info overlay in the camera view"""
        region = context.region
        space_data = context.space_data

        # Ensure we are in the camera view
        if space_data.region_3d.view_perspective != 'CAMERA':
            return

        scene = context.scene
        camera = scene.camera

        if not camera:
            return

        # Lock/unlock state
        is_locked = CameraInfoOverlay.is_camera_location_locked(camera)
        lock_icon = "🔒 Locked" if is_locked else "🔓 Unlocked"

        # Camera resolution
        resolution_x = scene.render.resolution_x
        resolution_y = scene.render.resolution_y

        # Focus distance and f-stop
        focus_distance = getattr(camera.data.dof, "focus_distance", None)
        focus_active = getattr(camera.data.dof, "use_dof", False)
        f_stop = getattr(camera.data.dof, "aperture_fstop", None)

        # Safeguard None values
        focus_distance_text = f"{focus_distance:.2f}m" if focus_distance else "N/A"
        f_stop_text = f"{f_stop:.2f}" if f_stop else "N/A"

        # Prepare text lines
        text_lines = [
            lock_icon,
            f"Resolution: {resolution_x} x {resolution_y}",
            f"Focus Distance: {focus_distance_text} (Active: {'Yes' if focus_active else 'No'})",
            f"F-Stop: {f_stop_text}",
        ]

        # Font setup
        font_id = 0
        blf.size(font_id, 16)
        blf.color(font_id, 1.0, 1.0, 1.0, 1.0)

        # Calculate starting position for bottom-centered text
        margin = 10
        total_height = len(text_lines) * 20
        center_x = region.width // 2
        start_y = margin + total_height

        # Draw each line
        for line in text_lines:
            text_width, _ = blf.dimensions(font_id, line)
            blf.position(font_id, center_x - text_width // 2, start_y, 0)
            blf.draw(font_id, line)
            start_y -= 20  # Move up for the next line

    @staticmethod
    def add_draw_handler():
        """Add the draw handler for the overlay"""
        if CameraInfoOverlay._handle is None:
            CameraInfoOverlay._handle = bpy.types.SpaceView3D.draw_handler_add(
                CameraInfoOverlay.draw_overlay, (bpy.context,), 'WINDOW', 'POST_PIXEL'
            )

    @staticmethod
    def remove_draw_handler():
        """Remove the draw handler"""
        if CameraInfoOverlay._handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(CameraInfoOverlay._handle, 'WINDOW')
            CameraInfoOverlay._handle = None


class CameraInfoOverlayOperator(bpy.types.Operator):
    """Camera Info Overlay Operator"""
    bl_idname = "view3d.camera_info_overlay"
    bl_label = "Camera Info Overlay"
    _running = False

    def execute(self, context):
        if not CameraInfoOverlay._handle:
            CameraInfoOverlay.add_draw_handler()
            self.report({'INFO'}, "Camera Info Overlay Enabled")
        else:
            CameraInfoOverlay.remove_draw_handler()
            self.report({'INFO'}, "Camera Info Overlay Disabled")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CameraInfoOverlayOperator)


def unregister():
    CameraInfoOverlay.remove_draw_handler()
    bpy.utils.unregister_class(CameraInfoOverlayOperator)


if __name__ == "__main__":
    register()
    bpy.ops.view3d.camera_info_overlay()
