# Independent review: strict copositivity on small articulation blocks

Date: 2026-10-02. Verdict: **PASS**. The reviewer read the complete actual
[elimination note](../new-direction/articulation-copositive-elimination.md).
Its exact recognition and witness claims follow from the displayed finite
support calculations, homogeneous scalar messages, and original-subtree
bit argument. No substantive correction was required. This review does
not establish novelty relative to classical copositive block decompositions;
that comparison remains a separate literature task.

## 1. Singular supports do not invalidate either enumeration

For the simplex minimum, choose a global minimizer with minimal positive
support. Its support stationarity system is

\[
 B_{SS}u=\lambda\mathbf1,\qquad\mathbf1^Tu=1.
\]

If the bordered system is singular, a nonzero kernel pair satisfies
`B_SS v=eta*1` and `1'v=0`. Multiplying by `u` and using its stationarity
gives `eta=0`. The vector `v` cannot vanish. Moving in this zero-sum null
direction until a coordinate first becomes zero stays in the simplex and
preserves the objective, contradicting minimal support. Thus some
minimizing support has a nonsingular bordered system. Singleton supports
always give candidates, including when their diagonal coefficient is zero.
Filtering by weak nonnegativity is harmless: each retained candidate is
feasible, so a non-minimizing stationary point cannot produce a value below
the true minimum.

Strict copositivity gives a positive minimum on the nonnegative unit
sphere. Consequently `y'By+2b'y` is coercive on the nonnegative orthant.
For a minimum with smallest positive support, singular `B_SS` would supply
a null direction `v` with `b_S'v=0`. Moving to the first support boundary
preserves feasibility and objective. Hence an attaining support has a
nonsingular principal matrix and is enumerated. The empty support supplies
the zero candidate. A stationary saddle may also be enumerated, but again
its feasible value cannot spoil the minimum calculation. There is no
unjustified requirement that every principal matrix be positive definite.

Each calculation therefore needs at most `2^k` rational linear systems
in dimension at most `k+1`, and returns a rational minimizer when needed.

## 2. Scalar messages and the strictness test

Interpret the rooted block tree as the usual block-cut tree. Once all
descendants of a nonroot block have been eliminated, its private vertices
have no edges to the unprocessed graph except through its parent
articulation `v`. The current diagonal of `v` stays wholly in the remaining
quadratic; it is not counted again in the leaf expression.

If the private matrix is not strictly copositive, a nonpositive private
witness with all remaining variables zero already disproves strict
copositivity of the current problem. Positive or negative couplings to
the parent cannot repair this failure, because the parent is zero.

Otherwise strict copositivity makes the recourse minimum finite and
attained. Homogeneity proves, for every `s>=0`,

\[
 \min_{y\ge0}(y^TBy+2s b^Ty)=\alpha s^2,
 \qquad y=s k\text{ attains it}.
\]

The zero case uses strict copositivity explicitly: when `s=0`, zero is
the minimum and is attained at `y=0`. The diagonal update by `alpha`
creates no off-diagonal fill. Strict copositivity of the reduced matrix
is equivalent to that of the current matrix: nonzero remaining vectors
are covered by the reduced strict inequality; vectors supported only in
the deleted variables are covered by the private strict inequality.
These two cases are both needed.

Sibling branches may share the same articulation. Each excludes its
boundary diagonal and contributes only its own scalar update, so arbitrary
branching does not double-count a unary coefficient. Disconnected
components and isolated vertices are handled by the stated component and
root tests.

## 3. Witness lifting and positive verification traces

Reversing completed eliminations and setting `y=s k` restores deleted
coordinates at exactly their attained recourse values. It preserves the
quadratic value, nonnegativity, and nonzeroness of a failure witness.
The same procedure applies to a failure at an intermediate private block,
not just a failure at the root. Direct evaluation in the original rational
matrix independently verifies the returned witness.

For a positive result, a verifier recomputes every local support enumeration
and diagonal update. This is a `2^p poly(I)` verification trace, rather
than an unsupported claim of a polynomial-time PSD/SPN certificate for
each local copositive matrix. Storing only a recourse minimizer would not
prove that its value is globally minimal; the specified recomputation
supplies that missing inequality.

## 4. Polynomial bit lengths across arbitrary depth

The direct original-subtree interpretation is valid and essential.
A completed message is the minimum of a subtree quadratic with its one
boundary coordinate fixed to one, excluding that boundary's original
unary term. All private unary and cross coefficients in this uneliminated
problem are original input entries. Messages from siblings outside that
subtree are not part of it.

The prior private strict tests and the current strict test prove strict
copositivity of the whole subtree-private matrix by applying the same
elimination equivalence with its boundary fixed to zero. Thus the original
subtree recourse is coercive. A minimum of minimal positive support solves
a nonsingular system with original rational coefficients. Clearing the
original denominators and applying determinant bounds in dimension at
most `n` gives a polynomial bound on its coordinates and objective value,
with an absolute exponent. This bounds every scalar message independently
of elimination depth.

An updated articulation diagonal sums at most `n` such values and its
original diagonal, so its reduced rational numerator and denominator
still have polynomial bit length. Local stationary systems have dimension
at most `p<=n`; rational elimination on them preserves a polynomial bit
bound even for candidates that are not ultimately selected. This last
point is needed to bound the actual enumeration algorithm, rather than
only its best answers.

Finally, a lifted coordinate is obtained through at most `O(n)` scalar
multiplications of stored polynomial-bit rationals. Product bit lengths
add, so witness recovery remains polynomial. There are `O(n)` blocks and
`O(2^p)` support calculations per block, establishing the claimed
`2^p poly(I)` bit complexity and output bounds. The proof does not rely
on a naive denominator recurrence or on unit-cost rational arithmetic.

## 5. Scope and significance

The algorithm is for strict positivity of a homogeneous quadratic on an
unbounded nonnegative orthant. It returns a zero-value witness as a valid
failure of strictness. It does not decide non-strict copositivity by the
same argument, since the strict private coercivity condition could fail.

Fixed box upper bounds break the scaling substitution, and a separator
with two free coordinates generally leaves a genuine multivariate value
function. Bounded biconnected-block size is therefore the stated parameter,
not treewidth alone. The proof neither assumes that those blocks are SPN
nor derives an SPN decomposition. It provides a useful exact baseline for
trees of bounded-size blocks, including connected fan chains, without
settling the broader sparse nonconvex optimization target.

## 6. Targeted independent diagnostic

The reviewer ran

```sh
python research-20261002/reviews/check_articulation_review.py
```

The [persistent checker](check_articulation_review.py) uses exact rational
linear algebra and passed:

- Four support edge cases, including singular strictly copositive private
  matrices, a singular simplex face, and a feasible stationary saddle.
- Twelve articulation stars, up to 64 triangles sharing one variable.
  Their private matrices are rank-one all-ones matrices; known sums of
  squares plus a signed root coefficient determine the expected answer.
- Nine rational chains, up to 64 edges, including a positive residual
  `2^-80`, a zero residual, and a negative residual. Fourteen nonpositive
  cases returned witnesses verified in the original matrix; long-chain
  witness bit lengths obeyed the explicit fixture bound.
- One failure in an intermediate private block, after an earlier leaf
  elimination. Reverse lifting restored the removed coordinate and
  preserved an exact zero value.

Small star cases were also compared against full simplex-face enumeration.
The larger fixtures use independently known algebraic forms for their
expected strictness. These finite checks do not establish the universal
bit bound or replace the minimal-support and elimination proofs. The
author's separately reported random triangle-chain test was not rerun.
No project-wide checks, CI inspection, external source search, or index
edits were performed.
