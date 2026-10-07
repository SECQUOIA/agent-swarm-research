# Core-only smoothing with native integer flows and arbitrary core faces

Date: 2026-10-02. Status: passed fresh independent
[full proof review](../reviews/smoothed-boundary-core-flow-adversary.md) and
[arithmetic/output review](../reviews/boundary-core-flow-bit-adversary.md),
with distinct exact diagnostics. The value-margin lemma also has a
[focused audit](../reviews/flow-boundary-margin-review.md).
No index or publication-priority claim.

The [interior theorem](smoothed-interior-core-flow.md) perturbs only a small
continuous core, but requires its optimizers to be interior. The
[optimal-flow face certificate](flow-optimal-face-certificate.md) removes
that restriction. It represents all tied optimal flows by tightened arc
intervals, minimizes inward derivatives over that entire set, and controls
losing flows by their distance from those intervals. The price is a larger
parameter-dependent precision budget. This note does not retain the
interior theorem's literal constant-base work expression or polynomial-in-
input sampling length.

## 1. Model and conclusion

Let `Y` be the nonempty set of integer flows in a fixed directed network,
with `r` arcs, `s` nodes, integral supplies, and finite integral arc bounds
encoded in binary. Let

```
v in [0,1]^k,
F_gamma(v,z)=phi(v)+sum_a f_a(v,z_a)+gamma'v.
```

The displayed functions are explicit rational polynomials of fixed degree
at most `d>=1`. Each `f_a(v,.)` is convex on its native real interval for every
core point. Supply a valid bound `partial_ii F_0<=L`, `L>0`, on the original
domain. These premises and any required verification records are included
in the base input length `I`, together with rational `sigma>0`. The core
changes only costs. There is no growth, interiority, integer-dimension,
graph-width, uniqueness-of-flow, or positive-Hessian premise.

There are effective functions `f_d` and a base-computable power of two `M`
such that

```
log M<=f_d(k) poly_d(I),                                  (1)
```

and independent uniform **core-only** noise on

```
{-sigma+2sigma j/(M-1):j=0,...,M-1}
```

admits exact optimization on every draw with expected bit work and expected
proof-record size

```
f_d(k) [3+(1+k/2)L/(2sigma)]^k poly_d(I).                  (2)
```

The exponent of the input polynomial is independent of `k`. Thus this is
expected FPT in `k` and `L/sigma`, with native capacities entering through
their binary lengths. The residual costs are not perturbed. Arbitrarily
many optimal flows may persist. All randomness is sampled once; an exact
fallback on the same draw handles every exceptional atom.

Output is an exact integer flow and a common-root algebraic representation
of one core optimizer and value. Its length on every draw is at most
`f_d(k) poly_d(I)`, and refinement to `t` bits costs
`f_d(k) poly_d(I+t)`. For quadratic objectives, rational output is available.
For `k=0`, use the exact integer-flow oracle directly. If all residual arc
coordinates are fixed, use the deterministic small-core box solver.

## 2. The algorithm and its sound certificates

Use exact conditional convex-cost flow at dyadic core corners, corrected by
`e_j=kLh_j^2/8`, and retain cells whose lower bound is at most the best
queried value. All original optimizer cores survive. The expected
near-optimal grid count is

```
Q=[3+(1+k/2)L/(2sigma)]^k                                 (3)
```

whenever `Mh_j>=1`, by the reviewed core search in the
[native-integer theorem](smoothed-native-integer-recourse.md). It uses only
core noise and the fixed residual domain. Let `D_j` be the retained hull.

At each level try the `3^k` original core faces compatible with `D_j`.
For a candidate face, project `D_j` onto it, choose the rational midpoint
`c`, and perform the exact tests in the
[deterministic face certificate](flow-optimal-face-certificate.md):

1. Solve conditional flow at `c`, find shortest-path polynomial potentials,
   and compute the exact optimal-flow intervals `I_a`.
2. Verify that every arc value in `I_a` remains tied on the projected hull.
   At most `d+1` integer representatives per arc suffice for the polynomial
   identity tests.
3. On that hull, test the first outside adjusted marginals against
   `rKT_1`, where `K` bounds core/arc mixed derivatives and `T_1` is the
   total normal width.
4. Minimize every inward derivative at `c` over the entire tightened flow
   set. With the notation of the certificate, require
   `beta-HR-(H/2)T_infty>0`.

For the face with no active coordinates, use the same interval identities
and first outside-marginal tests with threshold zero; there are no derivative
tests. These involve only original network arcs. Reduced costs of the
artificial source arcs are not tested. Original residual-arc nonnegativity
is sufficient for flow optimality. A passing test fixes the face for all global
optimizers in `D_j` and supplies a flow optimal at an original optimal core.
Solve its entire original core box exactly, using the
[constant-base polynomial solver](polynomial-component-primitive-limit.md),
and return. No step requires guessing the true face or assuming that a
selected flow is unique. Every successful test is sound on every draw.

The analysis below supplies a deterministic cutoff. Failure to pass by
that cutoff invokes the exact label-enumeration fallback. No actual
algorithm enumerates the flow charts used in the proof.

## 3. Face charts and their exceptional gradient images

For analysis only, consider every feasible integer flow `z`, every
structurally valid arborescence `T` of its augmented residual graph,
every original arc, and every
native adjacent pair `t,t+1` on that arc. The family includes trees whether
or not they occur as shortest-path trees at any core point. The polynomial potentials supplied
by `T` give the adjusted unit marginal

```
m_(z,T,a,t)(v)=f_a(v,t+1)-f_a(v,t)+pi_tail(v)-pi_head(v).
```

All polynomials have degree at most `d` and coefficient height at most a
base bound `H_0=poly_d(I)`. Tree paths have at most `s` arcs. Evaluation
at binary-encoded native labels and addition of polynomial coefficients
preserve this height bound. The number of polynomials is at most

```
N_chart=R_Z(2r+s)^s R_1,
R_Z=product_a(u_a-l_a+1),
R_1=sum_a(u_a-l_a+1).                                    (4)
```

This is a safe overcount; its logarithm is polynomial in `I`.

Fix an original core face `A` with `q>0` free coordinates. Restrict every
chart polynomial to that face, discard polynomial identities, and let `S_A`
be the union of their zero sets in its free unit cube. Nonzero constants
have empty zero sets. Then `S_A` is compact and has dimension at most `q-1`.
For a vertex face set `S_A` empty.

For each feasible flow `w`, let `F_{A,w}` be its unperturbed core slice on
the face. Define the cross-label exceptional set

```
E_A=union_(w in Y) [-grad F_(A,w)](S_A).                  (5)
```

It is compact of dimension at most `q-1`. The gradient label `w` need not
be the label defining the marginal polynomial. For one image piece the
formula has `q` free and `q` quantified variables, `O(q)` atoms, and fixed
degree. The same fixed-block elimination argument as in the interior
theorem encloses every `E_A` in a nonzero polynomial zero set of degree

```
D=max{1,R_Z N_chart E_d(k)^3},
E_d(k)=(k+1)^{O_d(k^2)}.                                 (6)
```

Only this degree bound is computed. No image polynomial, label list or
chart list is constructed. In particular `log D=poly_d(I)`.

Let `H>=1` bound all core Hessian norms. Suppose the global core optimizer
`a` belongs to the relative interior of face `A`. Every flow attaining its
conditional value makes its smooth fixed-flow slice globally minimal at
`a`. Thus its free gradient is `-gamma_A`, even if the lower envelope is
nonsmooth. Consequently

```
dist(gamma_A,E_A)<=H dist(a,S_A)                           (7)
```

when `S_A` is nonempty. The gradient uses only the free coordinates of
this face. There is no claim of stationarity in a normal direction.

The [finite-grid algebraic tube bound](core-noise-active-stratum-tube.md)
gives a simultaneous safe bound, for `k>=1`,

```
Pr{some positive-dimensional face A has
        dist(gamma_A,E_A)<=H delta}
 <=C_tot(H delta/sigma+k/M),
C_tot=3^k 16k^(k+1)D(4D+2)^(k-1).                        (8)
```

Each face uses its own independent free-coordinate noise marginal. A union
bound requires no independence between faces. Empty exceptional sets
contribute zero. The logarithm of `C_tot` is polynomial in `I`.

## 4. Normal margins without selecting or enumerating a label

For each fixed original face `A`, choose the lexicographically least
minimizer of its restricted value function. This analysis-only choice is
semialgebraic and measurable; it is not an extra output requirement on the
algorithm. It depends only on the free core noises:
the normal noises contribute constants on that face. At that core point,
take the minimum inward derivative over every attaining flow. For each
normal coordinate `i`, this derivative has the form

```
b_(A,i)+s_i gamma_i,
```

where `b_(A,i)` is independent of `gamma_i`, conditional on all other
noises. It includes the minimum over the full optimal flow set, so this
does not condition on an optimizer-selected label. The set is finite and
nonempty, even if the restricted core minimizer is nonunique.

The probability that this number belongs to `[0,tau]` is at most
`tau/sigma+1/M`. There are at most `N_normal=k3^k` face/normal pairs, hence

```
Pr{some such derivative is in [0,tau]}
 <=N_normal(tau/sigma+1/M).                              (9)
```

On a draw with a unique globally optimal core, the canonical optimizer of
its true face is that same core point: every minimizer of that face would
otherwise be another global optimizer. First-order optimality makes every
attaining flow's inward derivative nonnegative. Outside (9), their minimum
is therefore greater than `tau` in every active normal coordinate. No
residual perturbation is used.

## 5. Turning distance from a chart zero into a value margin

A value margin cannot be obtained from the geometric tube coefficient
alone. The following fixed-dimensional algebraic bound supplies it.

Let `p` be a rational degree-at-most-`d` polynomial on `[0,1]^q`, `q<=k`,
with coefficient height at most `H_0`, and let rational `delta>0`. Put

```
Z={x in [0,1]^q:p(x)=0},
K_delta={x in [0,1]^q:dist(x,Z)>=delta}.
```

If `Z` is empty, `K_delta` is the whole cube. If `K_delta` is nonempty,
compactness and `delta>0` give `m=min_(K_delta)|p|>0`. The scalar formula

```
exists x in [0,1]^q, for all y in [0,1]^q:
 (p(y)=0 implies ||x-y||^2>=delta^2),  0<p(x)^2<t          (10)
```

defines exactly `(m^2,infinity)`. It has two blocks of at most `k` variables,
one free scalar, fixed degree and `O(k)` atoms. Fixed-block rational
elimination therefore gives its boundary in polynomials with coefficient
height at most the following bound on their **integer coefficient bit
lengths after positive denominator clearing**:

```
B_0=E_d(k) poly_d(H_0+bits(delta)+1).                     (11)
```

The endpoint `m^2` is a root of a nonzero nonconstant output atom; otherwise
all signs would remain constant near it. After factoring out a power of
`t`, the reciprocal Cauchy bound gives `m^2>=2^{-(B_0+1)}`. Thus the coarser
dyadic lower bound `m>=2^{-(B_0+1)}` is safe. Empty `K_delta` is vacuous;
constant nonzero polynomials and `q=0` have the direct rational bound.
Zero polynomials were already excluded from the chart family.

This gives one base-computable `mu_0>0`, valid for every nonzero face chart
polynomial at distance at least `delta/2` from its zeros, with

```
log(1/mu_0)<=f_d(k) poly_d(I+bits(delta)).                 (12)
```

This bound is independent of which chart is selected after sampling. Its
encoding may have `f_d(k) poly(I)` bits. Claiming only polynomial-in-`I`
precision here would omit a material dimension dependence.

## 6. One finite law and termination

Use the projected core-growth tail from the interior theorem:

```
Pr{g_C<epsilon}<=k epsilon/sigma+2k C_growth/M,
log C_growth=poly_d(I).                                  (13)
```

The growth distance is only in the core. Persistent tied flows do not force
it to vanish. Its finite-grid section bound uses two quantified blocks;
native integer disjunctions have exponential size but polynomial logarithmic
length, which remains within the singly exponential section bound.

Let `B>=2` be the base exponential factor in the all-draw label-enumeration
fallback. Its cost is `B(I+log M+1)^{e_d}`, with fixed exponent `e_d`, and
`log B=poly_d(I)`. Define before sampling

```
rho=1/(8B),
g_0=rho sigma/(2k),       A_0=2+kL/g_0,
delta=min{1/4,rho sigma/(4 C_tot H)},
tau=rho sigma/(4 N_normal).
```

Compute the universal `mu_0` from (12). Let `J` be the least dyadic level
with

```
h_J<=min{ delta/(4kA_0),
          tau/(16kH A_0),
          mu_0/[4k max{1,rK} A_0] }.                    (14)
```

Choose the least power of two

```
M>=max{2,2^J,4k C_growth/rho,
                 4k C_tot/rho,4N_normal/rho}.            (15)
```

Here `K` is the core/arc derivative bound in the deterministic certificate.
All quantities are base-only. Equations (11)--(15) give
`J,log M<=f_d(k) poly_d(I)`, with no circular dependence on sampled heights.
The growth failure probability is at most `rho`. The tube and normal-margin
failure probabilities are each at most `rho/2`. Total failure is at most
`2rho=1/(4B)`.

On a complementary draw, let `a` be the unique optimal core and `A` its
true face. The retained hull is within infinity distance `A_0h_j` of `a`.
This follows from the near-optimal corner witness and growth, and the stated
constant is a conservative bound. Its projected hull and midpoint `c`
are within Euclidean distance `kA_0h_j` of `a`. The tube event gives
`dist(a,S_A)>delta` when the set is nonempty, so at level `J` the entire
projected hull is at least `delta/2` from every chart zero.

Take the conditional optimum and shortest-path tree computed at `c`.
Every within-interval unit marginal is zero at `c`. Because `c` avoids all
nonidentity chart zeros, these marginals are polynomial identities on the
face. Every first outside marginal is positive at `c`, hence positive on
the connected projected hull, and by (12) at least `mu_0`. Thus the same
intervals describe **all** optimal flows at `c`, at `a`, and throughout that
hull. This also proves the exact identity tests pass.

Every true normal derivative minimum at `a` exceeds `tau`. The common
optimal-flow set and the Hessian bound imply

```
beta_i(c)>tau-HkA_0h_J.
```

For the deterministic certificate, `R<=2kA_0h_J`,
`T_infty<=A_0h_J`, and `T_1<=kA_0h_J`. Equation (14) therefore gives

```
beta-HR-(H/2)T_infty>tau/2,
rKT_1<=mu_0/4.
```

All required tests pass on the true face. On an interior true face, the
same chart argument supplies the uniform-flow certificate without normal
tests. On a vertex face, chart polynomials are constants; the direct
rational margin bound and normal tests apply. These cases exhaust all
possible core optima.

## 7. Bit work, output, and limits

The sampler uses `k log M<=f_d(k) poly(I)` bits. All query points, integral
flows, coefficients, potentials and derivative costs through level `J`
have `f_d(k) poly(I)` bits. Exact convex-cost flow retains a fixed polynomial
input exponent. At most `3^k` face attempts per level use polynomially many
such flow calls, polynomial identities, and `c_d^k`-cost polynomial minima
on rational core boxes. Their total is `f_d(k) poly(I)`.

The expected corner count (3), its `8^k` generation factor, the number of
levels, and the query-bit cost combine to give (2). The expected fallback
cost is polynomial in `I+log M`, hence `f_d(k) poly(I)`, because its
exponential base factor is multiplied by a probability at most `1/(4B)`.
It uses the same draw and returns one winning small-core representation.
The final fixed-flow solve and its refinement use the reviewed constant-base
box solver. No representation must retain all examined labels or their
joint number field.

The result concerns separable convex integer-flow recourse with core-only
cost dependence. It does not cover arbitrary coupled integer recourse,
nonconvex arc costs, or core-dependent flow supplies. The coefficient height
and dimension dependence of (12) is explicit; this proof does not assert
the sharper literal interior bound. The single-flow boundary obstruction
remains valid for that narrower certificate, and is resolved here by a
different certificate over the full optimal-flow intervals.

The [focused prior comparison](../prior-art/smoothed-boundary-core-flow-prior.md)
credits the classical exact-flow, potential and parametric-optimization
ingredients. It distinguishes complete parametric-envelope enumeration
from the point-query and local-certificate method here. The comparison
does not establish publication novelty.

## Verification

The [deterministic face certificate](flow-optimal-face-certificate.md) has
passed fresh review and distinct author-side and reviewer exact diagnostics.
They cover optimal-flow intervals, the sharp proximity factor, two-point
derivative interpolation, the boundary obstruction and a necessary losing-flow
guard. The complete probabilistic composition passed the
[fresh full review](../reviews/smoothed-boundary-core-flow-adversary.md),
and a separate [arithmetic audit](../reviews/boundary-core-flow-bit-adversary.md)
checked the actual value-margin proof, sample-bit dependence, fallback and
all-draw output. A [focused bit audit](../reviews/flow-boundary-margin-review.md)
has approved the two-block value-margin argument, including empty zero
sets, strict scalar thresholds and reciprocal Cauchy bounds. Topic-scoped
document, local-link, checker-syntax and whitespace checks passed. No
index edits, project-wide verification or CI inspection were performed.

The author-side end-to-end diagnostic was run with

```sh
python3 -B research-20261002/new-direction/check_boundary_core_flow_search.py
```

The [exact two-arc search checker](check_boundary_core_flow_search.py) tested
all 64 atoms of an eight-point noise law in two core dimensions. Sixty
draws closed through boundary-face certificates, including 16 closures
using both tied flows and 44 with a singleton face-optimal flow. The four
negative diagonal atoms have two distinct global core optima; they correctly
used an exact same-draw two-label fallback at the diagnostic's cutoff.

Checks covered 1,815 conditional core evaluations, 1,428 corrected cells,
237 search levels, 2,133 face patterns, 1,099 exact potential/interval
checks, 120 exact minima of accepted face inequalities and 60 fixed-flow
whole-core completions. Every retained hull contained all independently
computed optimal cores, and every cell bound was compared with its exact
cell minimum. The diagnostic deliberately did not use the all-free
uniform-flow shortcut, to exercise the boundary certificates. It is specific
to this two-label quadratic example; it does not implement a general flow
oracle, general algebraic solver or the theorem's much larger finite-law
budget. These counts are separate from the reviewer's static-certificate
diagnostic and analytical probability checks.
