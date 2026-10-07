Analytic prewriting audit: point output and cubic recourse

Reviewer scope: the October 3 global point and cubic recourse proofs, report
sections 02, 03, and 06, and their October 2 point, value, comparison, and
fallback dependencies. This is an internal proof audit. I read the assigned
sources and reconstructed the arguments below; I did not rerun experiments,
run historical checkers, inspect CI, or browse literature. Literature and
priority conclusions remain with the designated source reviewer. Here L is
total binary input length, n is continuous dimension, k is core dimension,
and q is requested precision; auxiliary symbols are defined locally.

The audited results are mathematically coherent under their stated
representations and promises. I found no substantive counterexample or
unresolved analytic step in the global sparse point construction, the
domain-convex cubic construction, the paired quartic reductions, or the
new cubic face/LLL/residual-completion argument. Several proofs in the
October 3 report deliberately delegate details to repository notes. Those
delegations are publication blockers if copied into the journal article;
the repairs are to include the arguments identified below. The expected
work theorem additionally requires the inherited selected-core count and
growth theorems and the separated-height exact fallback to be established
in the manuscript or attributed to a precisely verified external theorem.
The cubic certificate alone does not prove those inherited interfaces.

| Sound claim | Necessary qualifications |
| --- | --- |
| Explicit sparse globally convex polynomial on an arbitrary rational polyhedron: emptiness/unboundedness decisions, attainment otherwise, computable radius and error modulus, and approximation of one minimum-norm optimizer in poly(L,D,q) bit work | D=max(2,deg f) is the numerical degree. Convexity is a promise or its verification is charged. No arithmetic-circuit input theorem and no polynomial dependence on log D are asserted. |
| Explicit cubic convex only on a bounded rational polytope: effective error exponent 1/4 and deterministic poly(L+q) point output, including minimum-norm selection | Reduce to the actual affine hull before using Hessian positivity; measure norm in original coordinates. No optimizer-interiority or positive definite Hessian is assumed. |
| One constant-accuracy query for domain-convex quartics can decide Square Root Sum or PosSLP | These are conditional implications, not proved NP-hardness or complexity-class separations. The target has a unique optimizer; no global convexity or useful uniform final growth modulus is claimed. |
| Product-box residual-convex cubics under one finite core-noise draw admit full selected-point output with expected f(k)(1+L_c/sigma)^k poly(L+q) work | L_c is the numerical coordinate-curvature bound, distinct from encoding length L. The objective and selector are sampled once and fixed across q. Product box, degree three, sound acceptance, and same-draw exact fallback are required. |

Use a separate notation such as L_c for the curvature bound when converting
the source notes, which use I for input length and L for curvature. Writing
both as L in the journal theorem would obscure a genuine distinction:
large numerical Hessian bounds used by the new margin analysis affect bit
lengths, whereas the inherited core complexity retains its numerical factor
(1+L_c/sigma)^k.

The output contracts must remain separate. A value enclosure certifies
ell <= f_* <= f(x), with feasible rational x and a small width. A point
near S may approach different optimizers at different precisions. A fixed
selector oracle must approximate the same p for every q; the quantitative
regularization schedules establish this stronger property. An implicit
argmin or KKT description can be short without furnishing any promised
evaluation complexity. Arbitrarily accurate coordinate enclosures do not
by themselves decide equality, coordinate sign, active constraints, or an
exact value comparison. Expanded algebraic output has a further size
obligation. The main positive theorems provide certified rational Cauchy
output, not polynomial-size expanded algebraic coordinates.

The active-bound radical construction is a particularly clear separation:
an explicitly encoded domain-convex cubic has a supplied constant strong
convexity modulus and polynomial-time point approximation, while deciding
whether its distinguished optimal coordinate is exactly at zero decides
Square Root Sum. Source: `research-20261002/new-direction/convex-active-set-radical-comparison.md`,
Sections 1–4. The canonical-selector quartic provides a second separation:
some optimizer can be approximated easily, while the minimum-norm
optimizer's last coordinate is zero or one according to the arithmetic
comparison. Source: `canonical-selector-radical-comparison.md`, Sections
2–4. The paired quartic is needed to extend the implication to approximation
of any optimizer. Do not attribute that stronger implication to the single
amplifier construction alone.

Global point proof: reconstruction and required details

The source is `research-20261003-arithmetic/global-point/theorem.md`:
representation at line 23, quadratic construction at line 64, attainment
and radius at line 164, sparse error modulus at line 259, fixed selector at
line 346, and value/bit interface at line 401. The earlier bounded theorem
is `research-20261002/new-direction/globally-convex-polynomial-point-oracle.md`.
Its sample-gradient construction is replaced by sparse coefficient rows
in the October 3 theorem; retaining its dense sample enumeration would
lose the uniform numerical-degree bound.

Put D=max(2,deg f) and K_D=(D+1)D^(D+2). Global convexity makes
h(t)=f(a+t(x-a))-f(a)-t grad f(a)'(x-a) nonnegative, with
0<=h(t)<=h(1) on [0,1]. At nodes j/D, the Lagrange denominator is at
least D^(-D), and its numerator's second derivative at zero has magnitude
at most D(D-1). Summing D+1 terms proves h''(0)<=K_D h(1).
Thus

```
f(x) >= f(a)+grad f(a)'(x-a)+(x-a)'Hess f(a)(x-a)/K_D.
```

Averaging over [0,1]^n gives a rational lower quadratic
f(x)>=c+ell'x+x'Mx/K_D, where M is the integrated Hessian. The
definitions of ell and c in the source should be displayed in the article;
all integrals are termwise products 1/(alpha_i+1). Nonnegativity and
continuity show that ker M equals the common kernel of every Hessian:
d'Md=0 forces d'Hess f(a)d to vanish on the cube, then everywhere by
polynomial identity, and PSD turns that scalar identity into Hess f(a)d=0.
The converse is immediate.

Let Pi project orthogonally onto range M and set
w=-(Id-Pi)grad f(0). This projector is rational: from a rational basis E
of range M use E(E'E)^(-1)E'. Integration along ker M proves
f(x)=f(Pi x)-w'x and ell=Pi ell-w. This is where the constant affine
slope along Hessian-kernel directions must be retained. Treating every
Hessian-kernel direction as an invariance direction would be incorrect.

For a denominator-clearing integer Q_M and an entry bound C_M>=1 for
Q_M M, take rho=[K_D Q_M(nC_M)^(n-1)]^(-1). If the integer PSD
matrix has rank r>0, the product of its nonzero eigenvalues is its r-th
elementary symmetric polynomial, a positive integer. Its largest
eigenvalue is at most nC_M. Hence x'Mx/K_D>=rho||Pi x||^2. If M=0,
both sides are zero; the same positive formula is harmless.

For a rational a in P, solve w=B'lambda+Mz, lambda>=0. Infeasibility
gives a rational Farkas direction d with Bd<=0, Md=0, w'd>0. Along
a+td the objective decreases linearly. Feasibility gives v=Mz,
beta=c-lambda'b, A=||Pi ell-v||_1, and

```
f(x) >= beta-A||Pi x||+rho||Pi x||^2  (x in P).
```

This proves a finite lower bound before assuming attainment. With F=f(a),
T=1+(A+|F-beta|+1)/rho bounds ||Pi x|| on f(x)<=F. An upper bound
on w'x follows from w'x<=lambda'b+v'Pi x. A separate lower bound
comes from convexity at zero:
w'x=f(Pi x)-f(x)>=f(0)-||grad f(0)||_1T-F. The one-sided constraint
inequalities do not give an absolute bound on w'x. The article must retain
both estimates, for example the source's W_0 formula.

An explicit safe choice is
W_0=1+|lambda'b|+||v||_1T+|f(0)|+||grad f(0)||_1T+|F|.
If Q_J clears denominators of J and m_0=max_ij|M_ij|, then
Y=Q_J(n^2m_0T+W_0) bounds ||J_Zy||_1. Scale each inequality row
positively to an integer row and take C to bound those rows and J_Z.

The reusable integer Hoffman lemma is valid as stated. If integer
matrices B,T have n columns and entries bounded by C>=1, and
Z={x:Bx<=b, Tx=t} is nonempty, then for a in {Bx<=b},

```
dist(a,Z) <= (nC)^(n-1)||Ta-t||.
```

For a proof, let y be the projection of a onto Z. Express a-y using
independent equality normals and a nonnegative combination of active
inequality normals. Conic elimination modulo the equality span retains
at most n independent integer rows R. Its Gram determinant is a positive
integer and its largest singular value is at most nC, so
sigma_min(R)>=(nC)^(-(n-1)). The normal coefficients have norm at
most ||a-y||/sigma_min(R). Dotting with a-y gives a nonpositive term
for every active inequality row because a is feasible. The equality term
is at most the coefficient norm times ||Ta-t||. Divide by ||a-y||.
Zero distance is immediate. This proof covers redundant rows, unbounded
polyhedra, lower-dimensional slices, and irrational right-hand sides.
It does not require rationality of y or t.

Stack M,w' into J, clear its denominators, and apply this lemma to
Z_y={x in P:J_Zx=J_Zy}. The bounds on Pi y and w'y bound J_Zy
on the sublevel. The projection of a onto Z_y has an explicit
polynomial-logarithmic norm, and equality of J-values preserves f.
Every sublevel point therefore has an equally good feasible bounded
representative. A minimizing sequence can be replaced by these
representatives, and compactness proves attainment. The source's explicit
radius R=1+||a||_1+H(||J_Za||_1+Y), with H=(nC)^(n-1), gives the
minimum-norm optimizer p a norm bound as well. This argument is not
circular: no optimizer is used to construct R.

For the error modulus, construct a row for each exponent gamma appearing
in a partial derivative:
N_(gamma,i)=(gamma_i+1)f_(gamma+e_i). There are at most n times the
input monomial count. The polynomial grad f(z)'d has coefficient vector
Nd, so ker N is the global translation-invariance space. Fix p, put
d=x-p and E=f(x)-f_* in [0,1], and use the globally nonnegative
Bregman polynomial h(u)=f(p+u)-f(p)-grad f(p)'u. Along the feasible
segment, 0<=h(td)<=E for t in [0,1]. Lagrange interpolation gives
|h(2td)|<=C_D E(1+2|t|)^D, C_D=(D+1)D^D.

For c in [0,1]^n, the midpoint bound is

```
0 <= h(c-p+td) <= h(2(c-p))/2+h(2td)/2.
```

Only p needs a radius bound. Coefficient sums on [-R-2,R+2]^n bound
the first term. On t in [0,E^(-1/D)], the second has an E-independent
bound because E(1+2E^(-1/D))^D<=3^D. Derivative interpolation at
zero gives |grad f(c)'d|<=C_*E^(1/D), with explicit rational C_*
of polynomial logarithmic size. At E=0 the polynomial along d vanishes
identically, and the midpoint inequality bounds the second polynomial
on the whole real line, forcing it to be constant. This supplies the
zero-gap argument without a limiting sequence.

For completely explicit coefficient bounds, put U=R, K=U+2,
V_f=sum_alpha|f_alpha|K^|alpha|,
G_f=sum_(|alpha|>0)|f_alpha||alpha|K^(|alpha|-1), and
H_f=max(1,2V_f+2G_f(U+1)). With J_D=(D+1)D^(D+1), take
C_*=1+J_D(H_f+3^D C_D). The points p and 2c-p used in the
midpoint argument lie in the coefficient-majorized box; x need not.

With r=D-1, a conceptual tensor interpolation grid on [0,1]^n bounds
every coefficient by B_r^n times the cube supremum, where
B_r=(r+1)2^r r^r. This is an analytic bound, never an enumerated grid.
Therefore |(Nd)_gamma|<=B_r^n C_*E^(1/D), and zero-gap invariance
gives S={x in P:Nx=Np}. Clear denominators with Q_N and apply the
same Hoffman lemma. For an integer entry bound C_N and row count s_N,

```
Gamma=max(1,(nC_N)^(n-1) Q_N max(1,s_N) B_r^n C_*).
```

This proves the global error bound on the original unbounded P, not merely
inside the radius box. Empty N in the constant case means S=P.
log(B_r^n)=O(nD log(D+1)); the matrix N stays polynomially small.
Sparse differentiation, integration, powers in coefficient bounds, LP,
and rational linear algebra have poly(L,D) bit cost. Binary exponents
must not be advertised as giving a poly(L,log D) theorem.

For epsilon=2^(-q), use the source's unbounded-set schedule

```
tau=epsilon^(2D-2)/(4*8^(D-1)*R^D*Gamma^D),
eta=tau epsilon^2/4.
```

The unique minimizer x_tau of f+tau||x||^2 over P has norm at most
||p|| and lies in Q=P intersect [-R,R]^n. Let s be nearest to x_tau
in S and e=||s-x_tau||. Comparison with p gives e<=2R and initial
gap<=tau R^2<=1. Comparison with s gives
e^D/Gamma^D<=gap<=tau e(2||x_tau||+e)<=4R tau e. Thus
e<=epsilon^2/(8R). Projection onto S gives p'(s-p)>=0, and hence
||x_tau-p||^2<=2R e<=epsilon^2/4. A feasible regularized objective
gap eta supplies the other epsilon/2 by strong convexity. The factor
4R is needed because nearest s need not lie in the radius box; copying
the bounded-domain 2R proof here without this change would be invalid.

The convex value interface must be part of the proof. Source:
`research-20261002/new-direction/convex-polytope-value-interface.md`,
Section 1. Universally tight rows determine the actual affine hull; an
average of positive-slack witnesses provides a rational relative inner
ball. Build a capped epigraph with rational inner and outer radii and
rational separators. Weak output is not automatically exactly feasible:
repair it by a rational LP in an error box, or the proved homothety toward
an interior center. Pair its feasible value with the weak-optimization
lower bound; optionally solve its tangent LP with a rational dual to
obtain an independently checkable lower certificate. For variable degree,
do not expand f(x_0+Vu). Evaluate the affine map and sparse polynomial,
and use the chain rule; majorize f and its derivatives on the original
box. Exact query arithmetic then remains poly(L,D,query bits).

The report currently sends constants and representation accounting to a
companion proof at `02-global-points.tex:38`. Its radius discussion also
suppresses the exact T,W_0,Y,R formulas. These are repairable presentation
gaps, not false claims; include them in the journal appendix together with
the relative-polytope value/repair proof. The same theorem cannot be stated
for an unevaluated arithmetic-circuit polynomial by replacing the input
model without a new argument.

Domain-convex cubic proof: reconstruction and limits

Source: `research-20261002/new-direction/convex-cubic-polytope-point-oracle.md`,
preprocessing at line 46, Hessian domination at line 119, affine slice
and constants at line 197, feasible value output at line 274, and
original-norm selection at line 357. The October 3 report's corresponding
statement is `03-domain-boundary.tex:14`; its companion-proof delegation
is at line 38.

Rows universally tight on P, identified by *maximum slack equal to zero*,
define aff(P). Rows merely active somewhere do not. Rational elimination
gives x=x_0+Vu with full-dimensional bounded P' in dimension m; choosing
free original coordinates makes V contain an identity submatrix. Convexity
on a lower-dimensional P says nothing about PSD of the ambient Hessian,
so reduction must precede the Hessian proof. Fixed degree three makes
explicit affine substitution polynomial in size.

A rational LP gives an interior ball B(c,rho) in P', rho>0, and
coordinate LPs give R>=1 with ||u-c||<=R on P'. The Hessian H(u) is
affine and PSD there. Reflection to c-(rho/R)(u-c) gives
0<=H(u)<=beta H_c, beta=1+R/rho, with H_c=H(c). Therefore ker H_c
is the common kernel on P', even though an individual boundary Hessian
can have a larger kernel. This gives a rational M>=1 bounding ||H(u)||.

For an optimizer v and u in P', put d=u-v, a=d'H(v)d, b=d'H(u)d,
E=phi(u)-phi(v). Cubic Taylor and constrained first-order optimality give
E>= (a+b)/6. Full third-derivative symmetry gives
d'H_cd=a+(c-v)'(H(u)-H(v))d. PSD gives
||H(u)d||<=sqrt(Mb) and ||H(v)d||<=sqrt(Ma). These imply a
conservative bound

```
E >= (d'H_cd)^2/(384MR^2)
  >= lambda^2||Pi d||^4/(384MR^2),
```

where Pi projects onto (ker H_c)^perp and lambda is H_c's smallest
positive eigenvalue. The constant is safely loose; the derivation uses
bounded diameter and the known center, not optimizer-interiority.

Let g_c=grad phi(c). Since phi-g_c'u has gradient in (ker H_c)^perp,
the optimizer set is
S'={w in P':H_c(w-v)=0, g_c'(w-v)=0}. The gradient row retains a
possible nonzero affine slope in ker H_c. Moreover
|g_c'd|<=E+MR||Pi d||. Clear denominators of H_c,g_c and polytope
rows with Delta. A positive maximal-rank principal minor gives the
computable lower bound lambda_0=Delta^(-m)M^(-(m-1)). With

```
R_0=384MR^2/lambda_0^2,
Gamma_u=(mC)^(m-1)Delta[1+M(1+R)R_0],
Gamma_P=max(1,||V|| bound)*Gamma_u,
```

the preceding estimates and integer Hoffman lemma give
dist(x,S)<=Gamma_P E^(1/4) for E<=1. If H_c=0, phi is affine;
the gradient row alone and the Hoffman lemma give a bound proportional
to E, hence to E^(1/4). If that gradient is also zero then S=P.
These branches must be stated explicitly, not hidden in a smallest
positive eigenvalue that does not exist.

The original-coordinate selector is obtained by minimizing
phi(u)+tau||x_0+Vu||^2, not phi(u)+tau||u||^2. With an original
radius R_x and tau=epsilon^6/(1024R_x^4Gamma_P^4), the same bounded
regularization proof gives bias epsilon/2. A regularized value gap
tau epsilon^2/4 gives epsilon/2 solve error directly in original
coordinates, including lower-dimensional P. No lower singular-value
bound for V is needed. The value-only solve at gap
(epsilon/Gamma_P)^4 supplies distance to S without a fixed selector.

This proof establishes exponent 1/4, not its optimality. The univariate
domain-convex cubic t^3 on [0,1] excludes a universal exponent greater
than 1/3. No effective all-dimensional exponent 1/3 is established here.
Globally convex degree-three polynomials have no cubic part and are
quadratic, so the domain-cubic theorem has distinct scope from the
global result. Do not merge their convexity hypotheses.

The quartic implications: proof obligations and safe interpretation

The complete sources are `convex-point-radical-comparison.md`, Sections
1–5, and `posslp-convex-point-extraction.md`, Sections 1–6, both under
`research-20261002/new-direction/`. The October 3 report begins the
constant-accuracy theorem at `03-domain-boundary.tex:208`. Its proof
includes the common amplifier but delegates the actual base reductions
at lines 230–234 and 284. Include both base constructions in the journal
appendix; the amplifier by itself is not a reduction from either source
decision problem.

For Square Root Sum, choose powers of two R_i with
R_i^2<=a_i<4R_i^2, c_i=a_i/R_i^2, M=max R_i, w_i=R_i/M,
and a power-of-two leaf count K. Cubic leaf terms u_i^3/3-c_i u_i on
[1,2] select sqrt(c_i). Squared averaging-tree residuals propagate the
root s^0=sum sqrt(a_i)/(KM). Their averaging matrix P has disjoint row
supports and norm at most 1/sqrt(2); leaf curvature and residual squares
give Hess F_0>=2(Id-P)'(Id-P)>=Id/8. Appending t^2 and a root tilt
of magnitude 1/32 leaves Hess>=Id/16. Opposite tilts in two copies
make exactly one optimal amplitude positive according to the strict
source comparison.

Equality requires no factorization. In the common field containing all
radicals, each nonsquare sqrt(a_i) has trace zero by trace transitivity,
whereas an integer has trace equal to that integer times the extension
degree. If a positive radical sum were an integer, the integer would
equal the sum of its perfect-square terms. Removing these terms would
leave a positive sum of nonsquare radicals equal to zero. Thus equality
is possible only when every radicand is a perfect square, which ordinary
integer square-root tests handle directly. The field is used in the
proof, never computed in the reduction.

For PosSLP, encode each integer gate value by a bounded rational pair
(u,v), v>0, u/v=A. Addition/subtraction use
(u_1v_2 +/- u_2v_1,v_1v_2)/4, multiplication uses
(u_1u_2,v_1v_2)/4, and inputs use (0,1/4),(1/4,1/4).
All pair variables lie in [-1/4,1/4]. The final affine signal
t=(2u-v)/4 has sign 2A-1 and never vanishes. Gate equations
x_i=p_i(x_<i) are triangular, have degree at most two, and satisfy
|p_i|<=1/4, ||grad p_i||_1<=1, ||Hess p_i||<=1 on the fixed box.
For G=sum_i64^(N-i)(x_i-p_i)^2, diagonal weight scaling gives a
scaled triangular derivative matrix with row norm <=1/8 and column
norm <=1/7. Its positive Jacobian Hessian part is >=(9/8)D^2,
and its negative residual part is >=-D^2/63. Hence Hess G>=Id.
This covers arbitrary fanout and repeated inputs. The exact gate values
are never expanded during construction. Opposite signal tilts with
independent amplitudes preserve constant base strong convexity.

For either construction, add eta[t_+^2(y-1)^2+t_-^2y^2] with
eta=1/192. The Hessian identity

```
D^2[t^2(y-c)^2][(p,q)]^2
 =2(tq+2(y-c)p)^2-6(y-c)^2p^2
```

proves convexity on the box after the losses are absorbed by base
curvature. The whole objective is at least the sum of base minima.
Choosing both base optimizers and y equal to the appropriate endpoint
attains this bound; every optimizer must do the same. Thus the complete
optimizer is unique and y is zero or one. Distance 1/4 suffices to
threshold y at 1/2, regardless of how small the positive amplitude is.
The final y curvature is 2eta[(t_+^*)^2+(t_-^*)^2], potentially tiny.
Base strong convexity therefore must not be advertised as a final
uniform polynomial-bit point-growth modulus.

The radical tree bags have size at most three, and the two endpoint
edges join the trees without larger bags: interaction treewidth is at
most two. Unit-box transformation preserves these scopes. Remove the
aggregate constant before claiming bounded collected coefficients.
No bounded-treewidth claim is made for PosSLP. Scaling its entire
objective yields bounded coefficients and preserves optimizers, while
also scaling its curvature. The reduction construction must not itself
evaluate A or decide the radical sign.

A deterministic polynomial-time target point oracle would put the
associated source predicate in P. An always-correct randomized oracle
with expected polynomial work gives a Las Vegas expected polynomial-time
decision algorithm, not a deterministic conclusion. Adding an independent
one-dimensional perturbed quadratic core leaves the same residual endpoint
on every draw. Therefore core-only noise cannot, by itself, turn a general
quartic residual value guarantee into a polynomial-time full-point
guarantee. This does not contradict the cubic theorem, and it does not
rule out compact unevaluated exact descriptions.

Cubic recourse: complete certificate reconstruction

Main source: `research-20261003-arithmetic/cubic-recourse/theorem.md`:
interfaces at line 16, nearby tilts at line 75, fiber bound at line 147,
success probability at line 234, fixed law/fallback at line 295, and
completion at line 350. Supporting sources are `lattice-certificate.md`
and `margin-tail.md` in the same directory, and
`research-20261002/new-direction/residual-convex-cubic-boundary.md`.

Let F(v,z) have total degree at most three on [0,1]^k times [0,1]^n,
with convex z-fibers. Supply or compute a rational coordinate bound
F_(v_i v_i)<=L_c and noise width sigma>0. Sample one endpoint-inclusive
product grid for gamma and use F_gamma=F+gamma'v. Select the
lexicographically least globally optimal core a and the minimum-norm
residual optimizer p in S_a. This selector must remain the same in the
ordinary and fallback branches and across all q.

For Lbar=max(1,L_c), choose a base t<=1/2 and query cores for
gamma +/- t e_i at coordinate error r<=t/(8Lbar). Sound rules are
u_i^-<t/Lbar => a_i=0 and ell_i^+>1-t/Lbar => a_i=1.
To prove the first, project all other variables out to W(s). It is
continuous, and W(s)-Lbar s^2/2 is concave because it is the infimum
of such concave functions. If a_i is an optimizer for gamma_i and b_i
for gamma_i-t, then a_i<=b_i. If 0<a_i<=b_i<t/Lbar<=1/2, both are
interior contact points, hence differentiable, and
t=W'(b_i)-W'(a_i)<=Lbar(b_i-a_i)<t, a contradiction. The upper
rule is symmetric. The conclusion holds for every original optimal
core, not just its lexicographic selection.

Let theta=sup_(s>0)(W(0)-W(s))/s. It is finite by coefficient-derived
Lipschitz bounds. A lower endpoint is optimal only if gamma_i>=theta.
If gamma_i>theta+t, every negatively shifted optimizer has coordinate
zero, so its certified upper interval endpoint is <=2r<t/Lbar and
the test succeeds. Thus a missed original lower endpoint needs
gamma_i in [theta,theta+t], and likewise for an upper endpoint. A
uniform endpoint-inclusive grid gives an interval of length t mass at
most t/(2sigma)+2/M. Hence missed endpoints have probability
<=kt/sigma+4k/M. This estimate is conditional on other noise labels,
so no independence of the optimizer's chosen face is assumed.

Let A be the face fixed by the sound rules, c_A its relative center,
c_z=(1/2,...,1/2), H_A=Hess_zz F(c_A,c_z), and
g_A(v)=grad_z F(v,c_z). The residual Hessian is affine and PSD.
Reflection on the face product gives 0<=H(v,z)<=2H_A. If a's free
coordinates are at least delta from the endpoints, then
H(a,c_z)>=2delta H_A and ker H(a,c_z)=ker H_A. The equality is at
the residual center and an interior core, not at every residual boundary
point. The cubic optimizer-slice theorem gives

```
S_a={z in [0,1]^n:H_A(z-y)=0, g_A(a)'(z-y)=0}
```

for any y in S_a. All square minors of [H_A;g_A(v)';Id_n] have
degree at most two in the free core because only one row varies.
Uniformly over original faces, clear entry coefficients by an integer d
obtained from input denominators and a factor eight, and bound their
cleared coefficient sums by C. With s_*=(k+1)(k+2)/2, use
Delta=d^n and B=Delta n!(s_*C)^n. Every minor multiplied by Delta
is an integer quadratic of height <=B. These are polynomial-bit
computations; neither all minors nor all faces are enumerated.

For m free coordinates, let phi(a) contain the s=(m+1)(m+2)/2
monomials of total degree <=2, including 1. A certified short Cauchy
oracle supplies b with ||b-a||_infinity<=1/(4T). Rounded integers
w_j=nearest(T phi_j(b)) satisfy |w_j/T-phi_j(a)|<=1/T because
each nonconstant monomial is 2-Lipschitz on the cube. The rank-s
integer lattice with row basis [Id_s | w] has vectors (h,h'w).
LLL at parameter 3/4 gives ||ell_1||<=2^((s-1)/2)lambda_1. Accept
only if

```
||ell_1||^2 > 2^(s-1)(4sB)^2.
```

The inequality direction is essential: this implies
lambda_1>4sB. If 0<||h||_infinity<=B had |h'phi(a)|<=sB/T,
then |h'w|<=2sB and ||h||<=sB, producing a lattice vector shorter
than sqrt(5)sB<4sB. Thus acceptance certifies
|h'phi(a)|>xi=sB/T for *every* nonzero bounded-height quadratic.
This includes coordinate polynomials v_i and 1-v_i, proving that the
provisionally free coordinates are actually interior. If an endpoint
test missed a boundary coordinate, acceptance is impossible. Every
identically nonzero minor polynomial has magnitude >xi/Delta; a minor
identically zero on the face is harmless. The LLL checker verifies a
unimodular basis change, reducedness, and the integer acceptance test.
Its coordinate enclosure still depends on the established core oracle;
an uncertified numerical approximation cannot replace that premise.

Use delta=min(1/2,xi), mu=min(1,xi/Delta). Every independent stack
of residual equality rows and active box normals has a square minor
of magnitude >=mu. With an entry bound C_z>=1, its least singular
value is >=mu/(nC_z)^(n-1) by Cauchy–Binet, so the projection proof
gives a Hoffman multiplier H_*=(nC_z)^(n-1)/mu. Bound H_A's positive
eigenvalues by a rational lambda_0 as in the deterministic cubic proof,
then use lambda_*=2delta lambda_0 in its transverse estimate. The
source's conservative formulas

```
M_z=max(1,max_i sum_j |(H_A)_ij|), M_*=2M_z,
R_0=max(1,96M_*n/lambda_*^2),
Gamma=max(1,H_*[1+(M_z+2M_*n)R_0])
```

give dist(z,S_a)<=Gamma gap^(1/4) for gap<=1. When H_A=0,
the fiber is affine and Gamma=max(1,H_*) suffices. For a vertex core
face, delta=1/2 and mu=min(1,1/Delta) are available directly, so no
lattice step is needed. All constants have length polynomial in
L+log T; no exact algebraic coordinates of a are computed.

Lattice soundness alone does not establish likely acceptance. Enlarge
the coefficient height to R_s=2^s4sB. If every nonzero quadratic of
height <=R_s has |p(a)|>=eta, then T eta>(s+1)R_s guarantees
acceptance: vectors with ||h||>R_s are already long, and the others
have |h'w|>=T eta-sR_s>R_s. Testing only height B in the probability
analysis would be an actual gap. The source correctly enlarges the family
to a common R=2^(s_*)4s_*B across all possible free dimensions.

For the probability estimate, bound Hess_vv F<=U Id with rational U>=1
of polynomial bit length. On each open face, V(v)=min_z F(v,z) is
U-semiconcave. At any interior point with an affine lower support,
the support slope is unique and
0<=V(x)-V(a)-g_a'(x-a)<=(U/2)||x-a||^2. For two nearby contact
points a,b, put r=||a-b|| and d=g_b-g_a. Lower support at b and
upper support at a give d'h<=(U/2)(r^2+||h||^2). Choosing
h=r d/||d|| inside the face gives ||d||<=Ur. A countable cover by
small interior balls makes this a Lipschitz bound on each piece, and
the image-volume inequality gives vol(g(E))<=U^m vol(E). It bounds
the probability of *some* interior optimal core in E, without residual
selection continuity or uniqueness.

A nonzero integer quadratic p satisfies
vol{|p|<=eta}<=min(1,8sqrt(eta)). If a square coefficient is nonzero,
coordinate slicing uses the univariate bound 4sqrt(eta/|a|). If only a
mixed coefficient x_i x_j is nonzero, slicing along
(e_i+e_j)/sqrt(2) has quadratic coefficient magnitude at least 1/2
and projected cube volume sqrt(2), giving the stated factor eight.
Linear and nonzero constant cases are simpler. Thus a union bound over
all faces and bounded-height quadratics has continuous probability
<=A sqrt(eta), where

```
A=8*3^k*max(1,U/(2sigma))^k*(2R+1)^(s_*).
```

Its logarithm is polynomial in L even though the family is never listed.

The finite-law transfer must include point atoms. A fixed face/polynomial
event has one existential full-point witness block and one universal
competitor block, total degree <=3. A verified two-block elimination
bound gives a base-computable bound C_sec=2^poly(L) on interval/point
components in each scalar-noise section, uniformly in all other fixed
real coefficients. Endpoint-inclusive grid CDF discrepancy is <=1/M;
an interval or point has discrepancy <=2/M. Replace marginals one at a
time and sum over the finite family to obtain
Pr_grid(bad margin)<=A sqrt(eta)+C_tail/M. This concerns a sufficient
geometric condition for success, not the algorithmically defined LLL
event. Letting eta decrease to zero includes exact algebraic-relation
atoms. Do not replace this transfer by an almost-sure continuous-noise
claim.

Choose a base-only exact fallback factor B_0>=2 first, then

```
t=min(1/2,sigma/(16kB_0)),
eta=min(1/4,(16AB_0)^(-2)),
T=least power of two strictly exceeding (s_*+1)R/eta.
```

Instantiate the selected-core evaluator for the original baseline and
the 2k baselines F +/- t v_i, all using the same gamma. Their coordinate
second derivatives are unchanged and their input lengths are polynomial
in L. Choose one sufficiently fine M satisfying all their mesh lower
bounds and (4k+C_tail)/M<=1/(8B_0). The face and margin estimates
bound rejection probability by 1/(4B_0). All quantities are fixed before
q, and log M is polynomial in L. Larger valid M only decreases the
finite-grid errors; this monotonicity of the inherited mesh requirements
must be recorded when composing the instances.

The same-selector fallback has a direct two-block description. For full
points x=(v,z), define a nested linear-size LexGT(v',v) predicate by
v'_1>v_1 or [v'_1=v_1 and (v'_2>v_2 or [...])]. A canonical witness
x is in the box and satisfies, for every competitor x' in the box,

```
F_gamma(x')>F_gamma(x), or
[F_gamma(x')=F_gamma(x) and
 (LexGT(v',v) or (v'=v and ||z'||^2>=||z||^2))].
```

This simultaneously enforces global optimality, lexicographically least
core, and minimum-norm residual in that core. Compactness and residual
convexity make it a singleton. For a coordinate, existentially quantify
x, impose its coordinate t, and universally quantify x'. There are only
two quantified blocks; degree is <=3 and atom count is linear in n+k.
The explicit nested formula repairs any ambiguity in the source's
“linear-size Boolean syntax” assertion at `cubic-recourse/theorem.md:343`;
the fully expanded prefix conjunction version would have quadratic size,
which also would not invalidate the complexity bound.

Apply the inherited separated-height elimination/root-isolation theorem:
the factor B_0=2^poly(L) depends only on base degree, dimensions, atoms,
and base data, while sampled coefficient length b and precision q enter
as B_0 poly(L+b+q). Separate singleton coordinate formulas identify the
same point, so coordinate root encodings cannot drift between minimizers.
Clipping continuous approximations to the product box preserves accuracy
and feasibility. This fallback is run on the original draw, not a new
sample, and every rejected relation or unresolved endpoint is handled
correctly. Rebuilding B_0 from L+b after selecting M would make the rare
event budget circular and must be avoided.

On an accepted draw, obtain full residual completion by regularization.
For epsilon=2^(-q), e=epsilon/2, rational R_z>=max(1,sqrt(n)) and
G>=max(1,sup||grad_v F||), put

```
tau=e^6/(1024R_z^4Gamma^4),
eta_q=tau e^2/8,
d_q=min(epsilon/2,tau e^2/(32G)).
```

Request a short rational b in A with ||b-a||<=d_q, set certified fixed
coordinates exactly, and clip the others. Solve the rational convex
Q_b(z)=F(b,z)+tau||z||^2 to feasible gap eta_q. At the exact core,
let z_tau minimize F(a,z)+tau||z||^2. If s is nearest to z_tau in
S_a and d=||s-z_tau||, bounded regularization gives
d^4/Gamma^4<=gap<=2R_z tau d and
||z_tau-p||^2<=2R_z d. The schedule yields d<=e^2/(8R_z) and
bias <=e/2. Uniform objective perturbation is <=Gd_q, so the returned
point's true regularized gap is <=eta_q+2Gd_q<=tau e^2/4. Strong
convexity gives solve error <=e/2. Residual error <=e and core error
<=epsilon/2 give combined Euclidean error <=epsilon. A finer point
query and a certified value lower bound add an objective enclosure.

One random factor controls all q: sum the common work factors of the
original and 2k auxiliary core evaluators, then add B_0 times the
indicator of the single base rejection event. The latter has expected
contribution <=1/4. No independence among factors and rejection events
is required. U, B, T, Gamma enter through their bit lengths; the numerical
parameter of the inherited work theorem remains L_c/sigma. Degree four
or coupled domains require new arguments. Approximate-core substitution
without regularization is inadequate even for cubic affine fibers:
F(v,z)=v^2(2-z) has minimum-norm residual zero at v=0 and residual
optimizer one at every v>0. No continuity of this selector is used above.

Publication blockers and bounded audit conclusion

The following are precise inclusion requirements, rather than unresolved
mathematical claims:

1. `02-global-points.tex:38–39` delegates the complete constants and
   sparse representation accounting. Include the explicit radius,
   interpolation constants, coefficient rows, and convex-value/repair
   interface; the preceding reconstruction supplies the required pieces.
2. `03-domain-boundary.tex:38` delegates domain-cubic constants and weak
   output. Include the actual affine-hull computation, rational inball,
   affine/rank-zero branch, original-norm penalty, and exact feasible
   repair. The October 2 polytope proof supplies these details.
3. `03-domain-boundary.tex:230–234,284` delegates the two quartic base
   reductions. Include normalization, tree conditioning, trace-based
   equality preprocessing, weighted gate convexity, and their precise
   coefficient/treewidth qualifications.
4. `06-recourse.tex:65–75` assumes the selected-core and exact-fallback
   interfaces, `06-recourse.tex:217` delegates the conditional fiber
   error bound, and `06-recourse.tex:301` delegates finite-section
   constants. The journal appendix must contain those proofs or cite a
   vetted external theorem with the exact bit/output contract. In
   particular, a core-value oracle alone does not supply a fixed selected
   core; use the retained hull, its containment of every optimal core
   and the incumbent, the base terminal depth, the growth-tail failure
   event, and same-selector fallback. Full selected-core counting and
   growth sources are `core-only-noise-core-oracle.md`, Sections 2–4,
   and its all-scale dependencies, outside the new cubic certificate.
5. The fallback and finite-grid section counts require the precise
   two-block elimination theorem that separates coefficient height from
   dimension. `polynomial-exact-fallback.md:158–198` gives the required
   contract; its primary-source accuracy belongs to the literature
   reviewer. A generic doubly exponential CAD citation would not justify
   the announced base-only singly exponential budget.

No theorem in this audit should be justified by a “proof complete” label,
prior internal review, or a finite diagnostic count. Existing diagnostics
can be recorded as historical evidence without rerunning them, but they
do not establish the universal asymptotic claims. Novelty cannot be
inferred from this analytic audit. The global radius/value/attainment
structure is explicitly attributed in the notes to prior work, and the
additional quantitative point-output claims require the designated
source reconciliation.

Luna's source-transfer cautions for the historical Hesse version do not
invalidate this independently reconstructed proof. Normalize a feasible
descent ray by its positive scalar w'd, or divide an affine-direction
vector by its squared norm when the required inner product is one;
division by its norm alone does not give that normalization. Keep the
separate lower estimate for w'x rather than converting a one-sided bound
into an absolute bound. Use rational lower bounds on positive eigenvalues,
not a claim that the eigenvalues are rational. Keep sparse composition
evaluation in variable numerical degree, and state global convexity in
every invariant-kernel and Bregman argument. Publication attribution and
the relationship between historical versions and the proceedings version
remain with the literature reviewer.

Targeted verification performed for this review: source reads with `cat`,
`sed`, and `rg`; analytic derivations recorded above;
`git diff --check -- paper-exact-arithmetic/evidence/reviews/prewrite-points.md`
(passed); and an inline `python3 - <<'PY'` owned-file document check
(passed: trailing whitespace, final newline, paired code fences, and control
characters). The inline check covers this new untracked file even when
`git diff` has no tracked patch to inspect. No mathematical experiments,
historical Python scripts, project-wide tests, or CI checks were run.
