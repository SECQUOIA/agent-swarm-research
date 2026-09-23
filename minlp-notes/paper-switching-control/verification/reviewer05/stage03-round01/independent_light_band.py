"""Check band boundaries on irregular pure profiles with prescribed equal masses."""
from fractions import Fraction as Q
from random import Random
rng=Random(50301)
cases=0;full_cases=0;partial_cases=0
for d in range(1,6):
    for shift in [-1,0,1]:
        n=d*d+d+shift;k=n-d
        if n<2 or k<1:continue
        T=Q(7,3); E=T/n
        for trial in range(3):
            # Each mode has mass T/n, split unequally then shuffled. Cells are
            # generally unequal and some consecutive cells select the same mode.
            pieces=[]
            for i in range(n):
                weights=[rng.randrange(1,8) for _ in range(3)]
                pieces.extend((i,E*Q(w,sum(weights))) for w in weights)
            rng.shuffle(pieces)
            segments=[];t=Q(0)
            for i,width in pieces:
                segments.append((t,t+width,i));t+=width
            assert t==T
            def allocation(t):
                val=[Q(0)]*n
                for lo,hi,i in segments:
                    val[i]+=max(Q(0),min(hi,t)-lo)
                return val
            assert allocation(T)==[E]*n
            used=set();blocks=[];left=Q(0)
            for j in range(1,k+1):
                right=min(T,Q(j*(n-j+1),n-j)*E)
                values=allocation(right)
                selected=max((i for i in range(n) if i not in used),key=lambda i:values[i])
                blocks.append((left,right,selected));used.add(selected);left=right
                if right==T:break
            checked_times={Q(0),left}
            checked_times.update(t for lo,hi,i in segments for t in [lo,hi] if t<=left)
            checked_times.update(t for lo,hi,i in blocks for t in [lo,hi])
            maximum=Q(0)
            for t in checked_times:
                a=allocation(t);w=[Q(0)]*n
                for lo,hi,i in blocks:w[i]+=max(Q(0),min(hi,t)-lo)
                maximum=max(maximum,*[abs(x-y) for x,y in zip(a,w)])
            assert maximum<=E
            assert len(blocks)<=k and len(used)==len(blocks)
            assert (left==T)==(d*d<=k)
            if left==T:
                assert maximum==E
                full_cases+=1
            else:partial_cases+=1
            cases+=1
print('PASS irregular equal-mass profiles:',cases,'; full-band cases:',full_cases,'; just-outside prefix cases:',partial_cases)
print('PASS boundaries d^2=k and d^2=k+/-1 for deficits d=1,...,5, with exact full-error evaluation')
