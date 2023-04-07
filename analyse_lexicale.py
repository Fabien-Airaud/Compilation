import sys
from sly import Lexer

class FloLexer(Lexer):
	# Noms des lexèmes (sauf les litéraux). En majuscule. Ordre non important
	tokens = { IDENTIFIANT, TYPE_ENTIER, TYPE_BOOLEEN, ENTIER, BOOLEAN, ECRIRE, LIRE, INFERIEUR_OU_EGAL, SUPERIEUR_OU_EGAL, INFERIEUR, SUPERIEUR, EGAL, PAS_EGAL,
	 ET, OU, NON, CONDITION_SI, CONDITION_SINON, CONDITION_SINON_SI, TANT_QUE, RETOURNER}

	#Les caractères litéraux sont des caractères uniques qui sont retournés tel quel quand rencontré par l'analyse lexicale. 
	#Les litéraux sont vérifiés en dernier, après toutes les autres règles définies par des expressions régulières.
	#Donc, si une règle commence par un de ces littérals (comme INFERIEUR_OU_EGAL), cette règle aura la priorité.
	literals = { '+','*','(',')', '-', '/', '%', ',', ';', '{', '}', '='}


	# chaines contenant les caractère à ignorer. Ici espace et tabulation
	ignore = ' \t'

	# Expressions régulières correspondant au différents Lexèmes par ordre de priorité

	# Comparaison :
	INFERIEUR_OU_EGAL = r"<="
	SUPERIEUR_OU_EGAL = r">="
	INFERIEUR = r"<"
	SUPERIEUR = r">"
	EGAL = r"=="
	PAS_EGAL = r"!="

	# Conditions et boucle:
	CONDITION_SINON_SI = r"sinon\ si" # Mis en n°1 car si on met si ou sinon devant, il detectera pas la condition 
	CONDITION_SINON = r"sinon" # Mis en n°2 car dans sinon il y a "si" donc il detectera pas si on l'aurais mis en n°3 
	CONDITION_SI = r"si"
	TANT_QUE = r"tantque"

	# Retour:
	RETOURNER = r"retourner" # Mis à cet emplacement là pour pas que le "et" enleve sa détection

	# Logique :
	ET = r"et"
	OU = r"ou"
	NON = r"non"

	# Type :
	# Ce regex permet de separer les variable et les types
	@_(r'\(?entier\ ')
	def TYPE_ENTIER(self, t):
		if(t.value[0] == '('):
			t.value = t.value[1:]
		t.value = t.value[:-1]
		return t

	@_(r'\(?booleen\ ')
	def TYPE_BOOLEEN(self, t):
		if(t.value[0] == '('):
			t.value = t.value[1:]
		t.value = t.value[:-1]
		return t

	@_(r'0|[1-9][0-9]*')
	def ENTIER(self, t):
		t.value = int(t.value)
		return t

	@_(r'Vrai|Faux')
	def BOOLEEN(self, t):
		if(str(t.value) == "Vrai"):
			t.value = int(1)
		else:
			t.value = int(0)
		return t

	# cas général
	IDENTIFIANT = r'[a-zA-Z][a-zA-Z0-9_]*' #en général, variable ou nom de fonction

	# cas spéciaux:
	IDENTIFIANT['ecrire'] = ECRIRE
	IDENTIFIANT['lire'] = LIRE
	
	#Syntaxe des commentaires à ignorer
	ignore_comment = r'\#.*'

	# Permet de conserver les numéros de ligne. Utile pour les messages d'erreurs
	@_(r'\n+')
	def ignore_newline(self, t):
		self.lineno += t.value.count('\n')

	# En cas d'erreur, indique où elle se trouve
	def error(self, t):
		print(f'Ligne{self.lineno}: caractère inattendu "{t.value[0]}"')
		self.index += 1

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
	else:
		with open(sys.argv[1],"r") as f:
			data = f.read()
			lexer = FloLexer()
			for tok in lexer.tokenize(data):
				print(tok)
