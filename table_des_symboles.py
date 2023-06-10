class TableSymbole:
    def __init__(self) -> None:
        self.listeTypeFonction = []
    def afficher(self) -> None:
        for typeFonction in self.listeTypeFonction:
            print("Type: " + typeFonction[0] + ", Nom : " + typeFonction[1])