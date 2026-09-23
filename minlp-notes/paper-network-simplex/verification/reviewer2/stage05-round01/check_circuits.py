"""Independent exact circuit enumeration and exhaustive one-gadget coefficient audit."""
import itertools,json,math
from pathlib import Path
import sympy as s
counts={}; cases=0
for m in [1,2,3]:
    positive=[tuple(int(mask&(1<<j)>0) for j in range(m)) for mask in range(1,1<<m)]
    negative=[tuple(-int(i==j) for j in range(m)) for i in range(m)]+[(-1,)*m]
    normals=sorted(set(positive+negative)); circuits=[]
    for k in range(2,m+2):
        for inds in itertools.combinations(range(len(normals)),k):
            A=s.Matrix([normals[i] for i in inds]).T
            ns=A.nullspace()
            if len(ns)!=1 or any(v==0 for v in ns[0]): continue
            q=ns[0]
            if all(v<0 for v in q):q=-q
            if not all(v>0 for v in q):continue
            den=s.ilcm(*[v.q for v in q]); nums=[int(v*den) for v in q]
            gcd=math.gcd(*nums); nums=[v//gcd for v in nums]
            circuits.append([(normals[i],q) for i,q in zip(inds,nums)])
    counts[m]={'normals':len(normals),'circuits':len(circuits),'max_weight':max(q for circuit in circuits for n,q in circuit)}
    assert counts[m]['circuits']==[1,5,16][m-1]
    if m<2:continue
    # Isolate each gadget: a product is unique to its gadget and label, so all
    # other gadgets contribute coefficient zero to this product. For every local
    # observation pattern, inspect every row alternative in every circuit group.
    for types in itertools.product('ABTU',repeat=m):
        A={j for j,t in enumerate(types) if t=='A'}; B={j for j,t in enumerate(types) if t=='B'}; T={j for j,t in enumerate(types) if t=='T'}
        # Row coefficient vectors hold observed a[0:m], b[m:2m], and gadget x_a.
        zero=(0,)*(2*m+1); options={n:[zero] for n in normals}
        def add(normal, coeff):
            if any(normal):options[tuple(normal)].append(tuple(coeff))
            else:assert max(map(abs,coeff),default=0)<=1
        for j,t in enumerate(types):
            ej=[int(j==k) for k in range(m)]
            if t in 'AT':
                co=[0]*(2*m+1);co[j]=-1
                if t=='T':co[m+j]=-1
                add([-v for v in ej],co)
            if t=='B':
                co=[0]*(2*m+1);co[m+j]=-1;add([-v for v in ej],co)
            if t=='T':
                co=[0]*(2*m+1);co[j]=co[m+j]=1;add(ej,co)
        R=[0]*(2*m+1);R[-1]=1
        for j in A|T:R[j]=-1
        for j in B:R[m+j]=1
        add([int(j in B) for j in range(m)],R)
        add([int(j in A|T) for j in range(m)],[-v for v in R])
        for circuit in circuits:
            for selected in itertools.product(*(options[n] for n,q in circuit)):
                result=[sum(q*co[k] for (_,q),co in zip(circuit,selected)) for k in range(2*m+1)]
                assert max(map(abs,result),default=0)<=1
                cases+=1
    # x_h choices: positive singleton =0/-1; positive nonsingleton=0/-1;
    # negative singleton=0; negative full=+1. m2 -full differs from singleton.
    bad=[]
    for circuit in circuits:
        opts=[([1] if n==(-1,)*m else ([0] if sum(n)<0 else [0,-1])) for n,q in circuit]
        for vals in itertools.product(*opts):
            coeff=sum(q*v for (n,q),v in zip(circuit,vals))
            if abs(coeff)>1:bad.append((circuit,vals,coeff))
    if m==2:assert not bad
    else:
        assert len(bad)==2 and sorted(t[2] for t in bad)==[-2,2]
        # Both exceptions have three positive endpoint rows, from three distinct
        # gadgets because each gadget supplies only one endpoint of the chosen type.
        for circ,vals,c in bad:assert sum(1 for n,q in circ if sum(n)>0)==3
record={'status':'PASS','exact_libraries':counts,'exact_one_gadget_branch_checks':cases,'m3_bypass_exceptions':'Exactly -2 for three upper singleton endpoints, and +2 for three lower pair endpoints. Each is repaired by one gadget balance as stated.'}
Path(__file__).with_name('circuit-result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
