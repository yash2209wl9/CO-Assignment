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

        data_mem[idx] = to_unsigned32(val)

    infinite = 1_000_000                 
    for step in range(infinite):
        idx = pc // 4
        if not (0 <= idx < len(instr_mem)):
            print("error: PC out of  instruction memory range ")
            flush_and_exit()

        b = instr_mem[idx]
        opcode, rd, funct3, rs1, rs2, funct7 = decode_fields(b)
        nextPc= pc + 4

        if vhalt(b):
            regs[0]= 0
            write_state()
            for i in range(DATA_MEM_DUMP_WORDS):
                addr = DATA_MEM_DISPLAY_BASE + i * 4
                output_lines.append(f"0x{addr:08X}:{to_bin32(data_mem[i])}")
            break

main()
