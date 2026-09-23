# Direct-product lower bounds at fixed relative tolerance

Date: 2026-09-05. Status: promoted after independent review to
`results/spatial-bb-relative-gap-exponential-lower-bound.md`.

## Purpose and application model

Adding a conserved linear term to the earlier objective makes every cost
increasing and concave, a standard economies-of-scale allocation model.
On one growing block this shifts the optimum by `Theta(n)`, so its constant
absolute obstruction no longer gives a fixed relative-gap obstruction.
A direct product of fixed-size blocks restores the relative-gap conclusion.

Take integers `r>=1`, `t>=2r-1`, and `G>=1`. There are `G` blocks, each with
`3t` variables `x_(b,i) in [0,1]` and a demand balance

```
sum_{i=1}^{3t} x_(b,i) = K := t+1/2,  b=1,...,G.
```

The total number of variables is `n=3tG`. Minimize

```
C(x)=sum_{b,i} [x_(b,i)(2-x_(b,i))+d_(b,i)x_(b,i)],
```

where all coefficients `d_(b,i)` are positive and distinct, are strictly
increasing within each block, and `sum_i d_(b,i)<=eta` for every block.
Each coordinate cost has derivative `2-2x+d>0` and second derivative `-2`:
it is strictly increasing and strictly concave on its capacity interval.

For a spatial box, or arbitrary coordinate product domain, use the full
degree-`2r` moment/preordering relaxation from the higher-order/product-domain
results, with all `G` demand equalities and all their products through degree
`2r`. The SOS polynomials may couple variables across **all** blocks.
The node oracle is global, not a collection of separate local SDPs.
Arbitrary additional coupled valid inequalities are outside this model.

A relative-gap certificate at tolerance `theta in (0,1)` requires each
feasible leaf to have node bound at least `(1-theta)OPT`. This is implied
by ordinary pruning `LB>=(1-theta)UB` with a feasible incumbent `UB>=OPT`.

## Candidate theorem

Define

```
q0=t-2r+2 >= 1,
tau=1/4-theta(K+1/4)-eta.
```

If `tau>0`, every such relative-gap certificate has at least

```
(3/2)^(q0 G tau)
```

leaves (more generally, every pruned product-domain cover has this size).
For fixed `r,t,theta,eta` with `tau>0`, this is `2^{Omega(n)}`.
The program has a unique global minimizer. The explicit coefficient choice
below also removes all nontrivial variable-permutation symmetries, including
symmetries after using the demand equalities.

For example, with `r=1`, `t=2`, `theta=1/32`, and `eta=1/32`, one has
`K=5/2`, `q0=2`, and `tau=17/128`. Thus even global SDP–RLT needs at least

```
(3/2)^(17n/384)
```

leaves to certify the fixed relative gap `1/32` on these increasing-concave
cost allocation instances. The same conclusion applies to every fixed
higher order by choosing a fixed `t>=2r-1` and a sufficiently small fixed
relative tolerance.

## Proof

For each block choose independently a uniformly random ordered partition
`(H_b,M_b,Z_b)` into three sets of size `t`, and use witness
`w_b=1_(H_b)+p 1_(M_b)`, where `p=1/(2t)`. Every combined witness is feasible.

Fix a product domain containing a witness. In each block let `A_b` denote
coordinates whose local set excludes zero, `D_b` those excluding one,
and `R_b=A_b union D_b`. Construct a block functional as follows.

- If `|R_b|<q0`, use the earlier deterministic-restriction/
  fractional-cardinality functional on that block. At least `2r-1` endpoint
  coordinates of each type remain unrestricted, so the moment and all
  localizing constraints through degree `2r` hold. The penalty-objective
  contribution is at most `|R_b|/(2t)<=|R_b|/(2q0)`.
- If `|R_b|>=q0`, evaluate at the true block witness. Its penalty objective
  is `t p(1-p)=1/2-1/(4t)<=1/2<=|R_b|/(2q0)`.

Every block functional respects its demand equality, has first moments in
`[0,1]`, and satisfies every allowed block preordering inequality. Define
the global functional on monomials of total degree at most `2r` as the
product of the block functionals. It is normalized and respects each demand
equality multiplied by any allowed polynomial. The following tensor argument
checks that it is feasible for the global SOS/preordering oracle.

### Tensor positivity with total-degree bookkeeping

Take a product of local nonnegative generators `g=prod_b g_b` and a global
polynomial `p` with `deg(g)+2deg(p)<=2r`. Set `d=deg(p)`. For each block,
form the localizing matrix indexed by block monomials of degree at most `d`,
with entries

```
M_b(alpha,beta)=L_b[g_b x_b^alpha x_b^beta].
```

It is defined and PSD because `deg(g_b)+2d<=deg(g)+2d<=2r` and `L_b` satisfies
the block preordering. The tensor product of these PSD matrices is PSD.
Restrict its indices to tuples of block monomials whose **total** degree is
at most `d`. This principal submatrix has entries exactly the global
functional applied to `g` times products of those global monomials.
Therefore its quadratic form at the coefficients of `p` equals `L[g p^2]`
and is nonnegative. This verifies every global preordering constraint,
including SOS polynomials that couple distinct blocks. The larger tensor
matrix is only a mathematical Gram construction: it need not correspond to
globally defined moments beyond degree `2r`.

### Objective and counting

The constructed global functional has objective at most

```
G K + [sum_b |R_b|]/(2q0) + G eta.
```

The true optimum is at least `G(K+1/4)`, because each block penalty is at
least `1/4` and all perturbations are nonnegative. A pruned domain therefore
has

```
G K + [sum_b |R_b|]/(2q0) + G eta
>= (1-theta)OPT
>= (1-theta)G(K+1/4),
```

which implies `sum_b |R_b|>=2q0 G tau`.

The fraction of witnesses in a fixed product domain is a product of block
fractions, because the partitions are independent and the domain factors
by coordinate. In block `b`, all contained witnesses satisfy
`Z_b intersect A_b=empty` and `H_b intersect D_b=empty`, so its fraction is
at most

```
min{(2/3)^|A_b|,(2/3)^|D_b|} <= (2/3)^(|R_b|/2).
```

The whole domain therefore contains at most `(2/3)^(q0 G tau)` of all
witnesses. The cover union bound proves the lower bound. QED.

### Unique optimizer and perturbation coefficients

The objective and feasibility set are products across blocks, so the unique
optimizer in every block is the one proved in the higher-order result:
first `t` coordinates equal one, the next equals one half, and the remainder
zero. The concatenation is the unique global optimizer. To remove all
nonidentity coordinate-permutation symmetries, including those valid only
after using the demand equalities, use the explicit choice

```
d_(b,i)=eta [(b-1)3t+i]^2/(3t n^2),   b=1,...,G, i=1,...,3t.
```

All coefficients are positive and distinct; the largest is `eta/(3t)`, so
every block coefficient sum is at most `eta`. Any permutation preserving
the feasible set must map whole blocks to whole blocks: the row space of
the demand equalities consists of vectors constant on each block, and a
permuted block indicator must again be one block indicator. If it preserves
the objective on the feasible set, the corresponding coefficient vectors
can differ only by an additive constant within each block. The sorted
successive differences of squared consecutive indices distinguish every
block, so each block must be fixed. Within one block, a permutation of a
finite distinct coefficient set can differ by a constant only when that
constant is zero; strict distinctness then forces the identity.

Merely using distinct coefficients across blocks is insufficient for this
strong symmetry statement: additive block offsets vanish modulo the demand
equalities. The squared-index construction avoids that issue.

## Important scope: exploiting decomposition is a different certificate

This family decomposes into `G` independent fixed-dimensional allocation
problems. Solving each component and adding its exact bound is a short
certificate if that operation is allowed. The theorem shows that a single
spatial branch-and-bound tree using the stated global degree-`2r` oracle
cannot simulate those component certificates without exponentially many
leaves. It does not prove computational hardness of finding the optimum or
exclude decomposition algorithms. This limitation must accompany any
statement of the application consequence.

The same issue already exists for symmetry, knapsack-specific cuts, and
arbitrary nonlocal valid inequalities in the earlier results. Here the
specific practical conclusion is that exact component bounds can be more
valuable than a fixed-order global SDP combined with one spatial tree.

## Relation to previous results

The fractional-cardinality moments, local positivity, and endpoint witness
count come from the earlier reviewed notes. The new candidate ingredient is
the direct-product tradeoff with a global SOS oracle, producing a fixed
relative-gap obstruction for monotone concave allocation costs. Separate
novelty review has not yet been done. See the shared literature comparison
for existing spatial, binary SDP, and SOS lower bounds.


## Reproducible checks

`code/spatial_bb_lower_bound/check_relative_gap.py` passed exact equality
products and objective estimates on three two-block configurations, including
both fractional-cardinality and deterministic witness blocks. Numerical
checks passed for full global moment matrices of dimensions 13, 190, and
325 and sampled cross-block box localizers. The example's `tau=17/128` and
exponent `17n/384` were verified with exact rational arithmetic.
