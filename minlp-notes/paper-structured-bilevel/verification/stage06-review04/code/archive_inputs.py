"""Archive the exact generated convex/screening data, outside timed solves."""
from pathlib import Path
import sys,json,hashlib
P=Path(__file__).resolve().parents[1];R=Path('/home/sgusev/repo/minlp-notes')
sys.path.insert(0,str(R/'code/bilevel_reopened'))
def main():
    (P/'data').mkdir(parents=True,exist_ok=True)
    from quadratic_tariff_benchmarks import tariff_instance
    from approximate_structure_checks import dense_family
    sets={}
    for n in (100,1000,10000):
        p=tariff_instance(n,50001+n,1)
        sets['convex_'+str(n)]=dict(instance=p.__dict__,objective=dict(x=0,z=[0]*n,xx=0,xz=[-1]*n),rows=[dict(a=0,b=[-1]*n,rhs=str(-(n//5)))])
    for n in (8,20):
        Q,Qhat,c,C,obj,rows=dense_family(n)
        sets['screening_'+str(n)]=dict(Q=Q.tolist(),Qhat=Qhat.tolist(),c=list(c),C=list(C),objective=[obj[0],list(obj[1])],rows=[[a,list(b),rhs] for a,b,rhs in rows],lo=0,hi=1)
    p=P/'data/stage06-convex-screening-inputs.json';p.write_text(json.dumps(sets,default=str,indent=2)+'\n')
    return p
if __name__=='__main__':main()
