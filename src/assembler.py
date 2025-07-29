from typing import List
import sys


def get_note_opcode(instr: str, chan: int) -> int:
    if instr == "NOTEOFF":
        return chan - 1  # 0x00–0x03
    elif instr == "NOTEON":
        return 0x03 + chan  # 0x04–0x07
    else:
        raise ValueError("Invalid NOTE* instruction")


def debug_actual_microcode(instr: str, chan: int) -> int:
    if not (1 <= chan <= 4):
        raise ValueError("Channel must be 1 to 4")

    opcode = (1 << 4) | ((chan - 1) & 0xFF)
    if instr == "NOTEON":
        opcode |= 1 << 3
    elif instr != "NOTEOFF":
        raise ValueError("Instruction must be NOTEON or NOTEOFF")

    return opcode


def compile_instructions(lines: List[str]) -> List[bytes]:
    bytecode = []

    jumps = {}
    instr_idx = 0

    for line in lines:
        tokens = line.strip().split()
        if not tokens:
            continue
        instr = tokens[0].upper()

        if instr in {"NOTEON", "NOTEOFF"}:
            chan = int(tokens[1])
            opcode = get_note_opcode(instr, chan)
            # print(debug_actual_microcode(instr, chan))

            if instr == "NOTEON":
                freq = int(tokens[2])
                vel = int(tokens[3])
                freq_hi = (freq >> 8) & 0xFF
                freq_lo = freq & 0xFF
                bytecode.append(bytes([opcode, freq_lo, freq_hi, vel]))
            else:  # NOTEOFF
                bytecode.append(bytes([opcode, 0x00, 0x00, 0x00]))

        elif instr == "LABEL":
            jumps[tokens[1].strip()] = instr_idx

        elif instr == "WAIT":
            delay = int(tokens[1])
            if delay > 0xFFFF:
                raise ValueError("Delay exceeds 16-bit max")

            while delay > 0:
                bytecode.append(bytes([0x08, 0x00, 0x00, 0x00]))
                delay -= 1

        elif instr == "JUMP":
            label = tokens[1].strip()
            if label not in jumps:
                raise ValueError(f"Could not resolve label '{label}'")

            addr = jumps[label]
            addr_hi = (addr >> 8) & 0xFF
            addr_lo = addr & 0xFF
            bytecode.append(bytes([0x09, addr_lo, addr_hi, 0x00]))

        else:
            raise ValueError(f"Unknown instruction: {instr}")

        instr_idx += 1

    return bytecode


def to_hex(bytecode: List[bytes]) -> List[str]:
    # return [' '.join(f'{b:02X}' for b in instr) for instr in bytecode]
    # return [''.join(f'{b:02X}' for b in instr) for instr in bytecode]
    return ["".join(f"{b:02X}" for b in reversed(instr)) for instr in bytecode]


def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <file>")
        sys.exit(1)

    filepath = sys.argv[1]

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    bc = compile_instructions(lines)
    text = []
    for line in to_hex(bc):
        text.append(line)
    print(" ".join(text))


if __name__ == "__main__":
    main()
