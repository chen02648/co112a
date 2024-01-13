symbol_table = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'SCREEN': 16384,
    'KBD': 24576
}

def add_labels_and_variables(lines):
    address = 0
    for line in lines:
        if line.startswith('('): 
            label = line[1:-1]
            symbol_table[label] = address
        else:
            address += 1


def process_A_instruction(instruction):
    try:
        address = int(instruction[1:])
    except ValueError:  
        label = instruction[1:]
        address = symbol_table[label]
    binary_address = format(address, '016b')
    return '0' + binary_address


def process_C_instruction(instruction):
    comp = '0' 
    dest = '000'
    jump = '000'
    
    if '=' in instruction:
        dest, comp = instruction.split('=')
    if ';' in instruction:
        comp, jump = instruction.split(';')

    return '111' + comp_code(comp) + dest_code(dest) + jump_code(jump)


def comp_code(comp):
    comp_mapping = {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101'
    }
    return comp_mapping[comp]


def dest_code(dest):
    dest_mapping = {
        '': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }
    return dest_mapping[dest]

def jump_code(jump):
    jump_mapping = {
        '': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }
    return jump_mapping[jump]


def assemble(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    lines = [line.strip().split('//')[0].strip() for line in lines if line.strip() and not line.startswith('//')]

    add_labels_and_variables(lines)

    binary_instructions = []
    for line in lines:
        if line.startswith('@'):  
            binary_instructions.append(process_A_instruction(line))
        else: 
            binary_instructions.append(process_C_instruction(line))

    with open(output_filename, 'w') as f:
        f.write('\n'.join(binary_instructions))

assemble('input.asm', 'output.hack')
