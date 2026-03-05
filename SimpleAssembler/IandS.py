def IandS(pieces):
    inst=pieces[0]
    configs={
        "addi": {"type": "I", "opcode": "001011", "funct3": "000"},
        "lw": {"type": "I", "opcode": "000011", "funct3": "010"},
        "jalr": {"type": "I", "opcode": "1100111", "funct3": "000"},
        "sw": {"type": "S", "opcode": "010011", "funct3": "010"},
        }
    reg_map={f"x{i}": format(i, "05b") for i in range(32)}
    c=configs[inst]
    if c["type"]==" I":
        rd=reg_map[pieces[1]]
        rs1=reg_map[pieces[2]]
        imm=format(int(pieces[3])& 0xFFF, "012b")
        return c["opcode"]+rd+c["funct3"]+rs1+imm
    if c["type"]=="S":
        rs2=reg_map[pieces[1]]
        offset_val, rs1_val=pieces[2].replace(")", "").split(",")
        rs1=reg_map[rs1_val]
        imm=format(int(offset_val) & 0xFFF, "012b")
    return f"{imm[:7]}{rs2}{rs1}{c['funct3']}{imm[7:]}{c['opcode']}"
