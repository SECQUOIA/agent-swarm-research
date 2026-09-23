# New parity development during Stage 2

The source's even-polynomial lower hierarchy discards global nonnegativity of
the limiting defect. Retaining it strengthens the concrete separation and
also gives an implicit optimal staircase for even transforms.

Define F_r(rho) as the best uniform approximation of y on [1,rho] by even
real polynomials P of degree at most 2r that are nonnegative on all of R.
The finite-dimensional closed-cone compactness argument proves attainment
and F_r>0. Squared approximations to v^(1/4) on [1,rho^2], substituted at
v=y^2, prove F_r tends to zero. The sequence is nonincreasing, with possible
plateaus. F_0=G_0.

For a bounded even transform q of degree d, the rescaled defect
(1-q(delta*y))/delta is even and nonnegative wherever |delta*y|<=1.
If d=o(delta^(-(2r+1)/(2r+2))), Taylor expansion through degree 2r+1
has vanishing remainder on every compact set; its limit is even, globally
nonnegative and degree <=2r. Thus K<F_r forces the same degree lower bound.

Conversely, a minimizing P for F_r can replace P_r^* in the existing
fixed-order pinned-gate proof. Its positive maximum-error contact set is
finite and nonempty: otherwise a small upward shift would improve the
approximation while preserving nonnegativity. The paired gate W and S_N(x^2)
are even, as is P(x/delta); the resulting transform remains even. All tail,
contractivity and contact-slack arguments use only the fixed degree and
global nonnegativity, not the explicit Chebyshev form. Therefore the optimal
even query exponent is -1+1/(2 ell), for ell the first index with F_ell<=K;
the coarse tier remains the same. Plateaus cause no problem because minimality
of ell gives K<F_(ell-1).

## First plateau and stronger concrete separation

F_1=E_1=(rho-1)^2/[8(rho+1)], attained by a*y^2+b with a,b>0.
Also F_2=F_1. Indeed write an admissible degree-four even polynomial as
A(v)=a2*v^2+a1*v+a0, v=y^2. Global nonnegativity on v>=0 implies a2>=0,
so A is convex. The chord l of sqrt(v) on [1,rho^2] differs from sqrt(v)
by 2 E_1 at v*=((rho+1)/2)^2. If A approximates sqrt with error E,
its endpoint bounds and convexity imply A(v*)<=l(v*)+E, while accuracy
implies A(v*)>=sqrt(v*)-E. Hence E>=E_1. The positive affine minimizer
attains equality. Thus every K<E_1 requires even degree Omega(delta^-5/6).

For rho=2 and K=1/32 a matching degree-six scaled defect is explicit:

    z=(2/5)*y^2-1,
    P(y)=sqrt(5/2)*(1+z/2-z^2/8+z^3/16).

For real y, z>=-1. The cubic B(z) has derivative
1/2-z/4+3 z^2/16>0 and B(-1)=5/16, proving global positivity.
For 1<=y<=2, |z|<=3/5. The absolute binomial coefficients beyond the cubic
are at most 5/128, so

    |P(y)-y| <= sqrt(5/2)*(5/128)*(3/5)^4/(1-3/5) < 1/32.

The fixed-order even upper construction therefore gives O(delta^-5/6),
matching the strengthened lower bound. The unrestricted threshold G_1<1/32
continues to give Theta(delta^-1/2). This changes the even row of the concrete
comparison from the source's Omega(delta^-3/4) to Theta(delta^-5/6).

The cubic argument and the exact E_1 equality case must be independently
verified by the Stage 2 author and all five reviewers before being claimed.
No classical preprocessing or gate-synthesis complexity follows from this
degree/query statement.

## Odd transforms: a matching logarithmic refinement

For every fixed rho>1, K>0, odd real bounded-polynomial transforms have
degree/query complexity Theta(delta^(-1)*log(1/delta)). The low band alone
proves the lower bound; the upper works on all [delta,1].

Lower bound: let q(t)=p(sin t), so q is a trig polynomial of degree d,
|q|<=1, and q(0)=0. Let A_n be its Taylor polynomial at zero. Put
t1=arcsin(delta), t2=arcsin(rho*delta). Bernstein and Taylor imply

    u := ||q-A_n||_[0,t2] <= (d*t2)^(n+1)/(n+1)!.

On [t1,t2], |q-1|<=(rho+K)*delta. Since 1-A_n has value one at zero,
exterior Chebyshev gives

    1 <= Rbar^n * [(rho+K)*delta + u],

where Rbar>R0 is any fixed number large enough for sufficiently small delta;
the exterior coordinate (t1+t2)/(t2-t1) tends to (rho+1)/(rho-1).
Choose n=floor(log(1/delta)/(2*log(Rbar))). The first term tends to zero,
so u >= (1/2)*Rbar^(-n). Taking (n+1)st roots and using Stirling gives
d*t2 >= c_rho*n, hence d=Omega_rho,K(delta^(-1)*log(1/delta)).

Upper bound: take tau=min(delta/2,K*delta/4) and eps=K*delta/4. A standard
bounded odd sign approximant s with gap tau and error eps has degree
O(tau^(-1)*log(1/eps)). Define p(x)=(s(x)-x)/(1+tau).
For 0<=x<=tau, p(x)>=(-1-tau)/(1+tau)=-1. For tau<=x<=1,
s(x)>=1-eps, so p(x)>=-eps/(1+tau)>-1 for small delta. Also p(x)<=1
for x>=0, and oddness supplies the entire [-1,1] bound. For x>=delta,

    |p(x)-(1-x)| <= (eps+tau)/(1+tau) <= K*delta.

Fixed K gives the claimed upper degree. This avoids needing a sign
approximant that is monotone or nonnegative throughout its transition gap.
The degree distinction from the unrestricted converter therefore includes
the previously absent logarithmic factor. Independent review remains required.
