"""Reproducible end-to-end benchmark; run from any directory with Python.

Times include LP assembly and solution, or separator preprocessing/separation as
labelled. Sparse matrix bytes are storage of input CSR matrices only, not peak
process memory. No run is a claim about optimized native solver performance.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import platform
import scipy
import sys
import time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from network_simplex.separator import NetworkSimplex, Point
from network_simplex_compressed import CompressedNetworkSimplex
from baselines import block_chain, full_ef, compressed_ef, full_ef_membership, OriginalLP, incidence


def point(instance, vector):
    E,m=instance.edge_count,instance.simplex_size
    q=[F(float(v)).limit_denominator(1_000_000) for v in vector]
    assert max(abs(float(a)-b) for a,b in zip(q,vector))<1e-7
    result=Point(q[:E],q[E:E+m],dict(zip(instance.observations,q[E+m:])))
    net=[F(0)]*len(instance.balances)
    for f,(a,b,_) in zip(result.x,instance.arcs): net[a]+=f;net[b]-=f
    assert net==[F(float(v)) for v in instance.balances], 'LP rational reconstruction did not preserve balances'
    return result


def cut_terms(instance,cut):
    E,m=instance.edge_count,instance.simplex_size
    obs={o:k for k,o in enumerate(instance.observations)}
    def idx(k):
        return k[1] if k[0]=='x' else E+k[1] if k[0]=='y' else E+m+obs[k[1:]]
    return [(idx(k),float(v)) for k,v in cut.coefficients.items()]


def timed(fn):
    start=time.perf_counter();out=fn();return out,time.perf_counter()-start


def check_decomposition(instance,p,dec):
    E=instance.edge_count
    total=[F(0)]*E
    for j in dec.positive_states():
        f=dec.flow(j)
        net=[F(0)]*len(instance.balances)
        for e,(a,b,u) in enumerate(instance.arcs):
            assert 0<=f[e]<=F(u)
            net[a]+=f[e];net[b]-=f[e]
            total[e]+=dec.weights[j]*f[e]
        assert net==[F(float(v)) for v in instance.balances]
        for e,h in instance.observations:
            if h==j: assert dec.weights[j]*f[e]==p.z[e,h]
    assert total==list(p.x)


def optimize_case(seed,blocks,paths,states,observed_states=3,max_rounds=500,fixed=True,audit_cuts=True):
    a=block_chain(seed=seed,blocks=blocks,paths=paths,states=states,observed_states=observed_states)
    E,m=a.edge_count,a.simplex_size
    rng=np.random.default_rng(seed+1000)
    c=np.r_[rng.normal(scale=.15,size=E),np.zeros(m),rng.normal(size=len(a.observations))]
    y=np.ones(m)*(.9/m) if fixed else None
    model,prep=timed(lambda:NetworkSimplex(a.arcs,(-a.balances).tolist(),m,a.observations))
    full,full_time=timed(lambda:full_ef(a,c,y))
    compact,compact_time=timed(lambda:compressed_ef(a,c,y))
    assert full.success and compact.success
    assert abs(full.fun-compact.fun)<1e-7
    general_model,general_prep=timed(lambda:CompressedNetworkSimplex(a.arcs,(-a.balances).tolist(),m,a.observations))
    general,general_solve=timed(lambda:general_model.optimize(c,y_fixed=y))
    assert general.success and abs(general.fun-full.fun)<1e-7
    lp,mc_assembly=timed(lambda:OriginalLP(a,y))
    initial,mc_time=timed(lambda:lp.solve(c));assert initial.success
    reasons={}; separation_time=0.;lp_time=mc_time;validated_cuts=0;overhead=0.
    lp_matrix_seconds=initial.assembly_seconds;lp_engine_seconds=initial.solve_seconds
    result=initial
    for rounds in range(max_rounds+1):
        p,elapsed=timed(lambda:point(a,result.x));overhead+=elapsed
        separated,elapsed=timed(lambda:model.separate(p,decompose=True));separation_time+=elapsed
        if separated.feasible:
            check_decomposition(a,p,separated.decomposition)
            assert abs(result.fun-full.fun)<1e-7
            break
        cut=separated.cut
        assert cut.evaluate(p)>0
        # An independent full-EF support optimization checks every generated cut.
        cc=np.zeros(len(c))
        for k,v in cut_terms(a,cut): cc[k]=v
        if audit_cuts:
            audit=full_ef(a,-cc)
            assert audit.success and -audit.fun+float(cut.constant)<1e-7, (cut.reason,-audit.fun,float(cut.constant))
            validated_cuts+=1
        reasons[cut.reason]=reasons.get(cut.reason,0)+1
        _,elapsed=timed(lambda:lp.add_cut(cut_terms(a,cut),-float(cut.constant)));overhead+=elapsed
        result,elapsed=timed(lambda:lp.solve(c));lp_time+=elapsed
        assert result.success
        lp_matrix_seconds+=result.assembly_seconds;lp_engine_seconds+=result.solve_seconds
    else:
        raise AssertionError('cut iteration limit')
    # Validation time is deliberately excluded from the optimization loop timing.
    return dict(seed=seed,blocks=blocks,paths=paths,states=states,edges=E,observations=len(a.observations),fixed_y=fixed,
                original_variables=len(c),preprocessing_seconds=prep,
                full_ef_seconds=full_time,full_ef_assembly_seconds=full.assembly_seconds,full_ef_solve_seconds=full.solve_seconds,
                compressed_ef_seconds=compact_time,compressed_ef_assembly_seconds=compact.assembly_seconds,compressed_ef_solve_seconds=compact.solve_seconds,
                general_compressed_preprocessing_seconds=general_prep,general_compressed_solve_seconds=general_solve,
                general_compressed_matrix_seconds=general.assembly_seconds,general_compressed_engine_seconds=general.solve_seconds,
                general_compressed_build_seconds=general_prep+general.assembly_seconds,
                general_compressed_seconds=general_prep+general_solve,general_compressed=general.model_stats,
                mccormick_assembly_seconds=mc_assembly,mccormick_seconds=mc_assembly+mc_time,
                cut_lp_matrix_seconds=lp_matrix_seconds,cut_lp_engine_seconds=lp_engine_seconds,
                cut_lp_seconds=lp_time,separation_seconds=separation_time,cut_loop_overhead_seconds=overhead,
                cutting_plane_seconds=prep+mc_assembly+lp_time+separation_time+overhead,
                mccormick_objective=initial.fun,hull_objective=full.fun,absolute_gap=full.fun-initial.fun,
                iterations=rounds,independently_validated_cuts=validated_cuts,cut_reasons=reasons,
                full_ef=full.model_stats,compressed_ef=compact.model_stats,final_original_lp=result.model_stats,
                final_decomposition_verified=True)


def membership_data(seed,blocks,paths,states,observed_states=3):
    a=block_chain(seed=seed,blocks=blocks,paths=paths,states=states,observed_states=observed_states)
    E,m=a.edge_count,a.simplex_size
    weights=[F(1,2*m)]*m
    x=[F(float(v)) for v in a.reference]
    z={(e,j):F(float(a.reference[e]))*weights[j] for e,j in a.observations}
    for bi,block in enumerate(a.blocks):
        for j in range(m):
            i=(j+bi)%len(block); h=(i+1)%len(block); d=F((j%3)-1,4)
            for path,delta in [(block[i],d),(block[h],-d)]:
                for e,sign in path:
                    x[e]+=weights[j]*sign*delta
                    if (e,j) in z: z[e,j]+=weights[j]*sign*delta
    return a,Point(x,weights,z)


def membership_case(seed,blocks,paths,states,observed_states=3):
    a,p=membership_data(seed,blocks,paths,states,observed_states)
    E,m=a.edge_count,a.simplex_size
    model,prep=timed(lambda:NetworkSimplex(a.arcs,(-a.balances).tolist(),m,a.observations))
    separated,sep_time=timed(lambda:model.separate(p,decompose=True))
    assert separated.feasible
    check_decomposition(a,p,separated.decomposition)
    ef,ef_time=timed(lambda:full_ef_membership(a,np.array(p.x,dtype=float),np.array(p.y,dtype=float),np.array([p.z[o] for o in a.observations],dtype=float)))
    assert ef.success
    general_model,general_prep=timed(lambda:CompressedNetworkSimplex(a.arcs,(-a.balances).tolist(),m,a.observations))
    general,general_solve=timed(lambda:general_model.membership(p))
    assert general.success
    return dict(seed=seed,blocks=blocks,paths=paths,states=states,edges=E,observations=len(a.observations),
                preprocessing_seconds=prep,separation_seconds=sep_time,full_ef_seconds=ef_time,full_ef=ef.model_stats,
                general_compressed_preprocessing_seconds=general_prep,general_compressed_solve_seconds=general_solve,
                general_compressed_matrix_seconds=general.assembly_seconds,general_compressed_engine_seconds=general.solve_seconds,
                general_compressed_build_seconds=general_prep+general.assembly_seconds,
                general_compressed_seconds=general_prep+general_solve,general_compressed=general.model_stats,
                decomposition_verified=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    # Warm up HiGHS once; timings below include model construction.
    warm=block_chain(blocks=1,states=2);full_ef(warm,np.zeros(warm.edge_count+2+len(warm.observations)))
    optimization=[]
    specs=[(31,1,4,8),(32,2,4,32),(33,4,5,128)]
    if args.quick: specs=specs[:1]
    for spec in specs:
        for fixed in (False,True):
            r=optimize_case(*spec,fixed=fixed);optimization.append(r)
            print(json.dumps({'optimization':r}),flush=True)
    membership=[]
    for states in ([16,128] if args.quick else [16,128,1024]):
        r=membership_case(41,4,6,states);membership.append(r)
        print(json.dumps({'membership':r}),flush=True)
    output={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'seed_policy':'fixed seeds listed per case','optimization':optimization,'membership':membership,
            'timing_caveat':'Sums of selected implementation components: Python rational separator versus SciPy HiGHS; assembly, point reconstruction, and cut-addition included; cut-validation and decomposition-audit time excluded.',
            'memory_caveat':'matrix_bytes counts input CSR arrays only, not solver/process peak memory.'}
    if args.output: args.output.write_text(json.dumps(output,indent=2)+'\n')

if __name__=='__main__':main()
