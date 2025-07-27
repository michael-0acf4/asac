# asac

A Simple Audio Chip (ASAC) is a simple chip in which we can write programs that
mimics the MIDI format.

It currently supports 4 channels.

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
  0x00: 0x08 (0b00001000) => pick chan 1, unset
  0x01: 0x09 (0b00001001) => pick chan 2, unset
  0x02: 0x0a (0b00001010) => pick chan 3, unset
  0x03: 0x0c (0b00001100) => pick chan 4, unset
  0x04: 0x18 (0b00011000) => pick chan 1, set
  0x05: 0x19 (0b00011001) => pick chan 2, set
  0x06: 0x1a (0b00011010) => pick chan 3, set
  0x07: 0x1c (0b00011100) => pick chan 4, set
  0x08: 0xe0 (0b11100000) => wait by 'value' amount
  0x09: 0x69 (0b01101001) => jump to 'value' addr
```
