import bpy

# =========================================================================
# PROPERTIES

class FEAProperties(bpy.types.PropertyGroup):
    
    filepath : bpy.props.StringProperty(name= "FEA filepath")
    data : dict()



# =========================================================================
# REGISTER PROPERTIES

classes = [FEAProperties]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    