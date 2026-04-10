import sys
import os

#basic helper functions(will be used later on) 

def u32(val):
    return val & 0xFFFFFFFF


def s32(val):
    val= val & 0xFFFFFFFF
    if val >= 0x80000000:
        val= val - 0x100000000
    return val


def sign_extend(val,bits):
    mask = (1 << bits) - 1
    val = val & mask

    if val >= (1 << (bits - 1)):
        val = val - (1 << bits)
    return val


def to_bin(val):
    val = val & 0xFFFFFFFF
    binary = format(val, '032b')
    return '0b' + binary


#decoding fields from instruction(given in binary)
def decode_fields(b):
    opcode = b[25:32]
    rd = int(b[20:25], 2)
    funct3 = b[17:20]
    rs1 = int(b[12:17], 2)
    rs2 = int(b[7:12], 2)
    funct7 = b[0:7]
    return opcode, rd, funct3, rs1, rs2, funct7


# immediate helpers (will use later)
def imm_I(b):
    return sign_extend(int(b[0:12], 2), 12)

def imm_S(b):
    return sign_extend(int(b[0:7] + b[20:25], 2), 12)

def imm_B(b):
    raw = b[0] + b[24] + b[1:7] + b[20:24] + '0'
    return sign_extend(int(raw, 2), 13)

def imm_U(b):
    return int(b[0:20], 2) << 12

def imm_J(b):
    raw = b[0] + b[12:20] + b[11] + b[1:11] + '0'
    return sign_extend(int(raw, 2), 21)

def vhalt(b):
    opcode, rd, funct3, rs1, rs2, funct7 = decode_fields(b)
    if opcode != "1100011" or funct3 != "000":
        return False
    if rs1 != 0 or rs2 != 0:
        return False
    return imm_B(b) == 0


DATA_MEM_DISPLAY_BASE = 0x00010000         # Base address for memory dump in output
DATA_MEM_WORDS = 4096                      # Total words in data memory (16KB)
DATA_MEM_DUMP_WORDS = 32                   # Number of words to dump from data memory at the end of simulation

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 Simulator.py <input> <output>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    #reading the intructions
    with open(input_path, 'r') as f:
        instr_mem = [line.strip() for line in f if line.strip()]

    for i, instr in enumerate(instr_mem, 1):
        if len(instr) != 32 or not all(c in '01' for c in instr):
            print(f"Invalid instruction at line {i}")
            sys.exit(1)

    #initial state(will add more)
    regs= [0 for i in range(32)]
    pc = 0
    data_mem=[0] * DATA_MEM_WORDS
    output_lines=[]

    def write_state():
        parts = [to_bin(pc)] + [to_bin(r) for r in regs]
        output_lines.append(' '.join(parts))

    def flush_and_exit():
        out_dir = os.path.dirname(output_path)
        if out_dir != "":
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write('\n'.join(output_lines) + '\n')
        sys.exit(1) 

    
    def addr_to_index(addr):
        if addr % 4 != 0:
            return None

        raw_idx = addr // 4
        if 0 <= raw_idx < DATA_MEM_WORDS:
            return raw_idx

        if addr >= DATA_MEM_DISPLAY_BASE:
            base_idx = (addr - DATA_MEM_DISPLAY_BASE) // 4
            if 0 <= base_idx < DATA_MEM_WORDS:
                return base_idx

        return None

    def mem_read(addr):
        idx = addr_to_index(addr)
        if idx is None:
            print(f"Error: Memory read out of range: 0x{addr:08x} (PC=0x{pc:08x})")
            flush_and_exit()
        return data_mem[idx]

    def mem_write(addr, val):
        if addr % 4 != 0:
            print(f"Error: Unaligned memory write at 0x{addr:08x} (PC=0x{pc:08x})")
            flush_and_exit()

        idx = addr_to_index(addr)
        if idx is None:
            print(f"Error: Memory write out of range: 0x{addr:08x} (PC=0x{pc:08x})")
            flush_and_exit()

        data_mem[idx] = u32(val)

    infinite = 1_000_000                 
    for step in range(infinite):
        idx = pc // 4
        if not (0 <= idx < len(instr_mem)):
            print("error: PC out of  instruction memory range ")
            flush_and_exit()

        b = instr_mem[idx]
        opcode, rd, funct3, rs1, rs2, funct7 = decode_fields(b)
        next_pc= pc + 4

        if vhalt(b):
            regs[0]= 0
            write_state()
            for i in range(DATA_MEM_DUMP_WORDS):
                addr = DATA_MEM_DISPLAY_BASE + i * 4
                output_lines.append(f"0x{addr:08X}:{to_bin(data_mem[i])}")
            break

        # =========R-Type===============
        elif opcode == "0110011":
            a = s32(regs[rs1])
            b_ = s32(regs[rs2])
            ua = u32(regs[rs1])
            ub = u32(regs[rs2])
            shft = ub & 0x1F

            if   funct3 == "000" and funct7 == "0000000": result = a + b_
            elif funct3 == "000" and funct7 == "0100000": result = a - b_
            elif funct3 == "001" and funct7 == "0000000": result = ua << shft
            elif funct3 == "010" and funct7 == "0000000": result = 1 if a < b_ else 0
            elif funct3 == "011" and funct7 == "0000000": result = 1 if ua < ub else 0
            elif funct3 == "100" and funct7 == "0000000": result = ua ^ ub
            elif funct3 == "101" and funct7 == "0000000": result = ua >> shft
            elif funct3 == "101" and funct7 == "0100000": result = a >> shft
            elif funct3 == "110" and funct7 == "0000000": result = ua | ub
            elif funct3 == "111" and funct7 == "0000000": result = ua & ub
            else:
                print(f"Error: Unknown R-type funct3={funct3} funct7={funct7} at line {idx+1}")
                flush_and_exit()

            if rd != 0:
                regs[rd] = u32(result)

        # =========I-Type=========
        elif opcode == "0010011":
            imm = imm_I(b)
            a = s32(regs[rs1])
            ua = u32(regs[rs1])
            shft = imm & 0x1F

            if   funct3 == "000": result = a + imm
            elif funct3 == "010": result = 1 if a < imm else 0
            elif funct3 == "011": result = 1 if ua < u32(imm) else 0
            elif funct3 == "100": result = ua ^ u32(imm)
            elif funct3 == "110": result = ua | u32(imm)
            elif funct3 == "111": result = ua & u32(imm)
            elif funct3 == "001": result = ua << shft
            elif funct3 == "101":
                if funct7 == "0000000":
                    result = ua >> shft
                elif funct7 == "0100000":
                    result = a >> shft
                else:
                    print(f"Error: Unknown I-shift funct7={funct7} at line {idx+1}")
                    flush_and_exit()
            else:
                print(f"Error: Unknown I-ALU funct3={funct3} at line {idx+1}")
                flush_and_exit()

            if rd != 0:
                regs[rd] = u32(result)

        # =========Load word===============
        elif opcode == "0000011":
            if funct3 != "010":
                print(f"Error: Unsupported load funct3={funct3} at line {idx+1}")
                flush_and_exit()
            addr = u32(regs[rs1] + imm_I(b))
            val = mem_read(addr)
            if rd != 0:
                regs[rd] = val

        # =========S-Type=========
        elif opcode == "0100011":
            if funct3 != "010":
                print(f"Error: Unsupported store funct3={funct3} at line {idx+1}")
                flush_and_exit()
            addr = u32(regs[rs1] + imm_S(b))
            mem_write(addr, regs[rs2])

        # =========U-Type===========

        # ========LUI===========
        elif opcode == "0110111":
            if rd != 0:
                regs[rd] = u32(imm_U(b))

        # =========AUIPC===========
        elif opcode == "0010111":
            if rd != 0:
                regs[rd] = u32(pc + imm_U(b))
        

        #=============J-Type================

        # =========JAL===========
        elif opcode == "1101111":
            link = pc + 4
            next_pc = pc + imm_J(b)
            if rd != 0:
                regs[rd] = u32(link)

        # =========JALR===========
        elif opcode == "1100111":
            link = pc + 4
            next_pc = u32((regs[rs1] + imm_I(b)) & ~1)
            if rd != 0:
                regs[rd] = u32(link)
        else:
            print(f"Error: Unknown opcode '{opcode}' at line {idx+1}")
            flush_and_exit()

        regs[0] = 0
        pc = next_pc
        write_state()

    else:
        print("Error: Exceeded maximum step limit — possible infinite loop")
        flush_and_exit()
        
    out_dir = os.path.dirname(output_path)          
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    with open(output_path, 'w') as f:      
        f.write('\n'.join(output_lines) + '\n')

    print(f"Simulation complete. Output written to '{output_path}'")


if __name__ == "__main__":
    main()


