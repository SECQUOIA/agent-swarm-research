"""Phase-two fixed diagnostic corpus; exact inputs, no planted random optima.

The independent small-instance oracle and old public-file reader are frozen
from phase one. New generated instances use new seeds and are not reductions
or truncations of public instances.
"""
from fractions import Fraction as F
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).parent / 'frozen' / 'baseline'))
from baseline_corpus import (Instance, matrix, value, exact_face_minimum,
                             minimum_degree_decomposition, random_band, read_qbn)


def from_squares(name, n, squares, linear=None, diagonal=None, bounds=None,
                 integers=(), description=''):
    a = matrix(n)
    b = list(linear) if linear is not None else [F(0)] * n
    c = F(0)
    for weight, terms, offset in squares:
        weight, offset = F(weight), F(offset)
        c += weight * offset * offset
        for i, v in terms.items():
            b[i] += 2 * weight * offset * v
            for j, w in terms.items():
                a[i][j] += 2 * weight * v * w
    for i, d in (diagonal or {}).items():
        a[i][i] += 2 * F(d)
    return Instance(name, a, b, bounds or [(F(-1), F(1))] * n,
                    set(integers), c, description)


def shuffle(p, seed):
    order = list(range(len(p.b)))
    Random(seed).shuffle(order)
    return Instance(p.name + '_shuffled', [[p.A[i][j] for j in order] for i in order],
                    [p.b[i] for i in order], [p.bounds[i] for i in order],
                    {k for k, i in enumerate(order) if i in p.integers}, p.c,
                    p.description + f'; variable permutation seed {seed}', p.source)


def tree(n, seed):
    rng = Random(seed)
    p = random_band(f'random_tree_{n}', n, 0, seed)
    for i in range(1, n):
        j = rng.randrange(i)
        p.A[i][j] = p.A[j][i] = F(rng.choice((-4, -3, -1, 1, 2, 4)), 5)
    p.description = f'Fixed seed {seed}, random recursive tree and signed rational coefficients; no planted optimum'
    return p


def cases():
    items = [random_band('fresh_path_5', 5, 1, 2103),
             random_band('fresh_width2_6', 6, 2, 2111),
             random_band('fresh_mixed_5', 5, 1, 2129, (1, 3)),
             tree(7, 2131), tree(32, 2137)]
    items += [random_band(f'fresh_path_{n}', n, 1, 2200+n) for n in (16,32,64)]
    items.append(shuffle(items[0], 2309))
    items += [from_squares('rational_face', 2, [(1, {0:F(1)}, F(-1,3))],
                          diagonal={1:-1}, bounds=[(F(0),F(1)),(F(0),F(2))],
                          description='Unique rational optimum (1/3,2), value -4'),
              from_squares('mixed_rational', 2,
                           [(1,{0:F(1),1:F(-1)},0),(1,{1:F(1)},F(-1,3))],
                           bounds=[(F(0),F(1))]*2, integers=(0,),
                           description='Mixed unique optimum (0,1/6), value 1/18'),
              from_squares('flat_diagonal', 4,
                           [(1,{i:F(1),i+1:F(-1)},0) for i in range(3)],
                           description='Singular PSD chain; full diagonal segment is optimal')]
    for residual in (4,16):
        items.append(shuffle(from_squares(f'affine_star_{residual+1}', residual+1,
                     [(64,{i:F(1),0:F(-1,2)},0) for i in range(1,residual+1)],
                     diagonal={0:-1},description='Concave core plus expensive affine convex leaf recourse; exact value -1'),2401))
    items += [from_squares('singular_affine',3,[(1,{1:F(1),2:F(1),0:F(-1)},0)],
                           diagonal={0:-1},bounds=[(F(0),F(2)),(F(0),F(1)),(F(0),F(1))],
                           description='Singular convex block; exact value -4 at (2,1,1)'),
              from_squares('clipped_response',2,[(1,{1:F(1),0:F(-2)},0)],diagonal={0:-1},
                           bounds=[(F(0),F(1))]*2,
                           description='Clipped response has no affine selector; value -1/3 at (2/3,1)'),
              from_squares('tilted_disconnected',3,[(1,{0:F(1),1:F(-1),2:F(1,2)},0)],
                           linear=[F(0),F(0),F(1,8)],diagonal={2:F(-1,8)},bounds=[(F(0),F(1))]*3,
                           description='Two tilted optimal segments, exact value zero'),
              Instance('false_growth_trap',[[F(2),F(-3)],[F(-3),F(2)]],[F(63,128)]*2,
                       [(F(0),F(1))]*2,set(),description='Nonglobal KKT at zero; true unique optimum (1,1), value -1/64')]
    for n in (7,33):
        rng=Random(2600+n); a=matrix(n);a[0][0]=F(2);b=[F(-2,3)]+[F(rng.randrange(-3,4),5) for _ in range(n-1)]
        for i in range(1,n):
            a[i][i]=F(-2,rng.randrange(1,5))
            a[i][0]=a[0][i]=F(rng.choice((-1,1)),5)
            for j in range(1,i): a[i][j]=a[j][i]=F(-rng.randrange(1,4),n)
        items.append(Instance(f'dense_mincut_{n}',a,b,[(F(0),F(1))]*n,set(),F(1,9),
                              'One convex core variable, dense attractive coordinatewise-concave residual; seed '+str(2600+n)))
    items.append(from_squares('endpoint_branch_8',8,
                 [(F(1,8),{i:F(1),(i-1)//2:F(-1)},0) for i in range(1,7)],
                 diagonal={i:-1 for i in range(7)},
                 bounds=[(F(-1),F(1))]*7+[(F(-2),F(2))],integers=(7,),
                 description='Concave branching tree; two tied sign assignments and five free native integer labels, exact value -7'))
    items += [read_qbn('3852'),read_qbn('5881')]
    return {p.name:p for p in items}


def metadata():
    out={}
    for name,p in cases().items():
        out[name]={'n':len(p.b),'integers':sorted(p.integers),'description':p.description,'source':p.source}
        if len(p.b)<=8: out[name]['exact_reference']=exact_face_minimum(p)
    return out
