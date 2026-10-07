import re,glob,sys
def keys(path):
    txt=open(path,encoding='utf8').read()
    return re.findall(r'@\w+\{([^,\s]+),',txt)
def cites(files):
    out={}
    for f in files:
        txt=open(f,encoding='utf8').read()
        # strip comments
        txt=re.sub(r'(?<!\\)%.*','',txt)
        for m in re.finditer(r'\\(?:cite|citet|citep|citealt|citealp|citeauthor|citeyear|nocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}',txt):
            for k in m.group(1).split(','):
                k=k.strip()
                if k: out.setdefault(k,set()).add(f.split('/')[-1])
    return out
new=keys('references.bib'); old=keys('process/w3/checks/bib-references-before-w3.bib')
import collections
print('new entries',len(new),'dups',[k for k,c in collections.Counter(new).items() if c>1])
print('old entries',len(old))
files=sorted(glob.glob('sections/*.tex'))
c=cites(files)
print('cited keys',len(c))
missing=[k for k in c if k not in new]
print('MISSING from bib:',{k:sorted(c[k]) for k in missing})
unc=[k for k in new if k not in c]
print('uncited in bib (%d):'%len(unc),unc)
deleted=[k for k in old if k not in new]
print('deleted (%d):'%len(deleted),deleted)
added=[k for k in new if k not in old]
print('added (%d):'%len(added),added)
# cites of deleted in old sections
c0=cites(sorted(glob.glob('process/w3/sections-before-w3/*.tex')))
print('deleted but cited in pre-w3 sections:',[k for k in deleted if k in c0])
print('missing in pre-w3 bib for pre-w3 cites:',[k for k in c0 if k not in old])
