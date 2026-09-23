# Adversarial audit of the star inverse-polytope obstruction

Date: 2026-09-22. Reviewer: a fresh agent, independent of the scout derivation.
Scope: Sections 2 and 3 of
[the frontier scout](research-20260922-frontier-scout.md), their cited conic
lower bounds, and the distinction from the original epigraph hull.

**Verdict.** The correlation face and the claimed exact conic-size transfers
are correct. The exact projected-state decision-diagram argument is correct
and strengthens to width at least `2^(n-1)` for every order of an `n`-leaf
star. No epigraph-hull lower bound follows from these arguments. The novelty
assessment must remain provisional; the contribution is an obstruction for
an established intermediate polytope, not a new hardness theorem for solving
unconstrained tree quadratic-indicator optimization.

## 1. Face, inverse map, and conditioning

Independently derive the principal inverse for an active root and leaf set
`S`. With `k=|S|`, block elimination gives Schur complement
`d=1-b^2 k`, reciprocal `t=1/d`, root-leaf entries `-bt z_i`, and leaf block
`Diag(z)+b^2 t zz^T`. All denominators are positive because
`b=1/(2m)` and `k<=2m` give `d>=1-1/(2m)>=1/2`.

The three face restrictions are valid in the stated order. First `z_0=1`
is a face. On that face, the paired off-diagonal entries are nonnegative,
so their zero sum selects a face and forces at most one selection per pair
at every positive-weight atom. On this second face, cardinality at most `m`
is valid, so maximizing it selects exactly one leaf per pair. A face of a
face is a face; no global validity of the cardinality bound is needed.

On the resulting face `t=tau=1/(1-mb^2)` is constant. For binary
`a in {0,1}^m`, the leaf indicator is `(a,1-a)`. The proposed cross block
`a1^T-X` has entry `a_i(1-a_j)`, the opposite cross block is its transpose,
and the bottom-right block has entry `(1-a_i)(1-a_j)`. Consequently the
displayed affine inverse recovers every coordinate on every atom. Since the
forward and inverse maps are affine, both identities extend to convex
combinations. Surjectivity alone would not prove isomorphism; this explicit
inverse supplies the missing property and is correct.

The eigenvalue calculation is also correct: the leaf subspace perpendicular
to `1` has eigenvalue one, and the remaining two eigenvalues are
`1+-1/sqrt(2m)`. The stated bound below six follows. The matrix actually
converges to the identity in operator norm as `m` increases, while the exact
face remains. This observation does not imply a robust approximation bound:
the inverse map scales off-diagonal coordinates by `1/(b^2 tau)`.

Sign congruence by `D=diag(-1,1,...,1)` gives a Stieltjes matrix. For each
support, its padded inverse is `D W^S D`. Thus the map `(z,W)->(z,DWD)`
really is an invertible linear map of the entire polytopes, and preserves
their lift complexities.

### An explicit exposure, supplementary to the scout proof

The following affine functional exposes exactly the same face:

```
g(z,W) = (m+1)(1-z_0)+m-sum_leaf z_i
         +b^(-2) sum_(i=1)^m W_(i,m+i).
```

At a root-inactive atom the inverse on the leaves is diagonal, so
`g=2m+1-k>=1`. At a root-active atom let `p` count fully selected pairs.
Then `k<=m+p`, and

```
g=m-k+t p >= (t-1)p >= 0.
```

If `p>0`, then `k>0` and `t>1`, so the inequality is strict. If `p=0`,
equality holds exactly when `k=m`. This proves the exposure. Its coefficients
are integers of size at most `4m^2`. Every off-face atom has `g>=b^2`:
root-inactive atoms have gap at least one; root-active atoms with `p=0`
have integer gap at least one; and for `p>0`,
`g>=(t-1)p=b^2kp/(1-b^2k)>=b^2`.

This last estimate is a simple atom-level stability observation. No
approximate extension-complexity theorem is claimed here. The root agent
should independently recheck this supplementary exposure before promoting
it as an audited result.

## 2. Exact conic-size statements checked against primary sources

For a lift `P_Q=pi(C intersect L)`, impose the three face equations on
`pi(y)` and then compose with the forward map to `COR(m)`. This gives a lift
over the same cone. The forward map is linear, so affine-versus-linear output
conventions cause no issue. No strict feasibility, conic duality, or closure
of arbitrary projections is needed for this transfer.

[Fawzi and Parrilo, Theorem 1, PDF page 3](https://arxiv.org/pdf/1311.2571)
gives, for fixed `d` and `m>=d`,

```
r >= (3^d-1)^(-(1-1/d)) (1-3^(-d))^(-m/d)
```

for a lift using `r` PSD blocks of order `d`. For order two their stronger
bound is `r>=7^(-1/2)(9/7)^(m/2)`. The same page explicitly reduces a
Lorentz cone `{(t,x): ||x||<=t}` with `x in R^k`, `k>=2`, to `k-1`
three-dimensional Lorentz cones. Each is isomorphic to `S_+^2`. A
two-dimensional Lorentz cone is two scalar nonnegative cones; a scalar cone
fits in one order-two PSD block. Thus total SOC dimension `D` gives at most
`D` order-two blocks, and `D>=7^(-1/2)(9/7)^(m/2)`. Arbitrary factor
dimensions are allowed. The conclusion is **not** an exponential number of
SOC factors if their dimensions are unbounded. Scalar inequalities count.

[Lee, Raghavendra and Steurer, Theorems 1.1 and 5.4, PDF pages 5 and
34](https://www.dsteurer.org/paper/sdpsize.pdf) state a lower bound
`q>2^(alpha m^(2/13))` for correlation-polytope PSD order, with an absolute
positive constant `alpha`. This is the cited exponent, not an assertion of
the best bound available today. Multiple PSD blocks can be placed on one
block diagonal, with order equal to the sum of their orders, so the same
lower bound holds for total PSD order. Scalar inequalities again count as
order-one blocks.

## 3. Decision-diagram audit and strengthening

[Choi et al., Definition 7 and its preceding state
definition](https://arxiv.org/html/2608.22815v1#S4.SS3) store the future rows
after projection onto the orthogonal complement of selected past rows,
together with the discrete completion data. Their quadratic Hessian is
`Q=F F^T`. Therefore the stored row matrix has Gram matrix

```
G_U(S)=Q_UU-Q_US Q_SS^(-1) Q_SU,
```

where `S` is the selected part of the processed prefix, and `U` comprises
all unprocessed indices. A difference between these Gram matrices certifies
a difference between the stored row matrices, regardless of the particular
factor `F`.

Use `b_i=2^(-i)`, with indices `i=1,...,n`. At the layer immediately before
the **last leaf** is processed, `n-1` leaves have been processed and one
leaf remains. If the root is also processed, restrict its indicator to one;
otherwise it remains future. Vary every processed-leaf support `S`.

If the root remains future, its residual diagonal is
`1-sum_(i in S)4^(-i)`. If it was processed, the future-leaf Gram matrix is
`I_U-b_U b_U^T/(1-sum_(i in S)4^(-i))`. All `b_i` are nonzero. Distinct
subsets have distinct sums: at the first differing index, its weight exceeds
the sum of every later weight. Thus all `2^(n-1)` subsets give distinct
Gram matrices in either case. Every prefix is allowed because there are no
combinatorial support restrictions. This proves width at least `2^(n-1)`
for every order. If the root is last, its preceding layer has `2^n` states.

The norm estimate `sum_i b_i^2<1/3` gives the asserted condition bound.
The entries have encoding length polynomial in `n`, although some are
exponentially small. This is an exact-state lower bound, compatible with
approximate merging. It does not rule out other exact state definitions,
cost-dependent pruning, or an unrelated small epigraph lift.

## 4. Significance and limits of novelty

[Liu et al., Section 4.3, Proposition 6](https://link.springer.com/article/10.1007/s10107-025-02272-7)
already prove NP-hardness of optimizing over the coordinatewise upward
closure for a positive-definite diagonal-minus-rank-one matrix. Their
objective selects an off-diagonal inverse entry with a nonnegative
coefficient, so upward closure does not alter that optimum. Thus this also
supplies prior computational hardness of the inverse graph itself. Their
result is a closer predecessor than generic quadratic-indicator hardness.
The star face contributes a sparse, uniformly conditioned family and
unconditional conic-size lower bounds that need no construction or bit-model
assumption. It is not the first indication that inverse-principal polytopes
can be difficult.

Additional web searches used `"inverse" "polytope" "correlation"
"Stieltjes"`, `"star" "inverse" "extension complexity" quadratic
indicators`, and `"principal" "inverse" "correlation polytope"`.
No matching star-face theorem was found; most hits were unrelated covariance
realization papers. This is weak novelty evidence and does not establish
priority. The relevant primary source definitions and theorem statements
above were inspected directly.

The epigraph limitation is essential. The standard formulation projects out
the inverse matrix; a lower bound for the intermediate polytope does not
survive an arbitrary projection. On the displayed correlation face, even
the projection retaining all `z`, all inverse diagonals, and every inverse
entry on the star edges is simply an affine copy of `[0,1]^m`: these
coordinates depend only on `a`, while the pairwise moments reside in the
leaf-leaf inverse fill. This is a concrete reason that keeping less inverse
information might avoid this particular obstruction.

Adding all second moments of the original continuous variables would make
a lower bound easier, but would change the problem substantially. Indeed,
for the full moment hull `conv{(z,x,X): z binary, x_i(1-z_i)=0,
X=xx^T}`, the valid inequality `sum_i(X_ii-2x_i+z_i)>=0` selects the face
`x=z` and hence `X=zz^T`. This works even for a diagonal Hessian. A lower
bound for that enriched hull therefore would not resolve the tree epigraph
question and is not a worthwhile replacement target.

## 5. Targeted exact verification

Executed one inline command `python - <<'PY' ... PY`, using SymPy rational
principal-matrix inversion. It enumerated all root-active supports for
`m=1,2,3,4`, checked every inverse leaf entry, the paired zero face,
cardinality, the complementary-pair form, the constant denominator, and
the entire affine inverse. It then enumerated every variable order for
`n=1,2,3,4`; at the layer before the last leaf it formed the full exact
Schur complement directly and checked both displayed residual formulas and
the number of distinct residual matrices. Output:

```
PASS: 340 star-face support checks; 152 variable orders and 1070 exact DD residual states
```

A second inline `python - <<'PY' ... PY` command used `fractions.Fraction`
and enumerated both root choices and every leaf support for `m=1,...,6`.
It checked the supplementary exposing functional, its exact zero set, and
the lower bound `b^2` at every off-face atom:

```
PASS: exposing functional and atom gap on 10920 supports
```

These finite checks independently challenge the algebra and the strengthened
choice of layer. They do not prove the all-dimensional theorem, certify
novelty, or verify the external conic lower-bound proofs. No project-wide
verification or CI inspection was performed.
