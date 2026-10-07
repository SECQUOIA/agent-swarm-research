import math
from fractions import Fraction as Fr
phi=lambda m: 0.75+8*math.log(1.25+4*math.sqrt(2*m))
psi=lambda m: 0.75+8*math.log(1.25+3*math.sqrt(m))
print("phi(1),phi(2)",phi(1),phi(2))
print("psi(1),psi(2)",psi(1),psi(2))
bad=[m for m in range(1,200000) if phi(m)>10*math.ceil(math.log2(m+2))]
print("phi violations",bad[:5])
bad=[m for m in range(1,200000) if psi(m)>8*math.ceil(math.log2(m+2))]
print("psi violations",bad[:5])
print("0.23^2/20 vs 1/379", 0.23**2/20, 1/379)
print("sqrt20+sqrt379", math.sqrt(20)+math.sqrt(379))
th2=Fr(1,16); print("prox bracket", 1+Fr(1,2)*(1+th2/2)+th2/2, Fr(99,64))
print("48*sqrt2", 48*math.sqrt(2))
# lem proximal (i): 3/4 + 8 ln(n+2) <= 7 ceil(log2(n+2))
bad=[n for n in range(1,100000) if 0.75+8*math.log(n+2) > 7*math.ceil(math.log2(n+2))]
print("prox (i) violations", bad[:5])
# lbproduct: (1+log2 k)^2 <= 4k
bad=[k/10 for k in range(10,100000) if (1+math.log2(k/10))**2>4*k/10]
print("log bound violations", bad[:5])
# falseguess constants
D=128; R=D*(2*D)*(2*D); print("R=2^",math.log2(R)); tau=Fr(1,4*2*R); print("tau=2^",math.log2(tau))
for kh in (1,2,4):
    j=0
    while 4**j*tau**2 < 4*kh*2*4: j+=1
    print("J",kh,j)
