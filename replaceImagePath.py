import bpy
import os

for img in bpy.data.images:
    print (img.filepath)

for img in bpy.data.images:
    filename = os.path.basename(img.filepath)
    oldPath = img.filepath.replace(filename, "")
    newPath = "E:\\Dropbox\\projects\\2017_veniceProject\\020_Production\\assets\\cathedral\\blender\\textures\\render\\"
    img.filepath = img.filepath.replace(oldPath, newPath)