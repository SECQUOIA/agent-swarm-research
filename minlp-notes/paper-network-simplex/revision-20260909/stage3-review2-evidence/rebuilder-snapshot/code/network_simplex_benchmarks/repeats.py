"""Five repetitions of the key cases after unrecorded warmups.

Separate symbolic/model assembly, numeric matrix assembly, and HiGHS solve
where available. These are synthetic implementation measurements, not an
asymptotic comparison. Independent cut support audits run once, outside timing.
"""
from pathlib import Path
import argparse
import json
import platform
from statistics import median
import scipy
from run import (np, block_chain, NetworkSimplex, CompressedNetworkSimplex,
                 full_ef_membership, point, check_decomposition, membership_data,
                 optimize_case, timed)


def summary(values):
    return {'median':median(values),'minimum':min(values),'maximum':max(values)}


def aggregate(runs):
    keys=[k for k in runs[0] if k.endswith('_seconds')]
    return {k:summary([r[k] for r in runs]) for k in keys}


def member_run(a,p,order):
    out={}
    for method in order:
        if method=='full':
            result,total=timed(lambda:full_ef_membership(a,np.array(p.x,dtype=float),np.array(p.y,dtype=float),np.array([p.z[o] for o in a.observations],dtype=float)))
            assert result.success
            out.update(full_total_seconds=total,full_build_seconds=result.assembly_seconds,
                       full_solve_seconds=result.solve_seconds,full_stats=result.model_stats)
        elif method=='separator':
            model,build=timed(lambda:NetworkSimplex(a.arcs,-a.balances,a.simplex_size,a.observations))
            result,solve=timed(lambda:model.separate(p,decompose=True))
            assert result.feasible
            # Exact full-state audit is outside timed components.
            check_decomposition(a,p,result.decomposition)
            out.update(separator_total_seconds=build+solve,separator_build_seconds=build,separator_solve_seconds=solve)
        else:
            eliminated=method=='eliminated'
            model,setup=timed(lambda:CompressedNetworkSimplex(a.arcs,-a.balances,a.simplex_size,a.observations,eliminate_observed=eliminated))
            result,solve=timed(lambda:model.membership(p))
            assert result.success
            out.update({method+'_total_seconds':setup+solve,method+'_symbolic_seconds':setup,
                        method+'_matrix_seconds':result.assembly_seconds,
                        method+'_build_seconds':setup+result.assembly_seconds,
                        method+'_solve_seconds':result.solve_seconds,
                        method+'_stats':result.model_stats})
    return out


def opt_run(a,c,y):
    # This invokes the exact same graph, objective, and y as the original suite.
    out=optimize_case(33,4,5,128,fixed=True,audit_cuts=False)
    model,setup=timed(lambda:CompressedNetworkSimplex(a.arcs,-a.balances,a.simplex_size,a.observations,eliminate_observed=True))
    result,solve=timed(lambda:model.optimize(c,y_fixed=y))
    assert result.success and abs(result.fun-out['hull_objective'])<1e-7
    # Exact certificate check on the new formulation's numerical optimizer.
    p=point(a,result.original_point)
    sep=NetworkSimplex(a.arcs,-a.balances,a.simplex_size,a.observations).separate(p,decompose=True)
    assert sep.feasible
    check_decomposition(a,p,sep.decomposition)
    out.update(eliminated_total_seconds=setup+solve,eliminated_symbolic_seconds=setup,
               eliminated_matrix_seconds=result.assembly_seconds,eliminated_build_seconds=setup+result.assembly_seconds,
               eliminated_solve_seconds=result.solve_seconds,eliminated_stats=result.model_stats)
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repetitions',type=int,default=5)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('repeated-results.json'))
    args=parser.parse_args()
    assert args.repetitions>=1
    output={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'repetitions':args.repetitions,
            'method':'At least one unrecorded warmup per case (optimization also audited once), then repeated construction and solution; membership method order rotated.',
            'timing_caveat':'Component sums exclude certificate audits and bookkeeping. Full model construction repeated; this is not a persistent native-solver callback comparison.',
            'membership':[]}
    methods=['full','compressed','eliminated','separator']
    for states in [16,128,1024]:
        a,p=membership_data(41,4,6,states)
        member_run(a,p,methods)
        runs=[]
        for repeat in range(args.repetitions):
            shift=repeat%len(methods);order=methods[shift:]+methods[:shift]
            runs.append(member_run(a,p,order))
        case={'states':states,'edges':a.edge_count,'observations':len(a.observations),
              'summary_seconds':aggregate(runs),'runs':runs}
        output['membership'].append(case)
        print(json.dumps({'membership':{'states':states,'summary':case['summary_seconds']}}),flush=True)
    a=block_chain(seed=33,blocks=4,paths=5,states=128)
    rng=np.random.default_rng(1033)
    c=np.r_[rng.normal(scale=.15,size=a.edge_count),np.zeros(128),rng.normal(size=len(a.observations))]
    y=np.ones(128)*(.9/128)
    # Once-only fresh audit of every cut in the changed-code environment; this
    # also warms up every original optimization method on this exact workload.
    audit=optimize_case(33,4,5,128,fixed=True,audit_cuts=True)
    opt_run(a,c,y)
    runs=[opt_run(a,c,y) for _ in range(args.repetitions)]
    output['optimization']={'seed':33,'states':128,'edges':a.edge_count,'fixed_y':True,
                            'once_only_independently_validated_cuts':audit['independently_validated_cuts'],
                            'summary_seconds':aggregate(runs),'runs':runs}
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'optimization':output['optimization']['summary_seconds']}),flush=True)

if __name__=='__main__':main()
