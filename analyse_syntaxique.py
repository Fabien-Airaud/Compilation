import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
	# On récupère la liste des lexèmes de l'analyse lexicale
	tokens = FloLexer.tokens
	debugfile = 'parser.out'

	# Règles gramaticales et actions associées

	@_('listeInstructions')
	def prog(self, p):
		return arbre_abstrait.Programme(p[0])

	@_('instruction')
	def listeInstructions(self, p):
		l = arbre_abstrait.ListeInstructions()
		l.instructions.append(p[0])
		return l

	@_('instruction listeInstructions')
	def listeInstructions(self, p):
		p[1].instructions.append(p[0])
		return p[1]
		
	@_('ecrire')
	def instruction(self, p):
		return p[0]
			
	@_('ECRIRE "(" expr ")" ";"')
	def ecrire(self, p):
		return arbre_abstrait.Ecrire(p.expr) #p.expr = p[2]

	@_('negation')
	def expr(self, p):
		return p.negation
	
	@_('NON disjonction')
	def negation(self, p):
		return arbre_abstrait.OperateurLogique(p[0], p.disjonction)
	
	@_('disjonction')
	def negation(self, p):
		return p.disjonction
	
	@_('conjonction ET conjonction')
	def disjonction(self, p):
		return arbre_abstrait.OperateurLogique(p[1], p[0], p[2])
	
	@_('conjonction')
	def disjonction(self, p):
		return p.conjonction
	
	@_('booleen OU booleen')
	def conjonction(self, p):
		return arbre_abstrait.OperateurLogique(p[1], p[0], p[2])
	
	@_('booleen')
	def conjonction(self, p):
		return p.booleen

	@_('VRAI')
	def booleen(self, p):
		return arbre_abstrait.Booleen(p[0])
	
	@_('FAUX')
	def booleen(self, p):
		return arbre_abstrait.Booleen(p[0])
	
	@_('somme')
	def booleen(self, p):
		return p.somme

	@_('comparaison')
	def booleen(self, p):
		return p.comparaison
	
	@_('somme SUPERIEUR somme',
	'somme INFERIEUR somme',
	'somme SUPERIEUR_OU_EGAL somme',
	'somme INFERIEUR_OU_EGAL somme',
	'somme EGAL somme',
	'somme DIFFERENT somme')
	def comparaison(self, p):
		return arbre_abstrait.Comparaison(p[1], p[0], p[2])

	@_('produit')
	def somme(self, p):
		return p.produit
	
	@_('somme "+" produit',
	'somme "-" produit')
	def somme(self, p):
		return arbre_abstrait.Operation(p[1], p[0], p[2])
	
	@_('facteur')
	def produit(self, p):
		return p.facteur
	
	@_('produit "*" facteur',
	'produit "/" facteur',
	'produit "%" facteur')
	def produit(self, p):
		return arbre_abstrait.Operation(p[1], p[0], p[2])
	
	@_('"-" facteur')
	def produit(self, p):
		return arbre_abstrait.Operation("*", arbre_abstrait.Entier(-1), p[1])

	@_('variable')
	def facteur(self, p):
		return p.variable

	@_('ENTIER')
	def facteur(self, p):
		return arbre_abstrait.Entier(p.ENTIER) #p.ENTIER = p[0]
		
	@_('LIRE "(" ")" ')
	def facteur(self, p):
		return arbre_abstrait.Lire()

	@_('"(" expr ")"')
	def facteur(self, p):
		return p.expr #ou p[1]
	
	@_('IDENTIFIANT "(" arglist ")"')
	def facteur(self, p):
		return arbre_abstrait.Fonction(p[0],p[2])
	
	@_('IDENTIFIANT "(" ")"')
	def facteur(self, p):
		return arbre_abstrait.Fonction(p[0], None)
	
	@_('expr')
	def arglist(self, p):
		l = arbre_abstrait.listArguments()
		l.arguments.append(p[0])
		return l

	@_('expr "," arglist')
	def arglist(self, p):
		p[2].arguments.append(p[0])
		return p[2]

	@_('IDENTIFIANT')
	def variable(self, p):
		return arbre_abstrait.Variable(p.IDENTIFIANT)


if __name__ == '__main__':
	lexer = FloLexer()
	parser = FloParser()
	if len(sys.argv) < 2:
		print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
	else:
		with open(sys.argv[1],"r") as f:
			data = f.read()
			try:
			    arbre = parser.parse(lexer.tokenize(data))
			    arbre.afficher()
			except EOFError:
			    exit()
