import bpy

class SocketCreate(bpy.types.Operator):
    bl_idname = "master.socket_create"
    bl_label = "Create Socket"
    bl_description = "CreateSocket"
    bl_options = {'REGISTER', 'UNDO'}

    my_socketSize = bpy.props.FloatProperty(name="Socket Size",  default= 15)


    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects == None:
            return False
        if bpy.context.scene.objects.active == None:
            return False
        return True

    def execute(self, context):
        parent = bpy.context.scene.objects.active
        selection = bpy.context.selected_objects[:].copy()
        socketList = main(self, parent,selection)
        return {"FINISHED"}


def main(self, parent, objects):
    socketList = []
    for obj in objects:
        print ("OBJ u Parent: " + str(obj) + str(parent))
        if obj != parent:
            socketName = "SOCKET_" + obj.name
            if socketName not in bpy.data.objects:
                if (obj.type == 'MESH' or obj.type == 'EMPTY'):
                    socket = bpy.data.objects.new("empty", None)
                    bpy.context.scene.objects.link(socket)
                else:
                    socket = bpy.data[socketName]


                socket.parent = parent
                socket.matrix_world = obj.matrix_world

                socket.empty_draw_size = self.my_socketSize
                socket.empty_draw_type = 'SPHERE'

                socket.name = socketName
                socketList.append(socket)

    return socketList