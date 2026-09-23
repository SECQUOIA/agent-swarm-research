from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import random,json,hashlib,subprocess
import networkx as nx
ROOT=Path(__file__).resolve().parent
rng=random.Random(3703)
counts={}
# Exact integration of balanced ambient orientation, including restricted supports.
def orient(p,S):
 n=len(p); out=[Q(0) for _ in range(len(S)+2)]
 for J in combinations(range(n),n//2):
  J=set(J); cuts=sorted({Q(0),Q(1)}|{p[i] if i in J else 1-p[i] for i in S})
  for l,u in zip(cuts,cuts[1:]):
   t=(l+u)/2
   k=sum(t<p[i] if i in J else t>1-p[i] for i in S)
   for j in range(len(out)):
    out[j]+=(u-l)*comb(k,j)/comb(n,n//2)
 return out
checks=0
for n in range(2,8):
 for case in range(45):
  p=[Q(rng.randrange(13),12) for _ in range(n)]
  S=sorted(rng.sample(range(n),rng.randrange(1,n+1))); d=len(S)
  O=orient(p,S); P=[Q(0)]*(d+2); C=P.copy(); V=P.copy()
  k=int(sum(p[i] for i in S)); theta=sum(p[i] for i in S)-k
  for j in range(d+2):
   P[j]=sum((__import__('functools').reduce(lambda a,b:a*b,(p[i] for i in A),Q(1)) for A in combinations(S,j)),Q(0))
   C[j]=Q(1) if j==0 else sum((min(p[i] for i in A) for A in combinations(S,j)),Q(0))
   V[j]=(1-theta)*comb(k,j)+theta*comb(k+1,j)
  beta=Q(n*(n-1),2*(n//2)*(n-n//2))
  for j in range(d+2):
   residual=beta*(C[j]-O[j])+V[j]-P[j]+(C[j-1]-P[j-1] if j else 0)
   assert residual>=0,(n,p,S,j,residual)
   checks+=1
counts['rational_coefficient_inequalities']=checks
# Exact all-cycle coloring, every bipartite graph with fixed parts of size 3,4.
accepted=0
for mask in range(1<<12):
 G=nx.Graph();G.add_nodes_from(range(7));G.add_edges_from((i,3+j) for i in range(3) for j in range(4) if mask>>(4*i+j)&1)
 H=G.copy()
 while H:
  v=min(H,key=lambda v:H.degree(v)); neigh=list(H[v])
  if len(neigh)>2:break
  if len(neigh)==2:H.add_edge(*neigh)
  H.remove_node(v)
 if H:continue
 accepted+=1
 cycles=[set(c)&set(range(3,7)) for c in nx.simple_cycles(G) if len(c)%4==2]
 assert any(all(len({color[v-3] for v in C})>1 for C in cycles) for color in product(range(2),repeat=4)),mask
counts['all_3_by_4_bipartite_graphs']=1<<12;counts['treewidth_at_most_two_checked']=accepted
# Incremental-slot gadget versus exhaustive binary optimization; integer costs incl negative.
for trial in range(120):
 n=5; edges=[(rng.randrange(n),rng.randrange(n)) for _ in range(7)];edges=[e for e in edges if e[0]!=e[1]]
 costs=[rng.randrange(-5,6) for _ in edges];deg=[sum(v in e for e in edges) for v in range(n)]
 tables=[]
 for d in deg:
  increments=sorted(rng.randrange(-5,6) for _ in range(d));t=[rng.randrange(-3,4)]
  for inc in increments:t.append(t[-1]+inc)
  tables.append(t)
 best=min(sum(tables[v][sum(v in edges[i] for i in J)] for v in range(n))+sum(costs[i] for i in J) for bits in product(range(2),repeat=len(edges)) for J in [[i for i,b in enumerate(bits) if b]])
 H=nx.Graph(); mandatory=set()
 for i,(u,v) in enumerate(edges):
  a=('a',i);b=('b',i);mandatory|={a,b};H.add_edge(a,b,c=0)
  for j in range(deg[u]):H.add_edge(a,('s',u,j),c=tables[u][j+1]-tables[u][j]+costs[i])
  for j in range(deg[v]):H.add_edge(b,('s',v,j),c=tables[v][j+1]-tables[v][j])
 M=2*sum(abs(data['c']) for a,b,data in H.edges(data=True))+1
 for a,b,data in H.edges(data=True):data['weight']=M*((a in mandatory)+(b in mandatory))-data['c']
 matching=nx.max_weight_matching(H)
 assert mandatory<=set(v for e in matching for v in e)
 val=sum(H[a][b]['c'] for a,b in matching)+sum(t[0] for t in tables)
 assert val==best,(trial,val,best)
counts['integer_matching_gadgets']=120
# Execute precisely the frozen printed programs, as an independent extraction replay.
snap=ROOT.parents[2]/'process/snapshots/whole-round01'
# Resolve repository root without depending on the replay scripts' output paths.
snap=Path('/home/sgusev/repo/minlp-notes/paper-relaxation-limits/process/snapshots/whole-round01')
import re
for name in ['appendix-finite-signings.tex','appendix-cubic-certificates.tex']:
 code='\n'.join(re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',(snap/'sections'/name).read_text(),re.S))
 path=ROOT/(name+'.py');path.write_text(code)
 run=subprocess.run(['python',str(path)],text=True,capture_output=True,check=True)
 (ROOT/(name+'.output')).write_text(run.stdout)
counts['printed_signing_and_cubic_programs']='PASS (exact integer/Fraction replay; no solver)'
counts['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(ROOT/'independent-results.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts,indent=2))
