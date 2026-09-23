# Next frontier: smoothed exact scalar messages

Date: 2026-09-22. Status: strategic research screen and independently derived
candidate lemma. The coordinator independently obtained the same isolation
argument during this investigation. The final section gives a candidate exact
algorithm and expected arithmetic bound, now undergoing independent adversarial
review. No publication priority claim is made.

## Selected question

Can independent perturbations of indicator penalties give a polynomial expected
size, and then a polynomial expected construction time, for exact scalar
parametric messages in convex mixed-integer optimization?

This is the strongest next target identified in this screen. It directly addresses
the obstruction in [the fixed-data scalar-message construction](research-20260922-constant-data-messages.md):
bounded coefficients, strong conditioning, contraction, and a scalar separator
do not prevent exponentially many indispensable quadratic formulas. A positive
theorem should replace a prescribed support-separation parameter by an explicit
probability model. It should preserve the nonlinear continuous problem rather
than only perturb an unrelated combinatorial surrogate.

The goal is a theorem about exact message construction under perturbations,
not merely a randomized approximation to the original unperturbed instance.
The perturbed problem is a different optimization problem. Its analysis could
explain when exact parametric dynamic programming remains manageable and could
support deliberate perturbation followed by a certified accuracy estimate.

## Candidate lemma: only a polynomial expected number of changes

Let `Z` be a nonempty subset of `{0,1}^m`. For each `z in Z`, let `q_z` be
an `L`-Lipschitz real function on a compact interval `I` of length `T`.
Let `xi_1,...,xi_m` be independent real random variables with densities bounded
by `phi`. Define

```
F_z(t)=q_z(t)+sum_i xi_i z_i,
V(t)=min_(z in Z) F_z(t).
```

The deterministic functions may contain arbitrary support-dependent intercepts.
They need not be additive in the support, convex, or quadratic.

**Candidate proposition.** Almost surely, there are finitely many points of
`I` with more than one minimizing support. The number `K` of open intervals
of unique minimizing support satisfies

```
E K <= 1+2 m phi L T.
```

This counts intervals, including repeated appearances of the same support.
For quadratic `q_z`, it bounds the actual number of formulas in an interval
description of the message. For more general functions, it does not bound the
complexity of describing an individual function.

**Proof using the one-dimensional coarea formula.** For each coordinate `i`
for which both support classes are nonempty, condition on all random variables
except `xi_i`. Define

```
h_i(t) = min_(z in Z:z_i=0) [q_z(t)+sum_(j != i) xi_j z_j]
       - min_(z in Z:z_i=1) [q_z(t)+sum_(j != i) xi_j z_j].
```

Each minimum is `L`-Lipschitz, so `h_i` is `2L`-Lipschitz. The two best
values in the two classes coincide exactly when `h_i(t)=xi_i`. For a
Lipschitz real function on an interval, the one-dimensional coarea/area formula
gives

```
integral_R #{t in interior(I): h_i(t)=y} dy
  = integral_I |h_i'(t)| dt <= 2 L T.
```

Integrating the level-set count against the conditional density of `xi_i`
therefore bounds its conditional expectation by `2 phi L T`. In particular,
the count is finite almost surely. At every tie between distinct globally
minimizing supports, the supports differ in some coordinate `i`; that point
belongs to the corresponding level set. Summing over coordinates proves that
the expected number of global tie points is at most `2m phi L T` and is finite
almost surely. Ties at either fixed endpoint have probability zero by the same
conditioning argument. Between consecutive tie points the unique minimizing
support is constant, by continuity and finiteness of `Z`. This proves the bound.

The coarea formula is classical and is an established input, not a new result.
The proposition and its application must be checked independently before being
promoted. It is possible to use a longer elementary proof for semialgebraic
functions, avoiding coarea at the cost of a factor two:

1. At a fixed `t`, the continuous isolation lemma gives
   `Pr(best distinct-support gap <= delta) <= 2m phi delta`.
2. If the minimizing support changes inside an interval of length `eta`, the
   gap at its left endpoint is at most `2L eta`.
3. Sum over an increasingly fine deterministic partition and apply Fatou's
   lemma. Finite semialgebraic switching and almost-sure absence of persistent
   ties give `E K <= 1+4m phi L T`.

Neither proof requires independent random values for the exponentially many
supports. Only the `m` coordinate penalties are independent.

## First MINLP consequence and the remaining algorithmic work

For the fixed-data construction,

```
q_z(t)=(t-c_z)^2/D_z,    0<=c_z<=1/9,    D_z>=1,    t in [0,1],
```

so `|q_z'(t)|<=2`. Adding independent penalty perturbations of density at most
`phi` gives the candidate bound `E K<=1+4m phi`, whereas the unperturbed family
has `2^m` indispensable formulas. The distinction concerns the exact envelope,
not an approximation obtained by dropping shallow wells.

A more useful result would cover arbitrary bounded-data quadratic objectives
on a chain of bounded-size blocks with scalar separators. The following
deterministic observation supplies a domain on which the candidate proposition
can be used uniformly.

Let the quadratic objective be `x^T Q x+c^T x`. Suppose

```
Q_ii >= d > 0,
sum_(j != i) |Q_ij| <= rho Q_ii,    rho<1,
Q_ii <= D,
|c_i| <= C.
```

Set `M=C/[2d(1-rho)]`. For any support restriction, and any subset of coordinates
fixed to boundary values in `[-M,M]`, the unique conditional minimizer on the
remaining active coordinates lies in `[-M,M]`. To prove this, choose an active
free coordinate with largest absolute value `X`. Its stationarity equation
implies

```
X <= C/(2d)+rho max(X,M).
```

If `X>M`, this contradicts the definition of `M`. Inactive coordinates equal
zero. Strict diagonal dominance makes every relevant principal matrix positive
definite, so the conditional minimizer exists and is unique.

For one boundary coordinate `t`, the derivative of the conditional support
value satisfies

```
|q_z'(t)| <= C+2 D M(1+rho).
```

This follows from the envelope theorem and
`q_z'(t)=2Q_bb t+c_b+2 sum_(j != b) Q_bj x_j(t)`.
Thus the Lipschitz constant and interval length can be independent of the
number of eliminated variables. Restricting all intermediate scalar messages
to this interval loses no globally optimal solution.

This observation is not yet a full dynamic-programming theorem. The next work
must specify the local elimination operation, prove that it constructs the
exact envelope from the preceding envelope, handle the special value at a
zero boundary variable with its indicator off, and recover an optimal support.
An output-sensitive envelope routine is essential. A first-moment bound on
`K` does not imply a polynomial bound on `E K^2`; using a routine with quadratic
cost in `K` would leave a real gap. A cost of `O(K log K)` could suffice because
the deterministic worst-case number of support quadratics is exponential only
in the input dimension, making `log K` polynomially bounded.

An arithmetic-time statement under real continuous perturbations is also not
automatically a Turing bit-complexity statement. Rational or finite-grid
perturbations introduce atoms and require a separate tie and precision analysis.
The general problem with separators of dimension two or more remains open in
this proposal: the one-dimensional count does not control the number of regions
in a multidimensional lower envelope.

## Source comparison and priority limits

The following primary sources were examined on 2026-09-22. Search result dates
were not used as publication dates.

- [Bhathena, Fattahi, Gómez, and Küçükyavuz, *Solving Convex Quadratic Optimization
  with Indicators Over Structured Graphs*, March 2026](https://arxiv.org/abs/2603.02103)
  gives exact parametric algorithms whose bounds include a margin parameter.
  The proposed contribution would replace that hypothesis by an explicit
  independent-penalty perturbation model for scalar messages. It would not
  subsume their graph-general theorem.
- [Choi, Fattahi, Gómez, Han, and Lozano, *Convexification of Mixed-Integer
  Quadratic Optimization via Decision Diagrams*, August 2026, §8 and Theorem 4](https://arxiv.org/html/2608.22815v1)
  gives quantitative approximation using spectral decay, volume growth, and
  boundary size. This already covers much of the tempting approximate
  bounded-bandwidth direction. An exact smoothed message bound has different
  assumptions and conclusions.
- [Beier and Vöcking, *Typical Properties of Winners and Losers in Discrete
  Optimization*, 2006](https://pure.mpg.de/view/item_1328602)
  is central prior work for the isolation argument and the connection between
  approximation/pseudopolynomial algorithms and smoothed exact complexity.
  Therefore simply combining an existing approximation scheme with isolation
  is a weaker and likely mostly classical target.
- [Moitra and O'Donnell, *Pareto Optimal Solutions for Smoothed Analysts*, §2](https://www.cs.cmu.edu/~odonnell/papers/pareto-optima.pdf)
  treats random linear objectives and one arbitrary deterministic objective.
  [Brunsch and Röglin, *Improved Smoothed Analysis of Multiobjective
  Optimization*](https://arxiv.org/abs/1111.1546) strengthens related bounds and
  studies zero-preserving perturbations. These results are important possible
  equivalents. They do not immediately apply to arbitrary deterministic
  support quadratics plus a single random linear penalty: both curvature and
  slope are support-dependent deterministic functions, and the deterministic
  intercept is not generally additive in the support.
- [Brunsch, Cornelissen, Manthey, Röglin, and Rösner, *Smoothed Analysis of the
  Successive Shortest Path Algorithm*, SODA 2013, §3 and Corollary 4.3](https://www.roeglin.org/publications/SODA13.pdf)
  uses the same broad proof pattern of partitioning a bounded interval,
  bounding the probability of a witness in each cell, and taking a fine-mesh
  limit. The proof technique itself is established. Its network-flow witness
  reconstruction and theorem are different from the nonlinear family above.
- [Applegate, Archer, Johnson, Nikolova, Thorup, and Yang, *Wireless Coverage
  Prediction via Parametric Shortest Paths*, full preprint §6, Theorem 7 and
  Corollary 8](https://arxiv.org/abs/1805.06420)
  gives a smoothed parametric-complexity theorem. The full proof perturbs both
  linear objective directions by random angular rotations and applies a
  polytope-shadow theorem. It does not establish the penalty-only nonlinear
  envelope claim. The shorter conference version numbers its informal result
  Theorem 3; the full version uses different numbering.
- [Shin, Anitescu, and Zavala, *Exponential Decay of Sensitivity in
  Graph-Structured Nonlinear Programs*, 2022](https://arxiv.org/abs/2101.03067)
  provides established continuous sensitivity theory. It does not by itself
  control changes of the optimal discrete support. This is why extending
  continuous correlation-decay arguments alone would leave an important gap.

The proof is short enough that an equivalent envelope statement may already
exist in smoothed parametric optimization, level-crossing theory, or stochastic
geometry. The search has not established novelty. Before claiming a substantial
advance, obtain an independent source audit, verify the coarea application,
and complete an exact dynamic-programming theorem with a valid runtime model.

## Verification record

This screen used symbolic reasoning and source inspection. The invariant-box
argument and the isolation/grid derivation were independently obtained by the
coordinator. The coarea sharpening has not yet received an independent review.
No experiments, Lean checks, or project-wide verification were run. Temporary
PDF extraction was used to inspect the full wireless-coverage proof; no solver
or experiment was needed for this strategic screen.

## Follow-up: an exact algorithm for bounded biconnected block size

The discussion above led to a simpler construction that appears to close the
arithmetic-time gap for graphs of bounded biconnected block size. It has not yet received adversarial
review. It should supersede the interval-constrained QP route if verified.

Assume every biconnected block of the support graph of `Q` has at most a fixed
number `b` of vertices, counting bridges as blocks of size two. The blocks need
not be cliques. Different blocks intersect in at most one vertex, and the
block-cut incidence graph of a connected component is a tree. Allow disconnected graphs
by solving their components separately. Keep the diagonal-dominance and
bounded-data assumptions above. Perturb every indicator penalty independently
by a real random variable of density at most `phi`.

Root the block-cut tree at a vertex. A block message conditions on its parent
vertex and eliminates all vertices below that block. It excludes the parent's
diagonal term, linear term, and indicator penalty. A vertex message includes
those terms for its own vertex and combines its child block messages.

The representation should retain **full support quadratics**, together with
their support labels, rather than restricting them to their active intervals.
For a given boundary variable these are the exact values obtained by fixing
all internal indicators and minimizing all free continuous variables. Each
quadratic is feasible for every real boundary value. Retain only quadratics
that attain the lower envelope on a nonempty open interval inside `I=[-M,M]`.
The remaining full quadratics still represent the exact message on `I`:
continuity preserves values at switching points and endpoints. A formula that
touches the envelope only at one point is unnecessary.
Deduplicate retained formulas by their support labels. The same support can
appear on several intervals, but it is stored only once in the retained list.

At a vertex `u`, first construct the message with its own indicator fixed to
one. Its indicator penalty is a constant added to every support formula. To
construct this message from its child block messages, take the union of their
breakpoints. On each resulting interval, sum the active child quadratics and
the vertex's own quadratic and linear terms. The resulting full quadratic
corresponds to a feasible combination of child supports. The minimum of these
full quadratics is the exact active-vertex message on `I`: it cannot lie below
the true message anywhere, and it attains it on every interval. At breakpoints,
continuity gives the same conclusion.

Also retain one inactive-vertex alternative. It fixes `x_u=0` and has value

```
min_q q(0) - lambda_u,
```

where `q` ranges over the active-vertex support quadratics and `lambda_u` is
the perturbed indicator penalty. Subtracting that penalty is valid because
fixing the indicator to zero at `x_u=0` imposes no additional restriction on
the descendant variables. This alternative needs only one minimizing
descendant support and a backpointer. The active-vertex alternatives may also
be evaluated at zero; they correspond to the feasible choice `z_u=1,x_u=0`.

Now consider a block `B` with parent vertex `v`. For each other vertex `u` of
the block, choose either a retained active-vertex quadratic or its inactive
alternative. Add the block's cross terms. Minimize over the active variables
of `B\{v}` without interval restrictions. The internal Hessian is positive
definite: it is the corresponding principal block after eliminating descendant
variables from a positive definite principal submatrix of the original `Q`.
Thus ordinary Schur complementation produces one full quadratic in `x_v`.

Unconstrained elimination is safe. Every candidate is the value of a complete
fixed-support conditional problem, whose conditional minimizer lies in `I`
by the maximum principle proved above. Conversely, take any true optimum for
`x_v in I`. All child boundary values lie in `I`; for each child, choose a
retained support attaining its message there. The corresponding block
candidate therefore attains the true optimum. This proves exactness of the
block step on `I`.

If vertex `u` has `K_u` retained active quadratics, the block generates at most

```
N_B = product_(u in B\{v}) (K_u+1)
```

candidate quadratics. The random variables used in the different child-vertex
subtrees are disjoint. Consequently their `K_u` are independent, and

```
E N_B = product_(u in B\{v}) E(K_u+1).
```

The scalar-envelope proposition bounds each expectation by
`2+2n phi L_0 T`, where

```
T=2M,    L_0=2 rho D M,
```

using the whole input dimension `n` as a coarse bound on each subtree size.
For this sharper Lipschitz constant, subtract the boundary vertex's own
quadratic, linear term, and penalty from all support functions. This common
function does not change their minimizing supports. The derivative of every
remaining support function is `2 sum_j Q_uj x_j(t)`, with the sum over internal
neighbors, and its absolute value is at most `2 rho D M`. The common random
penalty of the boundary vertex therefore has no effect on the count.
It follows that

```
E sum_B N_B <= n (2+2n phi L_0 T)^(b-1).
```

Here the number of blocks is at most `n-1` for a connected nontrivial block
graph with at least two vertices. Each active-vertex message is an envelope over fixed-support quadratics
with a common own-vertex penalty; apply the proposition to its internal
penalties. Dependence among messages at different depths does not affect the
displayed expectation: only children of a single block require independence.

The lower envelope of `N` full univariate quadratics has at most `2N-1` open
pieces. Indeed, a pattern `a,b,a,b` in the sequence of minimizing quadratics
would force at least three distinct zeros of the difference between two
quadratics. A standard order-two Davenport--Schinzel argument gives the bound.
Divide-and-conquer can merge two ordered envelopes in time linear in their
combined numbers of pieces: on an overlap interval, solve a single quadratic
comparison, which has at most two roots. Thus constructing the full lower
envelope takes `O(N log N)` arithmetic and quadratic-root operations. This is
the standard lower-envelope construction, not a new algorithmic primitive;
see [Sharir's computational-geometry notes, Theorem 3.2.6](https://www.math.tau.ac.il/~michas/notes.pdf),
which gives `O(lambda_s(N) log N)` and specializes to `lambda_2(N)=2N-1` here.

For fixed input dimension, every retained quadratic has a support label.
Hence `K_u<=2^(number of internal indicators)` and `log N_B=O(n)`.
The preceding first-moment estimate then suffices to bound the expected
construction work by a polynomial in `n` and `phi` for fixed `b,d,D,C,rho`.
It is not necessary to infer a second-moment estimate from a first-moment one.
Combining the child block messages at a vertex costs polynomial work in their
total envelope size; the same expectation argument applies. Store support
backpointers to reconstruct an optimal continuous point after minimizing the
root message.

More explicitly, put `A=2+8n phi rho D M^2`. Constructing all block envelopes
and combining them at vertices costs

```
O_b(n (n+sum_B N_B))
```

arithmetic, comparison, and quadratic-root operations. Indeed, each block
candidate requires a constant-size Schur complement for fixed `b`; every
logarithmic envelope factor is `O_b(n)`. The total number of child-envelope
pieces processed in all vertex combinations is at most `2 sum_B N_B`, because
each block message is a child of exactly one vertex. Sorting their union of
breakpoints costs another logarithmic factor bounded by `O_b(n)`.
Consequently a coarse explicit expected bound is

```
O_b(n^2 A^(b-1)).
```

If `C=0`, the continuous optimizer is identically zero for every support and
the indicator penalties can be minimized directly; the degenerate interval
`M=0` does not require an envelope construction. Isolated vertices are handled
directly as well.

This candidate would cover the chain of triangles used in the exact
bandwidth-two hardness construction. It would give a positive result under
independent penalty perturbations on a graph class where worst-case exact
optimization is already NP-hard. It also covers trees of larger fixed-size
blocks, including graphs of high vertex degree, without invoking a support
margin or polynomial volume growth. It does **not** cover all bounded-treewidth
graphs: intersections of neighboring bags must be single vertices.

The runtime model in this candidate counts arithmetic, comparisons, and real
quadratic-root operations. Continuous perturbations are not finitely encoded
inputs. A bit-complexity theorem needs a separate perturbation and precision
model. In particular, changing to finite-grid noise invalidates the density
assumption. These qualifications are part of the proposed theorem, not minor
implementation details.
