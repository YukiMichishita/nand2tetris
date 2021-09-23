// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
    // i = 0
    @i
    M=0
 
    //if M[KBD]>0 then goto SCREEN_BRACK
    @KBD
    D=M
    @SCREEN_BLACK
    D;JGT

    (SCREEN_WHITE)
        //M[SCREEN+i]=0
        @i
        D=M
        @SCREEN
        A=D+A
        M=0
        //i++
        @i
        M=M+1
        @i
        D=M
        //i<8192 then goto SCREEN_WHITE
        @8191
        D=D-A
        @SCREEN_WHITE
        D;JLE
        @LOOP
        0;JMP

    (SCREEN_BLACK)
        //M[SCREEN+i]=-1
        @i
        D=M
        @SCREEN
        A=D+A
        M=-1
        //i++
        @i
        M=M+1
        @i
        D=M
        //i<8192 then goto SCREEN_BLACK
        @8191
        D=D-A
        @SCREEN_BLACK
        D;JLE
        @LOOP
        0;JMP
         