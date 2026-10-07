# Exact strict-copositivity recognition with small articulation blocks

Date: 2026-10-02. Status: a direct algorithm and bit-length argument,
with a [fresh independent review](../reviews/articulation-copositive-elimination-review.md)
finding no substantive gap. A separate prior-art comparison remains
pending. The scalar-message mechanism is elementary; no novelty claim
is made.

## Scope and conclusion

Let `A` be a rational symmetric matrix and let its interaction graph join
`i,j` when `i!=j` and `A_ij!=0`. Suppose every biconnected block has at
most `p` vertices; bridges count as two-vertex blocks and isolated
vertices as one-vertex blocks. The block decomposition can be supplied
or computed.

There is an exact algorithm deciding whether

```
x'Ax>0 for every nonzero x>=0
```

in `2^p poly(I)` bit operations, where `I` is the rational input encoding
length and the polynomial exponent is absolute. It returns either a
rational nonzero witness `x>=0` with `x'Ax<=0`, or a verifiable elimination
trace establishing strict copositivity. No curvature, growth, or
uniqueness parameter is needed. The trace is verified within the same
parameterized bound.

This is a homogeneous orthant result. It is not an algorithm for general
box QP, and the graph assumption is stronger than bounded treewidth:
large biconnected graphs can have treewidth two. It does include arbitrary
trees of fixed-size blocks, with unbounded branching and repeated
articulation variables.

## Two exact calculations in at most p variables

### Strict copositivity by simplex faces

For a symmetric rational matrix `B` of order `k`, strict copositivity is
equivalent to positivity of the minimum of `u'Bu` on
`u>=0, sum u_i=1`. This minimum is rational and can be computed as follows.
For each nonempty support `S`, solve, when the bordered matrix is
nonsingular,

```
B_SS u=lambda 1,       1'u=1.
```

Keep the solution if `u>=0`. Its objective equals `lambda`. The smallest
retained value is the exact simplex minimum. In particular, a nonpositive
value provides a rational witness against strict copositivity.

To justify completeness despite singular stationary systems, choose a
global simplex minimizer with the smallest positive support. On that
support it satisfies the displayed stationary equations. If their
bordered matrix were singular, there would be a nonzero pair `(v,eta)`
with `B_SS v=eta 1` and `1'v=0`. Multiplying the first equation by the
minimizer gives `eta=0`. Necessarily `v!=0`; moving the minimizer along
`v` until a coordinate vanishes preserves its sum and objective, contrary
to minimal support. Thus at least one minimizing support has a nonsingular
bordered system. Every retained candidate is feasible, so extra stationary
candidates, including saddles, cannot lower the answer below the true
minimum. Singleton supports ensure the candidate set is nonempty.

This uses at most `2^k-1` rational linear solves. Positivity of coordinates
need not be imposed strictly when filtering candidates.

### Coercive orthant recourse

If `B` is strictly copositive, then for rational `b` the minimum

```
alpha=min_(y>=0) [y'By+2b'y]                         (1)
```

is finite and attained: a positive orthant growth constant for `B`
makes its quadratic term dominate the linear term at infinity.
Enumerate the empty support, giving candidate `y=0`, and every support
`S` for which `B_SS` is nonsingular. Solve

```
B_SS y_S=-b_S,
```

and keep nonnegative solutions, padded with zeros. The smallest candidate
objective is exactly `alpha`; store an attaining rational vector `k`.
In particular, `alpha<=0`.

Again, a global minimizer with the smallest positive support suffices.
If its stationary matrix were singular, a nonzero null vector would
preserve the objective along a feasible line segment to a smaller support:
`b_S'v=-y_S'B_SS v=0`. This contradicts minimality. Thus singular
principal matrices can be skipped safely. No check of the remaining
KKT signs is required for completeness: every retained point is feasible,
and some retained point is globally optimal.

## Leaf-block elimination

Disconnected components are processed independently; the full matrix is
strictly copositive exactly when each component is. Root the block tree
of a connected component at any block. Process blocks from the leaves.
At a nonroot block, let `v` be its parent articulation coordinate and
let `U` contain the other currently remaining coordinates of the block.
All descendant blocks have already been eliminated. The current quadratic
has the form

```
x_rest' C x_rest + y' B y + 2s b'y,
y=x_U,       s=x_v,
```

where `C` includes the entire current diagonal coefficient on `v`.
There is no separate `s^2` term in the leaf expression. This convention
avoids counting articulation diagonals twice. No coordinate in `U` has
an edge to the remaining graph except through `v`.

First test strict copositivity of `B` by simplex-face enumeration.
If it fails, its nonpositive witness, with all remaining coordinates
set to zero, is a nonpositive witness for the current matrix. Lift it
through earlier elimination records as described below and stop.

If `B` is strictly copositive, compute `alpha,k` from (1). Homogeneity
and attainment give the exact message, for every `s>=0`,

```
min_(y>=0) [y'By+2s b'y] = alpha s^2,                (2)
```

attained at `y=s k`. For `s>0`, substitute `y=s u`; for `s=0`, strict
copositivity gives minimum zero at `y=0`. Delete `U` and add `alpha` to
the diagonal coefficient of `v`. No off-diagonal fill is created.

Strict copositivity of the full current matrix is equivalent to strict
copositivity of this reduced matrix, provided the tested `B` is strictly
copositive. In one direction, attained recourse lifts every nonzero
reduced vector to one of the same value. In the other direction, if
remaining coordinates are nonzero, (2) bounds the full value below by
a strictly positive reduced value. If remaining coordinates are zero
but `y!=0`, strict copositivity of `B` gives a strictly positive value.

At the root, test its remaining matrix by simplex-face enumeration.
A failed test gives a rational nonpositive vector. A passed test, together
with all prior strict leaf tests and exact message identities, proves
strict copositivity of the original component.

## Witnesses and positive traces

Store one rational minimizing coefficient vector `k` for each eliminated
leaf. To lift a nonpositive vector from any later stage, reverse the
eliminations and set each removed vector to `y=s k`, where `s` is its
articulation coordinate. This preserves nonnegativity and the objective
exactly. It also preserves nonzeroness of the original failure vector.
An exact rational evaluation of the original quadratic verifies the final
witness.

For a positive result, retain the elimination order, updated diagonals,
strict private-matrix test results, and recourse values and witnesses.
A verifier can recompute the finite support calculations and check each
update. The proof above then establishes strict positivity for every
nonzero nonnegative vector. This is a parameterized verification trace,
not a claim that an arbitrary copositive matrix has a short PSD or SPN
certificate.

## Polynomial bit length does not follow from naive fraction recursion

There are `O(n)` blocks and at most `2^p` support calculations per block.
To obtain a bit bound, it is necessary to control intermediate numbers;
a recurrence which merely multiplies their current denominators is not
a sufficient argument.

Each completed scalar message has a direct meaning in the original
matrix: it is the minimum of an original subtree's quadratic with its
single boundary articulation fixed to one, excluding that boundary's
original unary term. All subtree-private coefficients and its boundary
linear coefficients are entries of the original input matrix. Previously
processed strict tests, followed by the current strict test, show that
the subtree-private quadratic is strictly copositive: elimination with
the boundary fixed to zero proves this by the same equivalence above.
Consequently the original subtree recourse problem is coercive and has
an attained minimum.

Choose a minimizing vector of that original problem with smallest
positive support `S`. By the recourse argument, the original principal
matrix `A_SS` on this support is nonsingular, and its positive coordinates
solve

```
A_SS y_S=-a_S,
```

where `a_S` consists of original boundary cross coefficients. Cramer's
rule bounds their rational encoding lengths by a polynomial in `I`,
independently of block-tree depth and `p`. The same holds for the message
value, obtained by evaluating the original quadratic there. For example,
clearing all original denominators uses only `O(I)` bits; determinants
have order at most `n<=I`, so their encoding lengths are polynomial in
`I` with an absolute exponent.

An articulation's current diagonal is its original diagonal plus at most
`n` such subtree message values. Summing them still has polynomial bit
length. Every local stationary system therefore has dimension at most
`p<=n` and coefficients of polynomial bit length. Exact Gaussian
elimination, feasibility comparisons, and candidate-value evaluations
have polynomial bit cost with an absolute exponent. This also covers
nonoptimal candidates encountered during enumeration. Reduced fractions
may be maintained by exact integer gcd operations.

The stored local vectors have polynomial encoding length. Lifting a
witness composes at most `O(n)` rational scalar multiplications along
block-tree paths, so its encoding length remains polynomial as well.
Thus the total bound is `2^p poly(I)` bit operations. The positive trace
and the failure witness satisfy the stated output bounds.

## Why this does not establish the bounded-treewidth target

The exact one-parameter message (2) relies on an unbounded nonnegative
orthant and homogeneity. Fixed box upper bounds would make the substitution
`y=s u` change the feasible set, and separators with two or more
coordinates would leave a nontrivial multivariate homogeneous value
function. Neither complication is treated here.

This result uses only the block-size parameter. It supplies a positive
class with arbitrarily many articulation blocks, but does not infer
tractability from treewidth alone, does not assert that its matrices
are SPN, and does not solve the general extraction-and-scaling question.
The relation to established copositive block decompositions and clique-sum
results needs a separate source comparison.

## Verification

An inline `python3 - <<'PY'` command using `fractions.Fraction`,
`itertools.combinations`, and `Random(26100231)` tested 120 rational
instances on chains of one, two, or three triangles. Leaf elimination
agreed with direct simplex-face enumeration on the entire matrix in
every case. All 75 nonpositive decisions produced lifted witnesses
whose original quadratic values were checked exactly. Three additional
rank-one or zero-matrix fixtures checked singular-face handling.
All checks passed. They do not establish the general bit bound or
replace the proof. The inline checker was not saved as a script.
The independent reviewer additionally ran
`python research-20261002/reviews/check_articulation_review.py`.
That persistent checker passed four support edge cases, twelve
articulation stars, nine rational chains, fourteen lifted nonpositive
witness checks, and one intermediate private-block failure with reverse
lifting. Those checks are separate from the author's inline experiment;
the [review](../reviews/articulation-copositive-elimination-review.md)
records their scope. No external search, project-wide verification, or
CI inspection was performed for this derivation.
