# Capstone Project: Make the Computer Draw a Box
Nand to Tetris - I (ETCCNT301), K.R. Mangalam University

- Roll No: 2501360014
- K = 14
- Box: starts at row 14, 20 rows tall, 48 pixels (3 words) wide, from left edge
- Assembler extra feature (K mod 3 = 2): warning for duplicate labels

## Files
| File | Part | Description |
|---|---|---|
| CPU.hdl, Memory.hdl, Computer.hdl | A | Computer built from built-in chips (ALU, ARegister, DRegister, PC, RAM16K, Screen, Keyboard, ROM32K) |
| assembler.py | B | Two-pass Hack assembler in Python |
| Box.asm / Box.hack | C | Box program and its output from my own assembler |
| tests/ | B | Add.asm, Max.asm, DuplicateLabel.asm |
| screenshots/ | A, C | Test and emulator screenshots (add yours) |

## Usage
    python assembler.py Box.asm            # creates Box.hack
    python assembler.py tests/DuplicateLabel.asm
    # -> Warning: Line 3: label 'LOOP' is defined more than once

## Note on Part A
CPU/Memory/Computer use built-in chips for ALU, registers, PC and RAM.
If you wrote your own versions in the lab, copy them into this folder and mention it in the report.
