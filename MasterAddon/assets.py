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

