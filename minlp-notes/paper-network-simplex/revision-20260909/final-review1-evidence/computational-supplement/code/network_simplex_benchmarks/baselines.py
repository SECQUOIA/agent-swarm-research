"""Independent sparse LP baselines for network--simplex hull experiments.

The full EF retains every simplex state, including the residual state.  It does
not use graph blocks, path coordinates, grouping, or separator implementation.
Balance convention: outgoing flow minus incoming flow equals balances.
"""
from dataclasses import dataclass
from time import perf_counter
import numpy as np
from scipy.optimize import linprog, OptimizeResult
from scipy.sparse import coo_matrix


@dataclass
class Instance:
    arcs: list
    balances: np.ndarray
    simplex_size: int
    observations: list
    reference: np.ndarray
    blocks: list | None = None

    @property
    def edge_count(self):
        return len(self.arcs)


def incidence(instance):
    rows, cols, data = [], [], []
    for e, (tail, head, _) in enumerate(instance.arcs):
        rows.extend([tail, head]); cols.extend([e, e]); data.extend([1., -1.])
    return coo_matrix((data, (rows, cols)), shape=(len(instance.balances), instance.edge_count)).tocsr()


class Rows:
    def __init__(self, n):
        self.n = n; self.row = []; self.col = []; self.data = []; self.rhs = []

    def add(self, terms, rhs):
        r = len(self.rhs)
        for c, a in terms:
            if a:
                self.row.append(r); self.col.append(c); self.data.append(a)
        self.rhs.append(rhs)

    def finish(self):
        return (coo_matrix((self.data, (self.row, self.col)), shape=(len(self.rhs), self.n)).tocsr(), np.asarray(self.rhs))


def matrix_stats(*matrices):
    return dict(rows=sum(a.shape[0] for a in matrices),
                nonzeros=sum(a.nnz for a in matrices),
                matrix_bytes=sum(a.data.nbytes + a.indices.nbytes + a.indptr.nbytes for a in matrices))


def full_ef(instance, objective, y_fixed=None):
    """Minimize c_x*x+c_y*y+c_z*z using only y and all disaggregated flows."""
    started = perf_counter()
    E, m, O = instance.edge_count, instance.simplex_size, instance.observations
    A, b = incidence(instance), instance.balances
    u = np.array([a[2] for a in instance.arcs])
    n = m + (m + 1) * E
    eq, ub = Rows(n), Rows(n)
    c = np.zeros(n); c[:m] = objective[E:E+m]
    for j in range(m + 1):
        off = m + j * E
        c[off:off+E] += objective[:E]
        for v in range(len(b)):
            terms = list(zip((off + A[v].indices).tolist(), A[v].data.tolist()))
            if j < m:
                terms.append((j, -b[v])); rhs = 0.
            else:
                terms.extend((h, b[v]) for h in range(m)); rhs = b[v]
            eq.add(terms, rhs)
        for e in range(E):
            terms = [(off+e, 1.)]
            if j < m:
                terms.append((j, -u[e])); rhs = 0.
            else:
                terms.extend((h, u[e]) for h in range(m)); rhs = u[e]
            ub.add(terms, rhs)
    for k, (e, j) in enumerate(O):
        c[m+j*E+e] += objective[E+m+k]
    ub.add([(j, 1.) for j in range(m)], 1.)
    ae, be = eq.finish(); au, bu = ub.finish()
    bounds = [(0., 1.)] * m + [(0., None)] * ((m+1)*E)
    if y_fixed is not None:
        bounds[:m] = [(float(v), float(v)) for v in y_fixed]
    assembled = perf_counter()
    result = linprog(c, A_ub=au, b_ub=bu, A_eq=ae, b_eq=be, bounds=bounds, method='highs')
    result.assembly_seconds = assembled-started
    result.solve_seconds = perf_counter()-assembled
    if result.success:
        flows = result.x[m:].reshape(m+1, E)
        result.original_point = np.r_[flows.sum(axis=0), result.x[:m], [flows[j, e] for e, j in O]]
    result.model_stats = dict(variables=n, **matrix_stats(ae, au))
    return result


def full_ef_membership(instance, x, y, z):
    """Independent fixed-point feasibility check with all (m+1)E flow variables."""
    started = perf_counter()
    E, m = instance.edge_count, instance.simplex_size
    A, b = incidence(instance), instance.balances
    n = (m+1)*E
    eq = Rows(n)
    weights = np.r_[y, 1-np.sum(y)]
    if np.min(weights) < -1e-10:
        return OptimizeResult(success=False, status=2, message="Point violates simplex constraints")
    for j in range(m+1):
        for v in range(len(b)):
            eq.add(zip((j*E+A[v].indices).tolist(), A[v].data.tolist()), weights[j]*b[v])
    for e in range(E):
        eq.add(((j*E+e, 1.) for j in range(m+1)), x[e])
    for k, (e, j) in enumerate(instance.observations):
        eq.add([(j*E+e, 1.)], z[k])
    ae, be = eq.finish()
    bounds = [(0., max(0., weights[j]*a[2])) for j in range(m+1) for a in instance.arcs]
    assembled = perf_counter()
    result = linprog(np.zeros(n), A_eq=ae, b_eq=be, bounds=bounds, method='highs')
    result.assembly_seconds = assembled-started
    result.solve_seconds = perf_counter()-assembled
    result.model_stats = dict(variables=n, **matrix_stats(ae))
    return result


class OriginalLP:
    """McCormick relaxation, with optional valid cuts added in original variables."""
    def __init__(self, instance, y_fixed=None):
        E, m, O = instance.edge_count, instance.simplex_size, instance.observations
        self.n = E+m+len(O); self.instance = instance
        A = incidence(instance)
        self.eq, self.ub = Rows(self.n), Rows(self.n)
        for v, b in enumerate(instance.balances):
            self.eq.add(zip(A[v].indices.tolist(), A[v].data.tolist()), b)
        self.ub.add([(E+j, 1.) for j in range(m)], 1.)
        for k, (e, j) in enumerate(O):
            z, y, u = E+m+k, E+j, instance.arcs[e][2]
            self.ub.add([(z,1.), (y,-u)], 0.)
            self.ub.add([(z,1.), (e,-1.)], 0.)
            self.ub.add([(e,1.), (y,u), (z,-1.)], u)
        self.bounds = [(0., a[2]) for a in instance.arcs]+[(0.,1.)]*m+[(0.,None)]*len(O)
        if y_fixed is not None:
            self.bounds[E:E+m] = [(float(v),float(v)) for v in y_fixed]

    def add_cut(self, coefficients, rhs):
        self.ub.add(coefficients, rhs)

    def solve(self, objective):
        started = perf_counter()
        ae, be = self.eq.finish(); au, bu = self.ub.finish()
        assembled = perf_counter()
        result = linprog(objective, A_eq=ae, b_eq=be, A_ub=au, b_ub=bu, bounds=self.bounds, method='highs')
        result.assembly_seconds = assembled-started
        result.solve_seconds = perf_counter()-assembled
        result.model_stats = dict(variables=self.n, **matrix_stats(ae,au))
        return result


def block_chain(seed=17, blocks=3, paths=4, length=2, states=100, observed_states=3, orientations=True):
    """Articulation-linked parallel-path blocks with one bridge between blocks.

Arbitrary orientations and nonzero balances stress graph preprocessing. Sparse
observations select only a few state labels per block, including repeated
observations on individual paths. Reference flow is strictly inside arc bounds.
"""
    rng = np.random.default_rng(seed)
    arcs, observations, block_metadata = [], [], []
    next_vertex, start = 1, 0
    for block in range(blocks):
        terminal = next_vertex; next_vertex += 1
        block_edges, path_metadata = [], []
        for path in range(paths):
            vertices = [start] + list(range(next_vertex,next_vertex+length-1)) + [terminal]
            next_vertex += length-1
            edge_signs = []
            for a,b in zip(vertices[:-1],vertices[1:]):
                sign = 1
                if orientations and rng.random()<.5: a,b=b,a; sign=-1
                edge_signs.append((len(arcs), sign))
                block_edges.append(len(arcs)); arcs.append((a,b,float(rng.integers(2,9))))
            path_metadata.append(edge_signs)
        block_metadata.append(path_metadata)
        label_rng = np.random.default_rng(seed+100000+block)
        edge_rng = np.random.default_rng(seed+200000+block)
        labels = label_rng.choice(states, min(states,observed_states), replace=False)
        for j in labels:
            for e in edge_rng.choice(block_edges, min(3,len(block_edges)), replace=False):
                observations.append((int(e),int(j)))
        start = terminal
        if block < blocks-1:
            arcs.append((start,next_vertex,4.)); start=next_vertex; next_vertex+=1
    reference = np.asarray([a[2]/2 for a in arcs])
    instance = Instance(arcs, np.zeros(next_vertex), states, sorted(set(observations)), reference, block_metadata)
    instance.balances = incidence(instance) @ reference
    return instance


def compressed_ef(instance, objective, y_fixed=None):
    """Independent observed-state cycle-coordinate EF, residual eliminated.

Uses generator metadata rather than separator preprocessing. There are exactly
sum_B (k_B-1)*a_B extra variables. Balances and path consistency of aggregate
flow remain in the original flow equations.
"""
    started = perf_counter()
    E,m,O=instance.edge_count,instance.simplex_size,instance.observations
    original_n=E+m+len(O)
    layout=[]; n=original_n; covered=set()
    for paths in instance.blocks:
        edge_path={e:(i,sign) for i,path in enumerate(paths) for e,sign in path}
        covered.update(edge_path)
        labels=sorted({j for e,j in O if e in edge_path})
        offsets={j:n+h*(len(paths)-1) for h,j in enumerate(labels)}
        n+=len(labels)*(len(paths)-1)
        layout.append((paths,edge_path,labels,offsets))
    eq,ub=Rows(n),Rows(n)
    A=incidence(instance)
    for v,b in enumerate(instance.balances): eq.add(zip(A[v].indices,A[v].data),b)
    ub.add([(E+j,1.) for j in range(m)],1.)
    for paths,edge_path,labels,offsets in layout:
        k=len(paths)
        def coordinate(i,j):
            return [(offsets[j]+i,1.)] if i<k-1 else [(offsets[j]+h,-1.) for h in range(k-1)]
        for j in labels:
            for i,path in enumerate(paths):
                lower=max(min(-sign*instance.reference[e],sign*(instance.arcs[e][2]-instance.reference[e])) for e,sign in path)
                upper=min(max(-sign*instance.reference[e],sign*(instance.arcs[e][2]-instance.reference[e])) for e,sign in path)
                terms=coordinate(i,j)
                ub.add(terms+[(E+j,-upper)],0.)
                ub.add([(c,-a) for c,a in terms]+[(E+j,lower)],0.)
        for i,path in enumerate(paths):
            lower=max(min(-sign*instance.reference[e],sign*(instance.arcs[e][2]-instance.reference[e])) for e,sign in path)
            upper=min(max(-sign*instance.reference[e],sign*(instance.arcs[e][2]-instance.reference[e])) for e,sign in path)
            e,sign=path[0]
            residual=[(e,sign)]+[(c,-a) for j in labels for c,a in coordinate(i,j)]
            ub.add(residual+[(E+j,upper) for j in labels],upper+sign*instance.reference[e])
            ub.add([(c,-a) for c,a in residual]+[(E+j,-lower) for j in labels],-lower-sign*instance.reference[e])
        for h,(e,j) in enumerate(O):
            if e in edge_path:
                i,sign=edge_path[e]
                eq.add([(E+m+h,1.),(E+j,-instance.reference[e])]+[(c,-sign*a) for c,a in coordinate(i,j)],0.)
    for h,(e,j) in enumerate(O):
        if e not in covered: eq.add([(E+m+h,1.),(E+j,-instance.reference[e])],0.)
    ae,be=eq.finish();au,bu=ub.finish()
    c=np.r_[objective,np.zeros(n-original_n)]
    bounds=[(0.,a[2]) for a in instance.arcs]+[(0.,1.)]*m+[(0.,None)]*len(O)+[(None,None)]*(n-original_n)
    if y_fixed is not None: bounds[E:E+m]=[(float(v),float(v)) for v in y_fixed]
    assembled = perf_counter()
    result=linprog(c,A_eq=ae,b_eq=be,A_ub=au,b_ub=bu,bounds=bounds,method='highs')
    result.assembly_seconds = assembled-started
    result.solve_seconds = perf_counter()-assembled
    if result.success: result.original_point=result.x[:original_n]
    result.model_stats=dict(variables=n,auxiliary_variables=n-original_n,**matrix_stats(ae,au))
    return result
