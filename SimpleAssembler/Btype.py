def to_signed_binary(value, bits):
    if value < 0:
        value = (1 << bits) + value
    return format(value, f'0{bits}b')

opcode = "1100011"

funct3_dict = {
    "beq": "000",
    "bne": "001",
    "blt": "100",
    "bge": "101",
    "bltu": "110",
    "bgeu": "111"
 }

registers = {
    "x0":"00000","x1":"00001","x2":"00010","x3":"00011",
    "x4":"00100","x5":"00101","x6":"00110","x7":"00111",
    "x8":"01000","x9":"01001","x10":"01010","x11":"01011",
    "x12":"01100","x13":"01101","x14":"01110","x15":"01111",
    "x16":"10000","x17":"10001","x18":"10010","x19":"10011",
    "x20":"10100","x21":"10101","x22":"10110","x23":"10111",
    "x24":"11000","x25":"11001","x26":"11010","x27":"11011",
    "x28":"11100","x29":"11101","x30":"11110","x31":"11111"
    }
def Btype(pieces, label_dict, pc):

    inst = pieces[0]
    rs1 = pieces[1]
    rs2 = pieces[2]
    label = pieces[3]

    target_pc = label_dict[label]
    offset = target_pc - pc

    imm_bin = to_signed_binary(offset, 13)

    imm12 = imm_bin[0]
    imm10_5 = imm_bin[1:7]
    imm4_1 = imm_bin[7:11]
    imm11 = imm_bin[11]

    binary = (
        imm12 +
        imm10_5 +
        registers[rs2] +
        registers[rs1] +
        funct3_dict[inst] +
        imm4_1 +
        imm11 +
        opcode
    )


 
    return binary
