# Investigation: Hessian rank and integer dimension

Date: 2026-09-05. The candidate proof is in
`results/quadratic-rank-integer-complexity.md`. Root and a second agent
independently converged on the maximal-simplex determinant argument.
A third agent independently reviewed the completed proof and reported
no mandatory correction; its review is recorded separately.

## What is established internally

For a scalar quadratic graph on a full-dimensional bounded box,
minimum convex-lift integer dimension and minimum linear-lift binary
dimension both have leading coefficient half the Hessian rank on
`log2(1/ε)`. This includes singular and indefinite Hessians and allows
unbounded integer coordinates in the lower-bound model. The upper
construction uses the established sawtooth relaxation on a decomposition
into rank-many squares, with total size logarithmic in inverse accuracy
for each fixed quadratic and box.

The geometric lower bound depends on absolute determinant, not an
inequality based on the smallest eigenvalue. This is essential for
indefinite forms: the usual strong-convexity diameter argument fails
because nonzero null directions can have zero midpoint gap. Bounding
the volume by a maximal simplex remains valid despite those directions.

The exact constant is deliberately loose. No optimal tiling or sharp
finite binary count is claimed, except for the previously established
univariate square result. Affine terms are irrelevant because they
cancel in midpoint errors and can be represented exactly.

## Primary-source comparison

Lubin, Vielma, and Zadik's published Midpoint Lemma provides the
integer-parity mechanism and bounds the rank of mixed-integer convex
representations using pairwise incompatible midpoints:
[[lubin2022-mixed-integer-convex-representability]] p.11-12.
Our source's abstract/read note was insufficient to identify its full
finite-dimensional strength; reading the actual lemma revealed that
unrestricted integers are covered. This corrected and strengthened the
local binary-only interpretation.

Pottmann et al. (2000), [open publisher PDF](https://www.heldermann-verlag.de/jgg/jgg01_05/jgg0403.pdf),
pp.35–36, derive the quadratic midpoint-error formula in arbitrary
dimension. Their pp.43–47 treat optimal indefinite bivariate affine
approximants; p.50 discusses the trivariate indefinite case and dimension
reduction for singular forms. These are close geometric precedents.
The present claim concerns arbitrary graph-containing convex lifts and
integer dimension, rather than the number or shapes of affine pieces.
That distinction needs to remain explicit in any publication claim.

Beach and collaborators supply the compact square-relaxation upper
bound. Spectral decomposition and rank reduction are classical. None
of these upper ingredients should be described as a new formulation.

Additional search leads include Agouzal, Lipnikov, and Vassilevski,
*Families of meshes minimizing P1 interpolation error for functions
with indefinite Hessian*, Russian Journal of Numerical Analysis and
Mathematical Modelling 26(4), 2011, DOI 10.1515/RJNAMM.2011.019, and
anisotropic approximation results on determinant-based interpolation
bounds. These are leads for further priority review; no repository
package was created, and no claim of a complete reading is made.

## Search record and novelty limits

Independent web searches on 2026-09-05 included:

- mixed-integer quadratic rank approximation lower bound formulation;
- quadratic convex cover approximation rank indefinite;
- mixed-integer convex approximation integer dimension;
- quadratic functions approximation indefinite simplices;
- piecewise linear approximation quadratic determinant;
- mixed-integer approximate representability.

The matching general convex-lift integer-dimension law did not appear
in these searches. This is limited negative search evidence, not proof
of novelty. The result may be seen as an elementary synthesis of
classical approximation geometry and the published midpoint lemma.
Its indefinite, arbitrary-signature and unrestricted-integer scope
makes it more substantial than a count for a prescribed PWL model,
but impact and priority remain questions for expert comparison.

## Verification

The proof received a complete independent agent audit. Separately,
`code/quadratic_rank/check_simplex.py` passed exact rational checks for
42 maximal-simplex examples, including every signature in dimensions
one through four, and 15 rank-deficient principal-minor cases. The
maximality enclosure, polarization identity, determinant equality,
Hadamard inequality, and principal-factorization identities were all
checked separately.

## Retained follow-up directions

1. Improve the determinant constant for indefinite signatures. The
   current theorem only claims the leading logarithmic coefficient.
2. Relate the interaction-graph exponent to the maximum rank of a
   symmetric matrix supported on that graph. Fractional matching and
   disjoint edge/cycle structures suggest the identity `max rank=2τ*`.
   This is established graph-matrix territory requiring appropriate
   attribution; it is not a new claim in the present note.
3. Study quadratic vector maps. Any scalar combination gives a Hessian
   rank lower bound, but simultaneous approximation may require a
   stronger invariant than a single combination. No general matching
   upper bound is asserted.
4. Investigate smooth nonquadratic functions with a nonsingular
   indefinite Hessian. Local Taylor errors depend on cell diameter,
   whereas indefinite geometry permits thin elongated contact sets.
   Therefore the constant-Hessian proof does not automatically extend
   by an unqualified continuity argument.
5. Revisit the scalar product's upper constant with rotated diamond
   cells. This may improve NMDT's error constant but is distinct from
   the rank exponent and needs its own construction and review.

## Independent check of the covariance refinement

The alternate covariance proof appended to
`notes/review-quadratic-rank-integer-complexity.md` was independently
checked by the original result author after the reviewer derived it.
The centered fourth-moment expansion, eigenvalue AM–GM inequality,
volume-covariance bound from the minimum second moment of a ball, and
final constant all pass. In particular, the stronger valid constant is

```
c_cov = sqrt(r) |det(H_I)|^(1/r) V_I^(2/r)
        / [4(r+2) omega_r^(2/r)].
```

This is a reviewed optional refinement. The primary theorem retains its
simpler maximal-simplex proof; the sharper constant is not necessary for
the leading rank law.
