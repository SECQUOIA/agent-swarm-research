from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import ceil

# Exhaustive four-slot reordering tests. Inputs have half-integral simplex rates.
# Original words need only full error <=1, not the stronger floor/ceiling property.
cols=[tuple(sum(i==h for i in pair) for h in range(3)) for pair in combinations_with_replacement(range(3),2)]
words=list(product(range(3),repeat=4))
checked=0; equality_cases=0; nonintegral_deadlines=0
for rates in product(cols,repeat=4):
    pref=[[0,0,0]]
    for col in rates: pref.append([a+b for a,b in zip(pref[-1],col)])
    def admissible(word):
        cnt=[0]*3
        for j,p in enumerate(word,1):
            cnt[p]+=2
            if any(abs(a-b)>2 for a,b in zip(cnt,pref[j])): return False
        return True
    for word in words:
        if any(a==b for a,b in zip(word,word[1:])) or not admissible(word): continue
        r=next(j for j,p in enumerate(word,1) if p in word[:j-1])
        q=word[r-1]
        def deadline(i):
            if pref[r][i]<=2: return Q(r)
            for j in range(1,r+1):
                if pref[j][i]>2:
                    return Q(j-1)+Q(2-pref[j-1][i],rates[j-1][i])
            raise AssertionError
        dq=deadline(q)
        j=min(r-2,max(0,ceil(dq)-2))
        rest=sorted(set(word[:r])-{q},key=lambda i:(deadline(i),i))
        reordered=tuple(rest[:j]+[q,q]+rest[j:])+word[r:]
        assert len(reordered)==4 and admissible(reordered),(rates,word,reordered)
        assert sorted(reordered[:r])==sorted(word[:r])
        checked+=1
        equality_cases+=pref[r][q]==2
        nonintegral_deadlines+=dq.denominator!=1
print('PASS first-repeat reordering:',checked,'admissible words; terminal equality cases:',equality_cases,'nonintegral selected deadlines:',nonintegral_deadlines)

# Separate all-word exclusion by exact Fourier--Motzkin elimination, not vertex
# enumeration. This includes both switching times in any ordered affine cells.
rows=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[(Q(t,146),tuple(Q(a,146) for a in aa)) for t,*aa in rows]
L=Q(57,8); last,mass=knots[-1]
terminal=tuple(m+(L-last)/3 for m in mass)
assert terminal==tuple(Q(a,1752) for a in [5281,3985,3217])
knots.append((L,terminal))
segments=[]
for (lo,a),(hi,b) in zip(knots,knots[1:]):
    slopes=tuple((v-u)/(hi-lo) for u,v in zip(a,b))
    assert sum(slopes)==1 and min(slopes)>=0 and max(slopes)<=Q(3,4)
    intercept=tuple(u-s*lo for u,s in zip(a,slopes))
    segments.append((lo,hi,slopes,intercept))
def feasible(ineq):
    pos=[row for row in ineq if row[0]>0]; neg=[row for row in ineq if row[0]<0]
    projected=[(b,c) for a,b,c in ineq if not a]
    for ap,bp,cp in pos:
        for an,bn,cn in neg:
            projected.append((bp/ap-bn/an,cp/ap-cn/an))
    lows=[]; highs=[]
    for b,c in projected:
        if b>0: highs.append(c/b)
        elif b<0: lows.append(c/b)
        elif c<0: return False
    return not(lows and highs and max(lows)>min(highs))
count=0
for word in product(range(3),repeat=3):
    for j,(a,b,mu,cu) in enumerate(segments):
        for c,d,mv,cv in segments[j:]:
            ineq=[(-Q(1),Q(0),-a),(Q(1),Q(0),b),(Q(0),-Q(1),-c),(Q(0),Q(1),d),(Q(1),-Q(1),Q(0))]
            for i in range(3):
                p,q,r=[Q(mode==i) for mode in word]
                ineq += [(p-mu[i],Q(0),1+cu[i]),(p-q,q-mv[i],1+cv[i]),(p-q,q-r,1+terminal[i]-r*L)]
            assert not feasible(ineq),(word,j,c)
            count+=1
print('PASS n=k=3 all-word exclusion by rational Fourier--Motzkin:',count,'cells across all 27 words')
