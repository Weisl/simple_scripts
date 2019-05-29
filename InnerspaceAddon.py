bl_info = {
    "name": "InnerspaceUtls",
    "author": "Matthias Patscheider",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy
import bmesh

class InnerspacePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Innerspace panel"
    bl_idname = "Innerspace"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("innerspace.modifier_sharp")
        row = layout.row()
        row.operator("innerspace.unparent_scale")
        row = layout.row()
        row.operator("innerspace.modifier_not_sharp")
        row = layout.row()
        row.operator("object.sharp_to_bevel")
        row = layout.row()
        row.operator("innerspace.convert_sharp_bevel")
        row = layout.row()
        row.operator("innerspace.select_non_uniform_scale")
        row = layout.row()
        row.operator("innerspace.add_lightmap_uv")
        row = layout.row()
        row.operator("innerspace.switch_main_uv")
        row = layout.row()
        row.operator("innerspace.switch_lightmap_uv")
        row = layout.row()
        row.operator("innerspace.delete_uvs")
        row = layout.row()
        row.operator("innerspace.set_seam_by_normal")


class SharpToBevel(bpy.types.Operator):
    "Converts Sharp Edges to Bevels"
    bl_idname = "object.sharp_to_bevel"
    bl_label = "sharp_to_bevel"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects.copy()

        for obj in selected:
            bpy.context.view_layer.objects.active = obj

            ob = bpy.context.object
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            edgeBevelWeight = bm.edges.layers.bevel_weight.verify()
            sharpEdge = bm.edges.layers.bevel_weight.verify()

            for edge in bm.edges:
                if edge.select:
                    if edge.smooth == False:
                        edge.smooth == True
                        edge[edgeBevelWeight] = 1.0

            bmesh.update_edit_mesh(me, False, False)

        bpy.ops.mesh.mark_sharp(clear=True)
        return {'FINISHED'}

class SelectObjWithModifiers(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "innerspace.modifier_sharp"
    bl_label = "modifier_sharp"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        """select all objects that use modifier (except Triangulate and Weighted Normals)"""
        import bpy

        selected = bpy.context.selected_objects.copy()
        new_selection = []

        for obj in selected:
            bpy.context.view_layer.objects.active = obj
            modifiers = obj.modifiers

            if len(obj.modifiers) > 0:
                for mod in obj.modifiers:
                    if mod.type not in {'TRIANGULATE', 'WEIGHTED_NORMAL'}:
                        new_selection.append(obj)

        bpy.ops.object.select_all(action='DESELECT')

        for ob in new_selection:
            ob.select_set(True)
        return {'FINISHED'}

class SelectWeightedNotSharp(bpy.types.Operator):
    """select all objects that use modifier (except Triangulate and Weighted Normals)"""
    bl_idname = "innerspace.modifier_not_sharp"
    bl_label = "modifier_not_sharp"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects.copy()
        new_selection = []

        for obj in selected:
            bpy.context.view_layer.objects.active = obj
            modifiers = obj.modifiers

            if len(obj.modifiers) > 0:
                for mod in obj.modifiers:
                    if mod.type == 'WEIGHTED_NORMAL' and mod.keep_sharp == False:
                        new_selection.append(obj)

        bpy.ops.object.select_all(action='DESELECT')

        for ob in new_selection:
            ob.select_set(True)

        return {'FINISHED'}

class BevelWeight(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "innerspace.convert_sharp_bevel"
    bl_label = "clear Bevel"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        "Sets all bevels weights to 0"
        selected = bpy.context.selected_objects.copy()

        for obj in selected:
            bpy.context.view_layer.objects.active = obj

            ob = bpy.context.object
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            cl = bm.edges.layers.bevel_weight.verify()

            for edge in bm.edges:
                if edge.select:
                    edge[cl] = 0.0

            bmesh.update_edit_mesh(me, False, False)

        return {'FINISHED'}

class SelectNonUniform(bpy.types.Operator):
    """select all objects that use modifier (except Triangulate and Weighted Normals)"""
    bl_idname = "innerspace.select_non_uniform_scale"
    bl_label = "select_non_uniform_scale"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects.copy()
        new_selection = []

        for obj in selected:
            bpy.context.view_layer.objects.active = obj

            if obj.scale is ((1.0, 1.0, 1.0)):
                new_selection.append(obj)

        bpy.ops.object.select_all(action='DESELECT')

        for ob in new_selection:
            ob.select_set(True)

        return {'FINISHED'}

class AddUVMap(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "innerspace.add_lightmap_uv"
    bl_label = "add_lightmap_uv"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects.copy()
        instanciatedObjects = []

        for obj in selected:
            # print(instanciatedObjects)
            if obj.type == 'MESH':
                if obj.data not in instanciatedObjects:
                    instanciatedObjects.append(obj.data)
                    bpy.context.view_layer.objects.active = obj
                    uvActive = obj.data.uv_layers.active
                    texSetList = list(obj.data.uv_layers)
                    idx_set = len(texSetList)

                    if "lightmap" not in obj.data.uv_layers:
                        bpy.ops.mesh.uv_texture_add()
                        bpy.context.object.data.uv_layers.active_index = idx_set
                        bpy.context.object.data.uv_layers[idx_set].name = "lightmap"

        #        else:
        return {'FINISHED'}

class SwitchToMainUV(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "innerspace.switch_main_uv"
    bl_label = "switch_main_uv"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects.copy()
        activeUvSet = "map1"
        #activeUvSet = "lightmap"

        for obj in selected:
            # print(instanciatedObjects)
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                uvActive = obj.data.uv_layers.active
                idx_set = obj.data.uv_layers.find(activeUvSet)
                bpy.context.object.data.uv_layers.active_index = idx_set
                bpy.context.object.data.uv_layers[idx_set].active_render = True

        return {'FINISHED'}

class SwitchToLightmapUV(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "innerpace.switch_lightmap_uv"
    bl_label = "Switch_lightmap_uv"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects.copy()
        #activeUvSet = "map1"
        activeUvSet = "lightmap"

        for obj in selected:
            # print(instanciatedObjects)
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                uvActive = obj.data.uv_layers.active
                idx_set = obj.data.uv_layers.find(activeUvSet)
                bpy.context.object.data.uv_layers.active_index = idx_set
                bpy.context.object.data.uv_layers[idx_set].active_render = True

        return {'FINISHED'}

class DeleteNonActiveUVs(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "innerpace.delete_uvs"
    bl_label = "delete_uvs"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects.copy()

        for obj in selected:

            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                uvActive = obj.data.uv_layers.active
                texSetList = list(obj.data.uv_layers)

                for tex in texSetList:
                    if tex != uvActive:
                        try:
                            obj.data.uv_layers.remove(tex)
                            print ("Deleted %s on object %s" % (str(tex), obj.name))

                        except Exception:
                            print ("couldn't delete textuteset %s on object %s" % (str(tex), obj.name))
                    else:
                        print ("LOL")

        return {'FINISHED'}

class UnparentApplyScale(bpy.types.Operator):
    """UnparentApplyScale"""
    bl_idname = "innerspace.unparent_scale"
    bl_label = "unparent_scale"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class SeamNormal(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "innerspace.set_seam_by_normal"
    bl_label = "innerspace.set_seam_by_normal"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.mesh.select_similar(type='NORMAL', threshold=0.1001)
        bpy.ops.mesh.select_more()
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_seam(clear=False)
        return {'FINISHED'}



def register():
    bpy.utils.register_class(InnerspacePanel)
    bpy.utils.register_class(SharpToBevel)
    bpy.utils.register_class(SelectObjWithModifiers)
    bpy.utils.register_class(SelectWeightedNotSharp)
    bpy.utils.register_class(BevelWeight)
    bpy.utils.register_class(SelectNonUniform)
    bpy.utils.register_class(AddUVMap)
    bpy.utils.register_class(SwitchToMainUV)
    bpy.utils.register_class(SwitchToLightmapUV)
    bpy.utils.register_class(DeleteNonActiveUVs)
    bpy.utils.register_class(UnparentApplyScale)
    bpy.utils.register_class(SeamNormal)


def unregister():
    bpy.utils.unregister_class(InnerspacePanel)
    bpy.utils.unregister_class(SharpToBevel)
    bpy.utils.unregister_class(SelectObjWithModifiers)
    bpy.utils.unregister_class(SelectWeightedNotSharp)
    bpy.utils.unregister_class(BevelWeight)
    bpy.utils.unregister_class(SelectNonUniform)
    bpy.utils.unregister_class(AddUVMap)
    bpy.utils.unregister_class(SwitchToMainUV)
    bpy.utils.unregister_class(SwitchToLightmapUV)
    bpy.utils.unregister_class(DeleteNonActiveUVs)
    bpy.utils.unregister_class(UnparentApplyScale)
    bpy.utils.unregister_class(SeamNormal)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
