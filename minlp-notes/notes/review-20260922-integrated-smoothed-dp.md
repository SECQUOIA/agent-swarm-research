# Integrated adversarial review of exact smoothed indicator dynamic programming

Date: 2026-09-22. This is a fresh review of the complete
[consolidated result](../results/smoothed-indicator-block-dp.md), including
continuous smoothing, finite-grid smoothing, the algorithm, bit costs, and
the original-objective certificate. Earlier reviews were consulted after
independently reconstructing the delicate steps.

**Assessment.** I found no mathematical gap in Theorems 1 and 2 or Corollary
5 under their stated assumptions. The exact construction of all messages,
with a polynomial expected bit bound under finite penalty noise, remains
the substantive candidate contribution. The additive corollary is correct,
but its significance needs an explicit qualification: a direct deterministic
grid dynamic program already gives additive approximation and a valid
objective interval under these numerical bounds. That simpler argument even
works on arbitrary graphs of bounded treewidth. The additive corollary should
therefore be presented as a consequence of the exact smoothed solver, not as
a new approximation frontier.

## 1. Isolation and the finite-grid limit

At a fixed parameter, the two best distinct binary supports differ in some
coordinate. The better support minimizes its bit class, and the second-best
support minimizes the other class: any smaller value in that other class
would contradict its rank. Conditioning on all other noises leaves one
random scalar whose favorable interval has length at most twice the desired
gap. The bound `2 m phi delta` is valid with arbitrary deterministic support
offsets, including the continuous-elimination cost.

The scalar Lipschitz proof also detects tangential ties with no change of
winner. A tie in a cell forces a midpoint winner gap at most `L` times the
cell length. For each finite subset of tie points, all sufficiently fine
grids separate those points. Thus the liminf argument bounds even an
initially infinite tie set; it does not assume finitely many roots or
semialgebraicity. Endpoint and grid-point ties have probability zero by the
fixed-parameter isolation bound. Fatou's lemma has the correct direction.

For grid noise, the interval-mass bound is
`Pr(xi_i in J) <= length(J)/(2 sigma) + 1/N`. Convolving with any independent
uniform jitter preserves this bound by conditioning on the jitter. The two
bit-class envelopes have fewer than `2^(m+1)` common quadratic pieces; splitting
each piece at its possible stationary point gives at most `2^(m+2)` monotone
arcs. Their image lengths sum to at most `2 L T`. Endpoints and constant arcs
have zero conditional probability after jitter. The resulting expected
number of level hits is at most `2 phi L T + 2^(m+2)/N` per coordinate.

Removing jitter requires counting distinct polynomial formulas, not support
labels. At a selected interior point of each original formula interval, its
class is separated by a positive gap from every other polynomial class.
Sufficiently small jitter keeps winners within that class. Adjacent selected
points belong to different original classes, so the jittered envelope has at
least as many intervals. Persistent duplicate formulas are harmless under
this argument. Fatou then gives precisely the displayed atomic term
`4 m 2^m/N`. Its bound by one when `N >= 4 n 2^n` is valid for every
message with at most `n` internal indicators.

The finite-grid statement is a separate proof. It does not improperly apply
a density estimate to atoms, or claim uniqueness at a grid outcome.

## 2. Exactness of the dynamic program

The maximum principle applies to every fixed support, not only a winning
support. A free coordinate of largest absolute value `X` obeys
`X <= C/(2d) + rho max(X,M)`, so `X <= M`. Subtree objective allocation
keeps each internal diagonal intact; omitted external edges only reduce
the relevant absolute row sum. This verifies the conditional domain claim.

Subtracting the boundary's own terms leaves derivative
`2 sum_j Q_vj x_j(t)`. The bound `L=2 rho D M` is independent of subtree
size. The support family to which isolation is applied is the full family
fixed before sampling, not the random retained list. Own-boundary noise is
a common constant and does not affect its envelope.

Every retained full quadratic is an exact value function for a genuine
support at all boundary values. This is stronger than being an expression
valid only on a winning interval. Consequently Schur elimination using that
quadratic outside its winning interval remains feasible support elimination;
it cannot produce an artificial lower bound. Conversely, at any true
conditional optimum, each child boundary is in the invariant interval and
a retained child formula attains its true value. Replacing descendants by
these representatives establishes coverage of the optimum. A tie occurring
only at one point does not require retaining the touching support, because
continuity supplies a neighboring retained formula with the same value.

The inactive atom `F_u(0)-p_u` is correct even for negative penalties.
Active zero and inactive zero remain separate alternatives. Descendants
connect to the remaining graph only through that vertex, so one attaining
descendant support suffices at the atom. Identical full polynomials are
interchangeable at future eliminations for the same reason.

Only bounded block size and a one-vertex intersection with the rest of the
block-cut tree are used. Completeness of block edges is unnecessary. A
four-cycle is covered when `b>=4`; arbitrary treewidth-two graphs are not.

## 3. Expected work and bit complexity

For a given block, its child-vertex subtrees have disjoint noise sets.
Deterministic local tie-breaking makes each retained count a function of
that subtree's data alone. Thus the product expectation factors. This would
not justify squaring the expected size of one message, but the proposed
construction never needs that inference.

The lower envelope of `r` full quadratics has at most `2r-1` pieces: an
alternating `a,b,a,b` winner pattern forces three distinct roots of their
difference. Isolated contacts and identical formulas must be handled as
specified in the result. Divide-and-conquer merging takes `O(r log r)`
operations. The logarithm is at most linear in `n`, since the candidates
have support representatives.

At a vertex of high degree, implement the child-breakpoint merge as an
incremental sweep: maintain the sum of the active polynomial coefficients,
and replace one child's contribution at its event. This avoids recomputing
all child sums at each interval. With sorting, the total vertex work is
bounded by the stated coarse `O_b(n(n+sum_B N_B))` expression. Explicit
support labels, if used, add at most linear work per generated formula,
already allowed there. The exposition's word “merge” admits this standard
implementation; spelling out the sweep would remove an avoidable ambiguity.

Rational bit sizes are controlled by a stronger invariant than recursion
depth: each completed coefficient is a Schur-complement expression for one
principal support problem in the original input. Determinant bounds give
polynomial encoding sizes uniformly over all supports. Constant-size
eliminations and sums of at most `n` such rational terms have polynomial-size
intermediate expressions when fractions are reduced. The algebraic
breakpoints have degree at most two and polynomial-size defining data.
They participate in comparison and sorting, not in the rational coefficient
recursion. Hence there is no growing algebraic degree hidden in the DP.

The final selected support has a rational optimizer. Negative penalties
affect support selection but do not compromise positive definiteness or
boundedness. Arbitrarily large penalty magnitudes affect bit lengths, not
the envelope-count estimate. Small smoothing scales and a vanishing
diagonal-dominance margin can make the operation bound large. The stated
dependence is polynomial in inverse smoothing scale, not in its logarithm.

## 4. The additive certificate is correct

Write `v_xi` for the perturbed optimum and `(xhat,zhat)` for its optimizer.
For every original feasible point,

```
original cost = perturbed cost - xi^T z
              >= v_xi - sum_i max(xi_i,0).
```

The returned point's original cost is `U=v_xi-xi^T zhat`. Subtracting the
displayed lower bound gives

```
sum_(zhat_i=0) max(xi_i,0) + sum_(zhat_i=1) max(-xi_i,0)
<= sum_i |xi_i| <= n sigma.
```

There is no missing factor two. Each coordinate contributes only one of its
two signs, according to the returned indicator. The bound holds for all
finite-grid outcomes, including ties. Setting `sigma=epsilon/n` yields the
claimed valid interval, with only runtime averaged.

## 5. A deterministic approximation comparison that should be added

The numerical assumptions make additive approximation elementary even
without smoothing. This observation is a limitation on significance, not a
replacement for exact smoothed message construction.

Let `(x*,z*)` be an original optimum, with support `S={i:z*_i=1}`. For its
fixed support, stationarity gives `(2Qx*+c)_S=0`. Let `xbar` round each
active coordinate to the nearest point of the rational grid

```
G_K={j M/K : j=-K,...,K},
```

and leave inactive coordinates zero. This preserves the indicator vector,
including any active coordinate rounded to zero. The maximum principle
places `x*` in the grid's box. If `e=xbar-x*`, then

```
objective(xbar,z*) - objective(x*,z*) = e^T Q e
 <= D(1+rho) ||e||_2^2
 <= n D(1+rho) M^2/(4 K^2).
```

The spectral bound follows directly from symmetric absolute row sums.
Define the rational final expression above as `delta_K`. Each coordinate
now has `2K+2` states: the inactive state `(0,0)` and the active states
`(t,1)` for `t in G_K`. The objective contains only vertex and edge factors.
Ordinary finite-state DP solves it exactly on the supplied block-cut tree
in `O_b(n(2K+2)^b)` arithmetic operations. More generally, the same standard
construction works given a width-`w` tree decomposition, with a polynomial
number of tables of size `(2K+2)^(w+1)`.

If `v_K` is the exact grid optimum, then

```
v* <= v_K <= v* + delta_K.
```

Thus `[v_K-delta_K,v_K]` is a deterministic valid objective interval, and
the grid optimizer is feasible. Choose an integer `K>=1` with
`n D(1+rho) M^2 <= 4 epsilon K^2`; the smallest such integer can be found
by rational comparisons. Its size is
`O(1+M sqrt(n D(1+rho)/epsilon))`. For fixed structural and numerical bounds,
the resulting bit algorithm is polynomial in input length and inverse
accuracy. No bound on the penalty magnitudes is needed beyond their input
encoding, because rounding preserves indicators and hence their costs.

This directly proves that the additive corollary does not establish a new
tractability boundary. It also explains why extending exact message control
to larger separators remains meaningful even though additive approximation
on those graphs is already straightforward under the strong numerical
bounds.

The relevant primary literature should be represented carefully.
[Bienstock and Chen, Theorem 1.4 and Section 2.2](https://arxiv.org/html/2411.11722v1)
give a structured-sparsity approximation framework, with a banded indicator
QP application that produces upper and lower objective bounds after repairing
auxiliary-variable violations. Their main theorem initially permits
constraint infeasibility and uses a constraint-block intersection graph.
It should not be quoted as literally the same feasible-output theorem under
the Hessian graph used here.
[Bhathena et al., Section 1.2](https://arxiv.org/html/2603.02103v1)
explicitly identifies that work as an approximation antecedent for bounded
treewidth indicator quadratics. The direct rounding argument above avoids
relying on an unchecked reformulation between their two graph notions.

## 6. Priority and verification limits

I inspected the consolidated theorem and earlier proof reviews, and opened
the primary sources linked above. I also rechecked
[Roglin and Teng, Theorem 6.2 and its proof](https://www.roeglin.org/publications/FOCS09.pdf).
It is an expected-time result, so expected polynomial time alone is not a
new distinction from general smoothed binary optimization. Its displayed
algorithm uses an exact oracle for several best rounded linear-objective
solutions. The nonlinear deterministic support cost in this problem does
not immediately supply that oracle. This checks the narrow comparison in
the main text; it does not rule out an alternative general conversion.

The stronger contribution remains the exact construction of every scalar
message under noise only in indicator penalties, including finite-grid
atoms and the expected Cartesian-product work at blocks. Neither this
review nor the earlier searches establishes publication priority.

This review used independent mathematical derivations and targeted source
inspection. It did not rerun the coordinator's nine-instance exact checker,
implement the efficient envelope routine, perform a Lean proof, inspect CI,
or run project-wide checks. The earlier computations test concrete
deterministic identities; the probability and asymptotic bit assertions
continue to rest on the written proofs.
