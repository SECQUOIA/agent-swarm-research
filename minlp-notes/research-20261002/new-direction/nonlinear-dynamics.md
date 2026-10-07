# Regridded certificates for stable nonlinear dynamics

Date: 2026-10-02. Status: complete proof with a fresh independent
adversarial review. No novelty claim or literature assessment.

The [regridded-certificate algorithm](../regridded-certificates/note.md)
extends to stable scalar nonlinear state dynamics. Each local optimization
problem remains convex: it enforces an affine outer strip around the
nonlinear graph on the current leaf. A forward simulation repairs the
resulting trajectory. Backward adjoints choose the separator slopes and
cancel its entire first-order repair cost, even though the repair itself
is nonlinear.

For fixed conditioning and derivative bounds, the final certificate has
`O(T log(T/eps))` leaves and separator cells for a horizon of length `T`.
The algorithm creates `O(T log^2(T/eps))` boxes and uses
`O(T log^3(T/eps))` exact convex-optimization oracle calls, each in at most
three variables. These are counts in an exact-real oracle model, not bit
complexity or claims about the lengths of explicit feasible trajectories.

## 1. Model and assumptions

There are continuous states `s_0,...,s_T` and controls
`u_0,...,u_(T-1)`, with `T>=1`. Their domain `X` is a product of compact
nondegenerate intervals `I_t` and `U_t`. Let `s0>0` denote its largest
side length; the symbol `s0` in constant formulas is not the state `s_0`.
Impose the equalities

```
q_t(s_t,u_t,s_(t+1)) = s_(t+1)-phi_t(s_t,u_t) = 0,
t=0,...,T-1.
```

Assume `phi_t` is continuously differentiable on a neighborhood of its
input rectangle, and, uniformly in `t`,

```
phi_t(I_t x U_t) subset I_(t+1),
|partial_s phi_t| <= a < 1,
|partial_u phi_t| <= b,
Lip(grad phi_t) <= H.
```

All Lipschitz constants use the Euclidean norm. A twice continuously
differentiable map with `||Hess phi_t||_2<=H` satisfies the last condition.
The box-invariance condition is a promise on the model. Forward simulation
then provides a feasible trajectory from every choice of initial state
and controls in their intervals. There are no additional state, terminal,
or control constraints beyond the displayed intervals and equalities.

Use the path decomposition, rooted at bag zero,

```
V_t = {s_t,u_t,s_(t+1)},
S_t = {s_t}              (t=1,...,T-1).
```

Assign `q_t` and a bag objective `a_t` to `V_t`, and write
`F=sum_t a_t`. Thus `N=T`, `p=3`, `w=2`, and the occurrence bound is
`k<=2`. In all constant formulas one may take `k=2`, including `T=1`.
More than one objective factor may be assigned to a bag; their evaluation
cost is not bounded merely by the number of bags.

Assume the objective conditions of the regridding note:

- Every `a_t` has an `M`-Lipschitz gradient on its box.
- On every leaf `B`, the supplied continuous convex objective lower
  model `a_(t,B)` satisfies
  `0<=a_t(z)-a_(t,B)(z)<=A0 width(B)^2/4` for all `z in B`.
- On the true feasible set `P={x in X:q(x)=0}`, there is a minimizer
  `x*` and a constant `g>0` such that
  `F(y)-F(x*)>=g||y-x*||_2^2` for every `y in P`.
- For every feasible center `c` and `j=1,...,T`,
  `|partial_(s_j) F(c)|<=G`.

The last assumption bounds an objective first derivative, not merely
curvature. For a fixed compact instance such a finite bound exists by
continuity. A horizon-independent result needs a horizon-independent
bound. For example, if each bag gradient component has magnitude at most
`G_b`, one may take `G=2G_b` because a state occurs in at most two bags.
The explicit example in Section 8 has the sharper value `G=2`.

The lower-model assumption is only the displayed width-squared error
bound. The original factorwise vertex-vanishing condition implies it,
but vertex or endpoint exactness is not required anywhere in this proof.
Thus continuous convex Taylor lower models satisfying this weaker
contract are also allowed.

Only feasible quadratic growth is required. The minimizer may be on the
boundary, and the objective need not be stationary there. The derivative
and relaxation bounds hold on the full boxes, including infeasible points.

## 2. Convex outer strips for the nonlinear graph

Let `B` be a bag leaf, `w_B=width(B)`, and let `m_B` be the midpoint of
its projection onto `(s_t,u_t)`. Set

```
ell_(t,B)(s,u) = phi_t(m_B) + grad phi_t(m_B) dot ((s,u)-m_B),
tau_B = H w_B^2/4,
O_t(B) = {z in B: |z_(s_(t+1))-ell_(t,B)(z_s,z_u)|<=tau_B}.
```

This is a compact convex polytope, possibly empty. Taylor's bound and
the two input-coordinate widths give

```
|phi_t(s,u)-ell_(t,B)(s,u)|
  <= (H/2)||(s,u)-m_B||_2^2 <= H w_B^2/4.
```

Consequently, `O_t(B)` contains every true graph point in `B`. Moreover,
every `z in O_t(B)` satisfies

```
|q_t(z)| <= K w_B^2,             K=H/2.           (2.1)
```

If `H=0`, the strip is the exact affine graph. Different leaves may use
different affine strips. They need not agree on shared faces; each
contains all true graph points on its own leaf, which is all that
certificate validity needs.

The local oracle minimizes the original convex objective lower model
plus the affine separator terms over `O_t(B)` intersected with the bag's
own separator cell. Thus it solves a convex problem with affine
constraints. No oracle is asked to optimize on a nonlinear graph, and no
convex relaxation of the multiplier-adjusted objective is needed.

The strip construction requires a valid supplied curvature bound `H`
(or an oracle supplying a certified affine enclosure). Unlike a constant
used only in a termination proof, this bound affects certificate
soundness. Dovetailing smaller grading ratios cannot make certificates
built with an underestimated `H` valid.

## 3. Adjoints and exact cancellation

At a feasible center `c`, let

```
d_j = partial_(s_j) F(c),
A_t = partial_s phi_t(c_(s_t),c_(u_t)),
mu_(T-1) = -d_T,
mu_(t-1) = A_t mu_t-d_t       (t=T-1,...,1).
```

Then, with `U=G/(1-a)`,

```
|mu_t| <= G sum_(r=0)^(T-1-t) a^r <= U.          (3.1)
```

Freeze these multipliers for the current stage and define

```
A_t^c(z) = a_t(z)+mu_t q_t(z),
G_c(x) = sum_t A_t^c(x_Vt),
Mbar = M+UH.
```

Each adjusted bag gradient is `Mbar`-Lipschitz. The recurrence gives

```
partial_(s_j) G_c(c) = 0        (j=1,...,T).     (3.2)
```

Use subtree slopes formed from the adjusted bag gradients
`grad A_t^c(c_Vt)`. On this path, the separator variable `s_t` occurs
only in bag `t` within its subtree, so the slope has the simple form

```
lambda_t(c) = partial_(s_t) a_t(c_Vt)
              -mu_t partial_s phi_t(c_(s_t),c_(u_t)),
t=1,...,T-1.
```

The forward repair `y=R(x)` leaves `s_0` and every control fixed and
recomputes `y_(s_(t+1))=phi_t(y_(s_t),x_(u_t))`. It maps `X` into `P`
and fixes every point of `P`. Its displacement is supported only on
`s_1,...,s_T`. Therefore (3.2) gives the exact identity

```
grad G_c(c) dot (x-R(x)) = 0.                    (3.3)
```

No linearity or differentiability of `R` is needed for (3.3). This is
the distinction from the affine-retraction proof: the adjusted gradient
annihilates a fixed coordinate subspace containing every repair
displacement. It need not annihilate only a tangent space at the center.

## 4. Feasible repair and aggregate drift

For an arbitrary `x in X`, write `e_t=R(x)_(s_t)-x_(s_t)` and
`r_t=q_t(x_Vt)`. Then `e_0=0` and

```
|e_(t+1)| <= a |e_t|+|r_t|.
```

The finite geometric convolution has Euclidean operator norm at most
`1/(1-a)`. For completeness, extend the residual magnitudes by zero;
each lag shift has Euclidean norm at most one, so the triangle
inequality gives the sum `1+a+a^2+...`. Thus

```
||R(x)-x||_2 <= ||q(x)||_2/(1-a).                (4.1)
```

Now consider a finite configuration returned by the constrained dynamic
program. Its bag points are `z^t in O_t(B_t)`. Form its consistent
top-copy point `x`, as in the regridding note, and let `y=R(x)`. Define

```
b_t = width(B_t),        d_t = width(D_t) (t!=0),
Q = sum_t b_t^2 + sum_(t!=0) d_t^2,
E_x = sum_t ||z^t-x_Vt||_2^2,
E_y = sum_t ||z^t-y_Vt||_2^2,
C0 = k(k-1)p,
Lq = sqrt(1+a^2+b^2).
```

The original copy-drift lemma depends only on box incidences and gives
`E_x<=C0 Q`. Also `q_t` is `Lq`-Lipschitz on its full bag box. By (2.1),
the triangle inequality, and `b_t<=s0`,

```
||q(x)||_2
 <= Lq sqrt(E_x)+K sqrt(sum_t b_t^4)
 <= (Lq sqrt(C0)+K s0) sqrt(Q).
```

Set

```
rho = (Lq sqrt(C0)+K s0)/(1-a),
D = (sqrt(C0)+sqrt(k) rho)^2.
```

Equation (4.1) gives `||y-x||_2<=rho sqrt(Q)`. Stacking the bag copies
and using coordinate multiplicity then gives

```
sqrt(E_y) <= sqrt(E_x)+sqrt(k)||y-x||_2,
E_y <= D Q.                                      (4.2)
```

The term `K s0` is necessary in this estimate: even with one bag and
no copy mismatch, its relaxed graph point may need repair.

## 5. The configuration identity and error estimate

Let `Phi` be the configuration value with the original objective lower
models and the adjusted slopes. Write
`err_t=a_t(z^t)-a_(t,B_t)(z^t)`. The subtree-gradient telescoping identity
first gives

```
Phi = sum_t a_t(z^t)-sum_t err_t
       -sum_t grad A_t^c(c_Vt) dot (z^t-x_Vt).
```

By (3.3), replacing `x` by `y` in the last sum changes nothing. Since
`q_t(y_Vt)=0`, the exact resulting identity is

```
Phi = F(y)+sum_t T_t-sum_t err_t-sum_t mu_t q_t(z^t),
T_t = A_t^c(z^t)-A_t^c(y_Vt)
      -grad A_t^c(c_Vt) dot (z^t-y_Vt).           (5.1)
```

The final residual term is present because local copies satisfy outer
strips rather than the true nonlinear equality. Its absolute value is
at most `UK sum_t b_t^2<=UK Q`.

Let `r=||y-c||_2` and set

```
B0 = Mbar D/2+A0/4+UK.
```

The Lipschitz-gradient remainder bound, Cauchy--Schwarz, and (4.2)
give

```
|F(y)-Phi|
 <= Mbar sqrt(k) r sqrt(E_y)+(Mbar/2)E_y+(A0/4+UK)Q
 <= Mbar sqrt(kD) r sqrt(Q)+B0 Q.                (5.2)
```

The proof needs the upper bound on `F(y)-Phi`; the absolute estimate
records that no sign of a multiplier or graph residual was assumed.

Build shell partitions around the feasible center `c`, at scale `h` and
grading ratio `theta`, as in the regridding note. Comparing every local
copy to `y` yields

```
Q <= 6N h^2+3(2k-1)theta^2 r^2+6theta^2 E_y.
```

Bag and separator copy-error sums are at most `2E_y`; they need not be
equal because the repair changes some variables that are private to their
top bag. If `12D theta^2<=1`, absorption gives

```
Q <= 12N h^2+12k theta^2 r^2.                    (5.3)
```

Choose a dyadic `theta<=1/2` satisfying

```
eta = g/20,
12D theta^2 <= 1,
sqrt(12) k sqrt(D) Mbar theta <= eta/4,
12k B0 theta^2 <= eta/4.
```

Let

```
C = 12B0+6kD Mbar^2/eta,
B = max(p,2C/g).
```

Substituting (5.3) into (5.2), and applying Young's inequality to the
`sqrt(N) h r` term, proves

```
|F(y)-Phi| <= (g/20)||y-c||_2^2+C N h^2.         (5.4)
```

All constants are independent of the horizon whenever
`a,b,H,G,M,A0,g,s0` are uniformly bounded, with `a<1` and `g>0`
uniformly separated from their excluded endpoints.

## 6. Certificate validity and the algorithm

The certificate changes the local validity condition to require its
convex inequality on `O_t(B)` intersected with the relevant separator
cell. These sets contain every true locally feasible point of their
leaves. The usual bottom-up induction therefore proves the lower bound
for the true nonlinear problem.

The oracle must return either a minimum and an attaining point on this
compact convex intersection or a certificate that it is empty. Empty
states are represented by infeasibility flags, following
[Section 3 of the affine note](affine-repair-exploration.md#3-empty-states-in-constrained-certificates).
In particular, no infinite intercept is treated as a finite affine
minorant. A leaf becomes unusable if every intersecting cell of one of
its children is flagged; otherwise its child intercept uses only the
unflagged intersecting cells. An own separator state is flagged only if
every incident leaf is unusable or has an empty local convex domain.

Inductively, a true feasible subtree assignment cannot encounter a
flagged state: its local graph point belongs to the selected outer strip
and its child values select intersecting states. Every true feasible
trajectory, including `x*`, therefore induces an available consistent
configuration. Its value is at most its objective value. Thus the root
minimum satisfies `LB_j<=F(x*)`. A feasible initial trajectory also
ensures that a finite root configuration exists. All finite local minima
are attained, and backtracking returns copies satisfying (2.1).

Start with any point in `X`, apply `R` to obtain a feasible `y_(-1)`, and
evaluate its objective for the incumbent. At stage `j>=0`:

1. Let `c=y_(j-1)` and `h_j=s0 2^-j`. Build fresh shell leaves and
   separator cells centered at `c` with the fixed `theta` above.
2. Construct the strips, compute the adjoints and adjusted slopes, and
   run the bottom-up convex dynamic program with maximal intercepts.
3. Backtrack a minimizing configuration with value `LB_j`. Form its
   top-copy point `x_j`, repair it to `y_j=R(x_j)`, and update the
   incumbent with `F(y_j)`.
4. Stop when `UBD-LB_j<=eps` and return the current certificate and
   incumbent.

The stopping test is valid for every choice of grading ratio. Its stated
smallness conditions prove the termination bound. For
`e_j=||y_j-x*||_2^2`, quadratic growth and (5.4) give

```
e_j <= e_(j-1)/9+(10C/(9g))N h_j^2,
e_j <= B N h_j^2,
0 <= UBD-LB_j <= gB N h_j^2.
```

These are exactly the induction and gap calculation of Section 6 of the
regridding note, now applied to feasible repaired centers. The initial
bound is `e_(-1)<=n s0^2<=pN s0^2`. Thus the algorithm stops no later
than

```
J = max(0,ceil(log2(s0 sqrt(gBN/eps)))).
```

## 7. Counts and exact-real scope

The strips do not change the leaves, separator cells, or their incidence
lists. Empty local domains can only remove finite choices. With
`m=4/theta`, the same shell counts give

```
final leaves plus cells <= 2N m^p (J+1),
total created boxes <= N m^p (J+1)(J+2),
exact local convex-oracle calls
  <= N 3^w m^p (J+1)(J+2)(2J+3)/6.
```

Every local convex-oracle call has dimension at most three and imposes
only box, separator, and affine-strip constraints. An empty return counts
as a call. The shell incidence proof includes touching boxes.

Each stage additionally uses `O(T)` evaluations and arithmetic to collect
the global state derivatives, compute the backward adjoints, and apply
the forward repair. Constructing one strip uses one value and gradient
evaluation of `phi_t`. These fit the box and oracle-work counts when
function evaluations are counted as exact oracle operations. Local
objective evaluation costs, oracle-internal solution work, and numerical
proof serialization are not hidden inside a bit-complexity assertion.

Exact nonlinear simulation can itself require an expensive numerical
representation. Even the stable polynomial map

```
phi(s)=s^2/4 on [0,1],       s_0=1/2,
s_t=2^(-(3*2^t-2))
```

has `|phi'(s)|<=1/2`, yet an explicitly written reduced rational
denominator needs exponentially many bits in `t`. The exact recurrence
has a short description. General smooth maps may produce transcendental
states. The theorem consequently treats exact function and gradient
evaluation, feasible recurrence representation, and convex minimization
as oracles. It does not prove polynomial time to evaluate the incumbent
or to emit all repaired coordinates as rationals. Certified rounding that
preserves nonlinear equality feasibility needs a separate treatment;
the [inexact unconstrained extension](../regridded-certificates/inexact-oracles.md)
does not automatically supply it.

The result is for continuous controls. Enumerating discrete control
assignments is possible but may be exponential and is not covered by
the displayed horizon bounds.

## 8. A nonlinear family with uniform constants

Let every interval be `[-1,1]`, and take

```
phi_t(s,u) = s/4+u/2+s^2/8,
F(s,u) = s_0^2
       +sum_(t=0)^(T-1) [s_(t+1)^2+u_t^2-u_t^4/4].
```

Assign `s_0^2` to bag zero and each bracket to its stage bag. The
dynamics are nonlinear and map the input rectangle into `[-5/8,7/8]`.
They satisfy

```
a=1/2,       b=1/2,       H=1/4,       s0=2,
G=2,         U=4,         M=2,         Mbar=3,
K=1/8,       Lq=sqrt(3/2),
p=3,         w=2,         k=2,         C0=6,
rho=13/2,    D=(sqrt(6)+13/sqrt(2))^2.
```

The zero trajectory is feasible. Since `u^2-u^4/4>=3u^2/4` on
`[-1,1]`, the objective obeys `F(x)>=3||x||_2^2/4` on the entire box.
Thus the unique feasible minimizer is zero and `g=3/4` works. Each
state derivative is `2s_j`, proving `G=2`.

Keep the square factors exact. For each unary quartic factor, the
standard alphaBB parameter `1/2` gives a convex lower model and
`A0=1/2`, independently of the horizon. Indeed, the quartic's second
derivative is `2-3u^2>=-1`, and subtracting
`(1/2)(u-l)(r-u)` adds one to it.

The reduced objective is nonconvex even along a simple feasible curve.
Set the initial state, all earlier controls, and hence all preceding
states to zero, and vary only the final control `v`. Then `s_T=v/2`
and the second derivative of the restricted objective is

```
5/2-3v^2.
```

At `v=15/16` it is `-35/256`, while the final state `15/32` is strictly
inside its interval. Thus this is a nonlinear constrained, nonconvex
family with all displayed conditioning constants independent of `T`.
Eliminating the states composes the quadratic state maps and generally
grows the scopes of later state-cost factors. Keeping the states retains
three-variable bags and one-variable separators.

## 9. What the extension establishes

The affine note requires a global affine repair because its cancellation
uses that repair's linear part. Here forward repair is nonlinear, but it
changes a known set of dependent coordinates. The adjoint recurrence
annihilates all adjusted derivatives on those coordinates. This gives
exact cancellation for every repair displacement, and the local graph
strips leave only second-order residual terms.

The new constants include `UH` and `UK`: a bound on the multipliers is
needed when the constraint graph is curved and its local relaxation is
inexact. They vanish in the affine limit `H=0`, where the sharper affine
result needs no multiplier-magnitude bound. The
[constraint obstruction](constraint-obstruction.md) explains why
uncorrected objective-gradient slopes are insufficient.

This is a sufficient structured class. Stable dynamics alone do not
imply feasible quadratic growth, and arbitrary nonlinear constraints
need not have either a box-preserving repair or the coordinate-supported
adjoint cancellation used here. No general constrained-MINLP result or
external novelty claim follows.

## 10. Verification status

The graph-strip constant, repair bound, multiplier recurrence, adjusted
telescoping identity, and contraction constants were derived independently
by a delegated adversarial reviewer. Its
[completed review](../reviews/nonlinear-dynamics-adversary.md) then checked
this full note, including the oracle counts, boundary handling, and
concrete nonlinear example, and found no mathematical blocker.

The targeted command actually run was

```text
python3 research-20261002/new-direction/check_nonlinear_dynamics.py
```

It passed 200 exact-rational configurations at horizons `1,2,3,4,6` for
the Section 8 dynamics. The checks cover strip membership and graph
residuals, sampled repair box preservation, the adjoint bound and state
cancellation, the adjusted telescoping identity, and the stable repair
bound. They include 632 nonzero local graph residuals and 439 nonzero
separator copy mismatches; every telescoping residual is exactly zero.
The artifacts are [the script](check_nonlinear_dynamics.py) and
[its report](check_nonlinear_dynamics.json).

These checks support the algebra and do not implement the full dynamic
program or replace the proof. No project-wide checks, CI inspection, or
literature search were performed in this workstream.
