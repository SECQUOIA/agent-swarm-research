"""Reviewer-only exact checks of degenerate networks and general graph lifts."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
import sys,json
s=Path('/home/sgusev/repo/minlp-notes/paper-power-flow/process/snapshots/full-round01')
sys.path.insert(0,str(s/'checks'))
import check_resistive_exact as r
import check_developments_exact as d
import check_ac_exact as a
import check_arithmetic_exact as b
out={}
# Empty source and independent unused coordinates preserve the entire box.
profiles=0
for n in range(5):
 names=tuple('x'+str(i) for i in range(n))
 net=r.build(names,())
 r.structural_checks(net)
 for vals in product((F(1,2),F(1),F(2)),repeat=n):
  v=r.profile(net,dict(zip(names,vals)))
  assert not any(d.violations(net,v).values())
  assert len(net.buses)==n and not net.edges
  profiles+=1
out['empty_and_unused_profiles']=profiles
# Connected structural convention for the unique R^0 point: one pinned bus.
net=r.Network((),())
i=net.bus('empty_source',(1,1),(0,0))
v={i:F(1)}
for L in (1,2,7):
 sub,w=d.subdivide(net,v,L)
 assert len(sub.buses)==1 and not sub.edges
 assert d.bipartite_and_girth(sub)==float('inf')
 assert not any(d.violations(sub,w).values())
out['empty_source_connected_subdivision_scales']=3
# Every endpoint assignment survives connection and subdivision of unused roots.
connected=0
for n in range(1,5):
 names=tuple('u'+str(i) for i in range(n))
 for vals in product((F(1,2),F(2)),repeat=n):
  net=d.widened(names,())
  v=d.wide_profile(net,dict(zip(names,vals)))
  net,v=d.connect(net,v)
  for L in (1,3):
   sub,w=d.subdivide(net,v,L)
   assert len(d.components(sub))==1
   assert d.bipartite_and_girth(sub)==float('inf')
   assert max(map(len,d.adjacency(sub).values()))<=3
   assert not any(d.violations(sub,w).values())
   assert all(w[net.roots[x]]==y for x,y in zip(names,vals))
   connected+=1
out['unused_root_connected_subdivision_profiles']=connected
# Whole-graph real lifts, independently in exact eighth-turn units.
# Integer winding potential test is compared with exhaustive bus lifts.
directions=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
cases=obstructed=0
for n in range(4):
 pairs=list(combinations(range(n),2))
 for mask in range(1<<len(pairs)):
  edges=[p for z,p in enumerate(pairs) if mask>>z&1]
  for phase in product(range(8),repeat=n):
   diffs={}
   ks={}
   for i,j in edges:
    raw=phase[j]-phase[i]
    if raw%8==4: break
    short=(raw+4)%8-4
    diffs[i,j]=short
    ks[i,j]=a.crossing(directions[phase[i]],directions[phase[j]])
    assert raw+8*ks[i,j]==short
   else:
    pot={}
    consistent=True
    for root in range(n):
     if root in pot: continue
     pot[root]=0
     todo=[root]
     while todo:
      i=todo.pop()
      for u,w in edges:
       if i not in (u,w): continue
       j=w if i==u else u
       diff=ks[u,w] if i==u else -ks[u,w]
       if j in pot:
        consistent &= pot[j]==pot[i]+diff
       else:
        pot[j]=pot[i]+diff
        todo.append(j)
    exists=any(all(phase[j]+8*z[j]-phase[i]-8*z[i]==diffs[i,j]
                   for i,j in edges) for z in product(range(-2,3),repeat=n))
    assert consistent==exists
    cases+=1
    obstructed+=not exists
out['whole_graph_lift_cases']=cases
out['whole_graph_lift_obstructions']=obstructed
# The inverse/square identities hold beyond the forward range neighborhood;
# violations of auxiliary bounds do not mask an algebraic reversal error.
squares=products=0
for av in (F(1,2),F(3,4),F(1),F(5,4),F(3,2),F(2)):
 circuit=b.Bounded(); ai=circuit.new(av)
 oi=circuit.square(ai)
 assert circuit.values[oi]==av*av
 squares+=1
 for bv in (F(1,2),F(1),F(2)):
  circuit=b.Bounded(); ai=circuit.new(av); bi=circuit.new(bv)
  oi=circuit.multiply(ai,bi)
  assert circuit.values[oi]==av*bv
  products+=1
out['off_neighborhood_square_identities']=squares
out['off_neighborhood_product_identities']=products
print(json.dumps(out,indent=2))
