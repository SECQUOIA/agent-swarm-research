"""Independent structural + exact-arithmetic audit of build_bounded."""
import random
from fractions import Fraction as Fr
from bounded_build_and_check import build_bounded, check_degrees_and_data, B

def structure(P, variables, constraints):
    outs = {n: [] for n in list(P.sources)+list(P.pools)}
    ins = {n: [] for n in list(P.pools)+list(P.terms)}
    for (u,v) in P.arcs:
        outs[u].append(v); ins[v].append(u)
    forced_pools = [p for p,i in P.pools.items() if i['forced']]
    for p in forced_pools:
        assert P.pools[p]['cap'] == B
        inn = ins[p]
        assert len(inn) == 2, (p, inn)
        dil = [s for s in inn if s.startswith('d')]
        q1 = [s for s in inn if not s.startswith('d')]
        assert len(dil) == 1 and len(q1) == 1, (p, inn)
        d = dil[0]
        assert P.sources[d]['q'] == 0 and P.sources[d]['cap'] == B and not P.sources[d]['forced'] and len(outs[d]) == 1
        assert P.sources[q1[0]]['q'] == 1 and P.sources[q1[0]]['forced']
        sl = [t for t in outs[p] if t.startswith('slack')]
        assert len(sl) == 1 and P.terms[sl[0]]['cap'] == B and not P.terms[sl[0]]['forced'] and len(ins[sl[0]]) == 1
        nonslack = [t for t in outs[p] if not t.startswith('slack')]
        assert len(nonslack) <= 2, (p, nonslack)
        # each non-slack arc is an emission terminal or a gadget terminal
        for t in nonslack:
            assert t.startswith(('te','tinv','tadd')), (p, t)
    # every P_v and Pbar_v emits (has an emission terminal out-arc)
    for v in variables:
        for p in (f'P_{v}', f'Pbar_{v}'):
            assert any(t.startswith('te') for t in outs[p]), p
    # unforced pools: out-degree 1
    for p,i in P.pools.items():
        if not i['forced']:
            assert len(outs[p]) == 1, p
    # sources out-degree <= 2, in-degree of everything <= 2
    for s in P.sources: assert len(outs[s]) <= 2
    for n in ins: assert len(ins[n]) <= 2, n
    info = check_degrees_and_data(P)
    assert info['max_in'] <= 2 and info['max_out'] <= 3, info
    assert set(info['caps']) <= {Fr(2),Fr(5,2),Fr(4),Fr(7)}, info
    assert set(info['bounds']) <= {Fr(0),Fr(1),Fr(1,14),Fr(2,35)}, info
    assert set(info['quals']) <= {Fr(0),Fr(1)}
    assert set(info['costs']) <= {0,-1,-2}
    return outs, ins, forced_pools

def intended_flow(P, variables, constraints, val):
    """Propagate the intended flow from variable values; return arc dict."""
    outs = {n: [] for n in list(P.sources)+list(P.pools)}
    ins = {n: [] for n in list(P.pools)+list(P.terms)}
    for (u,v) in P.arcs:
        outs[u].append(v); ins[v].append(u)
    x = {}
    for v in variables:
        x[(f's_{v}', f'P_{v}')] = Fr(val[v]); x[(f's_{v}', f'Pbar_{v}')] = Fr(5,2) - Fr(val[v])
    changed = True
    while changed:
        changed = False
        # forced pools: diluent and emission arcs from quality-1 inflow
        for p,i in P.pools.items():
            if i['forced']:
                q1 = [s for s in ins[p] if not s.startswith('d')][0]
                d = [s for s in ins[p] if s.startswith('d')][0]
                if (q1,p) in x and (d,p) not in x:
                    a = x[(q1,p)]; x[(d,p)] = B - a; changed = True
                    for t in outs[p]:
                        if t.startswith('te'): x[(p,t)] = 1/a
                sl = [t for t in outs[p] if t.startswith('slack')][0]
                others = [t for t in outs[p] if t != sl]
                if (p,sl) not in x and all((p,t) in x for t in others):
                    x[(p,sl)] = B - sum(x[(p,t)] for t in others); changed = True
            else:
                # unforced pool with single out-arc: out = sum in
                t = outs[p][0]
                if (p,t) not in x and all((s,p) in x for s in ins[p]):
                    x[(p,t)] = sum(x[(s,p)] for s in ins[p]); changed = True
                if (p,t) in x and len(ins[p]) == 1 and (ins[p][0],p) not in x:
                    x[(ins[p][0],p)] = x[(p,t)]; changed = True
        for t,i in P.terms.items():
            if i['forced']:
                unk = [u for u in ins[t] if (u,t) not in x]
                if len(unk) == 1:
                    x[(unk[0],t)] = i['cap'] - sum(x[(u,t)] for u in ins[t] if u != unk[0]); changed = True
        for s,i in P.sources.items():
            if i['forced']:
                unk = [p for p in outs[s] if (s,p) not in x]
                if len(unk) == 1:
                    x[(s,unk[0])] = i['cap'] - sum(x[(s,p)] for p in outs[s] if p != unk[0]); changed = True
    assert len(x) == len(P.arcs), (len(x), len(P.arcs), [a for a in P.arcs if a not in x][:5])
    return x, outs, ins

def check_flow(P, x, outs, ins):
    for a,f in x.items(): assert f >= 0, (a,f)
    profit = Fr(0)
    for (u,v),f in x.items(): profit += -P.cost(u,v)*f
    for s,i in P.sources.items():
        tot = sum(x[(s,p)] for p in outs[s]); assert tot <= i['cap'], s
        if i['forced']: assert tot == i['cap'], s
    w = {}
    for p,i in P.pools.items():
        X = sum(x[(p,t)] for t in outs[p]); inn = sum(x[(s,p)] for s in ins[p])
        assert X == inn and X <= i['cap'], p
        if i['forced']: assert X == i['cap'], p
        w[p] = sum(P.sources[s]['q']*x[(s,p)] for s in ins[p]) / X if X > 0 else Fr(0)
    for t,i in P.terms.items():
        X = sum(x[(p,t)] for p in ins[t]); assert X <= i['cap'], t
        if i['forced']: assert X == i['cap'], t
        mass = sum(w[p]*x[(p,t)] for p in ins[t])
        assert i['lo']*X <= mass <= i['up']*X, (t, mass, X)
    assert profit == P.zeta(), (profit, P.zeta())
    # non-slack arcs from forced pools carry at most 2, slack >= 3
    for p,i in P.pools.items():
        if i['forced']:
            for t in outs[p]:
                if t.startswith('slack'): assert x[(p,t)] >= 3, (p, x[(p,t)])
                else: assert x[(p,t)] <= 2, (p,t,x[(p,t)])
    return True

# --- exact (=>) checks on satisfiable instances with rational solutions ---
cases = [
    ('x*x=1', ['x'], [('inv','x','x')], {'x':1}),
    ('boundary x+x=y,y+y=z', ['x','y','z'], [('add','x','x','y'),('add','y','y','z')], {'x':Fr(1,2),'y':1,'z':2}),
    ('fan-out', ['u','w','y1','y2','y3'],
     [('add','u','u','w'),('inv','w','w'),('inv','u','y1'),('inv','u','y2'),('inv','u','y3')],
     {'u':Fr(1,2),'w':1,'y1':2,'y2':2,'y3':2}),
    ('x+x=y,y*y=1', ['x','y'], [('add','x','x','y'),('inv','y','y')], {'x':Fr(1,2),'y':1}),
    ('unused variable', ['x','q'], [('inv','x','x')], {'x':1,'q':Fr(3,4)}),
    ('no equations', ['a','b'], [], {'a':Fr(1,2),'b':2}),
    ('heavy fan-out u in 8 additions', ['u','w'] + [f'z{i}' for i in range(6)],
     [('add','u','u','w')] + [('add','u','u',f'z{i}') for i in range(6)] + [('inv','w','w')],
     dict({'u':Fr(1,2),'w':1}, **{f'z{i}':1 for i in range(6)})),
]
for name, V, C, val in cases:
    P = build_bounded(V, C)
    outs, ins, fp = structure(P, V, C)
    x, outs, ins = intended_flow(P, V, C, val)
    check_flow(P, x, outs, ins)
    nonslack = {p: len([t for t in outs[p] if not t.startswith('slack')]) for p in fp}
    print(f"OK {name}: |S|={len(P.sources)} |P|={len(P.pools)} |T|={len(P.terms)} |A|={len(P.arcs)} forced pools={len(fp)} max nonslack out={max(nonslack.values())} zeta={P.zeta()}")

# --- random structural checks and size scaling ---
random.seed(1)
for trial in range(300):
    n = random.randint(1, 6); m = random.randint(0, 12)
    V = [f'v{i}' for i in range(n)]; C = []
    for _ in range(m):
        if random.random() < 0.5: C.append(('inv', random.choice(V), random.choice(V)))
        else: C.append(('add', random.choice(V), random.choice(V), random.choice(V)))
    P = build_bounded(V, C)
    outs, ins, fp = structure(P, V, C)
    nnodes = len(P.sources)+len(P.pools)+len(P.terms)
    # size bound: advances <= 2*(#takes) + 2n ; each advance adds 10 nodes; base 6n nodes + gadget nodes
    takes = sum(2 if c[0]=='inv' else 3 for c in C)
    assert len(fp) <= 2*n + 2*takes + 2*n, (n, m, len(fp))
    ninv = sum(1 for c in C if c[0]=='inv'); nadd = len(C) - ninv
    advances = len(fp) - 2*n
    assert nnodes == 7*n + 10*advances + 5*ninv + 8*nadd, (n,m,nnodes, advances)
    assert advances <= 2*takes + 2*n
print("random structural checks OK")
