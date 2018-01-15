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

(START)
  @SCREEN
  D=A                   // put 16384 into D register
  @PIXEL_LOCATION
  M=D                   // put 16384 into pixel location pointer
  @FINAL_PIXEL
  M=D                   // * put 16384 into FINAL PIXEL
  @8192
  D=A
  @FINAL_PIXEL
  M=M+D                 // create FINAL_PIXEL value = 16384+8192

(KEYBOARD_LISTNER)      // loop that listens for change in KBD input
  @PAINT_BUCKET
  M=0
  @KBD
  D=M
  @COLOR_LOOP           // if the keyboard is zero, paint screen white
  D;JEQ
  @PAINT_BUCKET
  M=-1
  @COLOR_LOOP           // if the keyboard is not 0, paint the screen black
  0;JMP

(COLOR_LOOP)            // this loop will paint current pixel black or white
  @PAINT_BUCKET
  D=M                   // dip the paint brush (aka D) into the bucket
  @PIXEL_LOCATION
  A=M
  M=D                   // paint the current pixel value either black or white
  @PIXEL_LOCATION
  M=M+1                 // increment pixel location by 1
  D=M
  @FINAL_PIXEL
  A=M-D                 // FINAL_PIXEL - CURRENT_PIXEL
  D=A
  @START
  D;JEQ                 // if FINAL_PIXEL- CURRENT_PIXEL = 0 then jump to reseting pixel location

@KEYBOARD_LISTNER       // loop for new keyboard input
0;JMP