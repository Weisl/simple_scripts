import bpy
import os

for img in bpy.data.images:
    print(img.filepath)

for img in bpy.data.images:
    filename = os.path.basename(img.filepath)
    oldPath = img.filepath.replace(filename, "")
    newPath = ""
    img.filepath = img.filepath.replace(oldPath, newPath)
