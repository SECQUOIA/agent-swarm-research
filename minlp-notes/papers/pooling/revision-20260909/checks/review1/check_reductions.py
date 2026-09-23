"""Independent exact forward-flow checks; these do not prove soundness."""
from fractions import Fraction as F
from collections import Counter


class Network:
    def __init__(self):
        self.nodes = {}
        self.arcs = {}
        self.storage = []

    def node(self, kind, cap, quality=None, marked=False):
        name = f"{kind}{len(self.nodes)}"
        self.nodes[name] = dict(kind=kind, cap=cap, quality=quality, marked=marked)
        return name

    def arc(self, u, v, amount):
        assert (u, v) not in self.arcs
        self.arcs[u, v] = F(amount)

    def store(self, source, amount):
        p = self.node('p', None, marked=True)
        d = self.node('i', None, F(0))
        j = self.node('j', None)
        self.arc(source, p, amount)
        self.storage.append((p, d, j, amount))
        return p

    def emit(self, p, intake):
        j = self.node('j', F(2), F(1, 2), True)
        h = self.node('p', F(2))
        r = self.node('i', F(2), F(0), True)
        self.arc(p, j, 1/intake)
        self.arc(r, h, 2-1/intake)
        self.arc(h, j, 2-1/intake)
        return r, 1/intake

    def convert(self, source, amount):
        h0 = self.node('p', F(2))
        h1 = self.node('p', F(2))
        j = self.node('j', F(2), marked=True)
        r = self.node('i', F(2), F(1), True)
        self.arc(source, h0, amount)
        self.arc(h0, j, amount)
        self.arc(r, h1, 2-amount)
        self.arc(h1, j, 2-amount)
        return r, amount

    def finish(self):
        outdegree = Counter(u for u, _ in self.arcs)
        B = 2*max(outdegree[p] for p, *_ in self.storage)+3
        for p, d, j, a in self.storage:
            for node in (p, d, j):
                self.nodes[node]['cap'] = F(B)
            self.arc(d, p, B-a)
            self.arc(p, j, B-sum(v for (u, _), v in self.arcs.items() if u == p))
        for node in self.nodes.values():
            if node['kind'] == 'j' and node['quality'] is not None:
                node['quality'] /= B
        return B

    def check(self):
        incoming, outgoing = Counter(), Counter()
        indegree, outdegree = Counter(), Counter()
        for (u, v), amount in self.arcs.items():
            assert amount >= 0
            assert (self.nodes[u]['kind'], self.nodes[v]['kind']) in [('i', 'p'), ('p', 'j')]
            incoming[v] += amount
            outgoing[u] += amount
            indegree[v] += 1
            outdegree[u] += 1
        quality = {u: n['quality'] for u, n in self.nodes.items() if n['kind'] == 'i'}
        for p, node in self.nodes.items():
            if node['kind'] == 'p':
                assert incoming[p] == outgoing[p]
                mass = sum(quality[u]*v for (u, w), v in self.arcs.items() if w == p)
                quality[p] = mass/incoming[p] if incoming[p] else F(0)
        profit = F(0)
        for u, node in self.nodes.items():
            total = incoming[u] if node['kind'] == 'j' else outgoing[u]
            assert 0 <= total <= node['cap']
            if node['marked']:
                assert total == node['cap']
                profit += total
            if node['kind'] == 'i':
                assert outdegree[u] <= 2
            else:
                assert indegree[u] <= 2
            if node['kind'] == 'p' and not node['marked']:
                assert outdegree[u] == 1
            if node['kind'] == 'j':
                mass = sum(quality[v]*a for (v, w), a in self.arcs.items() if w == u)
                if node['quality'] is None:
                    assert 0 <= mass <= total
                else:
                    assert mass == node['quality']*total
        assert profit == sum(n['cap'] for n in self.nodes.values() if n['marked'])
        return len(self.nodes), len(self.arcs), sum(v == 0 for v in self.arcs.values())


values = dict(a=F(1,2), b=F(2), c=F(1), unused=F(3,2))
inversions = [('a', 'b'), ('c', 'c')]*12
additions = [('a', 'a', 'c'), ('c', 'c', 'b')]*12
net = Network()
stores = {}
for v, x in values.items():
    s = net.node('i', F(5,2), F(1), True)
    for label, a in [('P', x), ('barP', F(5,2)-x)]:
        p = net.store(s, a)
        stores[v, label] = p, a
        r, amount = net.convert(*net.emit(p, a))
        stores[v, 'R' if label == 'P' else 'barR'] = net.store(r, amount), amount
for x, y in inversions:
    r, amount = net.emit(*stores[y, 'barR'])
    h = net.node('p', F(5,2))
    j = net.node('j', F(5,2), F(2,5), True)
    net.arc(r, h, amount)
    net.arc(h, j, amount)
    net.arc(stores[x, 'P'][0], j, values[y])
for x, y, z in additions:
    h = net.node('p', F(4))
    j = net.node('j', F(5,2), F(2,5), True)
    for v in (x, y):
        r, amount = net.emit(*stores[v, 'R'])
        net.arc(r, h, amount)
    net.arc(h, j, values[x]+values[y])
    net.arc(stores[z, 'barR'][0], j, F(5,2)-values[z])
B = net.finish()
print('Many-pool construction:', net.check(), '(nodes, arcs, zero-flow arcs); B =', B)

# Pin algebra and capacity completion for the one-pool construction.
# Normalize repeated summands by the exact two-inversion copy gadget.
normalized = []
for i, (x, y, z) in enumerate(additions):
    if x == y:
        u, copy = f'inverse{i}', f'copy{i}'
        values[u], values[copy] = 1/values[x], values[x]
        inversions.extend([(x, u), (u, copy)])
        y = copy
    normalized.append((x, y, z))
auxiliary = []
covered = set()
for x, y in inversions:
    a, b = values[y], 1/values[y]
    assert values[x]*a == a*b == values[y]*b == 1
    auxiliary.extend([a, b])
    covered.update((x, y))
for x, y, z in normalized:
    a = 2/values[z]
    assert values[z]*a == (values[x]+values[y])*a == 2
    auxiliary.append(a)
for v in values.keys()-covered:
    a = 1/values[v]
    assert values[v]*a == 1
    auxiliary.append(a)
assert all(F(1,2) <= a <= 2 for a in auxiliary)
B = 4*(len(values)+len(auxiliary))
filler, slack = B-sum(values.values())-sum(auxiliary), B-sum(auxiliary)
assert B/2 <= filler <= B and B/2 <= slack <= B
assert sum(values.values())+sum(auxiliary)+filler == sum(auxiliary)+slack == B
assert all(0 <= 2-a <= 2 for a in auxiliary)
print('One-pool construction: exact pins, range, complements, filler and slack passed;', len(auxiliary), 'auxiliaries; B =', B)
