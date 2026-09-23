# Exact construction from planar support dictionaries

Date: 2026-09-22. Status: algorithmic transfer checked by a fresh
[independent review](review-20260922-planar-message-algorithm.md).
The deterministic construction below is separate from the analytic
[planar smoothed-region theorem](research-20260922-higher-dimensional-smoothing.md).
Its probabilistic consequences are conditional on that theorem. This note does
not establish an expected running-time bound for a prescribed random instance
or a finite-grid smoothing theorem.

Those limitations are resolved by later work: the
[spectral-bound construction](../results/smoothed-spectral-indicator-messages.md)
constructs all exact dictionaries at every fixed treewidth using only first
moments and a different enumeration algorithm. This note preserves the
independently checked direct algebraic construction and its original scope.

## Main conclusion and scope

For diagonally dominant indicator quadratic programs on graphs of treewidth at
most two, exact dynamic programming can construct its messages in polynomial
time in the sum of the sizes of their retained support dictionaries. The
polynomial degree is an absolute constant. No product of the dictionary sizes
of all children is necessary, even at a bag with arbitrarily many children.

Combining this deterministic statement with polynomial first moments for
planar support dictionaries gives polynomial running time with any prescribed
high probability in an exact algebraic computation model. It does not by
itself give polynomial expected running time: the construction is polynomial,
not linear, in the random dictionary sizes.

The graph class here includes arbitrary partial two-trees, whose biconnected
blocks can have arbitrarily many vertices. This is broader than the bounded
block-size class of the scalar message algorithm. The conclusion concerns
penalty-only smoothing of exact support optimization. It makes no claim of a
practical CAD-based implementation or of novelty of algebraic arrangements.

## Model and decomposition

Consider

```
min  x^T Q x + c^T x + sum_i (lambda_i+xi_i) z_i,
     x_i(1-z_i)=0,   z_i in {0,1},
```

with no additional constraints. Assume

```
0<d<=Q_ii<=D,
sum_(j!=i)|Q_ij|<=rho Q_ii,  0<=rho<1,
|c_i|<=C,  C>0.
```

The quadratic matrix is symmetric and positive definite. Put

```
M=C/[2d(1-rho)],   I=[-M,M].
```

The coordinate maximum principle implies that every conditional fixed-support
minimizer lies in the box `I` when its fixed boundary coordinates lie in `I`.
The bound does not depend on the indicator penalties.

Fix a rooted width-two tree decomposition of the sparsity graph before
sampling penalty noise, for example from the graph alone. Contract
adjacent bags when one contains the other. Every bag then has at most three
vertices and every parent-child intersection has at most two. There are at
most `n` nonempty bags: every nonroot bag contains a vertex absent from its
parent, and the running-intersection property assigns each vertex to a unique
highest bag. A decomposition can instead be supplied as part of the input;
the construction is polynomial in its number of bags.

For a bag `B`, let `S_B` be its intersection with its parent, and let `U_B`
be the vertices occurring below `B` but not in `S_B`. The outgoing message
conditions on the continuous variables and indicators in `S_B`, and optimizes
over `U_B`. Assign every original objective monomial to the highest bag
containing all its variables. Thus the subtree objective contains all terms
involving an internal vertex and contains no terms involving only `S_B`.
The latter terms occur at an ancestor. This convention prevents duplicate
costs and gives precisely the concave Schur-complement normalization used in
the planar-region theorem.

Maintain a separate message for each boundary indicator mode
`eta in {0,1}^{S_B}`. Boundary coordinates with `eta_i=0` are fixed at zero.
The remaining `k<=2` coordinates range over `I^k`. The mode `eta_i=1` permits
`x_i=0`; no artificial nonzero restriction is imposed.

A dictionary consists of full quadratic polynomials in those `k` coordinates.
Each polynomial is the unrestricted conditional value of one feasible
internal support, with a support backpointer. Its lower envelope equals the
message on the entire closed box. Identical polynomials are merged, retaining
one support representative. Only polynomials strictly winning at some point
of the relative interior are kept after this merging. When `k=0`, one
minimizer suffices.

This last pruning rule preserves the envelope on the closed box. For a finite
family of distinct polynomials, the union of pairwise equality sets has empty
interior. Every point of the box is a limit of points with a unique minimizer;
a subsequence has the same winning polynomial. Continuity proves coverage at
the limiting point. In particular, supports that are optimal only on a curve,
at an isolated point, or on the box boundary are unnecessary for value
coverage. One retained support still attains the value there.

## Simultaneous child arrangements avoid tuple enumeration

Suppose every child dictionary is available. Fix one of the at most eight
indicator modes on `B`. The active bag coordinates range over a box of
dimension `a<=3`. This mode determines the boundary mode to use for every
child.

Lift every polynomial in each selected child dictionary to the active bag
coordinates. Compare polynomials only within a child dictionary. Remove
identically zero comparison polynomials after restriction to this bag mode;
consistent ties between identical restricted polynomials may be broken by a
fixed rule. Include the box-boundary polynomials. The total number of
comparison polynomials is at most

```
s <= O(1 + sum_child K_child^2),
```

and their degree is at most two. A sign-invariant cylindrical algebraic
decomposition in at most three variables constructs polynomially many cells
and sample points in polynomial algebraic work. In the rational case the bit
work is polynomial in `s` and the coefficient bit length. No adjacency
information is needed. Retain the full-dimensional cells inside the relative
interior of the box. For `a=0`, use its single point directly.

At one sample point per retained cell, select a minimizing polynomial from
each child dictionary. The selected tuple is minimizing throughout that
cell, since all comparison signs are constant there. Add these full
polynomials and the objective terms assigned to `B`. This gives a full
quadratic polynomial in the active bag variables, together with a consistent
support in all child subtrees. The child interiors are disjoint and have no
edges between them, by the tree-decomposition property.

For every resulting polynomial, set inactive coordinates to zero and
unrestrictedly minimize over the active coordinates in `B` outside `S_B`.
The relevant Hessian is positive definite: it is the Schur complement for a
principal submatrix of the original positive definite `Q`. The result is a
full quadratic in the active coordinates of the parent separator and is
exactly the value of its complete internal support. Keep this polynomial as
a candidate. Repeat over the bag indicator modes and group candidates by
their parent boundary mode.

The full-dimensional cells are used only to discover sufficient tuples. The
candidate polynomials are subsequently evaluated and minimized on their
entire domains. There are no interval or cell constraints in the Schur
elimination.

## Exactness, including all lower-dimensional cases

There are two inequalities to check.

**Validity.** Every generated candidate is the unrestricted conditional value
of an actual internal support. It is therefore at least the true conditional
message value at every boundary point, including points outside the cell
that generated the candidate. Allowing its Schur minimizer to leave that cell
cannot produce an invalid value: the cell is not a constraint of the original
indicator problem.

**Coverage.** Fix a parent boundary point in its closed box and choose an
optimal internal support. Its complete conditional optimizer lies in the
invariant box, by the maximum principle. Denote its bag coordinates by `y`.
At `y`, each child envelope can attain the required optimal child value using
its retained dictionary, including when `y` lies on a lower-dimensional
restriction or on the box boundary.

Choose points in relative full-dimensional arrangement cells approaching
`y`. There are finitely many cells and tuples, so a subsequence uses one
fixed tuple. Its child polynomials attain all the child envelope values at
`y`, by continuity. The corresponding generated bag polynomial therefore
has the true conditional optimum as its value at `y`. Its unrestricted
minimum over the forgotten bag coordinates is no larger. Validity gives the
opposite inequality. Hence this candidate attains the true message value at
the fixed parent boundary point.

This argument does not require the original optimal support to win on an
open cell. It only requires some generated support to attain the same value.
It also covers a conditional optimizer on several child switching curves at
once. At a zero-dimensional bag mode there is no limiting argument to make:
the tuple selected at its only point gives the same conclusion.

Finally prune the candidate dictionary. One can use a two-dimensional
sign-invariant decomposition and retain the winning candidate on every
relative full-dimensional cell, merging duplicates. Equivalently, for each
distinct candidate test whether the quadratic strict inequalities making it
the unique minimizer have a solution in the open box. These are
fixed-dimensional real-algebraic operations and have polynomial cost in the
number of candidates. For zero active separator variables choose a minimum
constant. The earlier continuity argument proves that pruning preserves
exactness on the closed box.

Induction from the leaves proves the complete dynamic program. The root has
an empty separator and returns the exact optimal value and a support.
Solving its positive definite support system recovers an optimal continuous
vector; support backpointers permit equivalent recursive recovery.

## Deterministic complexity and coefficient growth

Let `K` be the sum, over all directed messages and boundary indicator modes,
of their final pruned dictionary sizes. Let `N` be the number of bags. The
preceding construction has cost bounded by one fixed polynomial

```
P(N+K)
```

in algebraic operations and real-algebraic sign/root procedures. Each local
arrangement is in at most three variables with quadratic input polynomials.
Its size is polynomial in the sum of its child dictionary sizes. Its
candidate count and the subsequent separator pruning cost are also
polynomial in that sum. Summing over `N` bags preserves polynomiality.
Neither a binary nice decomposition nor an intermediate three-dimensional
message-size estimate is needed. Combining children into unrestricted
intermediate joins would obscure this point.

For rational `Q,c,lambda,xi`, the bit running time is polynomial in `N+K` and
the input encoding length. Every stored candidate coefficient is a
fixed-support Schur-complement coefficient of the original rational problem.
Determinant bounds give polynomial coefficient bit length in `n` and the
original input bits. Algebraic CAD sample coordinates are used for selecting
polynomials only; they are never substituted into stored message
coefficients. Thus repeated algebraic sampling does not generate nested
algebraic coefficients in the dynamic program. Exact support-system recovery
has polynomial rational bit complexity as well.

This is an output-sensitive statement. For arbitrary rational penalties,
`K` may be exponential. It does not contradict the existing hardness results
for indicator QPs on bandwidth-two graphs.

## Consequence of the planar first-moment theorem

Now take independent continuous penalty perturbations with densities at most
`phi`. For every two-active-coordinate message, the eliminated support
branches are concave after subtracting the common boundary polynomial, and
have gradient norm at most

```
L=2 sqrt(2) rho D M.
```

There are at most `n` internal noise coordinates. The candidate planar theorem
therefore bounds its expected retained dictionary size by

```
H = 1 +(1+1/pi)n phi L (8M)
      +96 binom(n,2) phi^2 L^2 (4M^2).
```

For a one-active-coordinate message, the scalar estimate gives
`1+4n phi L M`; zero-dimensional messages use one polynomial. Boundary modes
introduce at most four dictionaries per message. Put

```
H_star=max(1, H, 1+4n phi L M),    B=4 N H_star.
```

Then `E K<=B`. This uses no independence between messages; many of them share
penalty noise. Markov's inequality directly gives, for `0<delta<1`,

```
Pr{ K>B/delta } <=delta.
```

Consequently the exact algorithm completes within `P(N+B/delta)` algebraic
work with probability at least `1-delta`, increasing the fixed polynomial
`P` if necessary. Under bounded structural constants and polynomial `phi`,
this is polynomial in `n` and `1/delta`. This is a polynomial-tail statement,
not a logarithmic dependence on inverse failure probability.

The continuous model requires exact real-algebraic access to the sampled
penalties. A rational-input bit-complexity statement is available for every
fixed rational realization, but these two facts do not establish a smoothed
Turing theorem. Finite precision must be analyzed separately; continuously
perturbed inputs are not finite binary strings, and arbitrary discretization
can introduce persistent ties or concentrate on exceptional levels.

The first moment also does not control `E P(N+K)`. Polynomial expected region
count and polynomial output-sensitive work are insufficient to conclude
polynomial expected work for the originally drawn instance.

## Redrawing a perturbation: a different guarantee

If the application is free to choose its perturbation, cap the work of a
trial at `P(N+2B)` and redraw independent perturbations after an unfinished
trial. Each trial succeeds with probability at least one half, so the
expected total capped algebraic work is at most `2P(N+2B)`. A successful trial
returns an exact optimizer for its own sampled instance. The accepted noise
law is biased by the completion event. This is not an expected-time algorithm
for an externally supplied perturbed instance.

For noise in `[-sigma,sigma]^n`, every successful trial also certifies the
original problem within `n sigma`. If its optimum is `v_xi` and its optimal
support is `z_hat`, then

```
L_original = v_xi - sum_i max(xi_i,0),
U_original = v_xi - xi dot z_hat,
0 <= U_original-L_original <= sum_i |xi_i| <= n sigma.
```

The lower bound follows by comparing every original feasible point with its
perturbed cost. The upper bound is the original objective at the returned
feasible point. These inequalities are deterministic and survive the biased
acceptance rule. Choosing `sigma=epsilon/n` gives an additive certificate,
conditional on successful exact completion. This elementary perturbation
comparison is not itself new. A finite-bit redraw algorithm still needs a
finite-grid analogue of the planar region estimate. Existing deterministic
additive approximation methods also limit the novelty of an approximation
consequence alone.

## Sources and limits of the contribution

The algebraic-arrangement ingredients are classical:

- Arnon, Collins, and McCallum, [*Cylindrical Algebraic Decomposition I:
  The Basic Algorithm*](https://www.lacl.fr/pvanier/cours/2015-2016/lm/articles/Cylindrical%20Algebraic%20Decomposition%20I-%20The%20Basic%20Algorithm.pdf),
  introduction and Sections 2–5, describes sign-invariant cells and explicitly
  states polynomial input-size complexity when dimension is fixed.
- Basu, Pollack, and Roy, [*An asymptotically tight bound on the number of
  semi-algebraically connected components of realizable sign conditions*](https://www.math.purdue.edu/~sbasu/combinatorica_final.pdf),
  supplies a sharper classical bound for the number of arrangement cells.
  No such sharp exponent is needed here.

The potentially useful step is the combination of full support quadratics,
simultaneous arrangements in bags of size three, and polynomial expected
planar dictionary size under penalty-only noise. The deterministic
arrangement construction itself is a standard fixed-dimensional device.
This note does not establish priority against all prior parametric quadratic
programming or bounded-treewidth algorithms; the broader literature audit in
the scalar and planar notes remains applicable.

The most consequential remaining obstacles are an independent review of this
coverage argument, completion of the planar analytic review, and a finite-bit
smoothing analysis. Higher moments or a sharper envelope-construction method
would be needed for polynomial expected work on a prescribed perturbed
instance. No computation or Lean proof verifies the analytic or algorithmic
theorems in this note. Only the files relevant to this investigation were
examined; no project-wide checks were run.
