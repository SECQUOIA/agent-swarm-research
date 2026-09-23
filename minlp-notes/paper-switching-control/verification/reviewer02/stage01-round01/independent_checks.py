from fractions import Fraction as Q
from itertools import product, permutations
import random

counts = {}
# Enumerate complete cell words, allowing repetitions, and evaluate every prefix.
uniform_cases=0
words_checked=0
for n in range(2,7):
  for N in range(1,7 if n <=5 else 6):
    by_s=[None]*(n-1)
    for word in product(range(n),repeat=N):
      s=sum(a!=b for a,b in zip(word,word[1:]))
      if s>n-2: continue
      occ=[0]*n; K=0
      for j,p in enumerate(word,1):
        occ[p]+=1
        K=max(K,max(abs(j-n*x) for x in occ))
      words_checked+=1
      for budget in range(s,n-1):
        by_s[budget]=K if by_s[budget] is None else min(K,by_s[budget])
    for s,brute in enumerate(by_s):
      for K in range(N,N*(n-1)+1):
        b=0
        for _ in range(s+1): b=(n*b+K)//(n-1)
        if b>=N: break
      assert K==brute,(n,N,s,K,brute)
      r=Q(n,n-1); E=max(Q(N,n),Q(N,n)/(r**(s+1)-1))
      assert E<=Q(brute,n)<E+Q(n-1,n)
      uniform_cases+=1
counts['uniform_grid_parameter_cases']=uniform_cases
counts['complete_schedule_words_checked']=words_checked

# Direct piecewise-affine cumulative evaluation. No repository imports.
def cumul(rows,t):
  n=len(rows[0]); out=[Q(0)]*n
  for j,row in enumerate(rows):
    length=max(Q(0),min(Q(1),t-j))
    for i,x in enumerate(row): out[i]+=length*x
  return out

def direct_error(rows,p,q,tau):
  T=len(rows); n=len(rows[0]); best=Q(0)
  for t in set(map(Q,range(T+1))) | {tau}:
    A=cumul(rows,t)
    W=[Q(0)]*n; W[p]=min(t,tau); W[q]+=max(Q(0),t-tau)
    best=max(best,max(abs(a-w) for a,w in zip(A,W)))
  return best

def pair_opt(rows,p,q):
  T=len(rows); m=cumul(rows,Q(T)); n=len(m)
  # f(t)=t-Ap(t), g(t)=T-mq-t. f-g strictly increases.
  for j in range(T):
    Ap=cumul(rows,Q(j))[p]
    t=Q(j)+(Q(T)-m[q]-2*j+Ap)/(2-rows[j][p])
    if j<=t<=j+1:
      return direct_error(rows,p,q,t)
  raise AssertionError('missing unique balance point')

profiles=0; formula_cases=0; construction_cases=0
rng=random.Random(29117)
for n in range(2,9):
  profiles_n=[]
  # All 2-cell profiles with simplex-half rates (flat coordinates and pure cells).
  options=[]
  for i in range(n):
    for j in range(i,n):
      row=[Q(0)]*n;row[i]+=Q(1,2);row[j]+=Q(1,2);options.append(tuple(row))
  if n<=5: profiles_n.extend(product(options,repeat=2))
  # Sparse and dense random profiles, with nonintegral rates and tied totals.
  for _ in range(50):
    rows=[]
    for j in range(3):
      ints=[rng.randrange(4) for i in range(n)]
      if sum(ints)==0: ints[0]=1
      rows.append(tuple(Q(x,sum(ints)) for x in ints))
    profiles_n.append(rows)
  profiles_n.append([tuple(Q(1,n) for _ in range(n))]*3)
  if n>=3:
    profiles_n.append([tuple(Q(i==j) for i in range(n)) for j in range(3)])
  for rows in profiles_n:
    rows=list(rows); T=len(rows); m=cumul(rows,Q(T)); profiles+=1
    for p,q in permutations(range(n),2):
      for tau in (Q(0),Q(T,3),Q(T,2),Q(T)):
        A=cumul(rows,tau)
        formula=max(max([m[i] for i in range(n) if i not in (p,q)]+[Q(0)]),tau-A[p],T-m[q]-tau)
        assert formula==direct_error(rows,p,q,tau),(rows,p,q,tau)
        formula_cases+=1
    if n>=3:
      E=T*max(Q(1,3),Q((n-1)**2,n*(2*n-1)))
      q,r=sorted(range(n),key=lambda i:m[i],reverse=True)[:2]
      if m[q]>=E:
        p=next((i for i in range(n) if i!=q and m[i]>E),next(i for i in range(n) if i!=q))
        tau=max(Q(0),T-m[q]-E)
        assert direct_error(rows,p,q,tau)<=E
      else:
        tq=T-m[q]-E; tr=T-m[r]-E; Aq=cumul(rows,tq)
        p=max((i for i in range(n) if i!=q),key=lambda i:Aq[i])
        assert min(direct_error(rows,p,q,tq),direct_error(rows,q,r,tr))<=E
      # Independent optimization of each ordered mode pair, including endpoints
      # through the unique intersection and omitted-mass plateau.
      opt=min(pair_opt(rows,p,q) for p,q in permutations(range(n),2))
      assert opt<=E
      construction_cases+=1
counts['rational_profiles']=profiles
counts['three_term_formula_cases']=formula_cases
counts['one_switch_constructions_and_pairwise_optima']=construction_cases
print(counts)
print('All exact independent checks passed.')
