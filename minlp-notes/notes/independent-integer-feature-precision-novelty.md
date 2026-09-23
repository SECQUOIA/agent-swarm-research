# Source audit: independent integer features and quadratic precision

Date: 2026-09-05. Focused independent source audit of
[the integer-feature candidate](independent-integer-feature-quadratic-precision.md).
Separate agents assess its mathematical correctness.

## Assessment

No matching finite minimum-integer theorem was found for the stated
feature representation. The supported contribution is the bound
`p_out<=p_conv+5r+sum_i log2 ||T_i||_1+1` for positive sums of squares of
independent integer linear forms, with arbitrary unconditional output
error. Bounded integer row lengths give linear overhead despite overlap
of feature supports and noncommuting original Hessians.

This is a direct generalization of the repository's forest application
and a useful way to state the geometric requirement behind it. The
single-minor volume estimate is elementary; separability after an affine
map and compact square approximation are established. The contribution
should be framed as a formulation-wide comparison with explicit
representation-dependent overhead, not as a new matrix-volume theorem
or a new separable reformulation.

## Established affine-feature approximation

Hijazi, Bonami and Ouorou,
[An outer-inner approximation for separable MINLPs](https://optimization-online.org/wp-content/uploads/2012/08/3581.pdf),
Section 1, explicitly defines its separable functions as sums of univariate
convex functions composed with affine forms. It notes that convex
quadratics fit this class by spectral decomposition. Its methods use
extended formulations, outer approximations, and univariate chords for
an inner approximation. Thus separability here does not mean that the
original-coordinate supports must be disjoint, and using linear feature
variables to expose it is clearly prior work.

Beach, Hildebrand and Huchette,
[Compact mixed-integer programming relaxations in quadratic optimization](https://arxiv.org/pdf/2011.08823),
supplies compact square approximation and quadratic reformulation
precedents. The candidate reuses that established approximation family.
The [diagonal source audit](diagonal-psd-quadratic-precision-novelty.md)
and [unconditional-body source audit](positive-separable-unconditional-error-novelty.md)
record the prior sharing, log-allocation, and oracle techniques.

The candidate's new comparison is not restricted to formulations that
retain its feature variables or to one prescribed chord model. Its lower
bound concerns every convex lift with unrestricted integer variables.

## Established volume ingredients

Dall and Pfeifle,
[A polyhedral proof of the matrix tree theorem](https://arxiv.org/pdf/1404.3876),
Theorem 5 and Corollary 6, printed pages 5--6, gives the generating
parallelotope decomposition and unimodular zonotope volume formula.
Gover and Krikorian's
[Determinants and the volumes of parallelotopes and zonotopes](https://www.sciencedirect.com/science/article/pii/S0024379510000443)
provides another primary predecessor for the general matrix/cube-image
viewpoint; its publisher abstract was checked.

The candidate only needs a simpler containment argument: a nonsingular
`r`-column submatrix defines a parallelotope inside the image zonotope.
Its normalized volume is `|det T_I|/product_i ||T_i||_1`. The determinant
of a nonsingular integer matrix has magnitude at least one. No matroid
theorem or total unimodularity is required for that lower estimate, and
there is no need to compute the whole zonotope volume.

This explains both the scope and the limitation. Integer row size gives
an elementary certificate that independent feature coordinates do not
compress the cube volume too much after normalization. For arbitrary
rational directions, clearing denominators can make those row lengths
large. The theorem records that cost rather than eliminating it.

## Relation to whole-formulation literature

Lubin, Zadik and Vielma,
[Mixed-integer convex representability](https://arxiv.org/abs/1706.05135),
provides the prior midpoint/parity obstruction for arbitrary integer
lifts. The candidate combines it with the repository's quantitative
diagonal covariance law on the actual image domain. Its upper construction
keeps the original continuous cube variables as an exact linear lift of
that domain. Consequently the minor-volume loss measures the difference
between the containing-cube construction and the universal lower bound.

The [forest audit](forest-laplacian-quadratic-precision-novelty.md) compares
nearby tree-indicator optimization and process/network approximation
results. Those target optimization or chosen approximation formulations,
not this minimum integer dimension. Forest incidence rows have length
two, so the broader statement recovers the forest `6r+1` estimate; the
forest's exact volume retains a potentially sharper constant.

## Limits and presentation

The full-row-rank feature representation is supplied as part of the
input. The theorem does not discover an optimal positive square
decomposition or optimize the bound over all representations. It also
does not cover an arbitrary dependent collection of bounded-support
features merely because each individual row is short.

The row-width expression is representation-dependent; scaling a row and
compensating in its positive coefficients leaves the function unchanged
but can worsen the crude bound. Primitive integer rows remove an obvious
redundancy. The version retaining an actual determinant minor is sharper
and makes the geometric meaning explicit. Neither version implies linear
overhead for all ill-conditioned rational changes of variables.

Fresh searches combined quadratic linear forms, separable affine-feature
MINLP approximations, zonotope mixed-integer representations, and minimum
binary approximation counts. No exact match was found in the checked
primary sources. This supports a qualified novelty statement for the
formulation-wide bound, not a claim that its individual ingredients are new.
