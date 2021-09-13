import bpy
import json

for obj in bpy.context.selected_objects:
    if obj.get("custom_meta"):
        str = obj["custom_meta"].replace("'", '"')
        obj["custom_meta"] = str

        dict = json.loads(obj["custom_meta"])

    if dict:

        # get the filepath from property
        filepath = dict["filepath"]

        print(filepath)

        if filepath.find('whiteboxing_temp') == -1:
            print('entered')
            filepath = filepath.replace('objects/', 'objects/whiteboxing_temp/')
        dict['filepath'] = filepath
        print(filepath)

        obj["custom_meta"] = json.dumps(dict)