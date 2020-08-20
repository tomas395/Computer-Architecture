import sys

"""CPU functionality."""

ADD = 0b10100000  # Add the values in two registers together and store the result in registerA.
DIV = 0b10100011  # Divide the values in two registers together and store the result in registerA.
HLT = 0b00000001  # Halt the CPU (and exit the emulator).
LDI = 0b10000010  # Set the value of a register to an integer.
MUL = 0b10100010  # Multiply the values in two registers together and store the result in registerA.
POP = 0b01000110  # Pop the value at the top of the stack into the given register.
PRN = 0b01000111  # Print numeric value stored in the given register.
PUSH = 0b01000101  # Push the value in the given register on the stack.
SUB = 0b10100001  # You guessed right


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.ram = [0] * 256
        self.pc = 0
        self.halted = False

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""
        self.address = 0
        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    n = comment_split[0].strip()
                    if n == '':
                        continue

                    val = int(n, 2)
                    self.ram[self.address] = val
                    self.address += 1

        except FileNotFoundError:
            print(f"{sys.argv[1]}: {filename} not found! Check to see if your path is valid ♥♥♥")
            sys.exit()

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            IR = self.ram[self.pc]  # `IR`: Instruction Register , contains a copy of the currently executing instruction
            instruction_length = ((IR >> 6) & 0b11) + 1  # (bitshifted instruction)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            # HLT: Halt the CPU (and exit the emulator).
            if IR == HLT:
                print("Exiting the program!")
                self.halted = True

            # LDI: Set the value of a register to an integer.
            elif IR == LDI:
                self.reg[op_a] = op_b

            # PRN: Print numeric value stored in the given register.
            elif IR == PRN:
                print("The answer is:", self.reg[op_a])

            # MUL: Multiply the values in two registers together and store the result in registerA.
            # expecting a number of 72
            elif IR == MUL:
                self.alu("MUL", op_a, op_b)

            elif IR == ADD:
                self.alu("ADD", op_a, op_b)

            # PUSH: Push the value in the given register on the stack.
            elif IR == PUSH:
                reg_index = self.ram[self.pc + 1]
                val = self.reg[reg_index]
                self.reg[7] -= 1
                SP = self.reg[7]
                self.ram[SP] = val
                self.pc += 2

            # POP: Pop the value at the top of the stack into the given register.
            elif IR == POP:
                reg_index = self.ram[self.pc + 1]
                val = self.ram[SP]
                self.reg[reg_index] = val
                SP = self.reg[7]
                self.reg[7] += 1
                self.pc += 2

            self.pc += instruction_length
