bl_info = {
    'name': 'Test Multifile Addon',
    'category': 'All',
    'version': (0, 0, 1),
    'blender': (3, 20, 0)
}
 
modulesNames = [
    'tools.utils',
    'tools.properties', 
    'tools.operators', 
    'UserPanel'
    ]
 
import sys
import importlib
 
modulesFullNames = {}
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
    
    
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        print("reload: {}".format(currentModuleFullName))
        # print("------> {}".format(sys.modules[currentModuleFullName]))
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                # print("register: {}".format(currentModuleName))
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":        
    register()