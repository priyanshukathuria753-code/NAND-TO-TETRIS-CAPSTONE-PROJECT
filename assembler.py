"""
assembler.py - Hack Assembler (Nand to Tetris)
K = 14  ->  K mod 3 = 2  ->  extra feature: warn if a label is defined twice.

Usage:  python assembler.py Prog.asm        (writes Prog.hack)
"""
import sys

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010',
    'D': '0001100', 'A': '0110000', '!D': '0001101', '!A': '0110001',
    '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
    'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
DEST = {'': '000', 'M': '001', 'D': '010', 'MD': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

PREDEFINED = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
              'SCREEN': 16384, 'KBD': 24576}
for _i in range(16):
    PREDEFINED['R' + str(_i)] = _i


def clean(line):
    """Remove comments and all whitespace."""
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def first_pass(lines):
    """Remove comments/blank lines, record labels. Returns (instructions, symbols)."""
    symbols = dict(PREDEFINED)
    instructions = []          # list of (line_number, text)
    seen_labels = set()
    pc = 0
    for n, raw in enumerate(lines, start=1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith('(') and line.endswith(')'):
            label = line[1:-1]
            if label in seen_labels:                       # --- extra feature ---
                print(f"Warning: Line {n}: label '{label}' is defined more than once")
            seen_labels.add(label)
            symbols[label] = pc
        else:
            instructions.append((n, line))
            pc += 1
    return instructions, symbols


def second_pass(instructions, symbols):
    """Translate every instruction into 16 bits. Variables start at RAM[16]."""
    out = []
    next_var = 16
    for n, line in instructions:
        if line.startswith('@'):
            sym = line[1:]
            if sym.isdigit():
                val = int(sym)
            else:
                if sym not in symbols:
                    symbols[sym] = next_var
                    next_var += 1
                val = symbols[sym]
            out.append(format(val, '016b'))
        else:
            dest, comp, jump = '', line, ''
            if '=' in comp:
                dest, comp = comp.split('=', 1)
            if ';' in comp:
                comp, jump = comp.split(';', 1)
            out.append('111' + COMP[comp] + DEST[dest] + JUMP[jump])
    return out


def assemble(path):
    with open(path) as f:
        lines = f.read().splitlines()
    instructions, symbols = first_pass(lines)
    return second_pass(instructions, symbols)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python assembler.py Prog.asm")
        sys.exit(1)
    src = sys.argv[1]
    result = assemble(src)
    dst = src.rsplit('.', 1)[0] + '.hack'
    with open(dst, 'w') as f:
        f.write('\n'.join(result) + '\n')
    print(f"Written {dst} ({len(result)} instructions)")
