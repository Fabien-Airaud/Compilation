"""
Affiche une chaine de caractère avec une certaine identation
"""
def afficher(s,indent=0):
	print(" "*indent+s)

# Entier, booleen et Variable
class Entier:
	""" Cette classe contient un entier """
	def __init__(self, valeur) -> None:
		"""
		Constructeur de la classe Entier

		Parametre :
		- op (str): L'opérateur de calcul
		- exp1: La première expression où on fera le calcul
		- exp2: La Deuxième expression où on fera le calcul
		"""

		self.valeur = valeur

	def afficher(self,indent=0) -> None:
		afficher("[Entier:"+str(self.valeur)+"]",indent)

class Booleen:
	""" Cette classe contient un booleen """
	def __init__(self, booleen) -> None:
		"""
		Constructeur de la classe Booleen

		Parametre :
		- booleen: booleen contenant vrai ou faux
		"""

		self.booleen = booleen

	def afficher(self, indent=0):
		temp = '0'
		if (self.booleen == "Vrai"):
			temp = '1'
		afficher("[Booleen:"+temp+']', indent)

class Variable:
	""" Cette classe contient le nom d'une variable"""
	def __init__(self, variable: str):
		"""
		Constructeur de la classe Booleen

		Parametre :
		- variable (str): booleen contenant vrai ou faux
		"""

		self.variable = variable

	def afficher(self, indent=0):
		afficher("[Variable:"+self.variable+"]", indent)

# Operation arithmétique et logique
class Operation:
	""" Cette classe permet de faire une opération arithmétique """
	def __init__(self, op: str, exp1, exp2) -> None:
		"""
		Constructeur de la classe Operation

		Parametre :
		- op (str): L'opérateur de calcul
		- exp1: La première expression où on fera le calcul
		- exp2: La Deuxième expression où on fera le calcul
		"""

		self.exp1 = exp1
		self.op = op
		self.exp2 = exp2

	def afficher(self, indent=0) -> None:
		afficher("<operation '" + self.op + "'>",indent)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</operation '" + self.op + "'>",indent)

class Comparaison:
	""" Cette classe compare deux expression """
	def __init__(self, comparateur: str, exp1, exp2) -> None:
		"""
		Constructeur de la classe Comparaison

		Parametre :
		- comparateur (str): Le comparateur qui permettra de faire la comparaison
		- exp1: La première expression où on fera la comparaison
		- exp2: La Deuxième expression où on fera la comparaison
		"""

		self.exp1 = exp1
		self.comparateur = comparateur
		self.exp2 = exp2

	def afficher(self, indent=0) -> None:
		afficher("<comparaison '" + self.comparateur + "'>", indent)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</comparaison '" + self.comparateur + "'>", indent)

class OperationLogique:
	""" Cette classe fait l'opération logique entre deux expression booléennes """
	def __init__(self, opLogique: str, booleen1, booleen2=None) -> None:		
		"""
		Constructeur de la classe OpérateurLogique

		Parametre :
		- opLogique (str): Opérateur logique 'non', 'ou', 'et'
		- booleen1: Première expression booléenne à comparer
		- booleen2: DeuxièmeExpression booléenne à comparer
		"""

		self.opLogique = opLogique
		self.booleen1 = booleen1
		self.booleen2 = booleen2

	def afficher(self, indent=0) -> None:
		afficher("<OperationLogique '" + self.opLogique + "'>", indent)
		self.booleen1.afficher(indent + 1)
		if (self.booleen2 != None):
			self.booleen2.afficher(indent + 1)
		afficher("</OperationLogique '" + self.opLogique + "'>", indent)

# Liste d'arguments des fonctions
class ListeArguments:
	""" Celle classe contient une liste d'argument """
	def __init__(self) -> None:
		""" Constructeur de la classe listArguments """

		self.arguments = []

	def afficher(self, indent=0) -> None:
		for i, argument in enumerate(self.arguments):
			afficher("<argument " + str(i) + '>', indent)
			argument.afficher(indent + 1)
			afficher("</argument " + str(i) + '>', indent)

# Instructions
# Instructions pour les fonctions
class RetourFonction:
	""" Cette classe contient le retour de fonction """
	def __init__(self, expr) -> None:
		"""
		Constructeur de la classe Boucle

		Parametre :
		- expr: expression de retour de fonction
		"""

		self.expr = expr

	def afficher(self, indent=0) -> None:
		afficher("<retourFonction>", indent)
		self.expr.afficher(indent + 1)
		afficher("</retourFonction>", indent)

class AppelFonction:
	""" Celle classe permet d'appeler une fonction avec ou sans arguments """
	def __init__(self, nomFonction: str, listArguments: ListeArguments | None = None) -> None:
		"""
		Constructeur de la classe AppelFonction

		Parametre :
		- nomFonction (str): nom de la fonction à appeler
		- listArguments: La liste des arguments
		"""
				
		self.nomFonction = nomFonction
		self.listArguments = listArguments

	def afficher(self, indent=0) -> None:
		afficher("<fonction: "+self.nomFonction+">", indent)
		if (self.listArguments != None):
			self.listArguments.afficher(indent + 1)
		afficher("</fonction: " + self.nomFonction + '>', indent)


# Instructions pour déclarer et affecter une variable
class Declaration:
	""" Cette classe permet de déclarer une variable """
	def __init__(self, type: str, nomVariable: str) -> None:
		"""
		Constructeur de la classe Declaration

		Parametre :
		- type (str): type de la variable
		- nomVariable (str): nom de la variable
		"""

		self.type = type
		self.nomVariable = nomVariable

	def afficher(self, indent=0):
		afficher("<declaration>", indent)
		afficher(self.type + " " + self.nomVariable, indent + 1)
		afficher("</declaration>", indent)

class Affectation:
	""" Cette classe permet d'affecter à une variable, une valeur """
	def __init__(self, nomVariable: str, expr) -> None:
		"""
		Constructeur de la classe Affectation

		Parametre :
		- nomVariable (str): nom de la variable
		- expr: expression à attribuer dans la variable
		"""

		self.nomVariable = nomVariable
		self.expr = expr

	def afficher(self, indent=0) -> None:
		afficher("<affectation " + self.nomVariable +  ">", indent)
		self.expr.afficher(indent + 1)
		afficher("</affectation " + self.nomVariable +  ">", indent)

class DeclarationAffectation:
	""" Cette classe permet de déclarer et affecter à une variable, une valeur """
	def __init__(self, type: str, nomVariable: str, expr) -> None:
		"""
		Constructeur de la classe DeclarationAffectation

		Parametre :
		- type (str): type de la variable
		- nomVariable (str): nom de la variable
		- expr: expression à attribuer dans la variable
		"""

		self.type = type
		self.nomVariable = nomVariable
		self.expr = expr

	def afficher(self, indent=0) -> None:
		afficher("<declaration>", indent)
		afficher(self.type + " " + self.nomVariable, indent + 1)
		afficher("</declaration>", indent)
		afficher("<affectation " + self.nomVariable +  ">", indent)
		self.expr.afficher(indent + 1)
		afficher("</affectation " + self.nomVariable +  ">", indent)


# Instruction Lire
class Lire:
	""" Cette classe pourra lire une valeur """
	def __init__(self) -> None:
		""" Constructeur de la classe Lire"""

		pass

	def afficher(self, indent=0) -> None:
		afficher("<lire>", indent)
		afficher("</lire>", indent)

# Instruction Ecrire
class Ecrire:
	""" Cette classe permet d'ecrire sur la sortie standard une expression """
	def __init__(self, exp) -> None:
		"""
		Constructeur de la classe Ecrire

		Parametre :
		- exp : expression à écrire
		"""
				
		self.exp = exp

	def afficher(self, indent=0) -> None:
		afficher("<ecrire>",indent)
		self.exp.afficher(indent+1)
		afficher("</ecrire>",indent)

class ListeInstructions:
	""" Cette classe contient toutes les instructions dans les fonctions, conditions et en dehors des fonctions """
	def __init__(self) -> None:
		""" Constructeur de la classe ListeInstructions	"""

		self.instructions = []

	def afficher(self,indent=0) -> None:
		afficher("<listeInstructions>",indent)
		for instruction in self.instructions:
			instruction.afficher(indent+1)
		afficher("</listeInstructions>",indent)

# Condition
class Conditionnelle:
	""" Celle classe contient les conditions 'si', 'sinon' et 'sinon si' """
	def __init__(self) -> None:
		""" Constructeur de la classe Conditionnelle """

		self.exprs = []
		self.listeInstructions = []

	def afficher(self, indent=0) -> None:
		n = len(self.exprs)

		afficher("<si>", indent)
		self.exprs[0].afficher(indent + 1)
		self.listeInstructions[0].afficher(indent + 1)
		afficher("</si>", indent)

		for arg in zip(self.exprs, self.listeInstructions, range(n)):
			if arg[2] > 0:
				afficher("<sinon si>", indent)
				arg[0].afficher(indent + 1)
				arg[1].afficher(indent + 1)
				afficher("</sinon si>", indent)

		if (n != len(self.listeInstructions)):
			afficher("<sinon>", indent)
			self.listeInstructions[n].afficher(indent + 1)
			afficher("</sinon>", indent)

# Boucle
class Boucle:
	""" Cette classe contient les boucles 'while' """
	def __init__(self, expr, listeInstruction: ListeInstructions) -> None:
		"""
		Constructeur de la classe Boucle

		Parametre :
		- expr: expression 
		- listInstuctions (ListeInstructions): La liste des instructions à exécuter
		"""
		self.expr = expr
		self.listeInstruction = listeInstruction

	def afficher(self, indent=0) -> None:
		afficher("<tant_que>", indent)
		self.expr.afficher(indent + 1)
		self.listeInstruction.afficher(indent + 1)
		afficher("</tant_que>", indent)

# Declaration de fonctions
class DeclarationListeArguments:
	""" Cette classe défini une liste d'argument avec chacun un type et un nom"""
	def __init__(self) -> None:
		""" Constructeur de la classe DeclarationListeArguments """

		self.listeArguments = []

	def afficher(self, indent=0) -> None:
		afficher("<listeArguments>", indent)
		for typeArgument in self.listeArguments:
			typeArgument.afficher(indent + 1)
		afficher("</listeArguments>", indent)

class DefinitionFonction:
	""" Cette classe défini chaque fonctions créer dans le programme """
	def __init__(self, type: str, nom: str, listeInstructions: ListeInstructions, listeArguments: ListeArguments = None) -> None:
		"""
		Constructeur de la classe Definition Fonction

		Parametre :
		- type (str): Le type de la fonction
		- nom (str): Le nom de la fonction
		- listeInstructions (ListeInstructions): La liste d'instructions dans la fonction
		- listeArguments (ListeArguments): Li liste d'arguments utilisé dans la fonction
		"""

		self.type = type
		self.nom = nom
		self.listeInstructions = listeInstructions
		self.listeArguments = listeArguments

	def afficher(self, indent=0) -> None:
		afficher("<fonction: type: " + self.type + ", nom: " + self.nom + ">", indent)
		if (self.listeArguments != None):
			self.listeArguments.afficher(indent + 1)
		self.listeInstructions.afficher(indent + 1)
		afficher("</fonction: type: " + self.type + ", nom: " + self.nom + ">", indent)

class ListeFonctions:
	""" Cette classe contient toutes les fonctions du programme """
	def __init__(self) -> None:
		""" Constructeur de la classe ListeFonctions """

		self.fonctions = []

	def afficher(self, indent=0) -> None:
		afficher("<listeFonctions>", indent)
		for fonction in self.fonctions:
			fonction.afficher(indent + 1)
		afficher("</listeFonctions>", indent)

# Programmme à exécuter au départ
class Programme:
	""" Classe d'initiation du Programme"""
	def __init__(self, listeInstructions: ListeInstructions, listeFonctions: ListeFonctions | None = None) -> None:
		"""
		Constructeur de la classe Programme

		Paramètre:
		- listeInstructions (ListeInstructions): Liste d'instructions
		- listeFonctions (ListeFonctions): Liste de fonctions
		"""

		self.listeInstructions = listeInstructions
		self.listeFonctions = listeFonctions

	def afficher(self,indent=0) -> None:
		afficher("<programme>",indent)
		if (self.listeFonctions != None):
			self.listeFonctions.afficher(indent+1)
		self.listeInstructions.afficher(indent+1)
		afficher("</programme>",indent)