"""Change image ending of path """
import bpy

for img in bpy.data.images:
    if img.filepath.endswith("_R.png"):
        print(img.filepath)
        try:
            img.filepath = img.filepath[0:-6] + "_M.png"
            print("sucess " + img.filepath)
        except:
            print("Err " + img.filepath)
    else:
        print("didn't enter" + img.filepath)
