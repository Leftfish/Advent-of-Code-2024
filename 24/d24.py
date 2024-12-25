import os

import re
from collections import deque, defaultdict

import graphviz

DAY = 24

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


def parse(data):
    wires = {}
    gates = []
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
        gates.append(new_gate)

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


def run_gates(wires, exec_queue, wire_to_gate):
    while exec_queue:
        to_exec = exec_queue.popleft()
        target = to_exec.out
        result = to_exec.exec(wires)
        #print(f'Executing {to_exec}. {result} ---> {target}.')
        wires[target] = result
        for potential_next in wire_to_gate[target]:
            if potential_next not in exec_queue and potential_next.ready(wires):
                exec_queue.append(potential_next)
    #print(wires)
    return get_z(wires)[1]


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
print(f'Day {DAY} of Advent of Code!')
print('Testing...')
print('Number:', run_gates(wires, exec_queue, wire_to_gate) == 2024)

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    wires, gates, exec_queue, wire_to_gate = parse(data)
    print('Number:', run_gates(wires, exec_queue, wire_to_gate))

### And now for something completely differnt. A couple of helpers to tinker with the gates
### and, most importantly, to render the whole blueprint of the adder.

def render():
    gates_graph = graphviz.Digraph('Day 24', format='png')
    shapes = {'XOR': 'invhouse', 'AND': 'polygon', 'OR': 'ellipse', 'wire': 'point'}

    for i, gate in enumerate(gates):
        gate_name = type(gate).__name__
        gate_id = f'gate {i}'
        gates_graph.node(gate_id, f'{gate_name} ({i})', shape=shapes[gate_name])
        a = gate.a
        b = gate.b
        o = gate.out
        gates_graph.node(a, a, shape='point')
        gates_graph.edge(a, gate_id, label=a)
        gates_graph.node(b, b, shape='point')
        gates_graph.edge(b, gate_id, label=b)
        gates_graph.node(o, o, shape='point')
        gates_graph.edge(gate_id, o, label=o)

    gates_graph.renderer = 'cairo'
    gates_graph.render()

def reset(wires):
    for i in range(46):
        x = f'x{str(i).zfill(2)}'
        y = f'y{str(i).zfill(2)}'
        wires[x] = 0
        wires[y] = 0

def get_x(wires):
    number = ''
    for wire in sorted(wires):
        if wire.startswith('x'):
            number += str(wires[wire])
    number = '0b' + number[::-1]
    return number, int(number, 2)

def get_y(wires):
    number = ''
    for wire in sorted(wires):
        if wire.startswith('y'):
            number += str(wires[wire])
    number = '0b' + number[::-1]
    return number, int(number, 2)

def setx(id, val):
    x = f'x{str(id).zfill(2)}'
    wires[x] = val

def sety(id, val):
    y = f'y{str(id).zfill(2)}'
    wires[y] = val

### This was used to check how subsequent bits are handled...

wires, gates, exec_queue, wire_to_gate = parse(data)
#render()
reset(wires)
setx(0, 1)
sety(0, 1)
run_gates(wires, exec_queue, wire_to_gate)
print(get_x(wires))
print(get_y(wires))
print('-----')
print(get_z(wires))
print(get_x(wires)[1] + get_y(wires)[1] == get_z(wires)[1])

### And finally the solution that I discovered by analyzing the rendered graph

def repair_gates(gates):
    gates[1].out = 'gpr'
    gates[59].out = 'z10'
    gates[111].out = 'nks'
    gates[7].out = 'z21'
    gates[109].out = 'ghp'
    gates[2].out = 'z33'
    gates[24].out = 'krs'
    gates[91].out = 'cpm'
    print(','.join(sorted(list(gates[i].out for i in (1, 59, 7, 111, 109, 2, 24, 91)))))
