# Stage 4, round 1 — independent review 3

Reviewed frozen snapshot `process/snapshots/stage04-round01`, its entire new
bounded-rank section, dependency definitions, and bibliography additions. No
other current-round reports were read; no manuscript sources were edited.

## Verdict and enumerated findings

**No major issues. Accept after one minor bibliography correction.** The two
new mathematical developments—the finite-basis recovery theorem and the
five-product, two-label K4 construction—pass this review.

1. **S04-R1-R3-01 — Minor: do not combine the preprint author list with the
   published article metadata.** In `references.bib`, entry
   `OnnRozenblit2014` uses the author names/order of arXiv:1208.5639v1, namely
   Shmuel Onn and Michal Rozenblit, but gives the journal publication details.
   The published article lists **Michal Melamed and Shmuel Onn**, in that order,
   and has DOI **10.1016/j.laa.2014.01.007**. This is supported by the
   [publisher result](https://doi.org/10.1016/j.laa.2014.01.007) and its
   publisher-deposited [Crossref metadata](https://api.crossref.org/works/10.1016/j.laa.2014.01.007).
   Conversely, the [2012 arXiv record](https://arxiv.org/abs/1208.5639)
   displays the author list currently used. Cite the published article with
   its published author list and DOI, retaining the preprint URL with an
   appropriate version note if useful; alternatively cite the preprint
   explicitly as a separate 2012 entry. The mathematical role of the citation
   is correct. This is a source-version metadata repair, not a novelty or
   correctness issue. The retrieved registration metadata is retained in
   `verification/reviewer3/stage04-round01/published-reference-metadata.json`.

No other required correction was identified.

## Mathematical audit

### State normal matrix and positive circuits

The signed distinct rows remain totally unimodular. Combining repeated rows
retains all original bounds, and every original cyclic-block arc has a nonzero
cycle row. Each observation enters exactly the two opposite normal lists.

The extreme-ray argument for the nonnegative dependence cone is valid: a
second dependence supported inside the positive support permits two-sided
perturbation and contradicts extremality. Minimal dependence implies at most
`s+1` rows. Cofactors of a full-rank column restriction yield a primitive
dependence with unit entries because the matrix is TU. Farkas certificates
therefore give the complete local test. The opposite-pair observation argument
correctly prevents doubled product coefficients after branch selection.

### Uniform directions and fan refinement

The cofactor direction of `s-1` independent normal rows is ternary and
primitive. Its product with any additional normal is a full TU determinant,
so the stronger fact `Md` is ternary also holds. This stronger fact is needed
later and is actually proved. The relative-interior argument for active-row
rank `s-1` includes lower-dimensional polyhedra and hence all edges of every
state slice.

I checked the arrangement argument on boundary and degenerate cases. Inside
a chamber no possible edge is orthogonal to the objective, so each summand
has a unique maximizing vertex. It remains fixed within that chamber. The
coordinate hyperplanes make chambers pointed; their extreme rays arise from
`s-1` independent hyperplanes and belong to the enumerated ray set. Continuity
extends each linear support expression to the closure. Consequently the
finite ray tests imply every support inequality, even if a summand or the
whole sum is lower-dimensional. Hadamard applies to order-`s-1` ternary
cofactors, yielding the stated `H_s` bound. The special rank-one convention
removes the zero-order exception cleanly.

### Dual multipliers and separation

The optimal dual-support reduction to independent supporting columns is valid
even for a lower-dimensional primal. Adding zero-multiplier rows completes a
basis, so the finite dual formula does not omit degenerate optima.

The transformed-edge proof has the correct transpose: if `q=B^{-T}h`, then
`(Bd_i)^T q=d_i^T h=0`. The unimodular map preserves primitive integer
vectors, and the transformed directions are still independent and ternary.
Their primitive cofactor null vector must therefore be `q` up to sign.
Hadamard bounds every multiplier by `H_s`; no unjustified triangle-inequality
estimate or assertion that arbitrary inverse multiplication preserves the
same entry bound is used.

A nonsingular basis cannot contain an opposite normal pair. Each selected
observed product therefore occurs once per state, and product indices differ
between states. The aggregate chord coordinates are distinct original flow
coordinates. Active minimum branches are affine majorants of the true
supports, so the emitted cuts are globally valid. The coefficient statement
is consistently restricted to the displayed rational scaling; integer
normalization of simplex data is not silently applied.

The library sizes are bounded by subsets of size `O(s)` of configurations
with `2^{O(s)}` elements. Their products remain `2^{O(s^2)}`. Per-state work
and block counts give the stated sparse-input factor. Constructing fundamental
cycles in `O(r |E|)` is also absorbed. No empirical runtime advantage is
claimed for these libraries.

### New finite-basis recovery theorem

The suffix inequality has the correct sign: `h(t-theta) <= S_i(h)` is
equivalent to `-h theta <= S_i(h)-h t`. Thus the recovery polytope is exactly
the intersection of the current state with the reflected suffix sum. It is
nonempty by the invariant and bounded by the current state domain.

At a vertex its active normals span the full ambient space, including on a
lower-dimensional polytope; otherwise both small signs of a null motion would
remain feasible. Therefore enumerating all nonsingular `s`-row bases of the
fixed normal list finds a feasible candidate. This proves the recovery
invariant and termination at zero remainder without invoking a generic online
LP solver.

There are `2^{O(s^2)}` fixed normals and at most their `s`-subsets to check,
giving `2^{O(s^3)}`. Testing each candidate against every normal keeps that
bound. The denominator argument is sound: sequential basis inversions add
the logarithms of selected integer determinants to a common denominator,
rather than multiplying its bit length. Feasible states stay inside scaled
base bounds, remainders are their sums, and rejected candidates are fixed
inverse matrices applied to bounded current right-hand sides. Their numerators
also have polynomial bit length. Positive-weight normalization only adds the
encoding length of the corresponding input weight. The compact output uses
`O(s)` coordinates per block default/exception; dense output is charged
separately.

### Section-to-facet lemma and new K4 construction

The coordinate section has local two-dimensional interior. Every affine
equation valid on the whole polytope therefore has zero coefficients on its
two free coordinates. At the boundary, some nonconstant restricted inequality
must be active; validity on both tangent directions forces its normal to be
the stated positive multiple. This establishes the claim for any finite
description and makes the ratio invariant under affine-equation additions.

For the five-observation K4 construction, I independently recomputed `Av`,
`C bar_theta`, all observed state equalities, and each residual arc deviation.
The first explicit state is `(p,q,p)` and the second is `(s,-s,0)`. The two
residual upper bounds imply residual support at most `1/3`, while the fixed
aggregate support is `1/3`; hence `2p+q>=0` is necessary. The proposed
`s=q/2` witness obeys all capacities throughout the stated open square on that
side. In particular the fourth residual entry stays strictly between `3/16`
and `11/48`, inside its asymmetric interval, and the first/last entries are
the only possibly tight endpoints. Thus the local half-plane statement is
proved, and the section lemma proves the necessary ratio two.

The symmetric-reference variant also checks out: both line states annihilate
`(1,1,1)`, their chosen signs give the displayed aggregate, and the residual
parameter satisfies `5/64 < a <= 1/8` in the stated neighborhood. The
comparison to a projection-cone multiplier in Khademnia–Davarnia correctly
distinguishes an antecedent from an actual ambient product-coefficient ratio.

## Independent executable evidence and build

`verification/reviewer3/stage04-round01/check_rank3.py` imports no repository
hull implementation. Its exact checks produced:

- 12 signed K4 normals, seven primitive edge directions, and 18 support rays;
- **2,304** transformed primitive vectors satisfying the magnitude-two bound,
  including **696** nonnegative support vectors;
- **694** rational feasible witnesses and **675** strict residual-support
  contradictions in the new K4 coordinate section;
- **10** independently assembled finite-basis recovery models with **30**
  recovered states, including three zero-weight states, all with exact
  remaining aggregate zero and all state inequalities satisfied.

The finite checks supplement the general proof; they do not replace it.
The JSON counts and script are retained. A private full-snapshot `latexmk`
build succeeded; the final 27-page log has no warnings or overfull/underfull
boxes.

## Source checks and review limits

The [open 2012 preprint](https://arxiv.org/html/1208.5639v1), Section 2 and
Theorem 2.3, supports the classical edge-direction/zonotope attribution. Its
setting concerns convex integer optimization and projections, rather than
the present continuous state-slice sum with a uniform original-coordinate
coefficient bound. The manuscript makes that classical-method boundary clear.
The [primary Onn–Rothblum–Tangir page](https://link.springer.com/article/10.1007/s10898-004-4313-z)
confirms its bibliographic data and its network-flow edge-direction subject.
I did not claim to read that subscription article's full text.

I did not perform an exhaustive priority search or certify practical
performance of the exponential-parameter procedures. Future manuscript stages
are outside this verdict. No report from another reviewer was consulted and
no manuscript changes were made.
