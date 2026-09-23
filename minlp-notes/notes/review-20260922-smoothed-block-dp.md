# Independent review: exact smoothed dynamic programming across scalar separators

Date: 2026-09-22. This is an independent proof review of the final algorithmic
section of [the next-frontier note](research-20260922-next-frontier.md), using
the independently reviewed [scalar-envelope bound](review-20260922-smoothed-envelope.md).
The review reconstructs the mathematical and runtime arguments. It does not
certify publication priority or exact bit complexity.

**Conclusion.** The proposed exact algorithm and polynomial expected arithmetic
bound are valid under the stated diagonal-dominance, bounded-block, and
independent-density hypotheses. The useful graph class is broader than block
graphs: every biconnected block may be an arbitrary graph on at most `b`
vertices. The proof only uses its size and its one-vertex intersection with
the rest of the rooted block-cut forest.

One representation clarification was needed during review. Retain support
quadratics winning on a nonempty open interval, rather than requiring retention
of every formula touching the envelope at an isolated point. Continuity
preserves the value at all omitted endpoints and ties. This makes the list-size
bound follow directly from the scalar-envelope proposition, without another
genericity argument. The author has incorporated this clarification.

## 1. Exact assumptions and invariant interval

Let `Q` be real symmetric, with

```
0 < d <= Q_ii <= D,
sum_(j != i) |Q_ij| <= rho Q_ii,   0 <= rho < 1,
|c_i| <= C.
```

The optimization problem is

```
min x^T Q x + c^T x + sum_i p_i z_i,
x_i(1-z_i)=0,   z_i in {0,1},
p_i=lambda_i+xi_i.
```

All deterministic data, the graph, and the interval below are fixed before
sampling. The noises are independent, with Lebesgue densities bounded by
`phi`. No bound on the penalty magnitudes or on the noise tails is needed.
Positivity of the perturbed penalties is also unnecessary for this theorem.

Strict diagonal dominance and positive diagonals make `Q` positive definite.
Consequently every support-restricted conditional quadratic problem has a
unique continuous optimizer. Put `M=C/[2d(1-rho)]` and `I=[-M,M]`.
If boundary variables lie in `I`, choose a free active coordinate of largest
absolute value `X`. Its stationarity equation implies

```
X <= C/(2d) + rho max(X,M).
```

If `X>M`, this gives `X<=M`, a contradiction. This argument applies to every
fixed support, including supports that never become globally optimal, and to
every subtree conditional problem used by the algorithm. This universal
quantifier is essential: it justifies later unconstrained elimination of
retained full quadratics. If `C=0`, all continuous optimizers are zero, and
the problem reduces directly to selecting the negative penalties.

For a message with one boundary vertex `v`, remove its own diagonal, linear,
and penalty terms. A fixed-support message then satisfies

```
q_z'(t) = 2 sum_(j internal) Q_vj x_j^z(t),
|q_z'(t)| <= L = 2 rho D M,   t in I.
```

The derivative formula follows by differentiating the conditional optimum;
its free-coordinate gradient vanishes. The perturbations contribute only
constants for fixed support. Thus the full, deterministic support family
satisfies the reviewed scalar-envelope proposition with interval length
`T=2M`. The expected number of unique-winner intervals is at most
`1+2m phi L T`, where `m` is the number of internal indicators. Subtracting
the boundary's own random penalty is harmless because it is common to all
active-boundary branches. The proposition is applied to the full support
family, not to a random family selected by the algorithm.

## 2. Objective allocation and vertex operations

Root each connected block-cut component at a vertex. Every edge belongs to
exactly one block. Assign its cross term `2Q_ij x_i x_j` to that block, and
assign every diagonal, linear, and penalty term to its vertex. A block message
excludes its parent vertex's own terms and includes all terms below the block.
These rules neither duplicate nor omit an objective term.

At vertex `u`, the active message is

```
F_u(t) = Q_uu t^2 + c_u t + p_u + sum_(child blocks B) H_B(t).
```

Merge the child breakpoint lists. On each nonempty interval the chosen child
support quadratics sum to a genuine full-support quadratic for `F_u`.
Retain those full quadratics, deduplicated by their support labels. Their
minimum equals `F_u` throughout `I`: every retained quadratic is the cost of
a feasible support, so it cannot lie below the true message; at every open
interval one attains the message; continuity handles the remaining points.
Full quadratics are retained, not formulas restricted to their winning arcs.

The inactive alternative has the single value

```
A_u = F_u(0)-p_u.
```

Retain any descendant support attaining this value. At `x_u=0`, changing
`z_u=1` to `z_u=0` removes exactly `p_u`; it imposes no new descendant
constraint. Descendants interact with the rest of the graph only through
`u`, so one optimal inactive descendant support suffices. Active alternatives
at `t=0` must remain available, especially when `p_u<0`.

## 3. Block elimination and the apparent extrapolation problem

For block `B` with parent vertex `v`, each vertex in `B\{v}` supplies either
one retained active quadratic or its inactive atom at zero. Add precisely
the cross terms assigned to `B`. Eliminate all active child variables by an
ordinary, unconstrained Schur complement.

This operation is valid for three separate reasons.

1. Every enumerated choice specifies a genuine complete internal support.
   Its quadratic formulas are exact conditional support values for every
   real child boundary value, including outside their original winning arcs.
2. The active Hessian is a Schur complement of a positive definite principal
   matrix of `Q`, so elimination has a unique finite optimizer. For parent
   value in `I`, the invariant-interval argument applies to the complete
   support and places every minimizing internal variable in `I`.
3. Given a true conditional optimum at `x_v=t in I`, its child boundary
   values lie in `I`. At each such value, replace the child descendants by a
   retained support attaining their message, or by the inactive atom.
   This preserves feasibility and the objective. The corresponding enumerated
   support therefore attains the true optimum after elimination.

The first point prevents a retained quadratic from creating an infeasible
underestimate when used beyond its winning arc. The third point prevents
pruning from losing the optimum. Both are needed. The argument also covers a
child optimum attained only at a tie: a retained neighboring interval formula
attains the same value there by continuity.

No step uses completeness of the edges within a block. Bridges are blocks
of size two. Isolated vertices can be solved directly. Therefore bounded
biconnected-block size is the correct graph hypothesis.

At the root, compare the inactive value with the minima of retained active
quadratics on `I`; then reconstruct the selected support and continuous
optimizer. The invariant interval contains an optimizer of every global
support problem, so this restriction loses no global optimum.

## 4. Expected construction time

Let `K_u` be the number of retained active quadratics at child vertex `u`.
The block enumerates

```
N_B <= product_(u in B\{v}) (K_u+1)
```

choices. The entire message at `u`, including its retained list, is a
measurable function only of noises in its own descendant subtree. Different
child-vertex subtrees of one block are disjoint. Hence the corresponding
`K_u` are independent. Shared deterministic matrix coefficients and a common
deterministic interval do not affect independence. Dependence between
ancestor and descendant message sizes is irrelevant to this product.

Writing

```
A = 2 + 8 n phi rho D M^2,
```

the scalar-envelope bound gives `E(K_u+1)<=A`, and therefore
`E N_B<=A^(b-1)`. A connected graph has at most `n-1` nontrivial blocks.

The required envelope construction does not use a quadratic-time pairwise
intersection list. For `N` distinct full quadratics, their lower envelope has
at most `2N-1` open pieces. In its winner sequence, `a,b,a,b` would force
three roots of the quadratic difference, and adjacent duplicate labels can
be merged. The resulting order-two Davenport--Schinzel bound is elementary:
partition around occurrences of the first label; the sets of other labels
in the intervening nonempty sections are disjoint, and induction gives
length at most `2N-1`. A divide-and-conquer merge compares two current
quadratics on each overlapping interval, solving at most two crossings.
It takes linear time in the two input envelope sizes, giving total
`O(N log N)` arithmetic, comparison, and quadratic-root operations.

Every retained formula has a support label, so `K_u<=2^m` for its `m`
internal indicators, and `log N_B=O(n)` deterministically. Thus only first
moments of the candidate counts are required; there is no unjustified
replacement of `E K^2` by `(E K)^2`.

All vertex merges together process at most `2 sum_B N_B` child-envelope
pieces. Their sorted breakpoint unions, support bookkeeping, and the block
constructions admit the coarse deterministic bound

```
O_b(n (n+sum_B N_B)).
```

For example, support labels can be integer masks with disjoint-subtree mask
sums, in the stated unit-cost arithmetic model; alternatively explicit labels
can be managed with at most linear-in-`n` overhead per generated formula.
Schur complements have dimension at most `b-1`. Reconstruction can use the
stored choices, or solve the selected rational principal system when the
deterministic data are rational. Consequently the claimed expected bound

```
O_b(n^2 A^(b-1))
```

is a valid coarse arithmetic bound. The case of isolated vertices also fits
this bound after direct preprocessing.

## 5. What the theorem does and does not establish

The result is an exact expected-polynomial construction algorithm for the
perturbed optimization problem, on graphs with bounded biconnected-block
size and a uniform strict diagonal-dominance margin. It addresses the gap
between a small expected envelope and efficiently finding that envelope.
Bounded degree is unnecessary. Every diagonal-dominance and density parameter
enters the bound explicitly; calling it polynomial in `n` alone requires
those parameters to be fixed or polynomially controlled.

This is not a theorem for all bounded-treewidth graphs. Two-vertex separators
would require a different envelope analysis. Nor is it a bit-complexity
theorem: the runtime treats real arithmetic, comparisons, and exact quadratic
roots as unit-cost operations, and the continuous noises are not finitely
encoded inputs. An exact finite-grid perturbation result would need a new
argument for atoms and ties. The algorithm optimizes the perturbed objective;
it does not recover an unperturbed exact optimizer in general.

The broader literature comparison in the source note still needs its own
novelty assessment. This proof review does not establish that no equivalent
smoothed dynamic-programming theorem exists.

## Verification record

This review independently reconstructed the maximum principle, term allocation,
off-atom formula, block elimination, exactness after pruning, sibling
independence, and first-moment runtime argument. The isolated-touch retention
clarification was communicated to the author and incorporated. The extension
to arbitrary bounded-size biconnected blocks was independently checked after
the coordinator proposed it. No computational experiment, Lean check, or
project-wide verification was run; the result rests on the written general
argument and the separately reviewed scalar-envelope proposition.
