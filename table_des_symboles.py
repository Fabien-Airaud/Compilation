class TableSymbole:
    def __init__(self) -> None:
        self.listeTypeFonction = []
    def afficher(self) -> None:
        for typeFonction in self.listeTypeFonction:
            print("Type: " + typeFonction[0] + ", Nom : " + typeFonction[1])
    def find(self, name) -> bool:
        for fonction in self.listeTypeFonction:
            if name == fonction[0]:
                return True
        return False
    def estBonType(self, name, type) -> bool:
        for fonction in self.listeTypeFonction:
            if name == fonction[0]:
                return True if type == fonction[1] else False
        return False