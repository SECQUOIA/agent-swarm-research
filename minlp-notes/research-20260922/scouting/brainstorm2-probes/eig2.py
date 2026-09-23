import sys, collections
exec(open('/tmp/bs2/scan.py').read().split('res=[]')[0])
fl=[l.split() for l in open('/tmp/bs2/scan.out') if len(l.split())==6 and l.split()[2]!='0']
for name,fam,*_ in fl:
    I=read(D+name+'.osil')
    rowinfo={}
    lamrows=collections.defaultdict(list)
    for r,R in I['rows'].items():
        if r<0 or R['lb']!=R['ub']: continue
        b,u=bil_terms(R)
        allv=set(R['lin'])|({v for t in R['quad'] for v in t[:2]})|(V(R['nl']) if R['nl'] else set())
        cnt=collections.Counter(v for p in b for v in p)
        for i,j in b:
            for lam,x in ((i,j),(j,i)):
                if sum(1 for p in b if lam in p)==1: lamrows[lam].append((r,x,allv))
    best=0
    for lam,L in lamrows.items():
        X={x for r,x,a in L}
        good=sum(1 for r,x,a in L if len((a-{x,lam})&X)>=2)
        best=max(best,good if len(X)>=4 else 0)
    print(name,fam,best,flush=True)
