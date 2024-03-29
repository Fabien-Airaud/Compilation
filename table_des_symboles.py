class TableSymbole:
    def __init__(self) -> None:
        self.listeTypeFonction = []
        self.listeVariable = []
    def afficher(self) -> None:
        for typeFonction in self.listeTypeFonction:
            print("Type: " + typeFonction[0] + ", Nom : " + typeFonction[1] + ", mémoire : " + str(typeFonction[2]) + ", arguments : " + str(typeFonction[3]))
    def find(self, name) -> bool:
        for fonction in self.listeTypeFonction:
            if name == fonction[0]:
                return True
        return False
    def getFonction(self, name) -> list:
        for fonction in self.listeTypeFonction:
            if fonction[0] == name:
                return fonction
        return None
    def getVariable(self, name) -> list:
        for variable in self.listeVariable:
            if variable[0] == name:
                return variable
        return None
    def estBonType(self, name, type) -> bool:
        for fonction in self.listeTypeFonction:
            if name == fonction[0]:
                return True if type == fonction[1] else False
        return False
    def estBonTypeVariable(self, name, type) -> bool:
        for variable in self.listeVariable:
            if name == variable[0]:
                return True if type == variable[1] else False
        return False