"""
Affiche une chaine de caractère avec une certaine identation
"""
def afficher(s,indent=0):
	print(" "*indent+s)
	
class Programme:
	def __init__(self,listeInstructions):
		self.listeInstructions = listeInstructions
	def afficher(self,indent=0):
		afficher("<programme>",indent)
		self.listeInstructions.afficher(indent+1)
		afficher("</programme>",indent)

class ListeInstructions:
	def __init__(self):
		self.instructions = []
	def afficher(self,indent=0):
		afficher("<listeInstructions>",indent)
		for instruction in self.instructions:
			instruction.afficher(indent+1)
		afficher("</listeInstructions>",indent)

class Lire:
	def __init__(self):
		pass
	def afficher(self, indent=0):
		afficher("<lire>", indent)
		afficher("</lire>", indent)

class Ecrire:
	def __init__(self,exp):
		self.exp = exp
	def afficher(self,indent=0):
		afficher("<ecrire>",indent)
		self.exp.afficher(indent+1)
		afficher("</ecrire>",indent)
		
class Operation:
	def __init__(self,op,exp1,exp2):
		self.exp1 = exp1
		self.op = op
		self.exp2 = exp2
	def afficher(self,indent=0):
		afficher("<operation>",indent)
		afficher(self.op,indent+1)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</operation>",indent)

class Comparaison:
	def __init__(self, comparateur, exp1, exp2):
		self.exp1 = exp1
		self.comparateur = comparateur 
		self.exp2 = exp2
	def afficher(self, indent=0):
		afficher("<comparaison>", indent)
		afficher(self.comparateur, indent + 1)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</comparaison>", indent)

class Entier:
	def __init__(self,valeur):
		self.valeur = valeur
	def afficher(self,indent=0):
		afficher("[Entier:"+str(self.valeur)+"]",indent)

class Booleen:
	def __init__(self, booleen):
		self.booleen = booleen
	def afficher(self, indent=0):
		temp = '0'
		if (self.booleen == "Vrai"):
			temp = '1'
		afficher("[Booleen:"+temp+']', indent)

class Variable:
	def __init__(self, variable):
		self.variable = variable
	def afficher(self, indent=0):
		afficher("[Variable:"+self.variable+"]", indent)

class OperateurLogique:
	def __init__(self, opLogique, booleen1, booleen2=None):
		self.opLogique = opLogique
		self.booleen1 = booleen1
		self.booleen2 = booleen2
	def afficher(self, indent=0):
		afficher("<operateurLogique>", indent)
		afficher(self.opLogique, indent + 1)
		self.booleen1.afficher(indent + 1)
		if (self.booleen2 != None):
			self.booleen2.afficher(indent + 1)
		afficher("</operateurLogique>", indent)

class Fonction:
	def __init__(self, nomFonction, listArguments):
		self.nomFonction = nomFonction
		self.listArguments = listArguments
	def afficher(self, indent=0):
		afficher("<fonction: "+self.nomFonction+">", indent)
		if (self.listArguments != None):
			self.listArguments.afficher(indent + 1)
		afficher("</fonction: " + self.nomFonction + '>', indent)

class listArguments:
	def __init__(self):
		self.arguments = []
	def afficher(self, indent=0):
		i = len(self.arguments) - 1
		for argument in self.arguments:
			afficher("<argument " + str(i) + '>', indent)
			argument.afficher(indent + 2)
			afficher("</argument " + str(i) + '>', indent)
			i -= 1