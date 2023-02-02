import bpy


class UserPanel(bpy.types.Panel):
    """Creates a new panel 'FEA' in 3D View"""
    bl_label = "Blender FEA"
    bl_idname = "BLENDERFEA_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FEA"
    # bl_context = "object"

    def draw(self, context):
        # grab layout        
        layout = self.layout
        # add label to inform user about this tool
        layout.label(text='Hello there')
        
        # grab scene
        scene = context.scene
        # grab our custom properties from the scene
        fea_props = scene.fea_properties
        
        # --------------------------------
        # show user interface
        # ask for filepath
        layout.prop(fea_props, "filepath")
        # 
        layout.operator("blender_fea.load_static_mesh")
        layout.operator("blender_fea.load_simulation")
        
        

def register():
    from tools.properties import FEAProperties
    
    # register class
    bpy.utils.register_class(UserPanel)
    # register properties
    bpy.types.Scene.fea_properties = bpy.props.PointerProperty(type=FEAProperties)


def unregister():
    bpy.utils.unregister_class(UserPanel)


