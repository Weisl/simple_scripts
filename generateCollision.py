import bpy

def duplicateObject(ob):
    me = ob.data # use current object's data
    me_copy = me.copy()
    me_copy.name = me.name + "_copy"

    new_ob = bpy.data.objects.new(ob.name + "_clone", me_copy)

    new_ob.matrix_world  = ob.matrix_world

    scene = bpy.context.scene
    scene.objects.link(new_ob)
    scene.update()

    new_ob.select = True
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.make_links_data(type='MODIFIERS')
    bpy.ops.object.make_links_data(type='MATERIAL')
    return new_ob


def applyMod(obj):
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    if obj is not None:
        for modi in obj.modifiers:
            try:
                midifiername = modi.name
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=midifiername)
            except (RuntimeError):
                obj.modifiers.remove(modi)

def main(self,context):
    allObjects = bpy.data.objects
    selectedObjects = bpy.context.selected_objects.copy()
    for obj in selectedObjects:
        parName = obj.parent.name
        collider = duplicateObject(obj)

        for mod in collider.modifiers:
            if mod.type == 'BEVEL' and self.my_bool == True:
                collider.modifiers.remove(mod)
            elif mod.type == 'SUBSURF' and self.my_bool2 == True:
                collider.modifiers.remove(mod)


        i = 1
        endNumeration = ('%02d' % i)
        newName = self.my_string + parName + "_" + endNumeration
        while (newName in allObjects):
            endNumeration = ('%02d' % i)
            newName = self.my_string + parName + "_" + endNumeration
            i = i + 1

        applyMod(collider)
        collider.name = newName
        collider.draw_type = 'WIRE'

        collider.select = True

        bpy.context.view_layer.objects.active = obj.parent
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    my_float = bpy.props.FloatProperty(name="InflateColission",  default= -0.5)
    my_bool = bpy.props.BoolProperty(name="Remove Bevel", default = True)
    my_bool2 = bpy.props.BoolProperty(name="Remove Subdivision Surface", default = True)
    my_string = bpy.props.StringProperty(name="Colission Prefix", default = "UCX_")


    @classmethod
    def poll(cls, context):
        if context.active_object is not None and context.active_object.parent is not None:
            return True
        else: # no object is active or object has no parent:
            return False

    def execute(self, context):
        main(self,context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
