"""CPU functionality."""

import sys
from sys import argv


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.SP = 7
        self.registers[self.SP] = 0xf4
        self.FL = 0b00000000

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        filename = sys.argv[1]

        file = open(
            filename, 'r')
        lines = file.readlines()

        for line in lines:

            temp = line.split()
            line = line.strip()

            if len(temp) == 0:
                continue

            if temp[0][0] == "#":
                continue

            try:
                self.ram[address] = int(temp[0], 2)

            except ValueError:
                print(f"Invalid number: {temp[0]}")
                sys.exit(1)

            address += 1

        # print(self.ram[:10])
        # sys.exit(0)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        # elif op == "SUB": etc
        if op == "MULT":
            self.registers[reg_a] *= self.registers[reg_b]
        # `FL` bits: `00000LGE`
        if op == "CMP":
            if self.registers[reg_a] == self.registers[reg_b]:
                self.FL = 0b00000001
            if self.registers[reg_a] > self.registers[reg_b]:
                self.FL = 0b00000010
            if self.registers[reg_a] < self.registers[reg_b]:
                self.FL = 0b00000100

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
        running = True
        while running:
            ir = self.ram[self.pc]
            # LDI
            if ir == 0b10000010:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.registers[reg_num] = value
                # print(reg_num, value)

                self.pc += 3
            # PRN
            elif ir == 0b01000111:
                reg_num = self.ram[self.pc + 1]
                print(self.registers[reg_num])

                self.pc += 2
            # MULT
            elif ir == 0b10100010:
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("MULT", a, b)

                self.pc += 3

            # PUSH
            elif ir == 0b01000101:
                # self.SP = self.registers[7]
                self.registers[self.SP] -= 1
                self.ram_write(self.registers[self.ram_read(
                    self.pc + 1)], self.registers[self.SP])
                self.pc += 2

            # POP
            elif ir == 0b01000110:
                # self.SP = self.registers[7]
                self.registers[self.ram_read(
                    self.pc + 1)] = self.ram_read(self.registers[self.SP])
                self.registers[self.SP] += 1
                self.pc += 2

            # # CALL
            # if ir == 0b01010000:
            #     # Push return address
            #     ret_addr = self.pc + 2
            #     self.registers[self.SP] -= 1
            #     self.ram[self.registers[self.SP]] = ret_addr

            #     # Call the subroutine
            #     reg_num = self.ram[self.pc + 1]
            #     self.pc = self.registers[reg_num]

            #     self.pc += 2

            # # RET
            # if ir == 0b00010001:
            #     # Pop the return addr off the stack
            #     ret_addr = self.ram[self.registers[self.SP]]
            #     self.registers[self.SP] += 1
            #     # Set the PC to it
            #     self.pc = ret_addr

            # CMP
            elif ir == 0b10100111:
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("CMP", a, b)

                self.pc += 3

            # JMP
            # `FL` bits: `00000LGE`
            elif ir == 0b01010100:
                self.pc = self.registers[self.ram_read(self.pc + 1)]

            # JEQ
            elif ir == 0b01010101:
                if self.FL & 0b00000001 == 1:
                    self.pc = self.registers[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2

            # JNE
            elif ir == 0b01010110:
                if self.FL & 0b00000001 == 0:
                    self.pc = self.registers[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2

            # HALT
            elif ir == 0b00000001:
                running = False

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
