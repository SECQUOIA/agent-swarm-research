"""Small exhaustive stationary-face checks; not an implementation of the bit algorithm."""
from itertools import combinations, product
from fractions import Fraction

import networkx as nx
import numpy as np
from scipy.optimize import linprog


def quadratic_candidates(Q, g, A, d):
    """Enumerate all independent active-normal sets, including singular systems."""
    dim = len(g)
    for count in range(dim + 1):
        for indices in combinations(range(len(d)), count):
            AI = A[list(indices)] if count else np.empty((0, dim))
            if count and np.linalg.matrix_rank(AI) < count:
                continue
            mat = np.block([[Q, -AI.T], [AI, np.zeros((count, count))]])
            rhs = np.r_[-g, d[list(indices)]]
            if np.linalg.matrix_rank(mat) == len(mat):
                point = np.linalg.solve(mat, rhs)[:dim]
                if np.max(A @ point - d) <= 1e-8:
                    yield point
            else:
                result = linprog(np.zeros(dim + count), A_ub=np.c_[A, np.zeros((len(d), count))],
                                 b_ub=d, A_eq=mat, b_eq=rhs,
                                 bounds=[(None, None)] * (dim + count), method='highs')
                if result.success:
                    yield result.x[:dim]


def path_family_member(tree, c, b, lower, upper, marked=None):
    if marked is None:
        marked = {v for v in tree if c[v] or tree.degree(v) >= 3}
    seen = set()
    for start in marked:
        for nxt in tree[start]:
            if frozenset((start, nxt)) in seen:
                continue
            path = [start, nxt]
            seen.add(frozenset((start, nxt)))
            while path[-1] not in marked:
                v = next(v for v in tree[path[-1]] if v != path[-2])
                seen.add(frozenset((path[-1], v)))
                path.append(v)
            cut = tree.copy()
            cut.remove_edge(path[0], path[1])
            weight = sum(c[v] for v in nx.node_connected_component(cut, start))
            assert weight != 0
            inner = path[1:-1]
            early, late = (upper, lower) if weight > 0 else (lower, upper)
            found = False
            for pivot in range(len(inner)):
                if (all(abs(b[v]-early[v]) < 1e-7 for v in inner[:pivot]) and
                    all(abs(b[v]-late[v]) < 1e-7 for v in inner[pivot+1:])):
                    found = True
            for split in range(len(inner)+1):
                if (all(abs(b[v]-early[v]) < 1e-7 for v in inner[:split]) and
                    all(abs(b[v]-late[v]) < 1e-7 for v in inner[split:])):
                    found = True
            if not found:
                return False
    return True


def tree_check(tree, c, lower, upper, beta_lower, beta_upper, marked=None):
    n = len(tree)
    edges = list(tree.edges())
    A = np.zeros((n, n-1))
    for j, (u, v) in enumerate(edges):
        A[u,j], A[v,j] = 1, -1
    C = np.linalg.inv(A[:-1])
    w = np.linalg.solve(A[:-1], c[:-1])
    assert np.all(abs(w) > 1e-9)
    base_A = np.vstack([np.eye(n-1), -np.eye(n-1), -np.ones(n-1), np.ones(n-1)])
    base_d = np.r_[upper[:-1], -lower[:-1], upper[-1], -lower[-1]]
    best = best_family = -np.inf
    candidates = 0
    for signs in product((-1, 1), repeat=n-1):
        signs = np.array(signs)
        beta = np.where(w*signs >= 0, beta_upper, beta_lower)
        Q = 2*C.T @ np.diag(w*beta*signs) @ C
        AA = np.vstack([base_A, -signs[:,None]*C])
        dd = np.r_[base_d, np.zeros(n-1)]
        if not linprog(np.zeros(n-1), A_ub=AA, b_ub=dd,
                       bounds=[(None,None)]*(n-1), method='highs').success:
            continue
        for z in quadratic_candidates(Q, np.zeros(n-1), AA, dd):
            candidates += 1
            value = z @ Q @ z / 2
            best = max(best, value)
            b = np.r_[z, -sum(z)]
            if path_family_member(tree, c, b, lower, upper, marked):
                best_family = max(best_family, value)
            flow = C @ z
            # Directly enumerate every resistance corner for each nomination.
            corner_best = max(np.sum(w*np.where(bits, beta_upper, beta_lower)*flow*abs(flow))
                              for bits in product((False,True), repeat=n-1))
            assert abs(corner_best-value) < 1e-6
    assert abs(best-best_family) < 1e-6, (best, best_family)
    return candidates, best


def contraction_checks():
    rng = np.random.default_rng(312640)
    count = 0
    for _ in range(30):
        graph = nx.from_prufer_sequence(list(map(int, rng.integers(0,8,6))))
        terminals = rng.choice(8,3,replace=False)
        c = [0]*8
        for v, value in zip(terminals, [2,-5,3]):
            c[int(v)] = value
        b = list(map(int,rng.integers(-3,4,7)))
        b.append(-sum(b))
        zero = nx.Graph(); zero.add_nodes_from(graph)
        data = []
        for i,(u,v) in enumerate(graph.edges()):
            cut = graph.copy();cut.remove_edge(u,v)
            component = nx.node_connected_component(cut,u)
            weight = sum(c[t] for t in component)
            flow = sum(b[t] for t in component)
            beta = Fraction(i+1,3)
            data.append((u,v,weight,flow,beta))
            if weight == 0: zero.add_edge(u,v)
        clusters = list(nx.connected_components(zero))
        owner = {v:i for i,cluster in enumerate(clusters) for v in cluster}
        reduced = nx.Graph();reduced.add_nodes_from(range(len(clusters)))
        for u,v,weight,flow,beta in data:
            if weight: reduced.add_edge(owner[u],owner[v])
        bb = [sum(b[v] for v in cluster) for cluster in clusters]
        cc = [sum(c[v] for v in cluster) for cluster in clusters]
        original = sum(weight*beta*flow*abs(flow) for u,v,weight,flow,beta in data)
        recovered = Fraction(0)
        for u,v,weight,flow,beta in data:
            if not weight: continue
            cut = reduced.copy();cut.remove_edge(owner[u],owner[v])
            comp = nx.node_connected_component(cut,owner[u])
            new_w, new_x = sum(cc[t] for t in comp),sum(bb[t] for t in comp)
            assert (new_w,new_x)==(weight,flow)
            recovered += new_w*beta*new_x*abs(new_x)
        assert original == recovered
        count += 1
    return count


def run():
    total = 0
    cases = [
        (nx.path_graph(4), [1,0,0,-1], [-2,-1,-1,-2], [1,2,2,1]),
        (nx.path_graph(5), [2,0,-5,0,3], [-1,-1,0,-1,-2], [2,1,3,2,1]),
        (nx.star_graph(3), [-3,1,1,1], [-2,-1,-1,0], [0,2,2,3]),
        (nx.path_graph(4), [1,0,0,-1], [0,0,0,0], [0,1,1,1]),
        (nx.path_graph(4), [2,0,-5,3], [-2,1,-1,-2], [0,1,3,0]),
    ]
    for graph,c,lo,hi in cases:
        size = len(graph)-1
        count,value = tree_check(graph,np.array(c,dtype=float),np.array(lo,dtype=float),
                                 np.array(hi,dtype=float),np.ones(size),np.arange(2,size+2,dtype=float))
        total += count
        print('tree',len(graph),'support',np.count_nonzero(c),'candidates',count,'optimum',value)
    # Interior, edge, vertex and flat quadratic optima in a square.
    A = np.array([[1,0],[-1,0],[0,1],[0,-1]],dtype=float);d=np.ones(4)
    examples = [(np.diag([-2.,-2.]),np.array([0.,0.]),0.),
                (np.diag([-2.,0.]),np.array([0.,1.]),1.),
                (np.diag([2.,2.]),np.array([0.,0.]),2.),
                (np.zeros((2,2)),np.zeros(2),0.)]
    for Q,g,expected in examples:
        found = max(z@Q@z/2+g@z for z in quadratic_candidates(Q,g,A,d))
        assert abs(found-expected)<1e-9
    print('PASS:',total,'stationary candidates;',contraction_checks(),'exact contractions; 4 degenerate QP controls')


if __name__ == '__main__':
    run()
