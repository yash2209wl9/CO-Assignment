registers = {"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100",
            "t0":"00101","t1":"00110", "t2":"00111","s0":"01000","s1":"01001",
            "a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110",
            "a5":"01111","a6":"10000","a7":"10001","s2":"10010","s3":"10011",
            "s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000",
            "s9":"11001","s10":"11010","s11":"11011","t3":"11100","t4":"11101",
            "t5":"11110","t6":"11111"}

opcode_table = {
        "lui": "0110111",
        "auipc": "0010111",
        "jal": "1101111",
    }

def integer_to_binary(val,bits):
    val = int(val)
    if(val < 0):
        val = 2**bits + val,
    return format(val,'0{}b'.format(bits))

def UandJ(pieces):
    instruction = pieces[0]
    rd = pieces[1]
    imm = pieces[2]
    binary_rd = registers[rd]
    opcode = opcode_table[instruction]

    if instruction == "lui" or instruction == "auipc" :
        binary_imm_u = integer_to_binary(imm,20)
        binary = binary_imm_u + binary_rd + opcode
        return binary
    else:
        binary_imm_j = integer_to_binary(imm,21)
        imm20 = binary_imm_j[0]
        imm10to1 = binary_imm_j[10:20]
        imm11 = binary_imm_j[9]
        imm19to21 = binary_imm_j[1:9]

        binary = imm20 + imm10to1 + imm11 + imm19to21 + binary_rd + opcode
        return binary
    


    

















































