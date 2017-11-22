import bpy
import os


# Use your own script name here:
filename = "toggleWireframes.py"

import os
pathMiniScripts = "Documents/GitHub/mp_mini_script_utils/"
documents = os.path.join(os.path.join(os.environ['USERPROFILE']), pathMiniScripts)
filepath = os.path.join(documents, filename)

global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)


