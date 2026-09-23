"""Exact rational certificates for numerical asymmetric-quadratic envelope flows.

The verifier uses only Fraction arithmetic and integer roots. Numerical routines
appear only in the test/demo certificate producer, not in verify_certificate.
"""
from dataclasses import dataclass, replace
from fractions import Fraction as F
from math import isqrt


def upward_root(value,degree,bits=80):
    """Smallest bits-dyadic upper enclosure of a nonnegative rational root."""
    value=F(value)
    assert value>=0 and degree in (2,3)
    scaled=value.numerator << (degree*bits)
    denominator=value.denominator
    if degree==2:
        k=isqrt(scaled//denominator)
    else:
        target=scaled//denominator
        lo,hi=0,1 << ((target.bit_length()+2)//3)
        while lo<hi:
            mid=(lo+hi+1)//2
            if mid**3<=target:
                lo=mid
            else:
                hi=mid-1
        k=lo
    if k**degree*denominator<scaled:
        k+=1
    result=F(k,1 << bits)
    assert result**degree>=value
    return result


def dyadic(value,bits=80):
    return F(round(F(float(value))*(1 << bits)),1 << bits)


def conserved_rounding(edges,b,numerical,bits=80):
    import networkx as nx
    require(all(isinstance(u,int) and isinstance(v,int) and 0<=u<len(b) and
                0<=v<len(b) and u!=v for u,v in edges),
            "rounding helper requires loopless valid edges")
    require(len({frozenset(edge) for edge in edges})==len(edges),
            "rounding helper requires a simple graph")
    graph=nx.Graph()
    graph.add_nodes_from(range(len(b)))
    graph.add_edges_from(edges)
    require(len(b)>0 and nx.is_connected(graph),"rounding helper requires a connected graph")
    tree=nx.minimum_spanning_tree(graph)
    index={frozenset(edge):e for e,edge in enumerate(edges)}
    y=[F(0)]*len(edges)
    residual=list(map(F,b))
    for e,(u,v) in enumerate(edges):
        if not tree.has_edge(u,v):
            y[e]=dyadic(numerical[e],bits)
            residual[u]-=y[e]
            residual[v]+=y[e]
    leaves=[v for v in tree if tree.degree(v)==1]
    while leaves:
        leaf=leaves.pop()
        if tree.degree(leaf)!=1:
            continue
        parent=next(iter(tree[leaf]))
        e=index[frozenset((leaf,parent))]
        y[e]=residual[leaf] if edges[e][0]==leaf else -residual[leaf]
        residual[parent]+=residual[leaf]
        residual[leaf]=F(0)
        tree.remove_edge(leaf,parent)
        if tree.degree(parent)==1:
            leaves.append(parent)
    require(all(r==0 for r in residual),"rounding helper requires balanced nominations")
    return y


def law(x,positive,negative):
    return (positive if x>=0 else negative)*x*abs(x)


def energy(y,positive,negative):
    return sum((positive[e] if x>=0 else negative[e])*abs(x)**3/F(3)
               for e,x in enumerate(y))


@dataclass
class Certificate:
    flow:list
    potentials:list
    root_upper:list
    gap:F
    radius:F


def make_certificate(edges,b,positive,negative,flow,potentials,bits=80):
    y=list(map(F,flow))
    p=list(map(F,potentials))
    roots=[]
    for e,(u,v) in enumerate(edges):
        d=p[u]-p[v]
        coefficient=positive[e] if d>=0 else negative[e]
        roots.append(upward_root(abs(d)**3/coefficient,2,bits))
    lower=sum(F(bv)*pv for bv,pv in zip(b,p))-F(2,3)*sum(roots)
    gap=energy(y,positive,negative)-lower
    assert gap>=0
    radius=upward_root(6*gap/min(positive+negative),3,bits)
    certificate=Certificate(y,p,roots,gap,radius)
    verify_certificate(edges,b,positive,negative,certificate)
    return certificate


def require(condition,message):
    if not condition:
        raise ValueError("Invalid certificate: "+message)


def verify_certificate(edges,b,positive,negative,certificate):
    """Check exact conditions, including under Python's optimized mode."""
    m,n=len(edges),len(b)
    y,p=certificate.flow,certificate.potentials
    require(len(y)==m and len(p)==n and len(certificate.root_upper)==m,"vector dimensions")
    require(len(positive)==m and len(negative)==m and m>0,"coefficient dimensions")
    require(all(isinstance(v,F) for v in b+positive+negative+y+p+certificate.root_upper+
                [certificate.gap,certificate.radius]),"all scalar data must be rational Fractions")
    require(all(c>0 for c in positive+negative),"coefficients must be positive")
    loads=[F(0)]*n
    for e,((u,v),x,upper) in enumerate(zip(edges,y,certificate.root_upper)):
        require(isinstance(u,int) and isinstance(v,int) and 0<=u<n and 0<=v<n,"edge indices")
        loads[u]+=x
        loads[v]-=x
        d=p[u]-p[v]
        coefficient=positive[e] if d>=0 else negative[e]
        require(upper>=0 and upper**2*coefficient>=abs(d)**3,"upward conjugate root bound")
    require(loads==b,"exact conservation")
    lower=sum(bv*pv for bv,pv in zip(b,p))-F(2,3)*sum(certificate.root_upper)
    require(certificate.gap==energy(y,positive,negative)-lower and certificate.gap>=0,"energy gap")
    require(certificate.radius>=0,"nonnegative radius")
    require(certificate.radius**3*min(positive+negative)>=6*certificate.gap,"flow radius bound")
    return True


def write_certificate(path,edges,b,positive,negative,certificate):
    import json
    payload={"edges":edges,"b":list(map(str,b)),
             "positive":list(map(str,positive)),"negative":list(map(str,negative)),
             "flow":list(map(str,certificate.flow)),
             "potentials":list(map(str,certificate.potentials)),
             "root_upper":list(map(str,certificate.root_upper)),
             "gap":str(certificate.gap),"radius":str(certificate.radius)}
    with open(path,"w") as stream:
        json.dump(payload,stream,indent=2)
        stream.write("\n")


def verify_file(path):
    import json
    with open(path) as stream:
        payload=json.load(stream)
    certificate=Certificate(list(map(F,payload["flow"])),
                            list(map(F,payload["potentials"])),
                            list(map(F,payload["root_upper"])),
                            F(payload["gap"]),F(payload["radius"]))
    verify_certificate(payload["edges"],list(map(F,payload["b"])),
                       list(map(F,payload["positive"])),
                       list(map(F,payload["negative"])),certificate)
    print("Exact rational certificate verified; radius =",certificate.radius)


def run(example_path=None):
    import networkx as nx
    import numpy as np
    from envelope_socp_checks import conic_flow
    from series_parallel_envelope_checks import incidence,physical
    rng=np.random.default_rng(593501)
    count=0
    max_radius=max_pressure_width=max_scenario_bound=max_actual=0.
    for k in [3,5,8]:
        graph=nx.complete_bipartite_graph(2,k)
        A,edges=incidence(graph)
        b=[F(int(v),3) for v in rng.integers(-4,5,len(graph)-1)]
        b.append(-sum(b))
        bf=np.array(list(map(float,b)))
        m=len(edges)
        lower=[F(int(v),3) for v in rng.integers(2,5,m)]
        upper=[l+F(int(v),3) for l,v in zip(lower,rng.integers(1,4,m))]
        target=k % m
        q=np.zeros(len(graph))
        u,v=edges[target]
        q[u],q[v]=1.,-1.
        h=np.zeros(len(graph))
        h[1:]=np.linalg.solve((A@A.T)[1:,1:],q[1:])
        signs=np.sign(A.T@h)
        for direction in [-1,1]:
            status=direction*signs
            status[target]=-direction
            positive=[upper[e] if status[e]>0 else lower[e] for e in range(m)]
            negative=[upper[e] if status[e]<0 else lower[e] for e in range(m)]
            pf,nf=np.array(list(map(float,positive))),np.array(list(map(float,negative)))
            numeric,_,_,solver_status=conic_flow(A,bf,pf,nf)
            y=conserved_rounding(edges,b,numeric)
            drops=np.array([float(law(x,positive[e],negative[e])) for e,x in enumerate(y)])
            p=[dyadic(v) for v in np.linalg.lstsq(A.T,drops,rcond=None)[0]]
            cert=make_certificate(edges,b,positive,negative,y,p)
            exact=physical(A,bf,pf,nf)
            actual=max(abs(np.array(list(map(float,y)))-exact))
            assert actual<=float(cert.radius)+1e-10
            radius=cert.radius
            pressure_width=law(y[target]+radius,positive[target],negative[target])-law(y[target]-radius,positive[target],negative[target])
            C0=1+F(2*m)*max(upper)/min(lower)
            scenario_bound=C0*radius
            assert verify_certificate(edges,b,positive,negative,cert)
            # Distinct negative controls: conservation, root enclosure, energy gap, modulus.
            bad_flow=list(y);bad_flow[0]+=1
            bad_roots=list(cert.root_upper)
            nonzero=next(e for e,r in enumerate(bad_roots) if r>F(1,1<<40))
            bad_roots[nonzero]/=2
            malformed=[replace(cert,flow=bad_flow),replace(cert,root_upper=bad_roots),
                       replace(cert,gap=cert.gap+1),replace(cert,radius=F(0))]
            for bad in malformed:
                try:
                    verify_certificate(edges,b,positive,negative,bad)
                except ValueError:
                    pass
                else:
                    raise AssertionError('Corrupted certificate accepted')
            print(f'rank{k-1}, direction{direction:+}: certified flow radius {float(radius):.3g}, envelope-pressure width {float(pressure_width):.3g}, scenario loss <= {float(scenario_bound):.3g}; observed flow error {actual:.3g}; status {solver_status}')
            max_radius=max(max_radius,float(radius));max_pressure_width=max(max_pressure_width,float(pressure_width))
            max_scenario_bound=max(max_scenario_bound,float(scenario_bound));max_actual=max(max_actual,actual)
            if example_path is not None and count==0:
                write_certificate(example_path,edges,b,positive,negative,cert)
            count+=1
    import subprocess,sys,tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as directory:
        bad_path=Path(directory)/"corrupted.json"
        write_certificate(bad_path,edges,b,positive,negative,replace(cert,gap=cert.gap+1))
        completed=subprocess.run([sys.executable,'-O',__file__,'--verify',str(bad_path)],
                                 capture_output=True,text=True)
        if completed.returncode==0 or 'Invalid certificate: energy gap' not in completed.stderr:
            raise RuntimeError('Optimized-mode verifier accepted a corrupted certificate')
    for bad_edges in [[(0,1),(0,1)],[(0,0)],[(0,1)]]:
        try:
            conserved_rounding(bad_edges,[F(1),F(-1),F(0)],[0.]*len(bad_edges))
        except ValueError:
            pass
        else:
            raise RuntimeError('Rounding helper accepted an unsupported graph')
    print(f'{count} exact rational certificates and {4*count} corruption rejections passed; optimized-mode corruption and3 unsupported rounding graphs also rejected.')
    print(f'Max certified radius {max_radius:.3g}; pressure width {max_pressure_width:.3g}; endpoint loss bound {max_scenario_bound:.3g}; observed error {max_actual:.3g}.')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--verify',metavar='JSON')
    group.add_argument('--write-example',metavar='JSON')
    args=parser.parse_args()
    if args.verify:
        verify_file(args.verify)
    else:
        run(args.write_example)
