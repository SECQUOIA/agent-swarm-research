"""Fixed-two-state flat-chain comparison, including fair full-disaggregation LP.

Canonical network has two parallel arcs per serial gadget plus one bypass.
All methods test identical exact rational points. Library precomputation is
reported separately and does not disappear into an unreported warmup.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import platform
import sys
from statistics import median
import numpy as np
import scipy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from baselines import Instance, full_ef_membership, full_ef
from run import timed, check_decomposition
from network_simplex.separator import Point
from network_simplex_compressed import CompressedNetworkSimplex


def candidate(gadgets,feasible):
    arcs=[(g,g+1,1.) for g in range(gadgets) for _ in range(2)]+[(0,gadgets,1.)]
    balances=np.zeros(gadgets+1);balances[0]=1.;balances[-1]=-1.
    observations=[(2*g,g%2) for g in range(gadgets)]
    if feasible:
        # Each explicit state has weight1/2 and branch profile1/4. Opposite
        # state allocations preserve aggregate arc-a=arc-b=1/4 at every gadget.
        x=[F(1,4)]*(2*gadgets)+[F(1,2)]
        z={}
        for g in range(gadgets):
            delta=F(g%3-1,16)
            z[2*g,g%2]=F(1,8)+(delta if g%2==0 else -delta)
    else:
        # Adjacent observations force w0,w1>=3/10 while w0+w1=1/2.
        # Each individual product nevertheless satisfies all McCormick bounds.
        x=[v for _ in range(gadgets) for v in (F(3,10),F(1,5))]+[F(1,2)]
        z={o:F(3,10) for o in observations}
    p=Point(x,[F(1,2),F(1,2)],z)
    a=Instance(arcs,balances,2,observations,np.asarray(x,dtype=float))
    # These inequalities are checked directly, outside timed components.
    for (e,j),v in z.items():
        assert 0<=v<=p.x[e] and v<=p.y[j] and v>=p.x[e]+p.y[j]-1
    return a,p


def summary(runs):
    return {k:{'median':median([r[k] for r in runs]),'minimum':min(r[k] for r in runs),'maximum':max(r[k] for r in runs)}
            for k in runs[0] if k.endswith('_seconds')}


def once(a,p,expected,order):
    from network_simplex.flat_chain import FlatChainSimplex
    out={}
    for method in order:
        if method=='full':
            result,total=timed(lambda:full_ef_membership(a,np.asarray(p.x,dtype=float),np.asarray(p.y,dtype=float),np.asarray([p.z[o] for o in a.observations],dtype=float)))
            assert result.success==expected
            assert expected or result.status==2, result.message
            out.update(full_status=int(result.status),full_total_seconds=total,full_build_seconds=result.assembly_seconds,full_solve_seconds=result.solve_seconds,full_stats=result.model_stats)
        elif method in ('compressed','eliminated'):
            model,setup=timed(lambda:CompressedNetworkSimplex(a.arcs,-a.balances,2,a.observations,eliminate_observed=(method=='eliminated')))
            result,total=timed(lambda:model.membership(p));assert result.success==expected
            assert expected or result.status==2, result.message
            out.update({method+'_status':int(result.status),method+'_total_seconds':setup+total,method+'_build_seconds':setup+result.assembly_seconds,
                        method+'_symbolic_seconds':setup,method+'_matrix_seconds':result.assembly_seconds,
                        method+'_solve_seconds':result.solve_seconds,method+'_stats':result.model_stats})
        else:
            model,setup=timed(lambda:FlatChainSimplex((a.edge_count-1)//2,2,a.observations))
            result,online=timed(lambda:model.separate(p,decompose=False))
            assert result.feasible==expected
            out.update(flat_constructor_seconds=setup,flat_online_seconds=online,flat_total_seconds=setup+online)
            if expected:
                constructed,with_decomp=timed(lambda:model.separate(p,decompose=True))
                assert constructed.feasible
                check_decomposition(a,p,constructed.decomposition)
                # Report separate workloads; do not subtract independent timings.
                out.update(flat_with_decomposition_seconds=with_decomp,
                           flat_total_with_decomposition_seconds=setup+with_decomp)
            else:
                assert result.cut.evaluate(p)>0
                out['flat_cut_reason']=result.cut.reason
    return out


def audit_cut(a,p):
    from network_simplex.flat_chain import FlatChainSimplex
    result=FlatChainSimplex((a.edge_count-1)//2,2,a.observations).separate(p,decompose=False)
    assert not result.feasible and result.cut.evaluate(p)>0
    E,m=a.edge_count,2;index={o:i for i,o in enumerate(a.observations)}
    c=np.zeros(E+m+len(index))
    for key,v in result.cut.coefficients.items():
        k=key[1] if key[0]=='x' else E+key[1] if key[0]=='y' else E+m+index[key[1:]]
        c[k]+=float(v)
    lp=full_ef(a,-c)
    assert lp.success and -lp.fun+float(result.cut.constant)<1e-7
    return {'maximum_violation':-lp.fun+float(result.cut.constant),'reason':result.cut.reason}


def main():
    from network_simplex.flat_chain import circuit_library
    parser=argparse.ArgumentParser();parser.add_argument('--repetitions',type=int,default=5)
    parser.add_argument('--lengths',type=int,nargs='+',default=[8,32,128,512])
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('flat-repeated-results.json'))
    args=parser.parse_args();assert args.repetitions>=1 and min(args.lengths)>=2
    circuit_library.cache_clear()
    library,cold=timed(lambda:circuit_library(3))
    # Library API returns normals and positive circuits.
    normals,circuits=library
    out={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
         'repetitions':args.repetitions,'circuit_library_cold_seconds':cold,'positive_circuits':len(circuits),
         'timing_caveat':'Constructors and all LP build/solve steps repeated after one full warmup per case; exact library cached. Method order rotated. Decomposition audits excluded.',
         'cases':[]}
    methods=['full','compressed','eliminated','flat']
    for length in args.lengths:
        for feasible in [True,False]:
            a,p=candidate(length,feasible)
            audit=None if feasible else audit_cut(a,p)
            warmup=once(a,p,feasible,methods)
            runs=[]
            for i in range(args.repetitions):
                shift=i%len(methods)
                runs.append(once(a,p,feasible,methods[shift:]+methods[:shift]))
            case={'gadgets':length,'edges':a.edge_count,'observations':len(a.observations),'feasible':feasible,
                  'cut_support_audit':audit,'warmup_measurements':warmup,'summary_seconds':summary(runs),'runs':runs}
            out['cases'].append(case)
            print(json.dumps({k:case[k] for k in ['gadgets','feasible','summary_seconds']}),flush=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
