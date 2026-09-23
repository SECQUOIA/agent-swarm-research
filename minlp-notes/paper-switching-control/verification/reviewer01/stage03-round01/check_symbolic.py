import sympy as S
n,k,c,x,h=S.symbols('n k c x h', positive=True)
f=((n-1)**2*c+1)/(n*(n-1)*(1+c))
assert S.factor(f-1/n)==(n-2)*(n*c-c-1)/(n*(c+1)*(n-1))
assert S.simplify((n*f-1)/(n*f+1)-(n-2)/n*((n-1)*c-1)/((n-1)*c+1))==0
C=(n*(n-1)+(n-k)*(n-k-1))/(n*k*(2*n-k-1))
assert S.simplify(C-1/(k+1)-2*(n-k-1)*(n-k*(k+1)/2)/(n*k*(k+1)*(2*n-k-1)))==0
assert S.simplify(1/k-C-(k+1)*(n-k)/(n*k*(2*n-k-1)))==0
for ell in range(1,5):
 d=k-ell
 eta=((1-d*x)*(1-(d+1)*x)/(1-x))*(2*((1-(d+1)*x)/(1-d*x))**ell-1)
 expected=1-2*k*x+k*(k-1)*x*x+(k*(k-1)-S.Rational(ell**3-ell,3))*x**3
 assert S.simplify(S.series(eta,x,0,4).removeO()-expected)==0
# All-light induction identity, with a generic step index k.
t=k*(n-k+1)/(n-k);prev=(k-1)*(n-k+2)/(n-k+1)
assert S.simplify((n-k)*t-(n-k+1)*prev-(n-2*k+2))==0
L4=1/(n*((n/(n-1))**4-1))
assert S.simplify(C.subs(k,4)-L4-(10*n*n-5*n+1)/(2*(2*n-5)*(2*n-1)*(2*n*n-2*n+1)))==0
U=(n**4-7*n**3+21*n*n-29*n+15)/(n*(2*n-3)*(2*n*n-6*n+5))
seed=1/((n-1)*(((n-1)/(n-2))**3-1))
assert S.simplify(f.subs(c,seed)-U)==0
p=n**4-17*n**3+77*n*n-130*n+75
assert S.expand(p.subs(n,12+h))==h**4+31*h**3+329*h*h+1286*h+963
num=6*n**4-20*n**3+21*n*n-7*n+1
den=(2*n-3)*(2*n-1)*(2*n*n-6*n+5)*(2*n*n-2*n+1)
assert S.simplify(U-L4-num/den)==0
assert S.expand(num.subs(n,5+h))==6*h**4+100*h**3+621*h*h+1703*h+1741
print('PASS symbolic mode-removal, plateau, dimension-free, all-light, seed-series, and predecessor identities')
