import collections
exec(open('/tmp/bs2/scan.py').read().split('res=[]')[0])
names=[l.split()[0] for l in open('/tmp/bs2/scan.out') if len(l.split())==6 and l.split()[3]!='0']
for name in names:
    I=read(D+name+'.osil'); ua=collections.defaultdict(set)
    for r,R in I['rows'].items():
        b,u=bil_terms(R)
        for k,v in u: ua[v].add(k)
    c=collections.Counter(tuple(sorted(s)) for s in ua.values() if len(s)>=2)
    print(name, dict(c.most_common(4)))
