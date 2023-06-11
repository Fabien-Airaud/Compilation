import sys
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser
import arbre_abstrait
from table_des_symboles import TableSymbole

num_etiquette_courante = -1 #Permet de donner des noms différents à toutes les étiquettes (en les appelant e0, e1,e2,...)

afficher_table = False
afficher_nasm = False
tableSymbole = TableSymbole() 
"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""
def printifm(*args,**kwargs):
    if afficher_nasm:
        print(*args,**kwargs)

"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""
def printift(*args,**kwargs):
    if afficher_table:
        print(*args,**kwargs)

"""
Fonction locale, permet d'afficher un commentaire dans le code nasm.
"""
def nasm_comment(comment):
    if comment != "":
        printifm("\t\t ; "+comment)#le point virgule indique le début d'un commentaire en nasm. Les tabulations sont là pour faire jolie.
    else:
        printifm("")
"""
Affiche une instruction nasm sur une ligne
Par convention, les derniers opérandes sont nuls si l'opération a moins de 3 arguments.
"""
def nasm_instruction(opcode, op1="", op2="", op3="", comment=""):
    if op2 == "":
        printifm("\t"+opcode+"\t"+op1+"\t\t",end="")
    elif op3 =="":
        printifm("\t"+opcode+"\t"+op1+",\t"+op2+"\t",end="")
    else:
        printifm("\t"+opcode+"\t"+op1+",\t"+op2+",\t"+op3,end="")
    nasm_comment(comment)


"""
Retourne le nom d'une nouvelle étiquette
"""
def nasm_nouvelle_etiquette():
    global num_etiquette_courante
    num_etiquette_courante+=1
    return "e"+str(num_etiquette_courante)

"""
Affiche le code nasm correspondant à tout un programme
"""
def gen_programme(programme):
    printifm('%include\t"io.asm"')
    printifm('section\t.bss')
    printifm('sinput:	resb	255	;reserve a 255 byte space in memory for the users input string')
    printifm('v$a:	resd	1')
    printifm('section\t.text')
    printifm('global _start')
    if programme.listeFonctions != None:
        gen_def_fonction(programme.listeFonctions)

    printifm('_start:')
    gen_listeInstructions(programme.listeInstructions)
    nasm_instruction("mov", "eax", "1", "", "1 est le code de SYS_EXIT")
    nasm_instruction("int", "0x80", "", "", "exit")

def get_Arguments(arguments) -> list:
    args = []
    for argument in arguments:
        args.append(argument.type)
    return args

def write_def_fonction(fonction):
    fonctions = fonction.listeFonctions
    if (fonctions != None):
        for defFonction in fonctions.fonctions:
            arguments = []
            if defFonction.listeArguments != None:
                arguments = get_Arguments(defFonction.listeArguments.listeArguments)
            tableSymbole.listeTypeFonction.append([defFonction.nom, defFonction.type, len(arguments) * 4, arguments])

def gen_def_fonction(fonctions):
    for fonction in fonctions.fonctions:
        printifm('_' + fonction.nom + ':')

        count = 0
        for instruction in fonction.listeInstructions.instructions:
            if type(instruction) != arbre_abstrait.RetourFonction:
                gen_instruction(instruction)
            else:
                exprRetour = gen_retourFonction(instruction)
                if tableSymbole.getFonction(fonction.nom)[1] != exprRetour:
                    raise TypeError("Mauvais type de renvoi")
                count += 1
        
        if count == 0:
            raise ValueError("Pas de retourner dans la fonction")


"""
Affiche le code nasm correspondant à une suite d'instructions
"""
def gen_listeInstructions(listeInstructions):
    for instruction in listeInstructions.instructions:
        gen_instruction(instruction)

"""
Affiche le code nasm correspondant à une instruction
"""
def gen_instruction(instruction):
    if type(instruction) == arbre_abstrait.Ecrire:
        gen_ecrire(instruction)
    elif type(instruction) == arbre_abstrait.Conditionnelle:
        gen_conditionnel(instruction)
    elif type(instruction) == arbre_abstrait.AppelFonction:
        gen_fonction(instruction, False)
    elif type(instruction) == arbre_abstrait.RetourFonction:
        raise TypeError("Retour pas au bon endroit")
    else:
        print("type instruction inconnu",type(instruction))
        exit(0)

"""
Affiche le code nasm correspondant au fait d'envoyer la valeur entière d'une expression sur la sortie standard
"""
def gen_ecrire(ecrire):
    gen_expression(ecrire.exp) #on calcule et empile la valeur d'expression
    nasm_instruction("pop", "eax", "", "", "") #charge l’adresse sinput sur eax
    nasm_instruction("call", "iprintLF", "", "", "") #on envoie la valeur d'eax sur la sortie standard

def gen_retourFonction(retour):
    gen_expression(retour.expr)
    nasm_instruction("pop", "eax", "", "", "On met dans eax l'expression de retour")
    nasm_instruction("ret", "", "", "", "On retourne la valeur de eax")

    if check_booleen(retour.expr):
        return "booleen"
    else:
        return "entier"

def check_Fonction(fonctionTableSymbole, fonction):
    argsFonction = []

    if (fonction.listArguments != None):
        argsFonction = fonction.listArguments.arguments
    tailleArgsFonction = len(argsFonction)
    if (tailleArgsFonction * 4 != fonctionTableSymbole[2]):
        raise AttributeError("Il manque des arguments ou il y a trop d'arguments")
    
    for i in range(tailleArgsFonction):
        typeArg = "booleen" if check_booleen(argsFonction[i]) else "entier"
        if typeArg != fonctionTableSymbole[3][i]:
            raise TypeError("Mauvais type")

def gen_fonction(fonction, estInstruction: bool):
    fonctionTableSymbole = tableSymbole.getFonction(fonction.nomFonction)    
    if fonctionTableSymbole == None:
        raise ValueError("Fonction non existante")
    check_Fonction(fonctionTableSymbole, fonction)

    nasm_instruction("call", "_" + fonction.nomFonction, "", "", "Appelle la fonction " + fonction.nomFonction)
    
    if estInstruction:
        nasm_instruction("push", "eax", "", "", "Ajoute la valeur de retour de fonction dans la pile")

"""
Affiche le code nasm pour calculer et empiler la valeur d'une expression
"""
def gen_expression(expression):
    if type(expression) == arbre_abstrait.Operation:
        gen_operation(expression) #on calcule et empile la valeur de l'opération
    elif type(expression) == arbre_abstrait.Entier:
        nasm_instruction("push", str(expression.valeur), "", "", "") ; #on met sur la pile la valeur entière
    elif type(expression) == arbre_abstrait.Lire:
        gen_lire()
    elif type(expression) == arbre_abstrait.Booleen:
        nasm_instruction("push", "1" if (str(expression.booleen) == "Vrai") else "0", "", "", "") ; #on met sur la pile la valeur booléenne
    elif type(expression) == arbre_abstrait.OperationLogique:
        gen_operationLogique(expression) #on calcule et empile la valeur de l'opération logique
    elif type(expression) == arbre_abstrait.Comparaison:
        gen_comparaison(expression) #on calcule et empile la valeur de la comparaison
    elif type(expression) == arbre_abstrait.AppelFonction:
        gen_fonction(expression, True)
    else:
        print("type d'expression inconnu",type(expression))
        exit(0)


"""
Affiche le code nasm pour calculer l'opération et la mettre en haut de la pile
"""
def gen_operation(operation):
    op = operation.op

    gen_expression(operation.exp1) #on calcule et empile la valeur de exp1
    gen_expression(operation.exp2) #on calcule et empile la valeur de exp2

    nasm_instruction("pop", "ebx", "", "", "dépile la seconde operande dans ebx")
    nasm_instruction("pop", "eax", "", "", "dépile la permière operande dans eax")

    code = {"+":"add","*":"imul","-":"sub","/":"idiv","%":"idiv"} #Un dictionnaire qui associe à chaque opérateur sa fonction nasm
    #Voir: https://www.bencode.net/blob/nasmcheatsheet.pdf
    if op in ['+', '-']:
        nasm_instruction(code[op], "eax", "ebx", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
    if op == '*':
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
    if op == '/':
        nasm_instruction("mov",  "edx" , "0", "", "initialise edx à 0");
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" +op+"ebx, met le résultat dans eax et le reste dans edx" )
    if op == '%':
        nasm_instruction("mov",  "edx" , "0", "", "initialise edx à 0");
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" +op+"ebx, met le résultat dans edx" )
        nasm_instruction("mov",  "eax" , "edx", "", "copie edx dans eax");
    nasm_instruction("push",  "eax" , "", "", "empile le résultat");

"""
Affiche le code nasm correspondant au fait de lire et enregistrer la valeur entière d'une expression sur l'entrée standard
"""
def gen_lire():
    nasm_instruction("mov", "eax", "sinput", "", "") #on dépile la valeur d'expression sur eax
    nasm_instruction("call", "readline", "", "", "attend une chaine de caractères sur l'entrée standard") #appelle la procédure readline de io.asm
    nasm_instruction("call", "atoi", "", "", "convertit la chaine en entier et la place dans eax") #appelle la procédure atoi de io.asm
    nasm_instruction("push", "eax", "", "", "empile l'entier")

"""
Affiche le code nasm pour calculer l'opération logique et la mettre en haut de la pile
"""
def gen_operationLogique(operation):
    opLog = operation.opLogique

    if not check_booleen(operation.booleen1):
        raise TypeError("Element pas de type booléen dans une opération logique")


    gen_expression(operation.booleen1) #on calcule et empile la valeur de booleen1
    if opLog != 'non':
        if not check_booleen(operation.booleen2):
            raise TypeError("Element pas de type booléen dans une opération logique")

        gen_expression(operation.booleen2) #on calcule et empile la valeur de booleen2
        nasm_instruction("pop", "ebx", "", "", "dépile la seconde operande dans ebx")

    nasm_instruction("pop", "eax", "", "", "dépile la permière operande dans eax")

    code = {"et":"and","ou":"or","non":"xor"} # Un dictionnaire qui associe à chaque opérateur sa fonction nasm
    if opLog in ['et','ou']:
        nasm_instruction(code[opLog], "eax", "ebx", "", "effectue l'opération eax" +opLog+"ebx et met le résultat dans eax" )
    if opLog == 'non':
        nasm_instruction(code[opLog], "eax", "1", "", "effectue l'opération eax" +opLog+"1 et met le résultat dans eax" )
    nasm_instruction("push",  "eax" , "", "", "empile le résultat");

def check_booleen(booleen):
    tB = type(booleen)
    if tB == arbre_abstrait.AppelFonction:
        return tableSymbole.estBonType(tB.nomFonction, "booleen")
    
    return (tB == arbre_abstrait.Booleen) or (tB == arbre_abstrait.OperationLogique) or (tB == arbre_abstrait.Comparaison)


"""
Affiche le code nasm pour calculer une comparaison et la mettre en haut de la pile
"""
def gen_comparaison(operation):
    expr1 = operation.exp1
    expr2 = operation.exp2
    opComp = operation.comparateur

    if not (check_entier(expr1) and check_entier(expr2)):
        raise TypeError("Element pas de type entier dans une comparaison")

    gen_expression(expr1) #on calcule et empile la valeur de expr1
    gen_expression(expr2) #on calcule et empile la valeur de expr2
    nasm_instruction("pop", "ebx", "", "", "dépile la seconde expression dans ebx")
    nasm_instruction("pop", "eax", "", "", "dépile la première expression dans eax")

    nasm_instruction("cmp", "eax", "ebx", "", "compare eax avec ebx")

    code = {"<":"jl",">":"jg","==":"je","<=":"jle",">=":"jge","!=":"je"} # Un dictionnaire qui associe à chaque opérateur sa fonction nasm
    etiquette1 = nasm_nouvelle_etiquette()
    etiquette2 = nasm_nouvelle_etiquette()

    nasm_instruction(code[opComp], etiquette1, "", "", "fait un saut vers l'étiquette " + etiquette1)
    nasm_instruction("push", "1" if opComp == "!=" else "0", "", "", "")
    nasm_instruction("jmp", etiquette2, "", "", "fait un saut vers l'étiquette " + etiquette2)

    printifm(etiquette1 + ":") # pour ajouter le label dans le nasm
    nasm_instruction("push", "0" if opComp == "!=" else "1", "", "", "")
    printifm(etiquette2 + ":") # pour ajouter le label dans le nasm


def check_entier(entier):
    tE = type(entier)
    if tE == arbre_abstrait.AppelFonction:
        return tableSymbole.estBonType(tE.nomFonction, "entier")
    
    return (tE == arbre_abstrait.Entier) or (tE == arbre_abstrait.Operation) or (tE == arbre_abstrait.Lire)

"""
Affiche le code nasm pour les instructions conditionnelles
"""
def gen_conditionnel(instruction):
    nbExprs = len(instruction.exprs)
    nbInstrs = len(instruction.listeInstructions)

    if nbInstrs > 1:
        etiquette1 = nasm_nouvelle_etiquette()

    for i in range(nbInstrs):
        if not (nbExprs < nbInstrs and i == nbExprs):
            # prend condition if
            gen_condition(instruction.exprs[i])
            nasm_instruction("pop", "eax", "", "", "dépile la permière operande dans eax")

            # vérifie condition if
            nasm_instruction("cmp", "eax", "0", "", "compare eax avec Faux")
            etiquette2 = nasm_nouvelle_etiquette()
            nasm_instruction("je", etiquette2, "", "", "fait un saut vers l'étiquette " + etiquette2)

        # instructions dans if
        gen_listeInstructions(instruction.listeInstructions[i])
        if nbInstrs > 1:
            nasm_instruction("jmp", etiquette1, "", "", "fait un saut vers l'étiquette " + etiquette1)

        if not (nbExprs < nbInstrs and i == nbExprs):
            # fin dans if
            printifm(etiquette2 + ":") # pour ajouter le label dans le nasm
    if nbInstrs > 1:
    	printifm(etiquette1 + ":") # pour ajouter le label dans le nasm


def gen_condition(expression):
    if type(expression) == arbre_abstrait.Booleen:
        nasm_instruction("push", "1" if (str(expression.booleen) == "Vrai") else "0", "", "", "")
    elif type(expression) == arbre_abstrait.OperationLogique:
        gen_operationLogique(expression)  #on calcule et empile la valeur de l'opération logique
    elif type(expression) == arbre_abstrait.Comparaison:
        gen_comparaison(expression)  #on calcule et empile la valeur de la comparaison
    else:
        raise TypeError("Element pas de type booléen dans une expression conditionnelle")


if __name__ == "__main__":
    afficher_nasm = False
    afficher_tableSymboles = False

    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 3 or sys.argv[1] not in ["-nasm","-table"]:
        print("usage: python3 generation_code.py -nasm|-table NOM_FICHIER_SOURCE.flo")
        exit(0)
    if sys.argv[1]  == "-nasm":
        afficher_nasm = True
    else:
        afficher_tableSymboles = True
    with open(sys.argv[2],"r") as f:
        data = f.read()
        try:
            arbre = parser.parse(lexer.tokenize(data))
            write_def_fonction(arbre)
            if not afficher_tableSymboles:
                gen_programme(arbre)
        except EOFError:
            exit()
    if afficher_tableSymboles:
        tableSymbole.afficher()
