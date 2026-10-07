from fractions import Fraction as F
from parse import load
for N in [50,100,200,400]:
    d,vars_,cons,lin,q=load(f'chain{N}.osil')
    names=[v['name'] for v in vars_]
    etas=set(); ok=True
    for r in range(N):
        terms=dict((names[j],v) for j,v in lin[r])
        a=f'x{r+1}'; b=f'x{r+2}'
        ok &= terms.get(a)==-1 and terms.get(b)==1 and cons[r]['lb']=='0' and cons[r]['ub']=='0'
        others=[v for k,v in terms.items() if k not in (a,b)]
        etas |= set(-v for v in others); ok &= len(others)==2
    (eta,)=etas
    print(f'chain{N}: dynamics rows x_(i+1)-x_i-eta*(u_i+u_(i+1))=0: {ok}; eta={eta} =1/(2N): {eta==F(1,2*N)}; fl(eta)!=eta: {F(float(eta))!=eta}; x_0 fixed {vars_[0]["lb"]}/{vars_[0]["ub"]}, x_N fixed {vars_[N]["lb"]}/{vars_[N]["ub"]}')
