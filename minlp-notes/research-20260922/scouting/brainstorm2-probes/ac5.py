import sys, collections, itertools
sys.path.insert(0,'/home/sgusev/repo/minlp-notes/research-20260922/scouting/minlplib-open-data')
from osil import read
def smono(name):
    I=read('/home/sgusev/.cache/minlplib/minlplib/osil/'+name+'.osil'); N=len(I['vt'])-1
    t=I['rows'][0]['nl']; mons=collections.Counter()
    for term in t[1:]:
        c=[1.0]; vs=[]
        def walk(u):
            if u[0]=='var': vs.append(u[1])
            elif u[0]=='num': c[0]*=u[1]
            elif u[0]=='times':
                for w in u[1:]: walk(w)
        walk(term); mons[tuple(sorted(vs))]+=c[0]
    S=collections.Counter()
    for m,c in mons.items():
        k=len(m)
        for r in range(k+1):
            for sub in itertools.combinations(m,r):
                S[sub]+=c/2**k
    return N,{m:c for m,c in S.items() if abs(c)>1e-9}
if __name__=='__main__':
    N,S=smono(sys.argv[1])
    byd=collections.defaultdict(list)
    for m,c in S.items(): byd[len(m)].append((m,c))
    for d in sorted(byd): print(d,len(byd[d]),collections.Counter(c for m,c in byd[d]).most_common(5),sorted(byd[d])[:4])
    # determine k-range
    q=[m for m,c in byd[4]]
    ks=collections.Counter()
    for a,b,c,d in q:
        if b-a==d-c: ks[b-a]+=1
        if c-a==d-b: ks[c-a]+=1
    print('max k seen',max(ks), sorted(ks.items())[:3], sorted(ks.items())[-3:])
    print('deg2',sorted(byd[2])[:10])
