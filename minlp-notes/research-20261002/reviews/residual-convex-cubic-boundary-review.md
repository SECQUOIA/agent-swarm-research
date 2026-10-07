# Independent review of the residual-convex cubic boundary note

Date: 2026-10-02. Result: passed the complete actual
[closing note](../new-direction/residual-convex-cubic-boundary.md), including
the subsequent normalization of supplied margins to short dyadic lower
bounds. No substantive mathematical gap remains in its stated structural
claims. This review does not establish the unresolved full-point algorithm.

The affine positive-semidefinite residual Hessian gives the claimed upper
bound by reflection on each core face. The decomposition
`v=2delta c_A+(1-2delta)w` gives the lower bound at the residual center.
Consequently the kernel is the fixed rational kernel of `H_A` throughout
the relative interior of the core face. The zero-dimensional face and
`delta=1/2` cases are handled correctly. The positive eigenvalue bound
uses this same fixed kernel and does not assume that an irrational core
has rational spectral separation.

The previously reviewed convex cubic optimizer-slice identity applies to
each fixed residual fiber, including affine fibers and nonunique minima.
Replacing its central Hessian by `H_A` is valid because their kernels
agree. The remaining gradient row has degree at most two in the core.
Every square minor therefore has degree at most two, regardless of the
residual dimension. The bound `2^(3n+1)` safely counts all row and column
selections, and determinant expansion gives polynomial coefficient bit
length. The note correctly makes no polynomial-time enumeration claim.

The real-coefficient Hoffman argument is sound. An independent stack of
selected equality rows and active signed box normals has at most `n`
rows. Cauchy--Binet and the supplied nonzero-minor margin bound its least
singular value by `mu/(nC)^(n-1)`. In the projection-normal proof, active
inequality terms have the required sign; removing them leaves the equality
residual in (6). Neither rational equality right-hand sides nor rational
values of the varying row are needed.

The constants in (7) are conservative and sufficient. The rational
principal-minor bound for `H_A`, the face margin, and the cubic transverse
estimate give the stated projected-distance bound. The central-gradient
row estimate and `sqrt(n)<=n` then give (8). The affine case follows
directly from its objective-gap equality residual. One encoding issue was
corrected during review: arbitrary rational margins can have long
denominators despite modest inverse magnitudes. Choosing powers of two
below the supplied margins, within a factor of two, resolves this and
justifies the stated polynomial binary lengths. This constructs constants
from supplied margins; it does not find or certify margins at an unknown
optimal core.

Both examples have exactly the stated scope. The family `v z^2` rules out
a uniform positive-power residual error modulus as `v` approaches zero,
and its Hessian prevents any finite quadratic core convexifier. For
`gamma v-v^2 z` with `gamma>1`, every positive core has residual optimizer
one, whereas the minimum-norm global optimizer is `(0,0)`. The resulting
sequence still converges to the different global optimizer `(0,1)`, so it
does not obstruct arbitrary selected-point Cauchy output. Neither example
is a computational hardness result.

The closing limitations are appropriate: no efficient margin certificate,
finite-noise analysis, or sound exceptional-draw stopping rule has been
proved for the proposed extension. No further algorithmic claim follows
from this review.

Verification consisted of reading the full actual file and checking the
proof and constants above. The two files passed targeted checks for local
Markdown links, code fences, and trailing whitespace. No optimization
experiments, project-wide checks, or CI inspection were performed.
