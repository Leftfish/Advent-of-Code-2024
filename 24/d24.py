import os

import re
from collections import deque, defaultdict

DAY = 23


class Gate:
    def __init__(self, name, a=None, b=None, out=None):
        self.name = name
        self.a = a
        self.b = b
        self.out = out

    def __repr__(self):
        return f'{self.a} {type(self).__name__} {self.b} => {self.out}'

    def ready(self, wires):
        return wires[self.a] is not None and wires[self.b] is not None
    
    def exec(self, wires):
        raise NotImplementedError

class AND(Gate):
    def exec(self, wires):
        return wires[self.a] & wires[self.b]
    
class OR(Gate):
    def exec(self, wires):
        return wires[self.a] | wires[self.b]

class XOR(Gate):
    def exec(self, wires):
        return wires[self.a] ^ wires[self.b]


TEST_DATA = '''x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02'''



def parse(data):
    wires = {}
    gates = set()
    exec_queue = deque()
    wire_to_gate = defaultdict(list)
    
    wire_regex = r'(\w+): (\d)'
    gate_regex = r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)'
    name_to_type = {'AND': AND, 'OR': OR, 'XOR': XOR}
    
    raw_wires, raw_gates = data.split('\n\n')

    for raw_wire in raw_wires.splitlines():
        name, value = re.findall(wire_regex, raw_wire)[0]
        wires[name] = int(value)
    
    for i, raw_gate in enumerate(raw_gates.splitlines()):
        in_left, gate_type, in_right, out = re.findall(gate_regex, raw_gate)[0]

        if in_left not in wires:
            wires[in_left] = None
        if in_right not in wires:
            wires[in_right] = None
        if out not in wires:
            wires[out] = None

        new_gate = name_to_type[gate_type](name=i, a=in_left, b=in_right, out=out)
        gates.add(new_gate)

        wire_to_gate[in_left].append(new_gate)
        wire_to_gate[in_right].append(new_gate)

        if new_gate.ready(wires):
            exec_queue.append(new_gate)
    
    return wires, gates, exec_queue, wire_to_gate

def get_z(wires):
    number = ''
    for wire in sorted(wires):
        if wire.startswith('z'):
            number += str(wires[wire])
    number = '0b' + number[::-1]
    return number, int(number, 2)

TEST_DATA = '''x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj'''



wires, gates, exec_queue, wire_to_gate = parse(TEST_DATA)

while exec_queue:
    to_exec = exec_queue.popleft()
    target = to_exec.out
    result = to_exec.exec(wires)
    wires[target] = result
    for potential_next in wire_to_gate[target]:
        if potential_next not in exec_queue and potential_next.ready(wires):
            exec_queue.append(potential_next)

print(get_z(wires))


print(f'Day {DAY} of Advent of Code!')
print('Testing...')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()

