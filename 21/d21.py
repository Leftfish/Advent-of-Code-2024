import os

import networkx as nx
from itertools import product

DAY = 21

TEST_DATA = '''029A
980A
179A
456A
379A'''

NUMPAD = '''789
456
123
.0A'''

KEYPAD = '''.^A
<v>'''

ENTER = 'A'

U, D, L, R, A = '^', 'v', '<', '>', 'A'

NUMPAD_DIRECTIONS = {('0', 'A'): R,
                      ('A', '0'): L,
                      ('1', '2'): R,
                      ('2', '1'): L,
                      ('2', '3'): R,
                      ('3', '2'): L,
                      ('4', '5'): R,
                      ('5', '4'): L,
                      ('5', '6'): R,
                      ('6', '5'): L,
                      ('7', '8'): R,
                      ('8', '7'): L,
                      ('8', '9'): R,
                      ('9', '8'): L,
                      ('1', '4'): U,
                      ('4', '1'): D,
                      ('4', '7'): U,
                      ('7', '4'): D,
                      ('0', '2'): U,
                      ('2', '0'): D,
                      ('2', '5'): U,
                      ('5', '2'): D,
                      ('5', '8'): U,
                      ('8', '5'): D,
                      ('A', '3'): U,
                      ('3', 'A'): D,
                      ('3', '6'): U,
                      ('6', '3'): D,
                      ('6', '9'): U,
                      ('9', '6'): D,
                      ('0', '0'): A,
                      ('1', '1'): A,
                      ('2', '2'): A,
                      ('3', '3'): A,
                      ('4', '4'): A,
                      ('5', '5'): A,
                      ('6', '6'): A,
                      ('7', '7'): A,
                      ('8', '8'): A,
                      ('9', '9'): A,
                      ('A', 'A'): A}

KEYPAD_DIRECTIONS = {('^', 'A'): R,
                     ('A', '^'): L,
                     ('<', 'v'): R,
                     ('v', '<'): L,
                     ('v', '>'): R,
                     ('>', 'v'): L,
                     ('v', '^'): U,
                     ('^', 'v'): D,
                     ('>', 'A'): U,
                     ('A', '>'): D,
                     ('A', 'A'): A,
                     ('>', '>'): A,
                     ('<', '<'): A,
                     ('v', 'v'): A,
                     ('^', '^'): A}

directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))

def get_paths(keyboard, keyboard_directions):

    grd = list(line for line in keyboard.splitlines())
    keyboard_graph = {}
    graph = nx.Graph()
    for i, line in enumerate(grd):
        for j, c in enumerate(line):
            if c != '.':
                keyboard_graph[(i, j)] = c
                graph.add_node(c)

    for k, v in keyboard_graph.items():
        i, j = k
        for direction in directions:
            di, dj = direction
            adj = (i+di, j+dj)
            if adj in keyboard_graph:
                graph.add_edge(v, keyboard_graph[adj])

    node_to_node = product(graph.nodes, graph.nodes)
    paths = {}
    for pair in node_to_node:
        start, end = pair
        paths[(start, end)] = nx.shortest_path(graph, start, end)
        paths[(end, start)] = nx.shortest_path(graph, end, start)


    proper_paths = {}
    for k, v in paths.items():
        steps = zip(v, v[1:])
        s = ''
        for step in steps:
            s += keyboard_directions[step]
        proper_paths[k] = s

    return proper_paths


numpad_paths = get_paths(NUMPAD, NUMPAD_DIRECTIONS)
keypad_paths = get_paths(KEYPAD, KEYPAD_DIRECTIONS)



to_write = list('v<<A>>^A<A>AvA<^AA>A<vAAA>^A')
steps = list(zip(to_write, to_write[1:]))
current = ENTER
nxt = steps[0][0]
steps.insert(0, (current, nxt))

total = ''
for pair in steps:
    total += keypad_paths[pair]
    total += ENTER
print(total)

### przekładanie ruchów na pady - działa bdb, te z przykładu przekłada jak trzeba
### brakuje optymalizacji (nie ma jednak ekwiwalentu między ścieżkami i Manhattan distance - to jak polecisz na pierwszym etapie skutkuje innymi ruchami na dalszych)
### więc może jednak wyszukiwać WSZYSTKIE SHORTEST PATHS OD KLAWISZA DO KLAWISZA???
### A POTEM WYGENEROWAĆ JE I WYBRAĆ NAJKRÓTSZĄ ŚCIEŻKĘ GDZIE NODE W GRAFIE TO JEST SHORTEST PATH OD KLAWISZA DO KLAWISZA
### PRZY CZYM TO ZNACZY, ŻE TRZEBA GENEROWAĆ TO TRZY RAZY (PIERWSZY STAN PO PIERWSZYM PILOCIE, KOLEJNY PO DRUGIM, KOLEJNY PO TRZECIM)
### czyli tak naprawdę: budujesz sobie graf stanów, gdzie kolejne stany zależą od tego, którą z najkrótszych ścieżek między przyciskami wybierzesz.
### całkiem prawdopodobne, że bez jakiegoś przycinania gałęzi się nie obejdzie

print(f'Day {DAY} of Advent of Code!')
print('Testing...')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()