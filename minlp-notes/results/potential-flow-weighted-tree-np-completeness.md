# NP-completeness of weighted potential optimization on trees

Date: 2026-09-05. Status: independently reviewed supporting boundary;
two full proof audits and a bounded source comparison are complete. The capped-simplex convex quadratic
encoding of Subset Sum is elementary and is not claimed new. The proposed
contribution is its precise passive-flow interpretation and scope.

This differs from both pairwise pressure optimization and fixed-nomination
law uncertainty. The objective here is a linear combination of potentials
whose support can grow with the instance, and the uncertain quantities are
the nominations. All resistances are fixed.

## Construction and statement

Take positive Subset-Sum integers `w_1,...,w_n,K` with
`0<K<W=sum_i w_i`. Trivial targets can be decided during preprocessing;
fixed yes/no instances in this nontrivial range are available, for example
`w=(1,2),K=1` and `w=(2,2),K=1`. Thus the restricted source remains NP-hard.

Make a backbone path `v_1,...,v_n` and attach a distinct leaf `l_i` to
each `v_i`. Orient backbone edges from `v_i` to `v_(i+1)` and leaf edges
from `v_i` to `l_i`. This is a simple tree of maximum degree three.
Give backbone edges resistance one and leaf edge `i` resistance `1/w_i`.
Every edge obeys the quadratic law

```
pi_u-pi_v=beta_e x_e |x_e|.
```

The root `v_1` injects exactly `K`. Other backbone nominations are zero.
Leaf `l_i` withdraws `y_i in [0,w_i]`. The balanced nomination box is
therefore exactly

```
0<=y_i<=w_i,       sum_i y_i=K.                         (1)
```

It is nonempty. Physical flow on leaf edge `i` equals `y_i`; backbone
flows are the remaining downstream withdrawals, hence nonnegative. All
flows are determined by conservation on this tree, and rational
nominations produce rational potentials.

Consider the zero-sum linear potential objective

```
F(pi)=sum_i (pi_(v_i)-pi_(l_i)).
```

Every nonzero objective coefficient is `+1` or `-1`. Its support has
`2n` vertices. Leaf laws give the exact identity

```
F(y)=sum_i y_i^2/w_i <=sum_i y_i=K,                     (2)
```

with equality if and only if every `y_i` is either zero or `w_i`.
Consequently `max F>=K` if and only if the source subset sum is feasible.

**Theorem.** On this explicitly specified tree family, deciding
whether the maximum weighted potential objective is at least its rational
threshold is NP-complete. All resistances are fixed, the physical law is
common quadratic, the objective coefficients have magnitude one, and only
a balanced nomination box is optimized. The numerical source data may be
large; strong NP-hardness is not claimed.

For completeness on this family, the objective is convex in `y`, and a
maximum over (1) occurs at a vertex. Such a vertex has at most one
coordinate strictly between its bounds. Its coordinates are integers:
the remaining coordinate equals `K` minus a sum of integer upper bounds.
These give polynomial-size certificates, and (2) is evaluated by rational
arithmetic. At the reduction threshold, a subset itself is a certificate.

## A constant absolute objective gap

If no subset sums to `K`, every vertex maximizing the convex objective
has exactly one fractional coordinate, meaning one coordinate strictly
between zero and its upper bound. Write it as an integer `r` with
`1<=r<=w_i-1`. Its contribution to the deficit in (2) is

```
r-r^2/w_i = r(w_i-r)/w_i >=(w_i-1)/w_i >=1/2.
```

All other coordinates have zero deficit. Therefore

```
yes: max F=K,       no: max F<=K-1/2.                   (3)
```

A polynomial-time value approximation with absolute error at most `1/8`
would distinguish these cases. The same obstruction holds for a feasible
rational nomination whose objective is within `1/8` of optimal. For a
yes instance its value exceeds `K-1/2`, which can be checked exactly.

One can also recover a subset directly from a sufficiently good feasible
nomination. Put `m_i=min(y_i,w_i-y_i)`. Then

```
K-F(y)=sum_i m_i(1-m_i/w_i) >=(1/2)sum_i m_i.
```

Rounding each `y_i` to its nearest endpoint changes the sum by at most
`sum m_i`. If `K-F(y)<1/4`, the rounded integer sum is within `1/2` of
the integer `K`, so it equals `K` exactly. This explains why a returned
near-optimal nomination is enough for the reduction; no algebraic
pressure comparison is needed.

The gap is absolute and the threshold `K` grows. No relative approximation
barrier, strong hardness, or normalized-objective gap is claimed.

## Scope and relation to the other flow results

- A tree has block cycle rank zero. Thus bounded block rank alone does
  not give a nomination-optimization algorithm for arbitrary weighted
  potential objectives with growing support.
- The reviewed algorithms for a prescribed potential difference have two
  objective terminals. The present reduction uses a growing number of
  signed terms; it does not refute those algorithms.
- Fixed nominations on a tree fix every physical flow. A weighted
  potential objective is then linear in the edge resistances, so its
  interval or independent finite resistance uncertainty is easy. The
  source of difficulty here is the nomination choice.
- The objective cancels backbone drops by its definition as a sum of
  leaf-edge differences. No zero-resistance edges, extra operating
  constraints, or controllable physical elements are hidden in the model.
- Multiplying all resistances by `prod_i w_i` gives positive integers
  with polynomial binary encoding, scales both objective and threshold,
  and preserves the reduction. The displayed unscaled constant gap already
  suffices, so this scaling is optional.

The unrestricted linear-potential objective should not be described as
an ordinary single-pair pressure-drop objective. The bounded source comparison below found no matching statement with all
these physical restrictions; it does not establish publication priority.


## The full tree class is NP-complete

The membership argument extends beyond the reduction family. Consider any
rational tree with common quadratic laws, a nonempty balanced nomination
box, independent positive resistance intervals or explicitly listed finite
sets, and any rational zero-sum weighted potential objective. Deciding
whether its maximum is at least a rational threshold is NP-complete.
Deciding whether every scenario satisfies a rational upper objective bound
is coNP-complete. Objective support is unrestricted in these statements.

To prove membership, orient each edge and let `w_e` be its objective cut
weight, so that `c^T pi=sum_e w_e beta_e x_e|x_e|`. Conservation makes every
`x_e` a rational affine function of the nominations. For fixed nominations,
maximize over each resistance independently: choose its largest allowed
value when `w_e x_e|x_e|>=0` and its smallest allowed value otherwise.
At zero either endpoint works. Explicit finite sets and intervals therefore
have the same maximum, without changing the nomination domain.

Take a global maximizer and select a closed flow-sign cell containing it.
The nomination box intersected with balance and those sign inequalities is
a bounded rational polytope. On it the endpoint-eliminated objective is a
rational quadratic with polynomial-size coefficients. This quadratic has
a polynomial-bit rational maximizer, the classical rational-QP property
credited to Vavasis (1990).

One can see the certificate-size argument directly. At a maximum in the
relative interior of its minimal polytope face, the gradient annihilates
that face's tangent space. The face equations and this stationarity
condition form a rational linear system. Any two of its solutions on the
face have the same quadratic value: their difference is tangent, both
gradients annihilate it, and subtraction forces its quadratic second-order
term to vanish. Intersect this stationary affine set with the original
polytope and choose a rational vertex. The intersection is nonempty and
bounded; its data and a vertex's rational encoding have polynomial bit
length by linear algebra and determinant bounds. Enumerating the correct
face may take exponential time, but NP membership requires only existence
of the certificate.

A certificate consists simply of that rational nomination and the selected
allowed resistance endpoints. Conservation and path integration recover
rational flows and potentials, and exact rational arithmetic verifies the
objective threshold. The same rational maximizing certificate proves NP
membership for a strict violation of an upper bound. For coNP-hardness use
the comb reduction with upper bound `K-1/4`: a yes Subset-Sum instance
violates it, while a no instance has maximum at most `K-1/2`.

The [first tree-algorithm audit](../notes/review-potential-flow-fixed-support-weighted-tree-independent.md)
and [global-rank second audit](../notes/review-potential-flow-fixed-support-global-rank-second.md)
include independent checks of this general membership extension. The
[source assessment](../notes/potential-flow-fixed-support-weighted-tree-novelty.md)
identifies the classical rational-QP ingredient; see also
[Del Pia, Dey, and Molinaro, Theorem 3](https://arxiv.org/abs/1407.4798).

## A pseudopolynomial algorithm for this family

For each possible nonendpoint coordinate `i`, run the ordinary subset-sum
reachability dynamic program on the other capacities up to `K`. For every
reachable sum `s` with `0<=K-s<=w_i`, evaluate
` s+(K-s)^2/w_i `. The largest value over these choices is the exact
maximum, because a convex maximum occurs at a capped-simplex vertex.
Backtracking gives the withdrawals and hence the rational physical state.
This uses `O(n^2 K)` arithmetic operations with polynomial-size rational
values. It confirms the ordinary numerical hardness scope of this family;
it is not a polynomial algorithm in the binary input length.

## Review, verification, and attribution

Both the [first audit](../notes/review-potential-flow-weighted-nomination-tree.md)
and [second audit](../notes/review-potential-flow-weighted-nomination-tree-hardness-second.md)
passed. The first independent checker evaluated 100 complete capped-simplex
instances, 1,751 exact physical vertices, and 2,000 rational mixtures. The
second review exhaustively checked 2,784 small instances. The reproducible
[first checker](../code/potential_flow_mpd/check_weighted_nomination_tree_review.py)
checks the physical construction as well as the objective identity.

The [source assessment](../notes/potential-flow-weighted-nomination-tree-novelty.md)
credits the established continuous convex knapsack reduction. In particular,
[Levi, Perakis, and Romero (2014), Proposition 1](https://www-2.rotman.utoronto.ca/facbios/file/CKP%20ORL.pdf)
uses endpoint forcing in a separable convex continuous knapsack problem to
encode Subset Sum. The retained contribution is the precise passive-flow
boundary with fixed resistances, degree-three trees, unit-magnitude objective
coefficients, and nomination uncertainty. No new knapsack mechanism is claimed.
