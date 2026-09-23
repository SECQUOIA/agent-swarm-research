# Independent review: rounding, profile counts, and PSD perturbation

Verdict: **PASS for the five modules reviewed.** Their statements and proofs
match the signed rounding and matrix perturbation arguments in Sections 3–5
of the DAG spectral approximation note. No mathematical defect or extra
nondegeneracy premise was found. This review does not certify the complete
DAG producer or its integration with these lemmas.

Reviewed files:

- [Rounding.lean](../../../Formal/DAGSpectral/Rounding.lean)
- [ProfileCount.lean](../../../Formal/DAGSpectral/ProfileCount.lean)
- [UpperTriangle.lean](../../../Formal/DAGSpectral/UpperTriangle.lean)
- [PSDAlgebra.lean](../../../Formal/DAGSpectral/PSDAlgebra.lean)
- [Perturbation.lean](../../../Formal/DAGSpectral/Perturbation.lean)

## Signed rounding and exact rational interpretation

`floor_residual` proves `0 <= x - h floor(x/h) < h` for every real entry,
assuming only `h > 0`. In particular, negative entries use mathematical floor,
not truncation toward zero. `path_residual_bounds` sums these inequalities for
any list of length at most `N`. Its separate empty-list case uses `N > 0` to
obtain the strict upper bound `N h`; it does not assume that a path has an edge.

`equal_label_sum_close` subtracts two residuals in `[0,N h)`. The resulting
bound is `< N h`, not `< 2 N h`. Both lists may be empty, and their lengths may
differ. Equality of the integer label sums is the only relation required
between them. `spectralMesh_pos` and `rank_mul_mesh` give the source mesh
`h = eta/(r N)` and the exact identity `r N h = eta` for positive rank and `N`.

`floorLabel_ratCast` proves equality with the actual rational floor of `x/h`;
`pathLabel_ratCast` extends it to the sum of rational labels. These are exact
scalar-extension results, with no numerical tolerance or floating-point
operation. The real definitions are noncomputable specifications. These
bridges alone do not prove execution time or bit bounds for a rational
producer; those remain obligations C04 and C05.

## Signed state-coordinate counts

`pathLabel_mem_coordinateRange` uses the actual path sum bound and rounding
residual to place every label sum in

```
[floor(-4 p N/h - N), floor(4 p N/h)].
```

This includes negative labels and all lengths from zero through `N`. In
particular, the lower endpoint retains the `-N` term. The interval is a safe
overestimate; neither endpoint must itself be attained by a path.

`floor_interval_card_le` bounds the number of integers by
`natCeil(b-a)+2`, including empty or reversed integer intervals. With the
positive mesh, `coordinateRange_card_le` substitutes the exact interval
width `8 p r N^2/eta + N`. Here this width is nonnegative, so the natural
ceiling represents the source ceiling without a discrepancy. The result is
exactly `C_r = ceil(8 p r N^2/eta + N)+2`.

`BoundedProfile` is a genuine finite integer-vector type, and its cardinality
is proved to be the coordinate-set size to the power `d`. `UpperCoord r` is
explicitly equivalent to the pairs `(i,j)` with `i <= j`; its cardinality is
`r(r+1)/2`, including rank zero. The resulting profile count therefore has
the source's exact exponent, rather than the larger exponent `r^2`.

These local modules do not identify this finite vector type with the actual
producer's states or prove state/output/operation counts; those connections
are covered by the [profile-DP review](profile-dp.md) and
[DP bit-cost review](dp-bit-cost.md). The noncomputable
`upperCoordIndex` is an existence-level finite equivalence, not a claim about
the implementation of coordinate enumeration.

## PSD order and perturbation

`Loewner A B` is the actual matrix condition that `B-A` is positive
semidefinite. The algebraic helpers preserve this condition under addition,
nonnegative scaling, and arbitrary rectangular congruence. There is no
invertibility requirement on the congruence matrix. The common-prior rule
requires a PSD prior and `eta >= 0`, precisely what its proof needs.

`entrywise_quadratic_bound` proves the exact bound

```
|x^T D x| <= n a sum_i x_i^2
```

from `|D_ij| <= a` and `a >= 0`. It sums the elementary pair bound
`a |x_i| |x_j| <= (a/2)(x_i^2+x_j^2)`. No dimension-dependent norm estimate is
assumed. Symmetry is then used explicitly by `entrywise_identity_bounds`
to construct both PSD inequalities `-n a I <= D <= n a I`. The statements
also handle dimension zero.

`relativeSandwich_of_entrywise` combines these inequalities with the actual
premise `I <= A`, matrix symmetry, and `n a <= eta`. It derives `eta >= 0`
from those premises and adds `eta(A-I)` to each relevant PSD difference.
The conclusion is exactly `(1-eta)A <= B <= (1+eta)A`; no positive-definite
prior, condition number, or eigenvalue oracle is assumed. The premise
`I <= A` must still be established by the normalization/owner construction;
this helper does not establish it itself.

`RelativeSandwich.kernel_iff` proves equality of the actual multiplication
kernels for PSD `A` and `B` and `eta < 1`. It uses the PSD quadratic-form
zero criterion and the strictly positive factor `1-eta`. Thus it includes
singular matrices and the zero matrix. A separate identification of ranges
from these kernels is not proved by the five reviewed files.

## Integration boundary

These modules supply P01, the numerical core of S01–S02, the kernel part of
S03, the coordinate-count part of C01, and the algebraic part of O06. Full
coverage of those obligations still requires their use with actual
normalized paths. In particular, a caller must prove that the prior cancels,
upper-triangular profile equality controls every entry by symmetry, the
target has normalized information at least `I`, and reconstruction uses the
same congruence matrix for the target and representative. No actual-path
existence or continuation claim is assumed proved by this review.

## Targeted verification

Run from `formal`, with `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```
lake build --wfail Formal.DAGSpectral.Rounding Formal.DAGSpectral.ProfileCount Formal.DAGSpectral.UpperTriangle Formal.DAGSpectral.PSDAlgebra Formal.DAGSpectral.Perturbation
lake env lean -DwarningAsError=true topics/21-dag-spectral/verification/RoundingReview.lean
```

The module build and final independent temporary client both passed. The
client checked a negative
rational floor, an empty path, equal profiles for different path lengths
including a negative edge, the concrete values `C_1=19` and interval size
`18` at `p=r=N=1, eta=1/2`, upper-triangle sizes at ranks zero and three, the
dimension-zero quadratic bound, and the zero-matrix kernel consequence.
Initial client drafts needed
explicit numeral casts, a matrix-notation import, and a linter adjustment;
these were client issues and required no changes to the reviewed sources.
`--wfail` is a Lake-build flag; direct Lean uses `-DwarningAsError=true`.

Selected axiom checks covered `floorLabel_ratCast`, `pathLabel_ratCast`,
`equal_label_sum_close`, `coordinateRange_card_le`, `card_upperCoord`,
`RelativeSandwich.kernel_iff`, and `relativeSandwich_of_entrywise`. All
reported only `propext`, `Classical.choice`, and `Quot.sound`. This was a
selected-declaration check, not the separate final topic audit. No
project-wide verification or CI inspection was run.

Reviewed source SHA-256 digests:

```
42d1318b0c6ddd5f3cc3ecb74dfa3d6c0f15931ebbe3d2a3278ef1e3ac50c741  Rounding.lean
ebcfebbb7363c96efdc80c8dfb30bed87a981b62fdc1caa1480e11b67494bb5a  ProfileCount.lean
5f94329e5e42186ce75d7a7f62ee3046443b296b8a9c2bd27ddcbcdd5df35522  UpperTriangle.lean
ef3182751f5bc9e05c6180ae0a09b1a8909bac8827f1e33622ffbe9c8ef3c87a  PSDAlgebra.lean
450af91626ba06c6560f5b3a172861f6ee37f3ed0417cee7a1ea6ac8141463ed  Perturbation.lean
```
