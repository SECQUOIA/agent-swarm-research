import re,glob,collections
txt={f:open(f).read() for f in sorted(glob.glob('sections/*.tex'))}
bib=open('references.bib').read()
keys=set(re.findall(r'^@\w+\{([^,]+),',bib,re.M))
cites=collections.Counter(); loc=collections.defaultdict(list)
for f,t in txt.items():
    for m in re.finditer(r'\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]*)\}',t,re.S):
        line=t[:m.start()].count('\n')+1
        for k in m.group(1).split(','):
            k=k.strip()
            cites[k]+=1; loc[k].append(f"{f.split('/')[-1]}:{line}")
print('cited keys',len(cites),'bib keys',len(keys))
print('missing in bib',[k for k in cites if k not in keys])
print('uncited bib',sorted(keys-set(cites)))
import sys
if len(sys.argv)>1:
    for k in sys.argv[1:]: print(k,loc[k])
