import bpy

# =========================================================================
# OPERATORS

class LoadStaticMesh(bpy.types.Operator):
    bl_label = "Load static mesh"
    bl_idname = "blender_fea.load_static_mesh"
    
    def execute(self, context):   
        # import required methods
        from .utils import load_data, create_new_object_from_data
        
        # grab props from context (within scene)
        fea_props = context.scene.fea_properties
        
        # --------------------------------
        # Start algorithm
        
        # load mesh
        data = load_data(fea_props.filepath)
        fea_props.data = data
        
        # build mesh
        new_object = create_new_object_from_data("Heart", data)
        return {'FINISHED'}


class LoadSimulation(bpy.types.Operator):
    bl_label = "Load Simulation"
    bl_idname = "blender_fea.load_simulation"
    
    def execute(self, context):   
        # import required methods
        from .utils import load_data, create_new_object_from_data
        from .utils import add_keyframes_from_sim
        
        # grab props from context (within scene)
        fea_props = context.scene.fea_properties
        
        # --------------------------------
        # Start algorithm
        
        # load mesh
        data = load_data(fea_props.filepath)
        fea_props.data = data
        # build mesh
        new_object = create_new_object_from_data("Heart", data)
        scene_obj = context.scene.objects["Heart"]
        keyframes = add_keyframes_from_sim(scene_obj, data)
        
        
        return {'FINISHED'}

# =========================================================================
# REGISTER OPERATORS

classes = [LoadStaticMesh, LoadSimulation]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    