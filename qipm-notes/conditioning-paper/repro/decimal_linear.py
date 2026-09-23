"""Small dense reference solves with the standard-library Decimal type."""
from decimal import Decimal as D, localcontext

def reference_errors(H,rhs,u):
    """80-digit reference for the exact real system defined by float64 H and rhs."""
    with localcontext() as ctx:
        ctx.prec=80
        A=[[D.from_float(float(v)) for v in row] for row in H]
        b=[D.from_float(float(v)) for v in rhs]
        M=[row.copy()+[v] for row,v in zip(A,b)];n=len(b)
        for j in range(n):
            pivot=max(range(j,n),key=lambda i:abs(M[i][j]));M[j],M[pivot]=M[pivot],M[j]
            assert M[j][j]
            for i in range(j+1,n):
                factor=M[i][j]/M[j][j]
                for k in range(j+1,n+1):M[i][k]-=factor*M[j][k]
                M[i][j]=D(0)
        exact=[D(0)]*n
        for i in reversed(range(n)):
            exact[i]=(M[i][-1]-sum(M[i][j]*exact[j] for j in range(i+1,n)))/M[i][i]
        def dot(a,b):return sum(x*y for x,y in zip(a,b))
        def apply(v):return [dot(row,v) for row in A]
        approximate=[D.from_float(float(v)) for v in u]
        residual=[v-w for v,w in zip(b,apply(approximate))]
        error=[v-w for v,w in zip(approximate,exact)]
        reference_residual=[v-w for v,w in zip(b,apply(exact))]
        assert max(abs(v) for v in reference_residual)<D('1e-60')*max(D(1),max(abs(v) for v in b))
        return float((dot(residual,residual)/dot(b,b)).sqrt()),float((dot(error,apply(error))/dot(exact,b)).sqrt())
