def to_signed_binary(value, bits):
    value = int(value)
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

registers = {"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100",
             "t0":"00101","t1":"00110", "t2":"00111","s0":"01000","s1":"01001",
             "a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110",
             "a5":"01111","a6":"10000","a7":"10001","s2":"10010","s3":"10011",
             "s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000",
             "s9":"11001","s10":"11010","s11":"11011","t3":"11100","t4":"11101",
             "t5":"11110","t6":"11111"}

def Btype(pieces):

    inst = pieces[0]
    rs1 = pieces[1]
    rs2 = pieces[2]

    imm_bin = to_signed_binary(pieces[3], 13)

    imm12 = imm_bin[0]
    imm10_5 = imm_bin[1:7]
    imm4_1 = imm_bin[7:11]
    imm11 = imm_bin[11]

  


 
    return imm12 +imm10_5 +registers[rs2]+registers[rs1]+ funct3_dict[inst] +imm4_1 +imm11 +opcode
