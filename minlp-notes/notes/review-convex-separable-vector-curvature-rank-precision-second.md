# Independent second audit: coupled separable convex vector precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.

**Status: PASS.** I independently checked the full argument in [the candidate](convex-separable-vector-curvature-rank-precision.md), including its shared curvature basis, comparison with the original vector integer minimum, simultaneous graph containment, finite constants, and polynomial rational encoding. The box bound is `p_out <= p_conv+n ceil(log2 r)+17n`; the compact unconditional polyhedral body bound has `18n` in place of `17n`. These statements use active input coordinates and the single concatenated curvature rank specified in the candidate. This audit is a correctness assessment, not a claim of literature novelty.

## Shared basis and convexity

Selecting one approximate barycentric spanner from the concatenated normalized coefficient rows is essential and valid. The same row coefficients reconstruct every coordinate's nonlinear coefficients, so every coordinate's remaining difference is affine. They therefore reconstruct its chord gaps exactly. All selected rows are original normalized outputs, and all their univariate summands are convex. Consequently signed reconstruction coefficients bounded by two imply `0 <= g_ji <= 2 sum_s g_si`. If the selected sum is affine in a coordinate, every original summand is affine in that coordinate.

I also checked the basis algorithm imported from the output-rank dependency. Restricting to independent coefficient columns loses no row relation. Each exchange with a coefficient of magnitude greater than two increases the absolute basis determinant by that factor. A product of the input denominators gives a polynomial logarithmic lower bound on a nonzero minor; Hadamard gives a polynomial logarithmic upper bound. Every intermediate basis remains an original rational submatrix. The number of exchanges and every rational inverse's encoding length are polynomial. There is no maximum-determinant oracle assumption. Barycentric spanners and determinant exchange are classical; see Awerbuch and Kleinberg, Section 2.3 of [Adaptive Routing with End-to-End Feedback](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf).

## Packing and comparison with the correct optimum

A finite maximal scalar set with pairwise midpoint gaps greater than the local tolerance exists by compactness and uniform continuity. Its compatibility intervals cover the domain. The reviewed scalar refinement gives `N_tau <= 6P`, and the scalar compiler's actual cell count gives `2^L <= 5832P`, including a one-cell construction.

Midpoint Jensen gaps are superadditive over ordered consecutive intervals. This follows directly from the convex-function tent-kernel formula; the longer interval's tent dominates the tent on each disjoint child interval. Thus an index difference of `h` contributes more than `h tau`. In the box case, `tau=1/(2n)` and product index distance greater than `2nr` force the selected sum's gap to exceed `r`. At least one of its `r` original normalized output components then has gap greater than one. This is incompatibility in the original vector error box. The argument does not substitute a scalar optimum with a different tolerance.

The geometric-series lattice bound is correct: a ball of radius `anr` in `Z^n` has fewer than `[3(2a+1)r]^n` points. Taking `a=2` yields `(15r)^n`; taking `a=4` yields `(27r)^n`. Greedy packing and the general-integer parity principle therefore give the claimed lower bounds on `p_conv`. General integer witnesses may be unbounded: same-parity witnesses still have an integral midpoint, which is all this argument needs. Neither the maximal scalar sets nor the product code is computed by the algorithm.

## Box graph containment and size

Each coordinate uses one local cell and one interpolation weight for every original output. The selected sum's chord gap is at most `13/(32n)`. Gap domination makes each original normalized output's total exact chord gap at most `13/16`. Downward rounding each coordinate endpoint by at most `1/(8n)` makes its total interpolated rounding error at most `1/8`. Therefore the band `[y_j-13/16,y_j+1/8]` contains the exact graph and admits normalized errors at most `15/16` in either direction.

This remains true simultaneously for all outputs because the same coordinate input and interpolation weight are used throughout. Affine terms are restored exactly. Endpoint evaluation, signed numerator offsets, Boolean circuit wires forced by the index bits, and binary-times-continuous products use the reviewed scalar compiler. No product between interpolation weights of different coordinates is introduced. Extra outputs add only polynomially many continuous variables and rows. The declared integer count is precisely the sum of local index lengths.

The count constant checks: `5832*15=87480 < 2^17`. Normalizing rational coefficients, forming the selected sums, evaluating original summands at polynomial-bit rational knots, and choosing the rounding precision all preserve polynomial encoding length for the supplied dense separated representation.

## Compact unconditional polyhedral bodies

For `K={e:A|e|<=b}`, with nonnegative rational `A`, positive rational `b`, and compact `K`, the normalized facet functions are convex separable. Apply the single shared basis to their concatenated nonlinear rows. At local tolerance `1/(4n)`, the exact coordinate chord gaps sum to at most `13/32` **for each facet**. The original vector chord gap is componentwise nonnegative, so this is precisely membership in `(13/32)K`.

Let `M_A=max_k sum_j A_kj/b_k`. Compactness ensures `M_A>0`. Rounding each original coordinate endpoint by at most `min(1,1/(16nM_A))` places the sum of rounding errors in `K/16`, including the case where the minimum chooses one. The rounded center is consequently within `(15/32)K` of the true vector. The band `w-y in K/2` contains the graph and lies in its `(31/32)K` error tube. Continuous absolute-value auxiliaries encode this band exactly because `A` is nonnegative.

Product distance greater than `4nr` forces one selected original facet's midpoint gap above one. Since the original output midpoint gap is componentwise nonnegative, this violates the original body. The count follows from `5832*27=157464 < 2^18`. Compactness also ensures every output column is observed by a positive facet coefficient, so rank zero and discarded affine coordinates really have only affine original outputs. Weighted l1 error is the stated one-facet rank-one special case.

## Exact independent checks

I wrote and ran [the exact rational checker](../code/quadratic_rank/check_coupled_separable_rank_review.py). Across twelve examples with multiple inputs and coupled convex outputs, it checks box and facet bases against the full concatenated rows, including negative reconstruction coefficients, and verifies simultaneous vector bands at rational points. The result was:

```
PASS: 24 shared bases (31 determinant exchanges, 39 negative representation entries); 540 gap dominations; 300 box bands; 600 coupled-body errors
```

These checks support the proof and specifically exercise signed polynomial coefficients and shared coordinate interpolation. They do not replace the analytical scalar compiler or prove a new oracle implementation.

The theorem's exclusions are necessary and correctly stated: this audit does not cover general mixed multivariate polynomial terms, sparse binary-encoded enormous degrees, or error bodies with signed tilted facets. No unresolved mathematical or encoding issue remains in the stated scope.

## Addendum: finite continuous-convex companion

I also independently checked [the finite companion](convex-separable-vector-finite-rank-precision.md). **PASS.** Its statements allow arbitrary continuous convex univariate summands and finite real-coefficient formulations, with no computability or polynomial-size claim.

The normalized output rows span a finite-dimensional subspace of the direct sum of function spaces modulo affine functions, even when those function spaces themselves are infinite dimensional. Choosing coordinates on that span permits the ordinary maximum-determinant basis argument on the finitely many rows. The coefficient bound is one, and the same coefficients work in every input coordinate. Thus each original coordinate chord gap is dominated by the selected sum's coordinate gap without the factor two used by the constructive polynomial theorem.

For box error, local tolerance `1/n` yields coordinate partitions with `N_i<=6P_i` and index capacities `2^L_i<=12P_i`. Summing the exact original-output chords gives normalized gaps between zero and one. The one-sided band `[T_j-1,T_j]` contains the graph and admits unit error. A finite disjunction in each coordinate carries all its output chord values with one shared interpolation weight. Their sums and affine restoration require no additional selector bits. Product separation greater than `nr` forces an original-output midpoint violation; the lattice-ball bound is `(9r)^n`. The count constant is `12*9=108<2^7`, proving the displayed `+n ceil(log2 r)+7n` bound.

For a compact nonnegative-facet body, local tolerance `1/(2n)` gives exact vector chord error in `K/2`. The symmetric `K/2` band contains the graph and remains in its `K` tube. Product separation greater than `2nr` and the `(15r)^n` lattice bound give `12*15=180<2^8`, proving the `+n ceil(log2 r)+8n` bound. The rank-zero and affine-coordinate arguments transfer unchanged by nonnegative facet weights and compactness. Both finite comparisons continue to allow arbitrary general integers in the lower-bound lift. No new issue arises from real coefficients or nonpolynomial continuous summands within this existence-only scope.
