import os

import re

from numpy import base_repr

DAY = 17

A = 'A'
B = 'B'
C = 'C'

class Computer:
    def __init__(self, instructions=[], init_a=0, init_b=0, init_c=0):
        self.registers = {A: init_a, B: init_b, C: init_c}
        self.instructions = [int(instruction) for instruction in instructions]
        self.ptr = 0
        self.running = True
        self.output = []
        self.debug = False

    def __repr__(self):
        return f'A: {base_repr(self.registers[A], 8)}, B: {base_repr(self.registers[B], 8)}, C: {base_repr(self.registers[C],8)}, PTR: {self.ptr}, OUT: {self.output}'

    def _parse_instruction(self):
        instruction_id = self.instructions[self.ptr]
        raw_operand = self.instructions[self.ptr+1]

        opcodes = {0: self.adv,
                   1: self.bxl,
                   2: self.bst,
                   3: self.jnz,
                   4: self.bxc,
                   5: self.out,
                   6: self.bdv,
                   7: self.cdv}
        
        self.combo_operands = {0: 0,
                                1: 1,
                                2: 2,
                                3: 3,
                                4: self.registers[A],
                                5: self.registers[B],
                                6: self.registers[C],
                                7: None}

        return opcodes[instruction_id], raw_operand, self.combo_operands[raw_operand]

    def adv(self, operand, combo):
        result = self.registers[A] >> combo
        self.registers[A] = result
        if self.debug:
            print(f'{self.ptr} => A DIV => A = A >> {combo} res: {base_repr(result, 8)}')
        self.ptr += 2

    def bdv(self, operand, combo):
        result = self.registers[A] >> combo
        self.registers[B] = result
        if self.debug:
            print(f'{self.ptr} => B DIV => B = A >> {combo} res: {base_repr(result, 8)}')
        self.ptr += 2

    def cdv(self, operand, combo):
        result = self.registers[A] >> combo
        self.registers[C] = result
        if self.debug:
            print(f'{self.ptr} => C DIV => C = A >> {combo} res: {base_repr(result, 8)}')
        self.ptr += 2

    def bxl(self, operand, combo):
        result = self.registers[B] ^ operand
        self.registers[B] = result
        if self.debug:
            print(f'{self.ptr} => B XOR LIT => B = B ^ {operand} res: {base_repr(result, 8)})')
        self.ptr += 2

    def bxc(self, operand, combo):
        result = self.registers[B] ^ self.registers[C]
        self.registers[B] = result
        if self.debug:
            print(f'{self.ptr} => B XOR C => B = B ^ C res: {base_repr(result, 8)})')
        self.ptr += 2
    
    def bst(self, operand, combo):
        result = combo % 8
        self.registers[B] = result
        if self.debug: 
            print(f'{self.ptr} => {[k for k, v in self.registers.items() if v == combo][0]} % 8 => B = {base_repr(combo, 8)} % 8  (res: {base_repr(result, 8)})')
        self.ptr += 2

    def jnz(self, operand, combo):
        if self.registers[A] == 0:
            if self.debug:
                print(f'{self.ptr} ==> JNZ; NO JUMP')
            self.ptr += 2
        else:
            if self.debug:
                print(f'{self.ptr} ==> JNZ; JUMP TO {operand}')
            self.ptr = operand

    def out(self, operand, combo):
        result = combo % 8
        self.output.append(result)
        if self.debug:
            print(f'{self.ptr} ==> OUTPUT {base_repr(combo, 8)} % 8 (res: {base_repr(result, 8)})')
        self.ptr += 2

    def exec(self):
        if self.ptr >= len(self.instructions):
            self.running = False
            if self.debug:
                print(f'{self.ptr} ==> EOF')
        else:
            if self.debug: 
                print('     Status:', self)
            instruction, operand, combo = self._parse_instruction()
            instruction(operand, combo)

    def run(self, debug=False):
        self.debug = debug
        while self.running:
            self.exec()
            
def find_quine(expected):
    # our program is 16 digits long and works in octal
    # LOW = 35184372088832 or 1000000000000000 base 8
    # HI = 281474976710655 or 7777777777777777 base 8
    # initiate the input for register A (will be octal)
    zeroes = ['0' for i in range(16)]
    Comp = Computer(expected, 0, 0, 0)

    stack = []
    # this is a DFS
    initial = (zeroes, 0)
    stack.append(initial)

    while stack:
        state, digit = stack.pop()

        for d in range(8):
            # make a new base8 candidate
            new = state.copy()
            new[digit] = str(d)
            octal = f"0o{''.join(new)}"
            # convert to base 10 to input to register A
            register = int(octal, 8)
            
            # reset computer
            Comp.registers[A] = register
            Comp.registers[B] = 0
            Comp.registers[C] = 0
            Comp.output = []
            Comp.ptr = 0
            Comp.running = True
            
            # run computer and test
            Comp.run()
            match = Comp.output[-digit-1] == Comp.instructions[-digit-1]

            # found it, return!
            if Comp.output == Comp.instructions:
                return register

            # not found yet but match at the next octal digit, so advance
            if match:
                new_state = (new.copy(), digit + 1)
                stack.append(new_state)


def parse(data):
    regex = r'Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.+)'
    a, b, c, instructions = re.findall(regex, data)[0]
    instructions = instructions.split(',')
    return int(a), int(b), int(c), instructions


input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    data = inp.read()
    a, b, c, prog = parse(data)
    Comp = Computer(prog,a,b, c)
    Comp.run()
    print('Result of first run:', ','.join([str(d) for d in Comp.output]))
    print('Quine is:', find_quine(prog))