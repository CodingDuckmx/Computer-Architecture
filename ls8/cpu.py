"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [number for number in range(256)]
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4 
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.program = [
            # Default program
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

    def ram_read(self,MAR):

        return self.ram[MAR]

    def ram_write(self, MAR, MDR):

        self.ram[MAR] = MDR

    def halt(self):

        sys.exit()

    def ldi(self,LDI,value):

        self.reg[LDI] = value

    def prn(self,value):

        print(self.reg[value])


    def load(self, program_route=None):
        """Load a program into memory."""

        address = 0

        if not program_route:

            program = self.program

        else:

            program = []

            with open(program_route) as f:

                for line in f:

                    if line[0].isdigit():

                        program.append(int(line[:8].split('#',1)[0],2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        print(program)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        running = True

        while running:

            IR = self.ram_read(self.pc)

            if IR == self.LDI:

                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)

                self.ldi(operand_a,operand_b)

                self.pc += 3
           
            elif IR == self.PRN:

                operand_a = self.ram_read(self.pc + 1)
                self.prn(operand_a)

                self.pc += 2

            elif IR == self.HLT:

                self.halt()

            elif IR == self.MUL:

                self.alu('MUL',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.PUSH:
                
                # Decrement the SP

                self.reg[self.sp] -= 1 

                # Copy the register value into SP's location
                # Get the reg num to push

                # reg_num = self.ram[self.pc + 1]

                # # Get the value to push

                # value = self.reg[reg_num]

                # # Copy the value to the SP's location

                # top_of_the_stack = self.reg[self.sp]

                # self.ram_write(top_of_the_stack,value)
                
                # In one line:
                self.ram_write(self.reg[self.sp],self.reg[self.ram[self.pc + 1]])


                self.pc += 2

            elif IR == self.POP:

                # Copy the value from SP's location to the register
                # Get the register number to pop into
                
                # reg_num = self.ram[self.pc +1]

                # # Get the top of the stack address

                # top_of_stack_addr = self.reg[self.sp]

                # # Get the value of the top of the stack

                # value = self.ram_read(top_of_stack_addr)

                # # Store the value into the register

                # self.reg[reg_num] = value

                # In one line:

                self.reg[self.ram_read(self.pc +1)] = self.ram_read(self.reg[self.sp])


                # Increment the SP
                
                self.reg[self.sp] += 1

                self.pc += 2


            else:

                print(f'Unknown instruction {IR}')
                
                self.pc += 1
                
        