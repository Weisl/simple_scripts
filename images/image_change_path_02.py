'''
import bpy
import os

# Use your own script name here:
filepath = "C:/Users/weisl/Documents/GitHub/mp_mini_script_utils/imagePath_02.py"
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)


'''

import bpy
import sys
from os.path import isfile

for img in bpy.data.images:
    filepath = img.filepath
    if img.filepath.startswith("//images\\2k"):
        filepath = filepath.replace("//images\\2k", "//images\\render")
        try:
            img.filepath = filepath
            print("sucess " + img.filepath)
        except:
            print("Err " + img.filepath)
    else:
        print("didn't enter" + img.filepath)

print("#################################")
for img in bpy.data.images:
    if img.filepath.endswith("_B.png"):
        print(img.filepath)
        try:
            img.filepath = img.filepath[0:-6] + "_C.png"
            print("sucess " + img.filepath)
        except:
            print("Err " + img.filepath)
    else:
        print("didn't enter" + img.filepath)

    if img.filepath.endswith("_R.png"):
        print(img.filepath)
        try:
            img.filepath = img.filepath[0:-6] + "_M.png"
            print("sucess " + img.filepath)
        except:
            print("Err " + img.filepath)
    else:
        print("didn't enter" + img.filepath)
