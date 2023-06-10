INPUT = exemple1 exemple2 multiplication eval_assembleur/soustraction eval_assembleur/division eval_assembleur/modulo eval_assembleur/lecture eval_assembleur/booleen eval_assembleur/opLogique eval_assembleur/comparaison eval_assembleur/conditionnel eval_assembleur/deffonctions eval_assembleur/fonction # priorite test test2 test3
ERROR = fonctionerror1 fonctionerror2 fonctionerror3

all : generation_code_nasm assembleur_vers_exercutable

assembleur_vers_exercutable: generation_code_nasm
	for a in $(INPUT); do echo "Assemblage: " $${a}; nasm -f elf -g -F dwarf output/$${a}.nasm; ld -m elf_i386 -o output/$${a} output/$${a}.o; rm output/$${a}.o; rm output/$${a}.nasm; done;

generation_code_nasm:
	for a in $(INPUT); do echo "Generation code nasm: " $${a}; python3 generation_code.py -nasm input/$${a}.flo > output/$${a}.nasm; done;

affichage_table_symbole:
	for a in $(INPUT); do echo "Affichage table symbole: " $${a}; python3 generation_code.py -table input/$${a}.flo; done;

test_error:
	for a in $(ERROR); do echo "Generation code nasm: " $${a}; python3 generation_code.py -nasm input/eval_assembleur/erreur_code/$${a}.flo > output/eval_assembleur/erreur_code/$${a}.nasm; done;

clean:
	rm ./output/*;
