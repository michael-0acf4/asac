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
JUMP            [       label        ]
```

# Microcode Spec

```
microcode
opcode       
  0x00: 0x28 (0b00101000) => pick chan 1, unset
  0x01: 0x29 (0b00101001) => pick chan 2, unset
  0x02: 0x2a (0b00101010) => pick chan 3, unset
  0x03: 0x2c (0b00101100) => pick chan 4, unset
  0x04: 0x38 (0b00111000) => pick chan 1, set
  0x05: 0x39 (0b00111001) => pick chan 2, set
  0x06: 0x3a (0b00111010) => pick chan 3, set
  0x07: 0x3c (0b00111100) => pick chan 4, set
                  ^^^
                  ||+ -- enable
                  |+ --- on/off speaker
                  +----- set kind flag (always 0 on other micro-instructions)
  0x08: 0xde (0b11011110) => wait by 'value' amount
  0x09: 0x42 (0b01000010) => jump to 'value' addr
```
