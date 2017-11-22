import bpy
import csv
import os

selection = bpy.context.selected_objects.copy()
assets = {}

blendFile = bpy.path.abspath("//")
fn = "exampleCsv2.csv"

fn = os.path.join(blendFile, fn)

print ("fn " + fn)

csv = open(fn, 'w')

columnTitleRow = "asset, status\n"
csv.write(columnTitleRow)

for assetName in assets.keys():
    print (assetName + "," + assets[assetName] + "\n")
    row = assetName + "," + assets[assetName] + "\n"
    csv.write(row)

# dictionary
for obj in selection:
    # only count objects without parent
    if obj.parent == None:
        assets['Name'] = obj.name
        assets['Status'] = "Blockout"

for asset in assets:
    print(assets[asset])