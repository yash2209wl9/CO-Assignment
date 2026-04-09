import sys
import os

#basic helper functions(will be used later on) 

def u32(val):
    return val & 0xFFFFFFFF


def s32(val):
    val= val & 0xFFFFFFFF
    if val >= 0x80000000:
        val= val - 0x100000000
    return val


def sign_extend(val,bits):
    mask = (1 << bits) - 1
    val = val & mask

    if val >= (1 << (bits - 1)):
        val = val - (1 << bits)
    return val


def to_bin(val):
    val = val & 0xFFFFFFFF
    binary = format(val, '032b')
    return '0b' + binary


#decoding fields from instruction(given in binary)
def decode_fields(b):
    opcode = b[25:32]
    rd = int(b[20:25], 2)
    funct3 = b[17:20]
    rs1 = int(b[12:17], 2)
    rs2 = int(b[7:12], 2)
    funct7 = b[0:7]
    return opcode, rd, funct3, rs1, rs2, funct7


# immediate helpers (will use later)
def imm_I(b):
    return sign_extend(int(b[0:12], 2), 12)

def imm_S(b):
    return sign_extend(int(b[0:7] + b[20:25], 2), 12)

def imm_B(b):
    raw = b[0] + b[24] + b[1:7] + b[20:24] + '0'
    return sign_extend(int(raw, 2), 13)

def imm_U(b):
    return int(b[0:20], 2) << 12

def imm_J(b):
    raw = b[0] + b[12:20] + b[11] + b[1:11] + '0'
    return sign_extend(int(raw, 2), 21)


#Main logic for the code

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 Simulator.py <input> <output>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    #reading the intructions
    with open(input_path, 'r') as f:
        instr_mem = [line.strip() for line in f if line.strip()]

    for i, instr in enumerate(instr_mem, 1):
        if len(instr) != 32 or not all(c in '01' for c in instr):
            print(f"Invalid instruction at line {i}")
            sys.exit(1)

    #initial state(will add more)
    regs= [0 for i in range(32)]
    pc = 0


    # execution logic will be added here

main()
