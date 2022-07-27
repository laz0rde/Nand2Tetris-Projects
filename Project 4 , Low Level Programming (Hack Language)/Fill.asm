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

// check is any key is pressed







(KLOOP)
@KBD
D=M

@WHITELOOP
D; JEQ

(BLACKLOOP)
@SCREEN
D=A

@addr
M=D

@i
M=0

@8170
D=A

@n
M=D

(LOOP)
@i
D=M

@n
D=D-M

@KLOOP
D; JGT

@addr
A=M
M=-1

@i
M=M+1

@1
D=A

@addr
M=D+M

@LOOP
0; JMP

(WHITELOOP)
@SCREEN
D=A

@addr
M=D

@i
M=0

@8170
D=A

@n
M=D

(LOOP1)
@i
D=M

@n
D=D-M

@KLOOP
D; JGT

@addr
A=M
M=0

@i
M=M+1

@1
D=A

@addr
M=D+M

@LOOP1
0; JMP
