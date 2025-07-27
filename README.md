# asac

A Simple Audio Chip (ASAC) is a simple chip in which we can write programs that mimics the MIDI format.

# Instruction Set

```
    8 bit          8 bits     8bits       8 bits
NOTEON  [chan]  [       freq         ]   [  vel  ]
NOTEOFF [chan]
WAIT            [       delay        ]
JUMP            [     addr_val       ]
```

# Microcode Spec

```
microcode
opcode       
  0x00: 0x00 (0b0000) => pick chan 1, unset
  0x01: 0x01 (0b0001) => pick chan 2, unset
  0x02: 0x02 (0b0010) => pick chan 3, unset
  0x03: 0x04 (0b0100) => pick chan 4, unset
  0x04: 0x08 (0b1000) => pick chan 1, set
  0x05: 0x09 (0b1001) => pick chan 2, set
  0x06: 0x0a (0b1010) => pick chan 3, set
  0x07: 0x0c (0b1100) => pick chan 4, set
  0x08: 0xde          => wait by 'value' amount
  0x09: 0x69          => jump to 'value' addr
```
