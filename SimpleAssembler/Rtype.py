registers = {"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100",
             "t0":"00101","t1":"00110", "t2":"00111","s0":"01000","s1":"01001",
             "a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110",
             "a5":"01111","a6":"10000","a7":"10001","s2":"10010","s3":"10011",
             "s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000",
             "s9":"11001","s10":"11010","s11":"11011","t3":"11100","t4":"11101",
             "t5":"11110","t6":"11111"}
function_table = {"add":["0000000","000"],"sub":["0100000","000"],"sll":["0000000","001"],
                  "slt":["0000000","010"],"sltu":["0000000","011"],"xor":["0000000","100"],
                  "srl":["0000000","101"],"or":["0000000","110"],"and":["0000000","111"]}

def Rtype(pieces):    
    Instruction = pieces[0]
    rd = pieces[1]
    rs1 = pieces[2]
    rs2 = pieces[3]
    opcode = "0110011"
    binary_rd = registers[rd]
    binary_rs1 = registers[rs1]
    binary_rs2 = registers[rs2]
    funct7,funct3 = function_table[Instruction]
    binary = funct7 +binary_rs2 +binary_rs1 +funct3 + binary_rd+ opcode
    return binary 
    
        
