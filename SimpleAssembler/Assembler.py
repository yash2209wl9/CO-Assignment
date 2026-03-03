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
    B_IN = ["beq", "bne", "blt", "bgt", "bltu", "bgtu"]
    for a in R_IN:
        return "R"
    for a in IandS_IN:
        return "I"
    for a in UandJ_IN:
        return "U"
    for a in B_IN:
        return "B"

i_file = sys.argv[1]
o_file = sys.argv[2]
f = open(i_file, 'r')
lines = f.readlines()
count = 0
output =  []
for i in lines:
    count +=1
    i = i.replace(","," ")
    pieces = i.split()
    CheckInstruction(pieces,count)
    type = Instructiontype(pieces[0])
    if type == "R":
        b = Rtype(pieces)
    elif type == "I":
        b = IandS(pieces)
    elif type == "U":
        b = UandJ(pieces)
    elif type == "B":
        b = Btype(pieces)

    output.append(b)
    g = open(o_file, 'w')
    for i in output:
        g.write(i)
        g.write("\n")
    g.close()