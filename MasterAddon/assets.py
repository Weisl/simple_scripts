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
