from itertools import product

def changes(w):return sum(a!=b for a,b in zip(w,w[1:]))
def peak(original,coarse,lengths,n):
 c=[0]*n;d=[0]*n;maximum=0;j=0
 for a,lenj in zip(coarse,lengths):
  for _ in range(lenj):
   c[original[j]]+=1;d[a]+=1;j+=1
   maximum=max(maximum,max(abs(u-v) for u,v in zip(c,d)))
 return maximum

for n,lengths,twice_bound,strict in [(3,(3,3,3),6,True),(2,(2,4,6),6,False)]:
 total=0;worst=0
 for original in product(range(n),repeat=sum(lengths)):
  start=0;support=[]
  for length in lengths:support.append(set(original[start:start+length]));start+=length
  best=10**9
  for coarse in product(*support):
   assert changes(coarse)<=changes(original)
   best=min(best,peak(original,coarse,lengths,n))
  assert (2*best<twice_bound if strict else 2*best<=twice_bound)
  worst=max(worst,best);total+=1
 print('PASS supported transfer exhaustive:',n,'modes, coarse widths',lengths,', original words',total,', maximal optimal peak',worst)
