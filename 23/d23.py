import os

import networkx as nx

DAY = 23


def parse(data):
    graph = nx.Graph()
    for line in data.splitlines():
        this, other = line.split('-')
        if this not in graph:
            graph.add_node(this)
        if other not in graph:
            graph.add_node(other)
        graph.add_edge(this, other)
    return graph


def solve_networkx(graph):
    s = set()
    for clique in [cl for cl in nx.enumerate_all_cliques(G) if len(cl) == 3]:
        for node in clique:
            if node.startswith('t'):
                s.add(tuple(clique))
    password = ','.join(sorted(sorted(list(nx.find_cliques(graph)), key=lambda cl: len(cl))[-1]))
    return len(s), password


TEST_DATA = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn'''


print(f'Day {DAY} of Advent of Code!')
print('Testing...')
G = parse(TEST_DATA)
candidates, password = solve_networkx(G)
print('Candidate cycles:', candidates == 7)
print('Password:', password == 'co,de,ka,ta')

input_path = f"{os.getcwd()}\\{str(DAY).zfill(2)}\\inp"
with open(input_path, mode='r', encoding='utf-8') as inp:
    print('Solution...')
    data = inp.read()
    G = parse(data)
    candidates, password = solve_networkx(G)
    print('Candidate cycles:', candidates)
    print('Password:', password)
