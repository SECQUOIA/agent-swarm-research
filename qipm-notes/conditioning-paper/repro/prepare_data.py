"""One-time provenance capture. Regeneration uses only the frozen JSON files.

Usage: python repro/prepare_data.py --cache /path/to/netlib
This script reads .std and .mps files; it never writes to the source cache.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parent

def frac(x):
    return Q.from_float(float(x))

def exact_solve(A, b):
    """Solve a nonsingular rational square system with pivoted elimination."""
    n = len(b)
    M = [list(row)+[value] for row,value in zip(A,b)]
    for j in range(n):
        p = next(i for i in range(j,n) if M[i][j])
        M[j],M[p] = M[p],M[j]
        pivot = M[j][j]
        M[j] = [v/pivot for v in M[j]]
        for i in range(j+1,n):
            t = M[i][j]
            if t:
                M[i] = [u-t*v for u,v in zip(M[i],M[j])]
    x = [Q(0)]*n
    for i in reversed(range(n)):
        x[i] = M[i][-1]-sum(M[i][j]*x[j] for j in range(i+1,n))
    return x

def reconstruct(Aq,bq, x, pivots):
    m,n = len(Aq),len(Aq[0])
    free = set(range(n))-set(pivots)
    result = [frac(v) for v in x]
    rhs = [bq[i]-sum(Aq[i][j]*result[j] for j in free) for i in range(m)]
    sol = exact_solve([[row[j] for j in pivots] for row in Aq],rhs)
    for j,v in zip(pivots,sol): result[j] = v
    assert all(sum(a*v for a,v in zip(row,result)) == rhs for row,rhs in zip(Aq,bq))
    return result

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare(cache):
    records = {}
    sizes = dict(afiro=[[27,32],[7,10],[9,18]],sc50b=[[50,48],[15,15],[15,29]],adlittle=[[56,97],[53,95],[55,136]])
    for name in sizes:
        src = cache/name/(name+'.std')
        with np.load(src) as z:
            A = csr_matrix((z['A_data'],z['A_indices'],z['A_indptr']),shape=z['A_shape']).toarray()
            b,c,offset = z['b'],z['c'],float(z['obj_offset'])
        m,n=A.shape
        Aq,bq,cq = [[frac(v) for v in row] for row in A],list(map(frac,b)),list(map(frac,c))
        pivots = qr(A,pivoting=True,mode='economic')[2][:m].tolist()
        phase = linprog(np.r_[np.zeros(n),-1],A_ub=np.c_[-np.eye(n),np.ones(n)],b_ub=np.zeros(n),A_eq=np.c_[A,np.zeros(m)],b_eq=b,bounds=[(0,None)]*n+[(0,1)],method='highs')
        assert phase.success and phase.x[-1]>0
        strict = reconstruct(Aq,bq,phase.x[:n],pivots)
        assert min(strict)>0
        eta = 0 if name!='adlittle' else 1
        bound = linprog(np.zeros(m), A_ub=-A.T,b_ub=eta*c-np.ones(n),bounds=[(None,None)]*m,method='highs')
        assert bound.success
        yb = list(map(frac,bound.x))
        margins = [sum(Aq[i][j]*yb[i] for i in range(m))+eta*cq[j] for j in range(n)]
        assert min(margins)>0
        opt = linprog(c,A_eq=A,b_eq=b,bounds=(0,None),method='highs')
        assert opt.success
        # Recover a nearby exactly feasible primal point after a small strict mixture.
        near = reconstruct(Aq,bq,opt.x,pivots)
        primal_blend=max([Q(0)]+[-v/(w-v) for v,w in zip(near,strict) if v<0])
        near=[(1-primal_blend)*v+primal_blend*w for v,w in zip(near,strict)]
        assert min(near)>=0
        # A strictly feasible dual anchor follows from the positive compactness vector.
        if eta:
            anchor=[-v for v in yb]
        else:
            scale=max(Q(1),max((Q(1)-cq[j])/margins[j] for j in range(n)))
            anchor=[-scale*v for v in yb]
        s0=[cq[j]-sum(Aq[i][j]*anchor[i] for i in range(m)) for j in range(n)]
        assert min(s0)>0
        approx=list(map(frac,opt.eqlin.marginals))
        sa=[cq[j]-sum(Aq[i][j]*approx[i] for i in range(m)) for j in range(n)]
        blend=max([Q(0)]+[-s/(t-s) for s,t in zip(sa,s0) if s<0])
        # Exact blend is feasible; no numerical tolerance is used in the certificate.
        dual=[(1-blend)*v+blend*w for v,w in zip(approx,anchor)]
        slack=[cq[j]-sum(Aq[i][j]*dual[i] for i in range(m)) for j in range(n)]
        assert min(slack)>=0
        lower,upper=dot(bq,dual),dot(cq,near)
        assert upper>=lower
        out=dict(name=name,A=A.tolist(),b=b.tolist(),c=c.tolist(),objective_offset=offset,
                 interpretation='Every stored JSON number is parsed as float64, then interpreted as that exact binary rational.',
                 certificates=dict(pivots=pivots,strict_point=list(map(str,strict)),compactness_y=list(map(str,yb)),compactness_eta=eta,
                  near_optimal_primal=list(map(str,near)),dual_lower_bound_y=list(map(str,dual)),objective_lower=str(lower),objective_upper=str(upper)))
        path=ROOT/'data'/(name+'.json')
        path.write_text(json.dumps(out,indent=2)+'\n')
        records[name]=dict(original_mps_sha256=sha(cache/name/(name+'.mps')),cached_std_sha256=sha(src),frozen_json_sha256=sha(path),dimensions=sizes[name],strict_margin=float(min(strict)),compactness_margin=float(min(margins)),objective_interval=[float(lower),float(upper)],objective_interval_width=float(upper-lower))
        print(name,records[name])
    provenance=dict(preparation_command='python repro/prepare_data.py --cache /path/to/netlib',source_cache_argument=str(cache),source_url='https://netlib.org/lp/data/',
      transformation='HiGHS 1.15.1 default presolve of original MPS; finite bounds shifted, free variables split, inequalities and upper bounds converted using nonnegative slacks. Frozen c,b,A,offset exactly matched the repository standard_form._lp_to_standard_form output. No further face reduction or artificial bound. Numerical Hessians use Euclidean coordinates of the frozen representation.',
      representation_definition='The frozen JSON arrays, not a reconstruction with a different presolver version, define the tested LPs.',instances=records)
    (ROOT/'data'/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,required=True)
    prepare(p.parse_args().cache)
