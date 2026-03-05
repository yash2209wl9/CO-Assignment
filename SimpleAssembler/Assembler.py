import sys
from errors import *
from Rtype import *
from Btype import *
from IandS import *
from UandJ import *

def Instructiontype(a):
    R_IN =["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]
    IandS_IN = ["addi", "lw", "sltiu", "jalr", "sw"]
    UandJ_IN = ["lui", "auipc", "jal"]
    B_IN = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
    if a in R_IN:
        return "R"
    elif a in IandS_IN:
        return "I"
    elif a in UandJ_IN:
        return "U"
    elif a in B_IN:
        return "B"
    else:
        return None




label = {}
i_file = sys.argv[1]
o_file = sys.argv[2]
f = open(i_file, 'r')
lines = f.readlines()
count = 0
output =  []
pc = 0
for i in lines:
    i = i.strip()
    if i == "":
        continue
    parts = i.replace(","," ").split()
    if ":" in parts[0]:
        if len(parts) == 1:
            label[parts[0].replace(":","")] = pc
        else :
            label[parts[0].replace(":","")] = pc
            pc = pc+4
    else:
        pc = pc+4
    
            
            
        
    
    



    


curr_pc = 0
for i in lines:
    count +=1
    i = i.strip()
    if i == "":
        continue
    
    i = i.replace(","," ")
    pieces = i.split()
    if ":" in pieces[0]:
        if len(pieces) == 1:
            continue
        else:
            pieces.pop(0)
            
    CheckInstruction(pieces,count,label)
    I_type = Instructiontype(pieces[0])
    if I_type == "R":
        b = Rtype(pieces)
    elif I_type == "I":
        b = IandS(pieces)
    elif I_type == "U":
        if pieces[0] == "jal":
            offset = label[pieces[2]] - curr_pc
            pieces[2] = str(offset)
        b = UandJ(pieces)
            
    elif I_type == "B":
        offset = label[pieces[3]] - curr_pc
        pieces[3] = str(offset)
        b = Btype(pieces)
        
    else:
        print("Error at line ")
        print(count)
        exit()

    output.append(b)
    curr_pc+=4
g = open(o_file, 'w')
for i in output:
    g.write(i)
    g.write("\n")
g.close()
f.close()
