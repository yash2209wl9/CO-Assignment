import sys

registers = {"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100",
             "t0":"00101","t1":"00110", "t2":"00111","s0":"01000","s1":"01001",
             "a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110",
             "a5":"01111","a6":"10000","a7":"10001","s2":"10010","s3":"10011",
             "s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000",
             "s9":"11001","s10":"11010","s11":"11011","t3":"11100","t4":"11101",
             "t5":"11110","t6":"11111"}

R_type = ['add','sub','sll','slt','sltu','xor','srl','or','and']
I_type = ['lw','addi','sltiu','jalr']
S_type = ['sw']
B_type = ['beq','bne','blt','bge','bltu','bgeu']
U_type = ['lui','auipc']
J_type = ['jal']

#helper functions-----__-_______

def integer_to_binary(val, bits):
    val = int(val)
    if val < 0:
        val = (2 ** bits) + val
    return format(val, f'0{bits}b')#2s complement form

def validate_reg(reg, line_num):
    if reg not in registers:
        print(f"error:invalid register '{reg}' at line {line_num}")
        sys.exit()

def Instructiontype(a):
    if a in R_type:
        return "R"
    elif a in I_type:
        return "I"
    elif a in S_type:
        return "S"
    elif a in B_type:
        return "B"
    elif a in U_type:
        return "U"
    elif a in J_type:
        return "J"
    return None

#different type -____-----------------

def Rtype(pieces, line_num):
    function_table = {"add":["0000000","000"],"sub":["0100000","000"],"sll":["0000000","001"],
                      "slt":["0000000","010"],"sltu":["0000000","011"],"xor":["0000000","100"],
                      "srl":["0000000","101"],"or":["0000000","110"],"and":["0000000","111"]}
    inst, rd, rs1, rs2 = pieces #spliting peices into inst and registers 
    for r in [rd, rs1, rs2]:
        validate_reg(r, line_num)
    f7, f3 = function_table[inst]
    return f7 + registers[rs2] + registers[rs1] + f3 + registers[rd] + "0110011"

def Btype(pieces, line_num):
    funct3_dict = {"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}
    inst, rs1, rs2, imm = pieces
    for r in [rs1, rs2]:
        validate_reg(r, line_num)
    
    imm_bin = integer_to_binary(imm, 13) # for 13 bits 
    return imm_bin[0] + imm_bin[2:8] + registers[rs2] + registers[rs1] + funct3_dict[inst] + imm_bin[8:12] + imm_bin[1] + "1100011"

def IandS(pieces, line_num):
    ops = {"lw":["0000011","010"], "addi":["0010011","000"], "sltiu":["0010011","011"],
           "jalr":["1100111","000"], "sw":["0100011","010"]}
    inst, rsd, r1, imm = pieces
    for r in [rsd, r1]:
        validate_reg(r, line_num)
    
    opcode, f3 = ops[inst]
    imm_bin = integer_to_binary(imm, 12)
    if inst != "sw":
        return imm_bin + registers[r1] + f3 + registers[rsd] + opcode
    else:
        return imm_bin[0:7] + registers[rsd] + registers[r1] + f3 + imm_bin[7:12] + opcode

def UandJ(pieces, line_num):
    op_table = {"lui":"0110111", "auipc":"0010111", "jal":"1101111"}
    inst, rd, imm = pieces
    validate_reg(rd, line_num)
    
    if inst in ["lui", "auipc"]: #for U
        return integer_to_binary(imm, 20) + registers[rd] + op_table[inst]
    
    imm_bin = integer_to_binary(imm, 21)
    return imm_bin[0] + imm_bin[10:20] + imm_bin[9] + imm_bin[1:9] + registers[rd] + op_table[inst]

# ---Assembler-------------


label = {}
with open(sys.argv[1], 'r') as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]
pc = 0
for line in lines:#for labels
    parts = line.replace(",", " ").split()
    if ":" in parts[ 0]:
        label[parts[0].split(":")[0]] = pc
        if len(parts) > 1:
            pc += 4
    else:
        pc += 4

output = []
curr_pc = 0
vhault_found = False

for idx, line in enumerate(lines, 1):#encoding
    pieces = line.replace(","," ").split()
    if ":" in pieces[0] :
        if len(pieces) == 1:
            continue
        pieces.pop(0)

    inst = pieces[0]
    itype = Instructiontype(inst)
    
    if itype == "R": b = Rtype(pieces, idx)
    elif itype in ["I","S"]:
        if inst in ["lw","sw"]:
            try:
                off, reg = pieces[2].split("(")
                pieces = [inst, pieces[1], reg.replace(")", ""), off]
            except ValueError:
                print(f"error:Invalid memory format at line {idx}")
                sys.exit()
        b = IandS(pieces, idx)
    elif itype == "B":
        target = pieces[3]
        off = label[target] - curr_pc if target in label else int(target)#calculating offset
        pieces[3] = str(off)
        b = Btype(pieces, idx)
    elif itype == "J":
        target = pieces[2]
        off = label[target] - curr_pc if target in label else int(target)#cal offset
        pieces[2] = str(off)
        b = UandJ(pieces, idx)
    elif itype == "U": b = UandJ(pieces, idx)
    else:
        print(f"error:unknown instruction '{inst}' at line {idx}")
        sys.exit()

    output.append(b)
    
    if pieces == ["beq", "zero", "zero", "0"]:
        vhault_found = True
        
    curr_pc = curr_pc + 4

if vhault_found == False:
    print("error:missing virtual halt")
    sys.exit()

with open(sys.argv[2], 'w') as g:
    for line in output:
        g.write(line + "\n")# writing the ouput line wise
