"""Four-group follow-up search; all ratios are floating-point evidence."""
import itertools
from cubic_symmetric_search import SymmetricCubic

if __name__=='__main__':
    f=SymmetricCubic(8,groups=4)
    best=(0,None)
    for x in itertools.combinations([.1,.2,.25,1/3,.5,2/3,.75,.8,.9],4):
        ratio=f.solve(x)
        if ratio>best[0]:
            best=(ratio,x)
            print('new',ratio,x,flush=True)
    print('BEST',best,flush=True)
    for m in [12,16]:
        f=SymmetricCubic(m,groups=4)
        print('larger',m,f.solve(best[1],True),flush=True)
