import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
	# On récupère la liste des lexèmes de l'analyse lexicale
	tokens = FloLexer.tokens
	debugfile = 'parser.out'

	# Règles gramaticales et actions associées

	# Init
	@_('listeInstructions')
	def prog(self, p):
		return arbre_abstrait.Programme(p[0])
	
	@_('listeFonctions listeInstructions')
	def prog(self, p):
		return arbre_abstrait.Programme(p[1], p[0])

	# liste Fonctions
	@_('definitionFonction')
	def listeFonctions(self, p):
		listeDeFonctions = arbre_abstrait.ListeFonctions()
		listeDeFonctions.fonctions.append(p[0])
		return listeDeFonctions 

	@_('listeFonctions definitionFonction ')
	def listeFonctions(self, p):
		p[0].fonctions.append(p[1])
		return p[0]

	@_('TYPE_ENTIER IDENTIFIANT "(" listeTypeArg ")" "{" listeInstructions "}"',
    'TYPE_BOOLEEN IDENTIFIANT "(" listeTypeArg ")" "{" listeInstructions "}"')
	def definitionFonction(self, p):
		return arbre_abstrait.DefinitionFonction(p[0], p[1], p[6], p[3])
	
	@_('TYPE_ENTIER IDENTIFIANT "(" ")" "{" listeInstructions "}"',
    'TYPE_BOOLEEN IDENTIFIANT "(" ")" "{" listeInstructions "}"')
	def definitionFonction(self, p):
		return arbre_abstrait.DefinitionFonction(p[0], p[1], p[5])
	
	@_('typeArg "," listeTypeArg')
	def listeTypeArg(self, p):
		p[2].listeArguments.insert(0, p[0])
		return p[2]
		
	@_('typeArg')
	def listeTypeArg(self, p):
		listeTypeArguments = arbre_abstrait.DeclarationListeArguments()
		listeTypeArguments.listeArguments.append(p[0])
		return listeTypeArguments 

	@_('TYPE_ENTIER IDENTIFIANT',
    'TYPE_BOOLEEN IDENTIFIANT')
	def typeArg(self, p):
		return arbre_abstrait.Declaration(p[0], p[1])
	
	# Instructions
	@_('instruction')
	def listeInstructions(self, p):
		l = arbre_abstrait.ListeInstructions()
		l.instructions.append(p[0])
		return l

	@_('instruction listeInstructions')
	def listeInstructions(self, p):
		p[1].instructions.insert(0, p[0])
		return p[1]
		
	@_('ecrire')
	def instruction(self, p):
		return p[0]
	
	@_('declaration')
	def instruction(self, p):
		return p.declaration
	
	@_('affectation')
	def instruction(self, p):
		return p.affectation
	
	@_('declarationAffectation')
	def instruction(self, p):
		return p.declarationAffectation
	
	@_('conditionnel')
	def instruction(self, p):
		return p.conditionnel
	
	@_('boucle')
	def instruction(self, p):
		return p.boucle
	
	@_('retourFonction')
	def instruction(self, p):
		return p.retourFonction
	
	@_('fonction')
	def instruction(self, p):
		return p.fonction
	
	# Ecrire			
	@_('ECRIRE "(" expr ")" ";"')
	def ecrire(self, p):
		return arbre_abstrait.Ecrire(p.expr) #p.expr = p[2]
	
	# Declaration + Affectation
	@_('TYPE_ENTIER IDENTIFIANT ";"',
    'TYPE_BOOLEEN IDENTIFIANT ";"')
	def declaration(self, p):
		return arbre_abstrait.Declaration(p[0], p[1])
	
	@_('IDENTIFIANT "=" expr ";"')
	def affectation(self, p):
		return arbre_abstrait.Affectation(p[0], p[2])
	
	@_('TYPE_ENTIER IDENTIFIANT "=" expr ";"',
    'TYPE_BOOLEEN IDENTIFIANT "=" expr ";"')
	def declarationAffectation(self, p):
		return arbre_abstrait.DeclarationAffectation(p[0], p[1], p[3])
	
	# Conditions
	@_('CONDITION_SI "(" expr ")" "{" listeInstructions "}"')
	def conditionnel(self, p):
		condition = arbre_abstrait.Conditionnelle()
		condition.exprs.append(p[2])
		condition.listeInstructions.append(p[5])
		return condition
	
	@_('CONDITION_SI "(" expr ")" "{" listeInstructions "}" conditionList')
	def conditionnel(self, p):
		p[7].exprs.insert(0, p[2])
		p[7].listeInstructions.insert(0, p[5])
		return p[7]
	
	@_('CONDITION_SINON CONDITION_SI "(" expr ")" "{" listeInstructions "}"')
	def conditionList(self, p):
		condition = arbre_abstrait.Conditionnelle()
		condition.exprs.append(p[3])
		condition.listeInstructions.append(p[6])
		return condition

	@_('CONDITION_SINON CONDITION_SI "(" expr ")" "{" listeInstructions "}" conditionList')
	def conditionList(self, p):
		p[8].exprs.insert(0, p[3])
		p[8].listeInstructions.insert(0, p[6])
		return p[8]
	
	@_('CONDITION_SINON "{" listeInstructions "}"')
	def conditionList(self, p):
		condition = arbre_abstrait.Conditionnelle()
		condition.listeInstructions.append(p[2])
		return condition
	
	# Boucle
	@_('TANT_QUE "(" expr ")" "{" listeInstructions "}"')
	def boucle(self, p):
		return arbre_abstrait.Boucle(p[2], p[5])

	# Retour Fonction
	@_('RETOURNER expr ";"')
	def retourFonction(self, p):
		return arbre_abstrait.RetourFonction(p[1])
	
	#  Appel Fonction sans retour pris en compte
	@_('IDENTIFIANT "(" ")" ";"')
	def fonction(self, p):
		return arbre_abstrait.AppelFonction(p[0])
	
	@_('IDENTIFIANT "(" arglist ")" ";"')
	def fonction(self, p):
		return arbre_abstrait.AppelFonction(p[0], p[2])

	@_('expr')
	def arglist(self, p):
		l = arbre_abstrait.ListeArguments()
		l.arguments.append(p[0])
		return l

	@_('expr "," arglist')
	def arglist(self, p):
		p[2].arguments.insert(0, p[0])
		return p[2]
	
	# Expression
	@_('disjonction')
	def expr(self, p):
		return p.disjonction

	@_('conjonction ET conjonction')
	def disjonction(self, p):
		return arbre_abstrait.OperationLogique(p[1], p[0], p[2])
	
	@_('conjonction')
	def disjonction(self, p):
		return p.conjonction
	
	@_('negation OU negation')
	def conjonction(self, p):
		return arbre_abstrait.OperationLogique(p[1], p[0], p[2])
	
	@_('negation')
	def conjonction(self, p):
		return p.negation
	
	@_('NON booleen')
	def negation(self, p):
		return arbre_abstrait.OperationLogique(p[0], p.booleen)
	
	@_('booleen')
	def negation(self, p):
		return p.booleen
	


	# Booleen
	@_('VRAI')
	def booleen(self, p):
		return arbre_abstrait.Booleen(p[0])
	
	@_('FAUX')
	def booleen(self, p):
		return arbre_abstrait.Booleen(p[0])
	
	@_('somme')
	def booleen(self, p):
		return p.somme
	
	@_('produit')
	def somme(self, p):
		return p.produit

	@_('comparaison')
	def booleen(self, p):
		return p.comparaison
	
	# Comparaison
	@_('somme SUPERIEUR somme',
	'somme INFERIEUR somme',
	'somme SUPERIEUR_OU_EGAL somme',
	'somme INFERIEUR_OU_EGAL somme',
	'somme EGAL somme',
	'somme DIFFERENT somme')
	def comparaison(self, p):
		return arbre_abstrait.Comparaison(p[1], p[0], p[2])

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
		return arbre_abstrait.Operation("-", arbre_abstrait.Entier(0), p[1])

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
	
	# Appel Fonction avec valeur
	@_('IDENTIFIANT "(" arglist ")"')
	def facteur(self, p):
		return arbre_abstrait.AppelFonction(p[0],p[2])
	
	@_('IDENTIFIANT "(" ")"')
	def facteur(self, p):
		return arbre_abstrait.AppelFonction(p[0])
	
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
