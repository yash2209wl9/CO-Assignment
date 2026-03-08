register_dict = {
'zero':0,'ra':1,'sp':2,'gp':3,'tp':4,
't0':5,'t1':6,'t2':7,
's0':8,'s1':9,
'a0':10,'a1':11,'a2':12,'a3':13,'a4':14,'a5':15,'a6':16,'a7':17,
's2':18,'s3':19,'s4':20,'s5':21,'s6':22,'s7':23,'s8':24,'s9':25,'s10':26,'s11':27,
't3':28,'t4':29,'t5':30,'t6':31
} 


R_type = ['add','sub','sll','slt','sltu','xor','srl','or','and']

I_type = ['lw','addi','sltiu','jalr']

S_type = ['sw']

B_type = ['beq','bne','blt','bge','bltu','bgeu']

U_type = ['lui','auipc']

J_type = ['jal']


def checkval(val,bits):
    try:
        val = int(val)
    except:
        return False
    
    minval = -(2**(bits-1))
    maxval = 2**(bits-1)-1
    
    if val < minval or val > maxval:
        return False
    else:
        return True

def CheckInstruction(pieces,line_number,dict_label):

    instruction = pieces[0]
    if instruction not in R_type+I_type+S_type+B_type+U_type+J_type:
        return f"Invalid instruction at {line_number}"
    
    if instruction in R_type:
        if len(pieces) != 4:
            return f"wrong count of operand at {line_number}"
        rd , rs1, rs2 = pieces[1],pieces[2],pieces[3]

        if rd not in register_dict or rs1 not in register_dict or rs2 not in register_dict:
            return f"wrong register at {line_number}"
        
    elif instruction in I_type:
        if instruction == "lw":
            if len(pieces)!= 3:
                return f"wrong count of operand at {line_number}"
        
            rd = pieces[1]

            if rd not in register_dict:
                return f"invalid register at {line_number}"
            try:
                imm, reg = pieces[2].split("(")
                reg = reg.replace(")", "")
            except:
                return f"invalid format of memory at {line_number}"
        
            if reg not in register_dict:
                return f"invalid register at {line_number}"
            if not checkval(imm,12):
                return f"immediate out of range at {line_number}"
        
        else:
            if len(pieces)!= 4:
                return f"wrong count of register at {line_number}"
            
            rd , rs1, imm = pieces[1], pieces[2], pieces[3]
            
            if rd not in register_dict or rs1 not in register_dict:
                return f"invalid register at {line_number}"
            
            if not checkval(imm,12):
                return f"immediate out of range at {line_number}"
            
    elif instruction in S_type:
        if len(pieces)!= 3:
            return f"wrong count of operand at {line_number}"
        rs2 = pieces[1]

        if rs2 not in register_dict:
            return f"invalid register at {line_number}"

        try:
            imm, reg = pieces[2].split("(")
            reg = reg.replace(")", "")
        except:
            return f"Error at line {line_number}: Invalid memory format"
        if reg not in register_dict:
            return f"invalid register at {line_number}"
        if not checkval(imm, 12):
            return f"immediate out of range at {line_number}"
        
    
    elif instruction in B_type:
        if len(pieces) != 4:
            return f"wrong count of operand at {line_number}"
        rs1, rs2, label = pieces[1], pieces[2], pieces[3]

        if rs1 not in register_dict or rs2 not in register_dict:
            return f"invalid register at {line_number}"
        if label not in dict_label:
            try:
                int(label)
            except:
                return f"undefined label at {line_number}"
        
    elif instruction in U_type:
        if len(pieces)!= 3:
            return f"wrong count of operand at {line_number}"
        rd , imm = pieces[1], pieces[2]

        if rd not in register_dict:
            return f"invalid register at {line_number}"
        
        if not checkval(imm, 20):
            return f"immediate out of range at {line_number}"
        
    elif instruction in J_type:
        if len(pieces)!= 3:
            return f"wrong count of operand at {line_number}"
        rd , label = pieces[1], pieces[2]

        if rd not in register_dict:
            return f"invalid register at {line_number}"
        
        if label not in dict_label:
            return f"undefined label at {line_number}"
    
    return None 
    
    

































