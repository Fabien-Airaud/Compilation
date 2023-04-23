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

class Declaration:
	def __init__(self, type, nomVariable):
		self.type = type
		self.nomVariable = nomVariable
	def afficher(self, indent=0):
		afficher("<declaration>", indent)
		afficher(self.type + " " + self.nomVariable, indent + 1)
		afficher("</declaration>", indent)

class Affectation:
	def __init__(self, nomVariable, expr) -> None:
		self.nomVariable = nomVariable
		self.expr = expr
	def afficher(self, indent=0) -> None:
		afficher("<affectation>", indent)
		afficher(self.nomVariable, indent + 1)
		self.expr.afficher(indent + 1)
		afficher("</affectation>", indent)

class DeclarationAffectation:
	def __init__(self, type, nomVariable, expr) -> None:
		self.type = type
		self.nomVariable = nomVariable
		self.expr = expr
	def afficher(self, indent=0) -> None:
		afficher("<affectation>", indent)
		afficher(self.nomVariable, indent + 1)
		self.expr.afficher(indent + 1)
		afficher("</affectation>", indent)
		afficher("<declaration>", indent)
		afficher(self.type + " " + self.nomVariable, indent + 1)
		afficher("</declaration>", indent)

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

class Conditionnelle:
	def __init__(self) -> None:
		self.exprs = []
		self.listeInstructions = []
	def afficher(self, indent=0):
		n = len(self.exprs)
		
		if (n != len(self.listeInstructions)):
			for i in range(n - 1, -1, -1):
				afficher("<condition>", indent)
				self.exprs[i].afficher(indent + 1)
				self.listeInstructions[i + 1].afficher(indent + 1)
				afficher("</condition>", indent)

			afficher("<sinon>", indent)
			self.listeInstructions[0].afficher(indent + 1)
			afficher("</sinon>", indent)
		else:
			for i in range(n - 1, -1, -1):
				afficher("<condition>", indent)
				self.exprs[i].afficher(indent + 1)
				self.listeInstructions[i].afficher(indent + 1)
				afficher("</condition>", indent)


class Boucle:
	def __init__(self, expr, listeInstruction) -> None:
		self.expr = expr
		self.listeInstruction = listeInstruction
	def afficher(self, indent=0) -> None:
		afficher("<tant_que>", indent)
		self.listeInstruction.afficher(indent + 1)
		afficher("</tant_que>", indent)

class RetourFonction:
	def __init__(self, expr) -> None:
		self.expr = expr
	def afficher(self, indent=0) -> None:
		afficher("<retourFonction>", indent)
		self.expr.afficher(indent + 1)
		afficher("</retourFonction>", indent)