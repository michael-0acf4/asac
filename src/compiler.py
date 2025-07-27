from typing import List

def get_opcode(instr: str, chan: int) -> int:
    if instr == "NOTEOFF":
        return chan - 1  # 0x00–0x03
    elif instr == "NOTEON":
        return 0x03 + chan  # 0x04–0x07
    else:
        raise ValueError("Invalid NOTE* instruction")

def compile_instructions(lines: List[str]) -> List[bytes]:
    bytecode = []

    for line in lines:
        tokens = line.strip().split()
        if not tokens:
            continue
        instr = tokens[0].upper()

        if instr in {"NOTEON", "NOTEOFF"}:
            chan = int(tokens[1])
            opcode = get_opcode(instr, chan)

            if instr == "NOTEON":
                freq = int(tokens[2])
                vel = int(tokens[3])
                freq_hi = (freq >> 8) & 0xff
                freq_lo = freq & 0xff
                bytecode.append(bytes([opcode, freq_lo, freq_hi, vel]))
            else:  # NOTEOFF
                bytecode.append(bytes([opcode, 0x00, 0x00, 0x00]))

        elif instr == "WAIT":
            delay = int(tokens[1])
            if delay > 0xffff:
                raise ValueError("Delay exceeds 16-bit max")
            delay_hi = (delay >> 8) & 0xff
            delay_lo = delay & 0xff
            bytecode.append(bytes([0x08, delay_lo, delay_hi, 0x00]))

        elif instr == "JUMP":
            addr = int(tokens[1])
            if addr > 0xffff:
                raise ValueError("Address exceeds 16-bit max")
            addr_hi = (addr >> 8) & 0xff
            addr_lo = addr & 0xff
            bytecode.append(bytes([0x09, addr_lo, addr_hi, 0x00]))

        else:
            raise ValueError(f"Unknown instruction: {instr}")

    return bytecode

def to_hex(bytecode: List[bytes]) -> List[str]:
    # return [' '.join(f'{b:02X}' for b in instr) for instr in bytecode]
    # return [''.join(f'{b:02X}' for b in instr) for instr in bytecode]
    return [''.join(f'{b:02X}' for b in reversed(instr)) for instr in bytecode]


if __name__ == "__main__":
    program = [
        "NOTEON 1 440 127",
        "NOTEON 2 440 127",
        "NOTEON 3 240 127",
        "WAIT 100",
        "NOTEOFF 3",
        "WAIT 200",
        "JUMP 0"
    ]
    bc = compile_instructions(program)
    text = []
    for line in to_hex(bc):
        text.append(line)
    print(" ".join(text))
