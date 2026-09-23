# Research frontier scouting: sparse quadratic indicators

Date: 2026-09-22. Status: research note with a proved candidate obstruction,
not independently reviewed. The root agent supplied the inverse-polytope
projective-correlation observation; this scout developed the affine-face
version below. Publication priority remains unestablished.

The main unresolved target identified here is an exact compact conic
convexification of arbitrary tree-structured positive-definite quadratic
objectives with indicators, or a conic extension lower bound for their
epigraph hulls. The inverse-principal polytope used by a standard
convexification already has an unconditional obstruction, even for uniformly
well-conditioned stars. This does **not** settle the epigraph target.

## 1. Literature boundary checked against primary sources

[Choi, Fattahi, Han, Gómez and Lozano, *Convexification of Mixed-Integer
Quadratic Optimization via Decision Diagrams*, arXiv:2608.22815v1](https://arxiv.org/html/2608.22815v1)
provides the relevant exact decision-diagram construction. Its §7.2 gives
`O(n^(k+1))` nodes for a rooted tree with `k` leaves. Thus its tree formulation
is polynomial when the leaf count is fixed; the abstract must not be read as
a uniform polynomial-size theorem for arbitrary trees. Definition 7 stores
the unprocessed row matrix after orthogonal projection away from selected
processed rows. Its low-rank and inverse-tree results also exclude several
otherwise tempting rediscoveries.

[Bhathena, Fattahi, Gómez and Küçükyavuz, *A parametric approach for solving
convex quadratic optimization with indicators over trees*](https://link.springer.com/article/10.1007/s10107-025-02222-3),
published online in 2025, gives an `O(n^2)` algorithm for the unconstrained
continuous-variable problem on arbitrary trees. A new polynomial optimization
algorithm for exactly that problem would therefore not be a new tractability
result. This algorithm does not by itself supply a polynomial conic lift.

[The same authors, *Solving Convex Quadratic Optimization with Indicators
Over Structured Graphs*, arXiv:2603.02103v1](https://arxiv.org/html/2603.02103v1)
gives exact parametric algorithms under treewidth, volume growth, conditioning,
and a margin condition. Definition 5 bounds the number of locally near-optimal
support patterns. Theorem 1 and Corollary 1 retain dependence on these margin
parameters. This is not an unconditional exact polynomial algorithm at fixed
treewidth and fixed conditioning.

[Wei, Atamtürk, Gómez and Küçükyavuz, *On the convex hull of convex quadratic
optimization problems with indicators*](https://link.springer.com/article/10.1007/s10107-023-01982-0)
introduces the inverse-principal polytope used below and represents the
epigraph hull with that polytope plus one PSD constraint. Their §3.1 and
Theorem 1 establish the representation, while §5 studies the polytope's
equalities and gives a compact mixed-integer formulation for its vertices.
The mathematical object below is therefore established literature, not a
new reformulation. The candidate addition is a correlation face for a
particularly simple matrix family and the ensuing unconditional lift bounds.

[Liu, Atamtürk, Gómez and Küçükyavuz, *Polyhedral analysis of quadratic
optimization problems with Stieltjes matrices and indicators*](https://link.springer.com/article/10.1007/s10107-025-02272-7)
is a closer comparison. Its Theorem 2 characterizes the downward closure
of the inverse-polytope graph. Proposition 6 proves NP-hardness for the
upward closure already for a positive-definite diagonal-minus-rank-one
matrix. Section 4.4 explicitly distinguishes these relaxations from the
exact Stieltjes polytope. Thus inverse-polytope difficulty is already known;
the candidate addition below is an unconditional conic-size bound on sparse,
uniformly conditioned stars. Flipping the sign of the root coordinate makes
our matrix Stieltjes and induces an affine isomorphism of its inverse polytope.
The theorem therefore also applies inside their named class of Stieltjes
polytopes; it does not contradict their tractable downward-closure result.

Searches included `quadratic indicators treewidth two hardness`, `quadratic
indicators NP-hard banded`, `sparse regression condition number banded
NP-hard`, `quadratic inverse correlation polytope indicators`, and exact
phrase variants for star/tree hulls. No matching inverse-polytope face was
located. This limited search does not prove novelty. The relevant sections
of the primary full-text pages above were inspected; unrelated search hits
were discarded.

## 2. A correlation-polytope face for well-conditioned stars

For positive-definite `Q` indexed by `{0,...,n}`, define the established
inverse-principal polytope

```
P_Q = conv{(1_S, W^S): S subset {0,...,n}},
```

where `W^S` equals `Q[S,S]^-1` in its principal `S` block and zero elsewhere.
The empty-set matrix is zero. An inverse always exists on a nonempty principal
block because `Q` is positive definite.

Fix `m>=1`, set `n=2m`, `b=1/(2m)`, and take

```
Q = [1      b 1^T]
    [b 1    I_n ].
```

The support graph is a star. Its eigenvalues are `1` with multiplicity
`n-1`, and `1 ± b sqrt(n)`. Consequently `Q` is positive definite and

```
kappa_2(Q) <= (1+1/sqrt(2))/(1-1/sqrt(2)) < 6.
```

All entries are rational with `O(log m)` bits.

**Proposition.** `P_Q` has a face affinely isomorphic to

```
COR(m) = conv{a a^T: a in {0,1}^m}.
```

**Proof.** The equation `z_0=1` selects a face because every generating
indicator satisfies `z_0<=1`. On this face every generator has root active.
Write `z` for its leaf indicator and `k=sum_i z_i`. Block inversion gives

```
t = 1/(1-b^2 k),
W_00 = t,
W_0i = -b t z_i,
W_ii = z_i+b^2 t z_i,
W_ij = b^2 t z_i z_j                 (distinct leaves i,j).
```

In particular leaf off-diagonal entries are nonnegative. Therefore

```
sum_(i=1)^m W_(i,m+i) = 0
```

selects a face of the root-active face. At a generator it says that at most
one member of each leaf pair is active, because `b^2 t>0`. Thus `sum z_i<=m`
holds on this face. Taking its maximizing face `sum z_i=m` selects exactly
one active leaf per pair. Faces of faces are faces, so the resulting set
`F` is a face of `P_Q`.

Its generating leaf indicators have the form `z=(a,1-a)` for binary
`a in {0,1}^m`. They all have the same value

```
tau = 1/(1-m b^2).
```

Define an affine map from `F` to symmetric `m`-by-`m` matrices by

```
X_ii = z_i,
X_ij = W_ij/(b^2 tau)       for i != j, 1<=i,j<=m.
```

It maps the selected generators to `a a^T`, hence maps `F` onto `COR(m)`.
For the inverse, put `a=diag(X)`, `z=(a,1-a)`, and define the affine matrix

```
R(X) = [X              a 1^T-X             ]
       [1 a^T-X        11^T-a1^T-1a^T+X    ].
```

Then recover `z_0=1`, `W_00=tau`, `W_0i=-b tau z_i`, and the leaf block

```
W_LL = Diag(z)+b^2 tau R(X).
```

At a binary generator, `R(X)=(a,1-a)(a,1-a)^T`, so these formulas recover
the inverse-principal matrix exactly. Affinity extends both identities to
the convex hull. The maps are mutual inverses, proving the proposition. ∎

### Consequences and exact scope

Every exact conic lift of `P_Q` gives one of the same cone size for `COR(m)`:
add the face equations to its affine slice and compose its projection with
the affine map above. No algorithmic constructibility assumption is needed.

The established lower bounds therefore imply exponential LP extension
complexity, exponential total SOCP dimension, exponentially many PSD blocks
of any fixed order, and superpolynomial unrestricted PSD order. For example
the original Lee–Raghavendra–Steurer bound gives order
`2^(Omega(m^(2/13)))`; this is a valid bound, not a claim of the strongest
currently available exponent.

The lower-bound sources are [Fawzi and Parrilo](https://arxiv.org/abs/1311.2571)
for fixed-size PSD blocks and SOCP, and
[Lee, Raghavendra and Steurer](https://www.dsteurer.org/paper/sdpsize.pdf),
Theorem 1.1, for unrestricted SDP order. The transfer follows the same
affine-face principle as the earlier repository
[rank-one hull lower bounds](../results/rank-one-correlation-face-conic-lower-bounds.md).
All scalar inequality factors must be counted in a conic size claim.

This result obstructs exact compact conic representations of the **entire
inverse-principal polytope**. It is not a lower bound for the associated
quadratic-indicator epigraph hull. Wei et al.'s representation projects the
inverse variable out; a projection can be much simpler. In optimization over
the original epigraph, eliminating continuous variables uses a restricted
rank-one objective in `W`, not every linear functional of `W`. Thus the
obstruction is compatible with the polynomial algorithm on trees.

The practical inference is limited but useful: a universal compact exact
tree convexification cannot simply be obtained by compactly describing this
whole intermediate polytope. An alternative formulation might discard
inverse-moment information that the original epigraph does not need.

### Exact computation

An inline Python command using `fractions.Fraction` and SymPy enumerated all
root-active supports for `m=1,2,3,4`, inverted their rational principal
matrices, and checked pair nonnegativity, the selected face, its `2^m`
generators, constant `tau`, and the cross-product formulas. It passed all
340 root-active support checks. This checks finite cases and the algebraic
implementation, not the all-dimensional proof or priority. No project-wide
verification or CI inspection was performed.

## 3. A narrower obstruction to exact decision diagrams

For `n` leaves use the same star form with `b_i=2^(-i)` instead. Its condition
number is less than `(1+1/sqrt(3))/(1-1/sqrt(3))`, uniformly in `n`.
The exact projected-row states of Definition 7 in arXiv:2608.22815 require
exponentially many states for every variable order on this family.

At the layer immediately after `k=floor(n/2)` leaves have been processed,
consider their `2^k` support choices `S`. If the root is not yet processed,
the Gram matrix of the unprocessed projected rows has root diagonal

```
1 - sum_(i in S) 4^(-i).
```

If the root is already processed, fix its indicator to one. There is at least
one future leaf when `n>=2`. On the future-leaf set `U`, the residual Gram
matrix is

```
I_U - b_U b_U^T / (1-sum_(i in S)4^(-i)).
```

Both identities are Schur-complement formulas for the selected principal
block. Distinct `S` have distinct base-four sums, hence distinct Gram
matrices and therefore distinct stored projected-row matrices. All these
partial support choices are allowed. The layer consequently has at least
`2^floor(n/2)` exact states, regardless of variable order.

This is a representation-specific lower bound. It is weaker than the
inverse-polytope consequence in its formulation scope, but it additionally
explains why changing the variable order alone cannot solve the exact-state
growth problem. It does not exclude approximate state merging, objective-aware
pruning, or unrelated conic formulations. It has not had independent review.

## 4. Highest-potential next questions

1. **The tree epigraph itself.** Decide whether arbitrary tree Hessians admit
   polynomial-size exact SOCP or SDP epigraph lifts. Start with a star. A
   successful positive theorem would add exact scalable hulls beyond the
   fixed-leaf bound; a negative theorem would separate efficient optimization
   from compact conic representation for an important MIQP primitive. Neither
   the polytope face nor the DD obstruction proves the negative theorem.
2. **Exact precision at width two.** Determine the exact complexity of
   indicator quadratic optimization on bandwidth-two, uniformly conditioned
   Hessians without a margin assumption. A stable cumulative-state reduction
   from SUBSET SUM was sent to the root agent for separate development and
   independent review. Its candidate significance is a sharp transition
   from treewidth one to two and a barrier to logarithmic-accuracy algorithms;
   it should not be confused with fixed-additive-accuracy hardness.

The scalar-anchor convex-order route was also considered as a way to glue
star moments. The repository's
[reciprocal-anchor hull](../results/common-factor-reciprocal-anchor-full-hull.md)
already proves the central least-law mechanism, including binary leaves in
its [integer extension](../results/common-factor-integer-anchor-hull.md).
Merely replacing the reciprocal moment by a quadratic moment would be a
modest corollary, so it was not promoted as a main research target.
