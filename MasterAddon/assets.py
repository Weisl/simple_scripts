class colliderEnum:
    items = (('UBX', "UBX", "Boxes are created with the Box objects type in Max or with the Cube polygonal primitive in Maya. You cannot move the vertices around or deform it in any way to make it something other than a rectangular prism, or else it will not work."),
               ('UCP', "UCP", "Capsules are created with the Capsule object type. The capsule does not need to have many segments (8 is a good number) at all because it is converted into a true capsule for collision. Like boxes, you should not move the individual vertices around."),
               ('USP', "USP", "Spheres are created with the Sphere object type. The sphere does not need to have many segments (8 is a good number) at all because it is converted into a true sphere for collision. Like boxes, you should not move the individual vertices around."),
               ('UCX', "UCX", "Convex objects can be any completely closed convex 3D shape. For example, a box can also be a convex object. The diagram below illustrates what is "),
               )

    @staticmethod
    def getList():
        enumList = list()
        for ent in colliderEnum.items:
            enumList.append(ent[0])

        return enumList

    @staticmethod
    def getTuple():
        return tuple(colliderEnum.getList())

class AssetName:

    assetType = {
        "SM": 1,
        "SK": 2,
    }
    assetLocation = {
        "pro": 1,
        "lea": 2,
        "hub": 4,
        "par": 8,
        "tre": 16,
        "rem": 32,
        "lia": 64,
        "cre": 128,
        "cmn": 256,
        "tst": 512,
    }

    assetCategory = {
        "Int": 1,
        "Ext": 2,
        "Nat": 3,
        "Fur": 4,
        "Prp": 5,
        "Chr": 6,
        "Oth": 7,
    }

    def __init__(self, name):
        self.name = name

    def getAssetType(self):
        assetName = self.name
        if isNameStructureValid(assetName):
            obPrefix = assetName[:2]
            if obPrefix in AssetName.assetType:
                type = obPrefix
                return type
            else:
                return False

    def getAssetLocation(self):
        assetName = self.name
        if isNameStructureValid(assetName):
            obPrefix = assetName[3:6]
            if obPrefix in AssetName.assetLocation:
                location = obPrefix
                return location
            else:
                return False

    def getAssetCategory(self):
        assetName = self.name
        if isNameStructureValid(assetName):
            obPrefix = assetName[6:9]
            if obPrefix in AssetName.assetCategory:
                category = obPrefix
                return category
            else:
                return False

    def isNameStructureValid(self):
        assetName = self.name
        prog = re.compile(r"^[A-Za-z]{2}_[A-Za-z]{6}_[A-Za-z0-9]+(_[A-Za-z0-9]+)?")
        match = prog.match(assetName)
        if match:
            return True
        else:
            return False

    def masterExportPath(self):
        assetName = self.name
        print ("Asset Name MasterExportPath " + assetName)
        AssetName.assetLocation = getAssetLocation(assetName)
        AssetName.assetCategory = getAssetCategory(assetName)

        if isNameStructureValid(assetName) and AssetName.assetLocation != False and AssetName.assetCategory != False:
            if bpy.data.is_saved == True:

                basedir = assetPath

                if AssetName.assetLocation != False and AssetName.assetCategory != False:

                    finalPath = os.path.join(basedir, AssetName.assetLocation, "final", AssetName.assetCategory, "")
                    print (finalPath)
                    # check for dir "final"
                    if not os.path.exists(finalPath):
                        print(os.makedirs(finalPath))

                    return finalPath

        else:  # isNameStructureValid() == False and AssetName.assetLocation == False and AssetName.assetCategory == False
            return False

    def getObjectCategory(self):
        assetName = self.name
        objectCategory = ""
        if re.search("^SM_[A-Za-z]{6}_", assetName):
            print("entered Regex")
            objectCategory = assetName[6:9]
            print(objectCategory)
        else:
            print(assetName + " doesn't fit naming scheme")
            objectCategory = assetName + " doesn't fit naming scheme"
        return


class Asset:
    def __init__(self, type, name):
        self.name = name
        self.type = type

    def getType(self):
        return self.type

    def getDictionary(self):
        dic = {"name" : self.name, "type" : self.type}
        return dic

class StaticAsset(Asset):
    def __init__(self, name, offset = 0):
        super().__init__("static",name )
        self.offset = offset

    def getType(self):
        return super().getType()

    def getDictionary(self):
        return super().getDictionary()

class SocketAsset(Asset):
    def __init__(self, name, offset = 0):
        super().__init__("socket",name )
        self.offset = offset

    def getType(self):
        return super().getType()

    def getDictionary(self):
        return super().getDictionary()


class ColliderAsset(Asset):
    def __init__(self, name, offset = 0):
        super().__init__("collider",name )
        self.offset = offset

    def getType(self):
        return super().getType()

    def getDictionary(self):
        return super().getDictionary()

