# Error bounds transfer feasible growth to spatial lower bounds

Date: 2026-09-22. Status: independent derivation and literature assessment by
the `error_bound_transfer` research agent; independently checked in the
[adversarial review](review-20260922-error-bound-transfer.md). Internal agent
review is not external peer review.
This note does not modify the existing cluster result. Its principal finding
is a simplification and a novelty correction: the required off-feasible growth
inequality is already part of classical exact-penalty theory.

## 1. What the argument establishes

Let `F` be the feasible set and `S` a compact set of minimizers with common
value `f*`. A local constraint error bound and quadratic growth of `f` on `F`
give

```
f(z) >= f* + a dist(z,S)^2 - b v(z),                                  (1)
```

where `v` measures constraint violation. Substituting the `O(w^2)` violation
and objective errors of a spatial relaxation gives

```
L(Z) >= f* + a dist(Z,S)^2 - C w(Z)^2.                                (2)
```

The projection in this proof is onto `F`, not onto `F intersect Z`. Thus a
box can be infeasible, and the projection can leave the box. This distinction
is precisely why (2) can hold even when the gap between the relaxation value
and the feasible minimum *inside that box* is only first order.

For isolated minimizers, (2) bounds the number of unfathomed, disjoint,
shape-regular boxes at each scale by a constant. For a minimizer manifold of
dimension `s`, the corresponding upper bound is `O(delta^(-s))`. The latter
growth reflects the size of the solution set and is not removed by the
quadratic estimate. These are counts at a fixed scale, not runtime bounds.

## 2. Precise transfer theorem

All distances and Lipschitz constants below use the Euclidean norm. Write
`N_r(S) = {z: dist(z,S) <= r}`. Let `F` be a nonempty closed subset of `R^n`,
let `S` be a nonempty compact subset of `F`, and fix `rho > 0`. Assume:

1. `f` is `L_f`-Lipschitz on `N_(2rho)(S)`.
2. For every `y in F intersect N_(2rho)(S)`,
   `f(y) >= f* + a dist(y,S)^2`, where `a > 0`, and `f=f*` on `S`.
3. There is a nonnegative residual `v` such that
   `dist(z,F) <= kappa v(z)` for every `z in N_rho(S)`.

**Theorem 1.** For every `z in N_rho(S)`,

```
f(z) >= f* + a dist(z,S)^2 - kappa (L_f + 3 a rho) v(z).               (3)
```

**Proof.** Closedness and finite dimensionality give a nearest point
`y in F` to `z`. Set `e=|z-y|`, `d=dist(z,S)`, and `d_y=dist(y,S)`.
Since `S subset F`, `e <= d <= rho`; the triangle inequality gives
`d_y <= d+e <= 2rho`. Both points therefore belong to the Lipschitz
neighborhood, and the growth assumption applies at `y`. The distance
function is 1-Lipschitz, so

```
d_y^2 >= d^2 - |d_y-d| (d_y+d) >= d^2 - 3 rho e.
```

Consequently

```
f(z) >= f(y)-L_f e
     >= f*+a d_y^2-L_f e
     >= f*+a d^2-(L_f+3a rho)e.
```

Apply `e <= kappa v(z)`. No uniqueness or regularity of the projection is
needed. The original coefficient `a` is retained. □

The Lipschitz assumption is automatic after shrinking the neighborhood when
`f` is continuously differentiable near compact `S`: finitely many local
neighborhoods control nearby pairs, while boundedness controls pairs at a
fixed positive separation. Alternatively a gradient bound on a larger
convex neighborhood is sufficient.

**Corollary 1 (spatial lower bound).** Boxes are closed bounded rectangles,
and `w(Z)` is their largest side length. For every box `Z subset N_rho(S)`,
suppose a relaxation has feasible set `R(Z) subset Z`, objective `f_Z`, and

```
v(z) <= tau_c w(Z)^2,             z in R(Z),
f_Z(z) >= f(z)-tau_f w(Z)^2,      z in R(Z),
```

with constants independent of `Z`. Define
`L(Z)=inf_{z in R(Z)} f_Z(z)`, with the infimum of the empty set `+infinity`.
Then (2) holds with

```
C = tau_f + kappa (L_f+3a rho) tau_c.
```

**Proof.** Substitute the residual and objective errors into (3), then take
the infimum. Convexity and attainment of the relaxation are unnecessary for
this implication. □

For a smooth nonlinear program the usual choice is

```
v(z)=max(0, max_j g_j(z), max_k |h_k(z)|).
```

Second-order pointwise underestimators of inequalities and two-sided
relaxations of equalities give the required residual bound. If `F` includes
the original search-domain bounds, those bounds must be included in the
error-bound system or retained as an exact ambient restriction throughout.
An error bound for a different feasible set does not suffice.

## 3. Regularity assumptions and comparison with the old theorem

MFCQ at an isolated minimizer implies a local linear error bound. MFCQ at
every point of compact `S` implies one uniform bound on a sufficiently small
neighborhood, by a finite covering argument. MFCQ is sufficient, not
necessary: the relevant property is metric subregularity of the constraint
system at right-hand side zero. Affine systems have such bounds even when
their given description violates MFCQ. See Solodov, Section 3, equation
(25), and the underlying Robinson theory in Section 8 below.

For an isolated solution `z*`, ordinary SOSC on the **actual critical cone**,
together with a KKT multiplier, implies feasible quadratic growth. Strict
complementarity is not needed. To recall the elementary argument, suppose
there were feasible `y_i -> z*`, with `t_i=|y_i-z*|>0`, such that the growth
ratio is below some `a<gamma/2`, where the Lagrangian Hessian is at least
`gamma` on unit critical directions. Pass to a limit of
`d_i=(y_i-z*)/t_i`. First-order feasibility and KKT imply `d` is critical:
the objective's first derivative along `d` is at most zero by the bounded
growth ratio and at least zero by KKT. Feasibility also gives
`f(y_i)-f* >= Lagrangian(y_i)-Lagrangian(z*)`. Stationarity and the
second-order expansion then give a limiting ratio at least `gamma/2`, a
contradiction. This proof uses a fixed multiplier whose Hessian is positive
on the critical cone.

Thus the named LICQ/strict-complementarity/SOSC version of the existing
[cluster theorem](../results/cluster-free-branch-and-bound-constrained-minima.md)
is an immediate special case of Corollary 1. One can replace LICQ by MFCQ,
remove strict complementarity, and allow nonisolated solution sets provided
quadratic growth relative to the whole set is assumed or separately proved.

**Example outside the old named assumptions.** Minimize
`f(x,y)=x^2+y^2+4xy` subject to `-x<=0`, `-2x<=0`, `-y<=0` near the origin.
The origin is the unique minimizer; on the feasible orthant,
`f>=x^2+y^2`. The duplicated constraint violates LICQ, all KKT multipliers
are zero, and strict complementarity fails. MFCQ holds with direction
`(1,1)`. The Hessian has eigenvalues `6,-2`, so positivity on the full
space annihilating the strongly active gradients also fails. Corollary 1
still applies to any scheme satisfying its second-order error bounds.

There is an important qualification: the old proof's remark also permits
some degenerate systems without LICQ or any linear feasibility error bound.
The new *error-bound* hypothesis does not automatically subsume every such
variant. For example, `min -x^2` subject to `x^2<=0` has `F={0}` and no
linear residual error bound, but the exact penalty
`-x^2+2(x^2)_+=x^2` has quadratic growth. The more general exact-penalty
formulation in the next section includes this example directly.

## 4. The natural assumption is quadratic growth of an exact penalty

One can start with the property

```
f(z)+b v(z) >= f*+a dist(z,S)^2                                    (PG)
```

on a neighborhood. Theorem 1 is one sufficient condition for (PG), but
(PG) itself plus second-order residual/objective errors gives (2), with
`C=tau_f+b tau_c`, in one line. The previous section's singular example
shows that (PG) can hold even when a linear feasibility error bound fails.

This is not a new growth principle. Applying the classical distance exact
penalty argument to `f(z)-a dist(z,S)^2` proves it under the hypotheses of
Theorem 1. More directly, Anitescu's open preprint states the isolated-point
inequality (PG), for both infinity- and one-norm residual penalties, as
equations (1.18)–(1.19), citing Bonnans–Shapiro, Theorem 3.113. Its sufficient
assumptions are a nonempty KKT multiplier set and generalized quadratic
growth `max{f(z)-f*,v(z)} >= sigma |z-z*|^2`. Under MFCQ it identifies this
growth condition with feasible quadratic growth. See Section 8 for precise
access and attribution limits.

Accordingly, an honest significance assessment is that the old distance
bound is a routine application of known exact-penalty growth once the
correct comparison value `f*` is selected. The box-counting consequence
and the distinction from convergence toward a box's own feasible optimum
may be useful clarification for spatial branch-and-bound, but neither
supports a claim of a substantial new optimality or error-bound theorem.
The present search has not established whether this exact branch-and-bound
application has already appeared.

## 5. A precise count for nonisolated minimizers

For `t>0`, let `N(S,t)` be the minimum number of Euclidean balls of radius
`t`, with centers in `S`, covering `S`. Suppose (2) holds with `a,C>0`.
Consider boxes contained in its neighborhood, with pairwise disjoint
interiors and every side length in `[delta/2,delta]`. With exact incumbent
`f*`, call a box unfathomed when `L(Z)<f*-eps`, where `eps>=0`.

**Theorem 2.** The number of these boxes is at most

```
N(S,delta) [4(sqrt(C/a)+1+sqrt(n))]^n.                              (4)
```

If `eps>0` and `C delta^2<=eps`, there are none.

**Proof.** An unfathomed box satisfies
`a dist(Z,S)^2 < C delta^2-eps <= C delta^2`. Choose a closest pair
`z in Z`, `s in S`. Choose a covering center `s_j` with `|s-s_j|<=delta`.
Every point of the box is within
`(sqrt(C/a)+1+sqrt(n))delta` of `s_j`. Assign each box to one such center.
The boxes in each assigned class fit inside a cube of side
`2(sqrt(C/a)+1+sqrt(n))delta`; their disjoint interiors and volume at least
`(delta/2)^n` give the claimed count. The positive-tolerance assertion
follows directly from the strict inequality. □

If `N(S,t)<=A t^(-s)` for small `t`, then the count is `O(delta^(-s))`.
Compact `C^1` embedded `s`-manifolds have such a bound using finitely many
bounded Lipschitz coordinate charts. A finite set gives `O(1)`.
Mere knowledge of the upper Minkowski dimension `s` does **not** imply
`N(S,t)=O(t^(-s))`; it only implies the bound with every exponent greater
than `s`, unless finite upper Minkowski content or another explicit
covering estimate is known.

The exponent cannot generally be improved from the assumptions alone.
On `[0,1]^s x [-1,1]^(n-s)`, take
`f(u,v)=|v|^2` and `S=[0,1]^s x {0}`. The convex underestimate
`f_Z=f-tau w(Z)^2` is valid and has second-order error. A grid contains
order `delta^(-s)` boxes of width `delta` meeting `S`, each with lower
bound `-tau delta^2`. All remain unfathomed when
`eps<tau delta^2`. This is an assumption-level example using an
intentionally loose underestimate; it does not assert unavoidable
clustering for tight convex relaxations or solvers.

## 6. Failure modes and a general exponent calculation

**Feasible growth alone is insufficient.** Minimize `f(x,y)=y^2-x`
subject to `g(x,y)=x^2<=0`. Then `F={0} x R`, `S={(0,0)}`, and feasible
quadratic growth holds with coefficient 1. The residual has only a
square-root error bound: `dist((x,y),F)=sqrt(g(x,y))`. For
`Z=[0,w] x [-w/2,w/2]`, use the valid convex underestimate
`g_Z=x^2-w^2/16` and keep the convex objective exact. The point
`(w/4,0)` is relaxed feasible and has value `-w/4`. Therefore no uniform
bound `L(Z)>=-Cw^2` can hold. Both relaxation errors are at most second
order. This counterexample isolates the missing feasibility regularity;
it again uses a deliberately loose constraint underestimate.

**Hölder error bounds.** Retain the closedness, compactness, neighborhood,
and Lipschitz assumptions of Theorem 1. Suppose feasible growth has exponent `q>=1`,
`f(y)>=f*+a dist(y,S)^q`, and
`dist(z,F)<=kappa v(z)^theta`, with `0<theta<=1`. On `[0,2rho]`, the
map `t -> a t^q` is Lipschitz with constant
`L_q=a q (2rho)^(q-1)`. The same projection argument yields

```
f_Z(z) >= f*+a dist(z,S)^q
          -tau_f w^beta_f -(L_f+L_q) kappa tau_c^theta w^(beta_c theta)
```

when residual and objective errors have orders `beta_c,beta_f>0`.
For `w<=1`, put `r=min(beta_f,beta_c theta)`. This gives
`L(Z)>=f*+a dist(Z,S)^q-Cw^r`. If `N(S,t)<=A t^(-s)`, the covering
argument now gives

```
O(delta^(-n+(r/q)(n-s)))     when r<=q,
O(delta^(-s))               when r>=q.                              (5)
```

Indeed the distance to `S` is `O(delta^(r/q))`; cover `S` at that radius
when it is at least `delta`, and at radius `delta` otherwise. Pack boxes
of volume at least `(delta/2)^n` in the resulting enlarged balls.
These are conservative upper bounds, not universal matching lower bounds.
They show exactly where a weak feasibility error exponent can defeat a
second-order relaxation. This exponent calculation is elementary and is
not presented as a separate research breakthrough.

**Other limits.** Constants and radii are local and may be poor. The
proof supplies no practical procedure to certify them. An incumbent
`f*+eta` changes the threshold to `eps-eta`; a uniform count as in (4)
requires `eta<=eps`, and guaranteed small-box fathoming requires
`eta<eps`. Anisotropic boxes with arbitrarily small volume relative to
their largest width do not satisfy this packing argument. A fixed
integer assignment can be analyzed as a continuous subproblem, but these
theorems do not control the number of integer assignments or the global
search outside the stated neighborhood.

## 7. Verification and research decision

The proof was checked directly through a nearest-feasible-point argument;
all neighborhood, attainment, and distance inequalities are displayed.
The counterexamples and the Hessian eigenvalues above are exact algebraic
calculations. Targeted command `python -` with an inline `fractions.Fraction`
script passed 24 dyadic-width checks of the singular-relaxation example,
exact determinant checks of the eigenvalues `6,-2`, a finite rational mesh
check of the squared-distance inequality at its boundary cases, and a
Markdown-fence balance check. These finite checks do not prove the general
inequality or asymptotic claims; their displayed proofs do that work.
`git diff --check -- notes/research-20260922-error-bound-transfer.md` also
returned success, but the file was untracked at the time, so that command
did not validate its content. A separate inline `python -` check read the
file and verified absence of trailing whitespace and conflict markers.
No floating-point solver evidence, Lean proof,
CI check, or project-wide check is used. The independent adversarial review
confirmed the proofs and prior-work comparison. Its minor scope
clarifications are incorporated above.

The most useful immediate change is to replace the elaborate proof under
LICQ and strict complementarity by the penalty-growth viewpoint, while
retaining its counterexample separating global fathoming from local box
convergence. The stronger assumptions should not continue to be portrayed
as essential. Conversely, the simpler proof lowers rather than raises the
novelty assessment: this direction needs an additional substantive idea
before it meets the user's objective of a major original contribution.

Potentially consequential unresolved questions include certified estimates
of penalty-growth constants from solver information, useful analyses when
linear error bounds fail, and reduced-space relaxations where error is
controlled by the relevant variable widths even though some coordinates
remain wide. None is resolved merely by the transfer theorem.

## 8. Literature examined and attribution limits

- **Mihai Anitescu (2005),** *On Using the Elastic Mode in Nonlinear
  Programming Approaches to Mathematical Programs with Complementarity
  Constraints*, SIAM J. Optim. 15(4):1203–1236,
  [published record](https://doi.org/10.1137/S1052623402401221),
  [open author preprint](https://optimization-online.org/wp-content/uploads/2004/08/918.pdf).
  Inspected Sections 1.2–1.3, preprint page 6, equations (1.16)–(1.19).
  This is the decisive prior statement: quadratic growth of exact
  penalties off the feasible set, under generalized quadratic growth and
  existence of KKT multipliers. It cites **Bonnans and Shapiro (2000),
  *Perturbation Analysis of Optimization Problems*, Theorem 3.113**.
  The book theorem was not directly inspected; the attribution and the
  exact inequality were checked in Anitescu's open paper. No claim about
  the full scope of the book theorem is made beyond this citation.
- **Mikhail V. Solodov (2010),** *Constraint Qualifications*,
  [author PDF](https://pages.cs.wisc.edu/~solodov/mvs10eORMS-CQs.pdf),
  Section 3, equation (25). Inspected the local constraint error bound,
  its validity under MFCQ and weaker qualifications, and the distinction
  between metric subregularity and metric regularity. This is an
  author-written survey, not the original proof of the MFCQ implication.
  The classical original reference is **Stephen M. Robinson (1976),**
  *Stability Theory for Systems of Inequalities, Part II: Differentiable
  Nonlinear Systems*, SIAM J. Numer. Anal. 13(4):497–513,
  [publisher record](https://doi.org/10.1137/0713043); only its abstract
  and bibliographic record were inspected in this pass.
- **Jane J. Ye (2012),** *The exact penalty principle*, Nonlinear Analysis
  75(3):1642–1654,
  [publisher text](https://doi.org/10.1016/j.na.2011.03.025).
  Inspected the introduction's statements of Clarke's distance exact
  penalty principle and its refinement. The author-preprint URL appeared
  in search results but returned 404 on direct retrieval. The projection
  argument in Section 2 is the elementary finite-dimensional instance of
  this established principle applied after subtracting the growth term.
- **J. Frédéric Bonnans and Alexander Ioffe (1995),** *Second-order
  Sufficiency and Quadratic Growth for Nonisolated Minima*, Mathematics
  of Operations Research 20(4):801–817,
  [publisher abstract](https://doi.org/10.1287/moor.20.4.801).
  The inspected abstract explicitly concerns nonisolated minimizer sets.
  Its full theorem statements were not obtained here, so this note does
  not claim a new characterization of quadratic growth on manifolds or
  exact equivalence to that paper's conditions.
- **Rohit Kannan (2018),** *Algorithms, analysis and software for the global
  optimization of two-stage stochastic programs*,
  [open thesis](https://rohitkannan.github.io/PDFs/Kannan_MIT_PhDThesis.pdf).
  Read the locally available text `/tmp/kb/kannan_thesis.txt`, notably
  Lemma 5.3.17 and the Chapter 6 conclusion. Chapters 5 and 6 reproduce
  the Kannan–Barton cluster and convergence-order analyses cited in the
  existing result. Their comparison target is the feasible minimum
  inside a box; our application of known penalty growth compares against
  `f*`. Their terminology “nonisolated” can mean a minimizer that is a
  nonisolated **feasible point**, not a nonisolated point of the minimizer
  set; these must not be conflated.

Searches also combined “cluster problem” with “error bound”, “metric”,
and “exact penalty”, and combined “branch-and-bound” with “quadratic
growth” and “penalty”. No directly matching branch-and-bound theorem was
located in this pass. The positive exact-penalty match is stronger evidence
about the core argument's lack of novelty than these unsuccessful searches
are evidence about novelty of its application.
