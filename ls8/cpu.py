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

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        filename = sys.argv[1]

        file = open(filename, 'r')
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

                self.pc += 3
            # PRN
            if ir == 0b01000111:
                reg_num = self.ram[self.pc + 1]
                print(self.registers[reg_num])

                self.pc += 1
            # MULT
            if ir == 0b10100010:
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("MULT", a, b)

                self.pc += 3
            # HALT
            elif ir == 0b00000001:
                running = False

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
