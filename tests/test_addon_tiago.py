import os
import sys
 
filesDir = "C:/Users/tiago/OneDrive/Documents/GitHub/Blender-addon-for-FEA/blender_fea"
 
initFile = "__init__.py"

if filesDir not in sys.path:
    sys.path.append(filesDir)
 
file = os.path.join(filesDir, initFile)
 
if 'DEBUG_MODE' not in sys.argv:
    sys.argv.append('DEBUG_MODE')
 
exec(compile(open(file).read(), initFile, 'exec'))
 
if 'DEBUG_MODE' in sys.argv:
    sys.argv.remove('DEBUG_MODE')