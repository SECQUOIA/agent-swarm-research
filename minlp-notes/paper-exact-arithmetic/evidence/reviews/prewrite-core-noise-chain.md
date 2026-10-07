Full inherited core-noise chain: analytic proof-completion report

This report implements the root's decision to retain and prove the full
expected-work theorem (architecture decision D1-B), overriding the
architecture's earlier recommendation to state an oracle-conditional
corollary. It covers V1–V5 and RQ1–RQ4. The conclusions below are derived
from the actual source arguments, not from their prior-review labels.
I found no analytic obstruction to
f_D(k)(1+Lambda/sigma)^k poly_D(L+q), with an absolute exponent in
input length and requested precision for every fixed degree D. The
all-dimensional count argument, finite-law format bound, and
coefficient-height-separated exact fallback are essential. A point-growth
count by itself only gives the earlier k<=2 theorem.

Notation: L is binary base input length; n is total continuous dimension;
k is the chosen coordinate-core dimension; D is a fixed objective degree;
q is requested precision; Lambda is the numerical upper coordinate
curvature bound in the product-box theorem; alpha is the supplied joint
core convexifier in the coupled theorem; sigma>0 is noise half-width.
Normalize the chosen coordinates to [0,1]^k, with the resulting data and
physical noise directions included in L. Fixed coordinates and empty or
zero-dimensional domains are handled first by rational LP. Convexity is a
promise or a supplied certificate whose verification is charged.

The proof ingredients fall into three groups. The convex value algorithm
is the rational separation/weak-optimization/feasibility-repair lemma
already assigned to Appendix C. The algebraic fallback and scalar-section
bound use a precise external elimination theorem, specified below for
Luna. Everything that turns those tools into the stated smoothed result
is derived here: continuous projected-growth tails, cell correctness,
all-scale counts, finite-law transfer, cap accounting, retained hulls,
and completion. Appendix I can therefore state the expected result
unconditionally under the declared optimization promises; it need not
introduce an unproved selected-core oracle as a theorem hypothesis.

Source locations and coverage

| Coverage | Source under `research-20261002/new-direction/` | Relevant content |
| --- | --- | --- |
| V1 | `core-only-noise-value-oracle.md`, Sections 2–7 | Convex corner intervals, coordinate rounding, two-pass pruning, k<=2 growth count, every-draw certificates |
| V1 | `all-scale-core-value-oracle.md`, Sections 2–6 | Maximum-simplex proxy, conjugate pushforward measure, covering tail, quadratic QR encoding, all-scale cap |
| V2 | `core-only-noise-core-oracle.md`, Sections 2–4 | Hull containing every optimum and incumbent, terminal depth, growth-failure event, common work factor |
| V3 | `coupled-polytope-core-value-oracle.md`, Sections 2–5; `coupled-polytope-core-oracle.md`, Sections 2–4 | Convex cell model, whole-cell packing, compact-domain growth, exact LP repair |
| V4 | `joint-convex-core-point-oracle.md`, Sections 2–5 | Buffered sublevel body, certified coordinate extrema, ordinary polynomial expected work |
| V5 | `qp-core-cauchy-reconstruction.md`, Sections 2–5 | Lexicographic rational height, rational reconstruction, rational face fallback, exact convex completion |
| Shared | `proximal-growth-tail.md`, Sections 2–6 | Continuous projected-growth argument; the uniform expanding-map proof is sufficient here |
| Shared | `polynomial-finite-noise-tails.md`, Sections 2–3 | Two-block scalar-section components, hybrid marginal replacement, zero/tie atoms |
| Shared | `polynomial-exact-fallback.md`, Sections 2–6; `convex-polytope-value-interface.md`, Section 2 | Same-selector singleton formulas, height-separated elimination, univariate refinement, feasible output |
| RQ1 | `cubic-core-full-point-oracle.md`, Sections 2–5 | Rational-row error modulus for an unknown-core convex surrogate, original-norm regularization |
| RQ2 | `globally-convex-polynomial-point-oracle.md`, Section 7; `affine-power-core-point-oracle.md` | Global-convexifier higher-degree completion and an explicit verifiable subclass |
| RQ3–RQ4 | October 3 `cubic-recourse/{theorem,lattice-certificate,margin-tail}.md`; October 2 `residual-convex-cubic-boundary.md` | New face/minor certificates and residual completion; reconstructed in `prewrite-points.md` |

Exact external contracts to verify and attribute

1. Rational linear programming has polynomial bit cost in its explicit
   rational input, produces polynomial-bit feasible/optimal primal and
   dual points when appropriate, and supplies infeasibility certificates.
   Exact rational convex QP on a bounded rational polytope also has
   polynomial bit cost and a polynomial-bit rational optimizer. The QP
   contract is needed only for V5, not the general polynomial theorem.
2. Rational weak optimization from rational separation: for a full-
   dimensional compact convex body K with a known rational inner ball
   and outer ball, given a rational linear objective p and eta>0,
   return a rational x in K_{+eta} with
   p(x)>=max_{K_{-eta}}p-eta, or correctly report K_{-eta} empty, in
   bit time polynomial in the body's representation, oracle query work,
   objective length, and the binary lengths of the radii and eta. The
   objective convention must cover arbitrary rational p; alternatively
   normalize p and change eta by a rational norm bound. The local source
   identifies GLS Definition 2.1.10, printed p. 50, and Corollary 4.2.7,
   printed p. 106, with the Turing-oracle conventions. Appendix C derives
   feasible convex value intervals by capped epigraphs and rational repair.
3. Fix a two-block real quantifier-elimination algorithm. With one free
   scalar, block sizes a,b, s polynomial atoms of degree <=d, a
   quantifier-free output has numbers of disjuncts, atoms per disjunct,
   and degrees bounded by H=(sd)^{c(a+1)(b+1)} for an effective absolute
   constant c. The combinatorial bound holds for arbitrary real
   coefficients, independent of their heights. For integer/rational
   coefficients of bit length tau, bit work is polynomial in tau times
   the same dimension/format factor, with an absolute polynomial exponent,
   and output coefficient lengths are <=(tau+1) times that factor. More
   generally the source's bound is
   tau log tau log log tau (sd)^{2^{O(omega)} ell product_j n_j},
   plus Boolean-formula evaluation work, with analogous output degree,
   atom, and coefficient-height bounds. The historical notes identify
   Renegar Theorem 1.1, printed p. 330. Its fixed-block and height
   dependence, not just an unspecified elimination existence theorem,
   must be verified by Luna. A general doubly exponential CAD bound does
   not establish the claimed polynomial sampling-bit budget.
4. Explicit univariate integer polynomials admit squarefree reduction,
   real-root isolation, signs of other polynomials at an isolated root,
   and refinement in bit work polynomial in explicit degrees, coefficient
   lengths, formula size, and requested precision, with an absolute
   exponent. This may use standard Sturm/subresultant algorithms; it
   must not be replaced by an exponent depending on n or degree.
5. Standard convex-conjugate/proximal facts: finite convex functions are
   differentiable almost everywhere; the proximal inverse of a monotone
   subgradient map is 1-Lipschitz; the conjugate of a 1/lambda-strongly
   convex finite function has a lambda-Lipschitz gradient; a 1-Lipschitz
   map on R^k does not increase k-dimensional Lebesgue outer measure.
   The uses and the relevant elementary proofs are given below. These
   are mathematical tools, not computational optimization oracles.

All later exponential budgets use an effective chosen algorithm in (3),
not an unknown constant estimated after sampling. Choose a sufficiently
large computable base factor 2^{p_D(L)} once. In this report, poly_D
means a polynomial whose exponent may depend on fixed D, but never on
n,k,noise coefficient height, or q.

Exact same-selector fallback and scalar-section counting

Let X be the original compact rational box or bounded rational polytope,
and F_gamma=F_0+gamma'v. Its globally optimal set is nonempty compact.
Successively minimizing coordinates gives a unique lexicographically
least optimizer, ordering the chosen core coordinates first. Use a
linear-size nested predicate LexGE(y,x), rather than assuming a finite
stationary set. The coordinate singleton formula is

```
exists x forall y:
  x in X and x_i=t and
  [y not in X or F_gamma(y)>F_gamma(x) or
   (F_gamma(y)=F_gamma(x) and LexGE(y,x))].
```

The value singleton replaces x_i=t by F_gamma(x)=t. All coordinate
formulas select the same point, including ties and positive-dimensional
optimal sets. There are two blocks of n variables, one free scalar,
poly(L) atoms and Boolean syntax, and degree <=max(D,2). Clearing
denominators gives coefficient lengths tau=poly_D(L+b), where b is
realized noise coefficient length. Contract (3) therefore gives a
base-computable B_alg=2^{poly_D(L)} with explicit output format and
coefficient lengths <=B_alg poly_D(L+b).

For an eliminated singleton formula, discard constant polynomial atoms;
form the product of nonconstant atom polynomials and take its squarefree
part P(t). The singleton must be a root of P: away from every such root,
all signs are constant on a neighborhood, which cannot define one point.
Isolate all roots, determine the atom signs, and retain the unique root
satisfying the formula. Separate coordinate and value encodings are
consistent because their formulas refer to the same canonical optimizer.
Contract (4) has an absolute polynomial exponent, so after enlarging the
base factor B_0, the whole construction and subsequent refinement cost

```
B_0 poly_D(L+b+q),   B_0=2^{poly_D(L)}.
```

The enlarged B_0 covers polynomial operations on exponentially long
records; it is fixed before the noise mesh. This is the reason sampled
height b and q are not placed into an exponential. Refine the canonical
point to max-norm error delta. In a product box clip its rational
approximations. In a polytope solve the rational LP
X intersect {|x_i-w_i|<=delta for every i}. The exact canonical point
witnesses nonemptiness; every LP solution is within 2delta of it in
max norm. With G>=max(1,sup_X||grad F_gamma||_1), this repair has
objective error <=2Gdelta. Choose delta<=2^(-q)/(4G), and refine the
exact value to width <=2^(-q)/2. This gives the feasible objective
interval. For core-distance output additionally use
delta<=2^(-q)/(4(k+1)). Additional precision is poly_D(L+b)+O(q).
Clipping alone is not valid on coupled domains.

For a scalar-section event, use the combinatorial part of contract (3)
with every other noise coordinate and every threshold fixed as arbitrary
reals. If H bounds disjuncts, atoms per disjunct, and degrees, at most
H^2 polynomial occurrences have at most H^3 real roots in total.
Discard identically zero polynomials, whose signs are constant. The
event and its complement are unions of at most C=2H^3+1 intervals or
individual points. This bound is uniform at singular specializations
and independent of thresholds or coefficient heights.

An endpoint-inclusive M-point uniform grid on [-sigma,sigma] has CDF
distance at most 1/M from continuous uniform noise. An interval or point
has probability discrepancy <=2/M with any endpoint convention. Replace
the k independent marginals successively, conditioning on all other
coordinates at each step. The section bound remains valid for arbitrary
hybrid continuous/discrete values. Thus the product-law discrepancy for
the event is <=2kC/M. This argument does not require Mh>=1, does not
lose control when query grids become finer than the noise grid, and
does not discard exact-zero or tie atoms.

Projected growth under continuous and finite noise

For any continuous F_0 on a compact joint domain X whose core v has
coordinate widths <=1, define g(gamma) as the supremum of t>=0 for
which some x_*=(a,z_*) in X satisfies

```
F_gamma(v,z)-F_gamma(a,z_*) >= t||v-a||^2  (all (v,z) in X).
```

Residual ties are allowed. Distinct optimal cores force g=0. If the
core projection is a singleton, set g=infinity. For t>0, compactness
shows that g>=t is exactly the displayed existential-universal property,
including equality at the threshold. It is closed as a set of coefficients:
along a convergent coefficient sequence pass a subsequence of compact
witnesses to the limit. This establishes measurability and supports
exact two-block section counting without assuming projected-value
continuity on a coupled domain.

The following uniform-noise proof is shorter than the general bounded-
density divergence proof in the source and suffices for every theorem
here. Translate each core coordinate so its range is centered at zero;
objective constants and growth distances are unchanged. For t>0 define

```
H_t(c)=max_{(v,z) in X}[c'v-F_0(v,z)+t||v||^2].
```

It is finite convex and globally Lipschitz. Every maximizing core is a
subgradient; all subgradient coordinates lie in [-1/2,1/2]. Let
P(y)=argmin_c[H_t(c)+||c-y||^2/(4t)]. Its unique minimizer satisfies
y-c in 2t partial H_t(c). Monotonicity implies that P is 1-Lipschitz:
dot the difference of two subgradient relations with c-c' to obtain
||c-c'||^2 <= (c-c')'(y-y').

At a differentiability point c of H_t, all maximizing cores equal
a=grad H_t(c). For y=c+2ta, optimality in the defining maximum gives

```
F_0(v,z)-y'v-[F_0(a,z_*)-y'a] >= t||v-a||^2.
```

Thus g(-y)>=t and P(y)=c. The nondifferentiability set N is Lebesgue
null. Every c in the inner coefficient cube
[-sigma+t,sigma-t]^k outside N maps to a good y in [-sigma,sigma]^k,
because |2ta_i|<=t. Let G_t be the closed good set in that noise cube.
Then P(G_t) contains the inner cube except N. Lipschitz volume
contraction gives |G_t|>=|P(G_t)|>=|inner cube|. If t<sigma,

```
Pr_cont(g<t) <= 1-(1-t/sigma)^k <= kt/sigma.
```

If t>=sigma the final bound is already at least one. Widths smaller
than one give the sharper sum-of-widths bound. The same proof holds
for a compact joint domain: it uses the unique maximizing core, not a
unique residual witness or continuous partially minimized objective.
Reflection preserves the symmetric noise law and handles either sign
convention. Deterministic linear offsets are harmless.

For polynomial F and rational domain, the good-growth property has one
existential joint witness and one universal joint competitor block,
poly(L) atoms, degree <=max(D,2). The preceding scalar-section and
hybrid replacement proof yields a base-computable C_g=2^{poly_D(L)}
such that, on every sufficiently fine fixed grid and for every t>0,

```
Pr_grid(g<t) <= kt/sigma+C_g/M.
```

Decreasing thresholds gives Pr(g=0)<=C_g/M and also includes finite
ties, unique zero-growth optima, and exact polynomial relations. No
almost-sure argument substitutes for this bound. This projected growth
is used only to choose a cost cutoff; all returned certificates remain
valid without assuming a probable growth event.

Product-box cells: deterministic correctness before probability

For X=[0,1]^k times a fixed residual box, F_0(v,.) convex, and
F_(v_i v_i)<=Lambda, set h=2^(-j) and e_h=k Lambda h^2/8.
Assume Lambda>0 for now. A rational convex residual solve at every
queried corner w returns ell_w<=V_gamma(w)<=u_w=F_gamma(w,z_w)
with u_w-ell_w<=e_h. On a generated core cell C define
LB(C)=min_corner ell_w-e_h. Query all its corners, maintain the best
feasible upper value U from this and previous levels, and retain exactly
the cells with LB(C)<=the final U in a second pass. Do not count cells
using an obsolete incumbent.

Independent rounding of a core point v to its cell corners preserves
means. For a univariate function with second derivative <=Lambda,
subtracting Lambda s^2/2 makes it concave, so expected rounding cost
is <=Lambda times variance/2. Successively rounding coordinates adds
at most k Lambda h^2/8=e_h. Hold a residual optimizer at v fixed while
rounding; minimizing residuals at corners can only lower these values.
Therefore LB(C) is a valid bound throughout the cell. Every optimal
core survives every subdivision. An optimal cell has a true corner
value <=f_*+e_h and an oracle upper <=f_*+2e_h, so U-f_*<=2e_h.
All current LB(C)>=U-2e_h because ell_w>=u_w-e_h>=U-e_h.
Previously discarded cells had LB above their then incumbent, hence
above the current U. Current and previously discarded cells cover the
domain. Thus [U-2e_h,U] is globally valid.

Every retained cell separately has a minimizing-lower-bound corner with
true V_gamma value <=U+2e_h<=f_*+4e_h. This invariant is independent
of oracle tie choices. List construction and the two passes are linear
in generated count. A corner is incident to at most 2^k cells; repeated
queries add a parameter factor, not a quadratic list operation. Stop
at the first J with 2e_(2^-J)<=2^-q; J=poly(L)+O(q).
For Lambda=0, rounding to the original core vertices never increases
expected value, so the minimum is the least of 2^k convex residual
vertex values; this gives deterministic 2^k poly_D(L+q) value work.
Selected-core output uses Lambda_+=Lambda+sigma>0 instead, changing
(1+Lambda/sigma)^k by only a factor <=2^k.

The earlier low-dimensional count follows directly from growth. A
retained witness corner is within h sqrt(kLambda/(2g)) of the unique
optimal core when g>0. Node counts and incidence give generated count
<=4^k(3+sqrt(2kLambda/g))^k. For k<=2 this is
<=512 max(1,Lambda/g)^(k/2). With Z=max(1,Lambda/g), the growth tail
gives Pr(Z^(k/2)>s)<=kLambda s^(-2/k)/sigma+C_g/M.
Its truncated integral is bounded for k=1 and logarithmic for k=2;
for k>2 it grows as B^(1-2/k), so this route does not prove arbitrary
core dimension. Explicitly, with r=kLambda/sigma and beta=C_g/M,
the truncated expectations are <=1+r+beta B for k=1 and
<=1+r log B+beta B for k=2, while B Pr(Z^(k/2)>B)<=r+beta B.
A cap 512B and B>=B_0 therefore prove the sharper
(1+Lambda/sigma)poly_D(L+q) value bound for k<=2. Adding the
selected-core growth-failure event below preserves that sharper bound.
The all-scale count below is the actual repair for unrestricted k.

All-dimensional count: convex conjugacy and one weak first moment

Use the negative-tilt convention f_c(v)=V_0(v)-c'v, where V_0 is
continuous on the core box. Define

```
eps_h=k Lambda h^2/2,
S_h(c)={v:f_c(v)<=min f_c+eps_h},
K_h(c)=conv(S_h(c))+[-h/4,h/4]^k,
D_h(c)=max_{y_0,...,y_k in K_h}|det(y_1-y_0,...,y_k-y_0)|,
A(c)=sup_(0<h<=1)D_h(c)/h^k,  W(c)=max(1,A(c)).
```

For any compact full-dimensional convex K and its maximum simplex
determinant D(K), D(K)/k!<=vol(K)<=2^kD(K). The lower bound is its
maximizing simplex volume. For the upper bound, any point of K has
each coordinate in the maximizing edge basis of absolute value <=1:
replacing a maximizing vertex by that point multiplies its determinant
by the relevant barycentric coordinate. The edge parallelepiped with
coefficient cube [-1,1]^k contains K and has volume 2^kD(K).

If N_h distinct h-grid nodes lie in S_h, their centered side-h/2 cubes
have disjoint interiors and lie in K_h. Thus N_h(h/2)^k<=vol(K_h)
and N_h<=4^kA. Every retained cell has such a node, incident to at
most 2^k cells; subdivision contributes another factor 2^k. Generated
cells at every level are <=16^kW. This includes the initial cell and
holds for every admissible sequence of convex-oracle answers.

Define on all coefficient space
b(c)=max_v[c'v-V_0(v)] and H(c)=b(c)+||c||^2/(2Lambda).
The finite convex b has subgradients in [0,1]^k. H is
1/Lambda-strongly convex, and H* has Lambda-Lipschitz gradient.
Let mu(E)=Leb{y:grad H*(y) in E}. This is a Borel pushforward measure,
locally finite: if E is in [a,b]^k, its inverse image is in
[0,1]^k+[a,b]^k/Lambda because y in partial H(c).

For v in S_h(c), approximate maximizing optimality gives
b(t)>=b(c)+v'(t-c)-eps_h for every t. Completing the square in
H*(v+c/Lambda) gives the Fenchel residual
r_c(y)=H(c)+H*(y)-c'y at y_0=v+c/Lambda bounded by eps_h.
Strong convexity of H gives
||grad H*(y_0)-c||<=sqrt(2Lambda eps_h). Smoothness gives, for
u in [-h/4,h/4]^k,

```
r_c(y_0+u)
 <=eps_h+sqrt(2Lambda eps_h)||u||+(Lambda/2)||u||^2
 <=(25/32)k Lambda h^2 <=k Lambda h^2.
```

The convexity of r_c extends this bound to K_h+c/Lambda. Strong
convexity again implies that this translated body maps by grad H*
into the open ball B(c,4kLambda h). Consequently
vol(K_h)<=mu(B(c,4kLambda h)). No smoothness or absolute continuity
of mu is assumed.

Put R=4kLambda and Q=[-sigma,sigma]^k. Every such ball with h<=1
lies in Q_R=[-sigma-R,sigma+R]^k, and
mu(Q_R)<=(1+2sigma/Lambda+8k)^k. If A(c)>s, some h gives
mu(B(c,Rh))>s(Rh)^k/(k!R^k). A 5r disjoint-ball selection covers all
such centers by fivefold enlargements. In this bounded setting its proof
is elementary: repeatedly choose a ball of radius more than half the
remaining supremum, discard all intersecting balls, and continue.
Selected balls are disjoint; each discarded ball has radius <=2 times
its selected ball, so its center lies in the selected fivefold ball.
Infinitely many selected balls of radii bounded below cannot fit in
the bounded Q_R, so every remaining positive-radius ball is eventually
discarded. The selected family is countable.

Summing disjoint-ball measures and enlarged-ball volumes gives

```
Leb{c in Q:A(c)>s}
 <=5^k v_k k!R^k mu(Q_R)/s,
Pr_cont(A>s) <=a_k/s,
a_k=(180k^3)^k(1+Lambda/sigma)^k.
```

Here v_k<=2^k and k!<=k^k yield the conservative displayed a_k.
This is a weak first-moment tail, not a finite untruncated expectation
of W. It holds in every core dimension and controls all real scales
simultaneously. It avoids products of directional growth constants.

The all-scale event is a finite two-block formula

To define A(c)>s, existentially choose 0<h<=1 and k+1 points y_i of
K_h. Caratheodory supplies each as
y_i=sum_(j=0)^k lambda_ij v_ij+u_i, lambda_ij>=0,
sum_j lambda_ij=1, |u_i,l|<=h/4. Choose residual witnesses z_ij and
require for every original feasible competitor (v,z), simultaneously
for all i,j,

```
F_c(v_ij,z_ij) <=F_c(v,z)+k Lambda h^2/2.
```

Attainment makes this exactly v_ij in S_h, not a relaxation. A single
universal competitor block serves all comparisons. Finally require
|det(y_1-y_0,...,y_k-y_0)|>s h^k. Do not expand this determinant
into k! monomials. Existentially introduce Q,R with Q'Q=Id,
R upper triangular with positive diagonal, and the edge matrix QR.
Scalar product chains encode the diagonal product and h^k; compare
those two products. A nonsingular real edge matrix always has such a
QR factorization, and its positive diagonal product equals the absolute
determinant. Conversely these equations force the same determinant.
All added equations have degree <=2 and polynomial-size explicit
encoding, and no extra quantified block is introduced.

The existential block has O(k^2 n+k^2) variables, the universal block
n variables, poly(L) atoms, and degree <=max(D,2). With one noise
coordinate free and all others plus s arbitrary fixed reals, the scalar
section bound is 2^{poly_D(L)}. Marginal replacement therefore gives
one base-computable C_a such that for all s>=1 on the same finite law,

```
Pr(W>s) <=a_k/s+beta,  beta=C_a/M.
```

It also proves measurability of A and W, including W=infinity.
No volume or integral is quantified, and no section bound for the
algorithm's execution path is required. Exact tied/singular atoms
remain in beta. A symbolic determinant expansion would create an
unjustified format-size shortcut; the QR encoding repairs it.

One cap, one finite law, and the common factor

Choose before sampling B>=max(2,B_0), log B=poly_D(L), and a power-of-
two M>=C_a B. Sample each label j with log_2 M random bits and form
gamma_i=-sigma+2sigma j/(M-1). Then realized coefficient height
b=poly_D(L), beta B<=1, and the law is independent of q. Cap
generated product-box cells at 16^kB, checking children counts before
construction or oracle calls. A cap at any level or query implies W>B.
There is no union over levels or future queries. Completed ordinary
work and record length are bounded pathwise, for all q, by

```
[f(k) min(B,W)+B_0 1_(W>B)] poly_D(L+q).
```

Integrating the tail gives
E min(B,W)<=1+a_k log B+beta B and
B Pr(W>B)<=a_k+beta B. Since B_0<=B and log B is polynomial in L,
these prove V1's expected f_D(k)(1+Lambda/sigma)^k poly_D(L+q).
Repeated oracle calls and their bit arithmetic are absorbed in the fixed
polynomial. All ordinary certificates are the cell/pruning/convex-value
certificates already proved sound; probability only pays for their cost.
Fallback solves the same sampled objective on every exceptional atom.

Selected core via a retained hull

Use Lambda_+=Lambda+sigma. Every optimal core survives all cells. The
incumbent core survives as well: at insertion it belongs to a producing
cell; at later levels any child containing it has LB<=its feasible
objective U, so it survives the final pass. Earlier pruned cells had
LB>their then incumbent>=the current U, hence cannot contain that
incumbent. Let H_j be the coordinate hull of retained cells. It contains
every optimal core, including the selected core a, and the incumbent.
The rational test sum_i width_i(H_j)^2<=2^(-2q) therefore certifies
the incumbent's distance to this fixed a without deciding uniqueness.

Choose g_0=sigma/(2kB), one common M>=2B max(C_a,C_g), and
D_hull=4k+k^2Lambda_+/g_0. On g>=g_0, each retained witness is
within h sqrt(kLambda_+/(2g_0)) of the unique optimal core; every point
of its cell differs from it by at most h in each coordinate. Hence
diam(H_j)<=2sqrt(k)h(1+sqrt(kLambda_+/(2g_0)))<=D_hull h.
Stop at the first J satisfying both 2e_J<=2^-q and
D_hull 2^-J<=2^-q; J=poly_D(L)+O(q). If the actual hull test fails,
invoke the same-selector exact fallback. Failure at any q implies the
single event g<g_0, with probability <=1/B.

The pathwise factor becomes
f(k)min(B,W)+B_0 1_(W>B or g<g_0). Its extra expected contribution
is <=B_0/B<=1. The fallback lexicographic core and the ordinary hull
therefore provide V2 for the same a on every draw and every precision.
Residual output still has only objective-gap accuracy. Dyadic shortening
can give a core vector of poly_D(L)+O(q) bits even when the internal
fallback record is exponentially long; its production is charged inside
the same random factor.

Coupled domains under a supplied convexifier (V3)

Suppose P is a bounded rational polytope and
G_alpha=F_0+(alpha/2)||v||^2 is convex on P. On a dyadic cell
C=prod[l_i,u_i], solve over Q_C=P intersect {v in C} the convex

```
phi_C=F_c+(alpha/2)sum_i(v_i-l_i)(v_i-u_i),
e_h=alpha k h^2/8.
```

Empty cells have LP certificates. Otherwise a feasible convex solve to
gap e_h gives ell_C and w_C with phi_C(w_C)-ell_C<=e_h, while
0<=F_c-phi_C<=e_h. Therefore the true upper U_C=F_c(w_C) is
<=ell_C+2e_h. Two-pass pruning ell_C<=U gives exactly the same
value interval [U-2e_h,U], survival, and per-cell true witness gap
<=4e_h. The witness may lie anywhere in its cell; core corners need
not be feasible. The convex value lemma handles relative affine hulls
and exact LP repair, so no lower-dimensional condition is omitted.

Define S_h as projected joint near-optimal points with true gap
<=alpha k h^2/2 and K_h=conv(S_h)+[-h,h]^k. Every retained full
cell lies in K_h, although much of that cell may be infeasible. Disjoint
interiors and the maximum-simplex comparison give retained count
<=2^kA and generated count <=4^kW. Define
b(c)=max_(v,z) in P[c'v-F_0(v,z)] and H=b+||c||^2/(2alpha).
Its subgradients remain in [0,1]^k even if the projection is proper or
lower-dimensional. The larger padding gives Fenchel residual <=
2k alpha h^2, and hence maps K_h+c/alpha into B(c,4k alpha h).
The same measure and covering derivation gives a_k with alpha replacing
Lambda. The event formula uses membership in P and padding |u|<=h,
with the same two-block QR construction. Thus its scalar sections,
cap 4^kB, weak tail, and budget are unchanged up to parameter constants.

For a selected core, use alpha_+=alpha+sigma, the compact-domain growth
proof above, and the same retained hull: every cell containing the
feasible incumbent has ell_C<=F_gamma(incumbent)=U. Terminal depth
and failure events are identical with alpha_+ replacing Lambda_+.
Fallback feasibility is restored by LP, not ambient clipping. This proves
V3 in full without a projected-continuity assumption. If alpha=0, values
are deterministic convex optimization; selected coordinates have the
sharper V4 guarantee below. Mere residual fiber convexity on a coupled
domain does not supply this joint convex cell model.

Joint convexity: ordinary expected polynomial selected-coordinate output (V4)

For convex F_gamma on P, use only the growth tail and fallback, with
B>=B_0, g_0=sigma/(2kB), M>=2C_gB. Then Pr(g<g_0)<=1/B.
For epsilon=2^-q choose
delta=min(epsilon/4,g_0 epsilon^2/(128k)) and zeta=epsilon/(8k).
Obtain a feasible incumbent y with true value U and certified gap
<=delta. Its buffered convex sublevel K={x in P:F_gamma(x)<=U+delta}
contains y and all global optimizers and has true gaps <=2delta.

In rational affine-hull coordinates x=x_0+A w, let R contain
B(0,r_R) and lie in B(0,R_R). Put psi(w)=F_gamma(x_0+A w),
W_f>=max(1,sup_R|psi|), lambda=min(1/2,delta/(8W_f)),
c=(1-lambda)w_y, and r=lambda r_R. Convexity shows that
(1-lambda)w_y+lambda R lies in the buffered sublevel, with value
<=U+2W_f lambda<=U+delta/4. Thus K has a known relative ball
B(c,r) and outer radius 2R_R. Linear rows and polynomial tangents give
a rational separation oracle. All radius lengths are poly_D(L)+O(q).

For each selected affine coordinate p(w)=b_i+a_i'w and its negative,
let A_i>=||a_i||. With eta<=r/2, moving a maximizer toward c by
fraction eta/r puts it in K_{-eta} and loses at most eta/r in p,
because its feasible coordinate range has width <=1. Weak optimization
gives p(w_hat)>=p_* -eta(1+1/r), while near-feasibility gives
p(w_hat)<=p_*+A_i eta. Hence
p(w_hat)+eta(1+1/r) is a certified upper bound on p_* with excess
<=eta(A_i+1+1/r). Use eta=min(r/2,zeta/(A_i+1+1/r)).
After 2k calls, the resulting rational coordinate hull encloses both
y's core and every optimal core. No feasibility repair of w_hat is
needed because only its scalar bound is used; output feasibility comes
from y. The hull's squared-diameter test <=epsilon^2 is sound.

On g>=g_0, K's cores lie within sqrt(2delta/g_0)<=epsilon/(8sqrt(k))
of the unique optimal core. Each true coordinate range is therefore
<=epsilon/(4sqrt(k)), and enclosure error adds 2zeta, for total width
<=epsilon/(2sqrt(k)). The test passes. Failure at any q implies the
same event g<g_0. Fallback is same-selector and exactly repaired. The
common factor 1+B_0 1_(g<g_0) has expectation <=2. All ordinary
calls are polynomial in L+q and k<=n<=L; there is no exponential k
factor or numerical inverse-noise factor. This proves V4, including
arbitrarily thin and lower-dimensional P. Noise on the requested
coordinates is essential; unperturbed residual coordinates are not
covered by this selected-coordinate conclusion.

Exact QP reconstruction (V5)

For a rational quadratic q(x)=x'Ax/2+c'x+c_0 on bounded rational P,
the core-first lexicographic global optimizer x_* has polynomial rational
height even if the full QP is nonconvex and its optimal set is not
convex. On its smallest face choose independent active rows R and an
integer nullspace basis N of R. Two-sided tangent stationarity gives
N'(Ax_*+c)=0. The rational polytope
S=P intersect {Rx=d_R,N'(Ax+c)=0} contains x_* and has constant
q-value: for x,y in S, w=x-y is tangent, w'(Ay+c)=0, w'Aw=0,
so the exact quadratic difference is zero. Its lexicographic minimum
x_* is a vertex, because one endpoint of any nontrivial segment through
it would be lexicographically smaller.

Choose an even integer Delta clearing all data and making Delta A
entrywise even; twice the product of denominators suffices. Bound all
entries of Delta A,Delta c,Delta c_0,Delta E,Delta d by C>=1.
An integer nullspace basis constructed from minors has entries
<=n!C^n. Stationary-face equations have integer coefficients and right
side bounded by C_1=n n!C^(n+1). Cramer's rule at a vertex gives
one coordinate denominator and numerator bound U=n!C_1^n. The exact
value denominator divides Delta times that coordinate denominator
squared. Thus Q=Delta U^2 is a uniform reduced-denominator bound for
the selected coordinates and value, with log Q polynomial in input
bits including sampled noise.

After fixing the common finite law, choose this bound uniformly over
draws using the base denominators, sigma denominator, and M-1; no mesh
revision is needed. Query the established selected-core/value evaluator
at 2^-t<=1/(8Q^2), so t=poly(L+log M)=poly(L). Each coordinate error
interval and the value interval contain exactly one rational with
denominator <=Q, because distinct such rationals differ by >=1/Q^2.
Continued fractions of their rational midpoint, or an interval Euclidean
algorithm, recover it in polynomial bit work; the approximation error
is below 1/(2Q^2), so the relevant rational occurs as a convergent.
Signed values, zero, and exact midpoint equality are handled directly.

Use a rational face-enumeration fallback inside this QP evaluator.
On x_*'s smallest face, a nonzero tangent Hessian null direction would
permit both small signs at the same value, one lexicographically smaller.
Thus that tangent Hessian is PD, with a vertex allowed. Enumerating
independent active-row sets, solving nonsingular stationary systems,
discarding infeasible candidates, and choosing minimum value then
lexicographic order includes x_*. The number of solves is a base-only
exponential factor; each solve and rational output has polynomial bits.
Choose the fallback budget before the mesh, as above. This avoids
charging nonlinear postprocessing of generic expanded algebraic records
as polynomial work merely because their expected size is bounded.

At the reconstructed exact core a, solve the rational residual QP
exactly. In the product model its residual Hessian is PSD; in the
coupled model the convexifier is constant on a fixed-core fiber, so the
restricted quadratic is convex there. Affine-hull reduction covers
lower-dimensional fibers. Any rational residual optimizer completes a
global optimizer; no full residual lex selection is needed. This proves
V5 with the inherited expected work and polynomial output size on
every draw. The height argument is specific to QPs and cannot be
transferred to cubic/quartic exact recovery.

Full completion with a supplied convexifier (RQ1 and RQ2)

For cubic F_0 on coupled P with a supplied alpha, set beta=alpha+1
and G=F_0+(beta/2)||v||^2. For exact selected a define
T_a=G-(beta a+c)'v+(beta/2)||a||^2
    =F_c+(beta/2)||v-a||^2.
Its optimizer set is exactly the globally optimal fiber S_a, hence
convex. The core search still uses alpha; beta is only a polynomial-bit
completion coefficient and does not change its numerical smoothing factor.

In rational affine-hull coordinates x=x_0+B w, v=v_0+Ew, let
h(w)=G(x_0+B w), H_0=Hess h(0), g_0=grad h(0). With a rational
inner ball of radius r and outer radius R>=1, affine cubic Hessians
obey 0<=H(w)<=beta_0H_0, beta_0=1+R/r. Thus ker H_0 is common.
For u representing any y in S_a, the target fiber is the rational-row
slice [H_0;g_0';E](w-u)=0 inside the reduced polytope. The unknown
core appears only in the right-hand side.

Let Delta=T_a(x)-f_*. Cubic Taylor/transverse estimates give
||Pi(w-u)||<=C_perp Delta^(1/4), where Pi projects off ker H_0
and one conservative rational choice is
C_perp=108R^2 beta_0 M/lambda_0^2,
M>=max(1,||H_0||), lambda_0 a rational lower bound on its positive
eigenvalues. Indeed, writing s=d'H(u)d+d'H(w)d gives Delta>=s/6,
d'H_0d<=s+R sqrt(2beta_0Ms)<=3R sqrt(2beta_0Ms), and the
coarser coefficient follows. If H_0=0, put C_perp=0.
Also ||Ed||<=2sqrt(Delta) and
|g_0'd|<=Delta+N||Ed||+beta_0MR||Pi d||,
N=k(beta+sigma). For Delta<=1 the stacked rational residual is
<=C_res Delta^(1/4), C_res=3+2N+M(1+beta_0R)C_perp.
Clear denominators and apply the integer Hoffman lemma, then multiply
by ||B||, to obtain uniform polynomial-bit Gamma for distance to S_a.
No irrational coefficient of T_a is computed by the algorithm.

Regularize in the original norm with
tau=epsilon^6/(1024R_x^4Gamma^4), eta=tau epsilon^2/8,
delta=tau epsilon^2/(32 beta k). Obtain a short dyadic core b with
||b-a||<=delta and solve on original P
G-(beta b+c)'v+tau||x||^2 to feasible gap eta. Core perturbation
changes this objective by <=beta sqrt(k)delta uniformly; the exact-core
regularized gap is <=eta+2beta sqrt(k)delta<=tau epsilon^2/4.
The minimum-norm selection lemma gives bias epsilon/2, and strong
convexity gives solve error epsilon/2. This establishes RQ1 for the
fixed minimum-original-norm optimizer in the selected fiber. Feasibility
of b as a projected point is unnecessary; feasibility is imposed on x
by the convex solve. Read only the short Cauchy output, not an expanded
fallback record as an uncharged postprocessing input.

RQ2 follows when the supplied G_alpha is globally convex of fixed higher
degree. The same T_a is globally convex. Its linear-tilt coefficients
have known magnitude bounds from |a_i|<=1 and |c_i|<=sigma. The global
Bregman/interpolation proof therefore bounds its gradient coefficient
residuals by a uniformly computed constant times Delta^(1/D).
Use the rational coefficient-row matrix N_G of grad G plus the core
extraction matrix E. The nonconstant coefficient rows of grad T_a equal
those of grad G; the constant row differs by (beta a+c)'E, whose
contribution is bounded by ||Ed||<=sqrt(2Delta/beta). Hence every row
of [N_G;E] has residual O(Delta^(1/D)) for Delta<=1. Its zero slice
is exactly S_a; equality of E removes the unknown tilt, and equality
of N_G preserves G globally. Rational Hoffman gives the uniform
polynomial-bit Gamma and the general 1/D selector schedule. The same
short-core perturbation budget and convex solve prove full output with
the inherited expected bound. An explicit PSD quadratic plus positive
even powers of affine functions is a polynomial-time verifiable
certificate subclass: check equality of the fixed-degree polynomials
and PSD of the quadratic matrix. It is a corollary of this broader
completion, not a recognition algorithm for all globally convex inputs.

Composition with the new residual-convex cubic theorem (RQ3–RQ4)

The face/LLL/margin/completion proof in `prewrite-points.md` now consumes
the fully proved V2, not a hypothesis left outside the paper. Nearby
tilts use the original and 2k shifted baselines F +/- t v_i with the same
gamma. Each satisfies the same residual convexity and coordinate bound;
their bit lengths are polynomial in L. Each common-law requirement is a
lower bound on M, independent of q. Select a common power-of-two M
satisfying all 2k+1 requirements and the separate rare margin/face
budget. Increasing M improves every C/M atom estimate, so no instance
needs a different sample. Each all-scale/growth factor keeps the same
expectation under the larger valid M.

The full selector fallback is a singleton formula with global optimality,
lexicographically least core, and minimum squared residual norm among
equal-core global optima. It retains two quantified blocks and degree
three. Its preselected base B_full covers all univariate representation
and short-output work. Add B_full times the indicator of the single
base face/LLL rejection event to the sum of the 2k+1 inherited random
work factors. Rejection has probability <=1/(4B_full). The sum has the
announced expected f(k)(1+Lambda/sigma)^k poly(L) factor; no
independence of these factors or events is required. All requested
core accuracies are poly(L)+O(q), so this same sum controls every q.

RQ4's counterexamples do not invalidate the repaired composition:
F(v,z)=vz^2 has no core-uniform residual modulus, and affine fibers
can have discontinuous minimum-norm selection at a boundary core.
RQ1 uses a convex surrogate on the original fixed P; RQ3 certifies the
exact core face, a draw-specific polynomial-bit fiber modulus, and
regularization. No unstated continuity of residual selection enters.
Quartic residuals and arbitrary coupled domains without a joint
convexifier remain outside these completion arguments.

Remaining manuscript obligations and audit result

Appendix I must actually include the cell/pruning proof, all-dimensional
maximum-simplex/conjugate/count proof, QR event encoding, finite-law
replacement, exact separated-height fallback, projected-growth proof,
retained-hull proof, and their cap/work bookkeeping before invoking V2
inside RQ3. V3–V5 and RQ1–RQ2 can then be stated as corollaries with
the modifications proved above. Replacing any one of these steps by
“previously reviewed” or an internal note link would leave the
self-contained expected theorem incomplete.

The exact external theorem contracts in items 1–5 are the only source
verification requests arising from this audit. In particular, if Luna
cannot verify the fixed-two-block coefficient-height contract, the
sampling-bit and base-fallback complexity claims cannot be asserted
from an unspecified QE theorem. With that classical contract, no
remaining analytic blocker was found. Both determinant encodings and
fallback formulas have polynomial-size explicit format, and every
random exceptional event is paid for on its original finite draw.

No experiments, mathematical script reruns, browsing, delegation, or
CI inspection were performed. Read-only source inspection used `cat`,
`sed`, and `rg`. Targeted checks actually run are
`git diff --check -- paper-exact-arithmetic/evidence/reviews/prewrite-core-noise-chain.md`
and an inline `python3 - <<'PY'` check of this owned file's final newline,
trailing whitespace, paired code fences, and control characters. Both
passed. The inline check covers this new untracked file even if the
scoped diff has no tracked patch. These check the document, not the
universal mathematical claims, and are distinct from CI.
