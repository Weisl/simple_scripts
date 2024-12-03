import bpy
import gpu
import bpy_extras
from mathutils import Vector
from gpu.types import GPUShader
from gpu_extras.batch import batch_for_shader


class CameraLockGizmo:
    """Persistent Camera Lock Gizmo"""
    _handle = None
    _shader = None
    _gizmo_radius = 0.2  # Gizmo radius for click detection

    @staticmethod
    def is_camera_location_locked(camera):
        """Check if the camera's location is locked"""
        return any(camera.lock_location)

    @staticmethod
    def toggle_camera_lock(camera):
        """Toggle the camera's location lock state"""
        if camera:
            is_locked = CameraLockGizmo.is_camera_location_locked(camera)
            new_state = not is_locked
            camera.lock_location = (new_state, new_state, new_state)
            print(f"Camera lock state toggled to: {'Locked' if new_state else 'Unlocked'}")

    @staticmethod
    def draw_callback():
        """Draw the gizmo in the 3D viewport"""
        scene = bpy.context.scene
        camera = scene.camera

        if not camera:
            return

        is_locked = CameraLockGizmo.is_camera_location_locked(camera)

        # Define gizmo color based on lock state
        color_locked = (1.0, 0.0, 0.0, 1.0)  # Red for locked
        color_unlocked = (0.0, 1.0, 0.0, 1.0)  # Green for unlocked
        color = color_locked if is_locked else color_unlocked

        # Gizmo position (slightly above the camera)
        position = camera.matrix_world.translation + Vector((0, 0, 1))

        # Shader for drawing
        if CameraLockGizmo._shader is None:
            vertex_shader = """
            uniform mat4 ModelViewProjectionMatrix;
            in vec3 pos;
            void main()
            {
                gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0);
            }
            """
            fragment_shader = """
            uniform vec4 color;
            out vec4 FragColor;
            void main()
            {
                FragColor = color;
            }
            """
            CameraLockGizmo._shader = GPUShader(vertex_shader, fragment_shader)

        # Create batch for drawing
        batch = batch_for_shader(CameraLockGizmo._shader, 'POINTS', {"pos": [position]})

        # Bind shader and draw
        CameraLockGizmo._shader.bind()
        CameraLockGizmo._shader.uniform_float("color", color)
        batch.draw(CameraLockGizmo._shader)

    @staticmethod
    def handle_click(event, context):
        """Handle mouse click on the gizmo"""
        scene = context.scene
        camera = scene.camera

        if not camera or event.type != 'LEFTMOUSE' or event.value != 'PRESS':
            return

        # Gizmo position
        gizmo_position = camera.matrix_world.translation + Vector((0, 0, 1))

        # Convert 3D position to 2D screen space
        region = context.region
        rv3d = context.region_data
        if not rv3d:  # Ensure rv3d is valid
            return

        gizmo_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(region, rv3d, gizmo_position)

        if not gizmo_2d:
            return

        # Check if the click is within the gizmo radius
        mouse_x, mouse_y = event.mouse_region_x, event.mouse_region_y
        distance = ((mouse_x - gizmo_2d[0]) ** 2 + (mouse_y - gizmo_2d[1]) ** 2) ** 0.5
        if distance <= CameraLockGizmo._gizmo_radius * 100:  # Adjust for screen space
            CameraLockGizmo.toggle_camera_lock(camera)

    @staticmethod
    def add_draw_handler():
        """Add the draw handler for the gizmo"""
        if CameraLockGizmo._handle is None:
            CameraLockGizmo._handle = bpy.types.SpaceView3D.draw_handler_add(
                CameraLockGizmo.draw_callback, (), 'WINDOW', 'POST_VIEW'
            )

    @staticmethod
    def remove_draw_handler():
        """Remove the draw handler"""
        if CameraLockGizmo._handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(CameraLockGizmo._handle, 'WINDOW')
            CameraLockGizmo._handle = None


class CameraLockGizmoModalOperator(bpy.types.Operator):
    """Interactive Camera Lock Gizmo"""
    bl_idname = "view3d.camera_lock_gizmo"
    bl_label = "Camera Lock Gizmo"
    _running = False

    def modal(self, context, event):
        if event.type == 'ESC':
            CameraLockGizmo.remove_draw_handler()
            self._running = False
            return {'CANCELLED'}

        CameraLockGizmo.handle_click(event, context)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if not self._running:
            CameraLockGizmo.add_draw_handler()
            context.window_manager.modal_handler_add(self)
            self._running = True
            return {'RUNNING_MODAL'}
        else:
            CameraLockGizmo.remove_draw_handler()
            self._running = False
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(CameraLockGizmoModalOperator)


def unregister():
    CameraLockGizmo.remove_draw_handler()
    bpy.utils.unregister_class(CameraLockGizmoModalOperator)


if __name__ == "__main__":
    register()
    bpy.ops.view3d.camera_lock_gizmo('INVOKE_DEFAULT')
