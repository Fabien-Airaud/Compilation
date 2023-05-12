INPUT = exemple1 exemple2 multiplication eval_assembleur/soustraction eval_assembleur/division eval_assembleur/modulo eval_assembleur/lecture eval_assembleur/booleen eval_assembleur/opLogique # priorite test test2 test3

assembleur_vers_exercutable: generation_code_nasm
	for a in $(INPUT); do echo "Assemblage: " $${a}; nasm -f elf -g -F dwarf output/$${a}.nasm; ld -m elf_i386 -o output/$${a} output/$${a}.o; rm output/$${a}.o; rm output/$${a}.nasm; done;

generation_code_nasm:
	for a in $(INPUT); do echo "Generation code nasm: " $${a}; python3 generation_code.py -nasm input/$${a}.flo > output/$${a}.nasm; done;

clean:
	rm ./output/*;
