// Box.asm  -  K = 14
// Box: starts at row 14, 20 rows tall, 48 pixels (3 words) wide, from left edge.
// While any key is pressed -> black box. Key released -> box erased.
// Row r starts at SCREEN + 32*r  ->  16384 + 32*14 = 16832

(MAIN)
    @KBD
    D=M
    @BLACK
    D;JNE          // key pressed -> black
    @color
    M=0            // no key -> white
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1           // all 16 pixels black

(DRAW)
    @16832
    D=A
    @addr
    M=D            // addr = start of row 14
    @20
    D=A
    @rows
    M=D            // rows = 20

(ROW)
    @3
    D=A
    @cols
    M=D            // cols = 3 words per row
    @addr
    D=M
    @p
    M=D            // p = pointer inside current row

(COL)
    @color
    D=M
    @p
    A=M
    M=D            // write one word
    @p
    M=M+1
    @cols
    M=M-1
    D=M
    @COL
    D;JGT

    @32
    D=A
    @addr
    M=D+M          // addr += 32 (next screen row)
    @rows
    M=M-1
    D=M
    @ROW
    D;JGT

    @MAIN
    0;JMP
