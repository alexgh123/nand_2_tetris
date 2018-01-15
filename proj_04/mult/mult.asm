// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2                     //create new varible R2 is the variable that will hold the total
M=0                     // set @R2/@total to 0

(LOOP)                  // begin loop :/

  @R0                  // end loop block:
  D=M                  // populate the D register with the value from R0
  @END
  D;JEQ                // IF D is Zero, jump to END

  @R1
  D=M                  // populate the D register with the value from R1

  @R2
  M=M+D                // reasssign R2 to the former value of R2 + D (R1)

  @R0
  M=M-1                // reassign R0 to the former value of R0 - 1

  @LOOP
  0;JMP                //   loop


(END)                  // end loop block

@END
0;JMP
