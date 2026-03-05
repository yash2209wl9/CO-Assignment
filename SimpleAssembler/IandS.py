registers = {"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100",
            "t0":"00101","t1":"00110", "t2":"00111","s0":"01000","s1":"01001",
            "a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110",
            "a5":"01111","a6":"10000","a7":"10001","s2":"10010","s3":"10011",
            "s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000",
            "s9":"11001","s10":"11010","s11":"11011","t3":"11100","t4":"11101",
            "t5":"11110","t6":"11111"}
operation_indentity={
    lw:["0000011","010"],
    addi:["0010011","000"],
    sltiu:["0010011","011"],
    jalr:["1100111","000"],
    sw:["0100011","010"]

}

def twos_complement(value, bits):
    val = int(value)
    if val < 0:
        val = (1 << bits) + val
    return format(val, f'0{bits}b')
    
def IandS(pieces):
    instruction=pieces[0]
    rsd=pieces[1]
    r1=pieces[2]
    imm=pieces[3]
    opcode = operation_indentity[instruction][0]
    funct3 = operation_indentity[instruction][1]

    imm_bin= twos_complement(imm,12)

    if instruction in ["lw", "addi", "sltiu", "jalr"]:
        rd = registers[rsd]
        rs1 = registers[r1]
        
        return imm_bin + rs1 + funct3 + rd + opcode
    elif instruction == "sw":
        rs2=registers[rsd]
        rs1 = registers[r1]
        imm_11_5 = imm_bin[0:7]
        imm_4_0 = imm_bin[7:12]

        return imm_11_5 + rs2 + rs1 + funct3 + imm_4_0 + opcode
        
    
    
