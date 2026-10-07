# Independent review of the active-pattern and small-multiplier lemmas

Date: 2026-10-02. Verdict: **passed** for the actual
[active-pattern tube note](core-noise-active-stratum-tube.md) and the
[quantitative small-multiplier lemma](small-residual-multiplier-curvature.md).
This review checks their mathematical interfaces. The complete optimization
theorem still requires their separate composition with global pruning,
exact closure, and the finite fallback budget.

## Boundary geometry and exact finite-grid probability

Uniform residual strong convexity gives a unique Lipschitz selector even
when its minimizer lies on a box boundary. The envelope gradient is globally
Lipschitz on each closed original core face. Neither assertion needs strict
complementarity, smooth active-set behavior, or a positive interior slack.

The sets where a selector coordinate equals an original bound are closed
and semialgebraic. Their boundaries relative to a closed core face have
empty relative interior and dimension below that face's dimension. Adding
the ordinary boundary of the core face is necessary: the relative boundary
of the entire closed face in itself would be empty. Compactness of these
sets and continuity of the envelope gradient make the exceptional gradient
image compact. Semialgebraic dimension does not increase under this map.

The KKT formula used to define the selector is exact for convex box
optimization, including zero multipliers at either endpoint. The explicit
three-block formula for a lower-active boundary says that the point is
lower-active and every relative neighborhood contains a non-lower-active
point. Since the active set is closed, this is exactly its boundary.
The upper-bound and original-core-boundary versions follow as stated.
Keeping the finitely many image pieces separate avoids invalid quantifier
interchanges across a disjunction.

The fixed-block elimination bound gives exponentially bounded output
count and degree, with logarithms polynomial in the base input. The
coarse exponent in the note safely covers three blocks of sizes `N,1,N`
and at most `N` free coordinates. No sampled coefficient occurs in these
formulas: core noise changes neither residual optimality nor the original
value gradient used to define the exceptional set.

The polynomial-product enclosure is valid. At a point where every
nonconstant output polynomial is nonzero, the signs in a quantifier-free
formula are constant on a neighborhood. A lower-dimensional image cannot
contain such a neighborhood. Thus every image point zeros at least one
nonzero atom polynomial. Their product is nonzero and contains the whole
image in its zero set. Empty images and constant/zero atoms are correctly
handled. The algorithm needs only the degree bound; it need not construct
this product or enumerate the active-pattern strata.

The exact Basu--Lerario Theorem 1.1 contract was independently checked
against the primary preprint by the literature researcher and supplied to
this reviewer. It allows real dimension **at most** `m`, arbitrary real
coefficients, singular sets, and unbounded zero sets. I checked the saved
specialization of that contract. Taking `m=q-1`, enclosing the noise cube
in the radius-`sqrt(q) R` ball, and charging the volume ratio gives the
claimed conservative integer constant

```
C(q,D)=16 q^(q+1) D (4D+2)^(q-1).
```

Its logarithm is polynomial in `q` and `log(D+1)`. This quantitative size
bound matters; an unspecified dimension-dependent constant would not prove
the claimed sampling precision. The primary-source package is being
handled by the sole literature ingester; this reviewer performed no
external search.

The finite-grid reduction is exact. For endpoint-inclusive grid spacing
`2h=2sigma/(M-1)`, the cubes of half-width `h` about the grid points tile
`[-sigma-h,sigma+h]^q` with disjoint interiors and equal volumes. Uniform
jitter therefore produces the uniform distribution on that larger cube.
A grid point within `delta` of the exceptional image contributes an entire
cube inside its `(delta+sqrt(q)h)` tube. Dividing by `sigma+h` yields
precisely the note's mesh term `sqrt(q)/M`. In particular, atoms on the
exceptional set are covered even at `delta=0`.

For a stationary point on an original core face, its free noise equals
minus the unperturbed face gradient. Gradient Lipschitz continuity gives
the stated implication from proximity to an active-pattern boundary to
proximity to its exceptional noise image. All core faces exist before
sampling, so the union bound remains valid for the face selected by an
optimizer after sampling. Fixed core coefficients add only constants on
that face. Zero-dimensional faces require no tube event and are correctly
handled separately.

## Weak multipliers and quantitative curvature

On a stable two-sided core ball, the signed original-bound multipliers
are nonnegative smooth functions. Their second-derivative bounds come
from differentiating only the stationary free-residual system. Uniform
residual strong convexity controls every inverse free Hessian. The saved
bound

```
K=max{1,B3(1+M/mu)^3}
```

correctly bounds every multiplier Hessian across every fixed active
pattern. The existing third-derivative row-sum bound permits the safe
choice `B3=nT`; the sharper `B3=T` stated in the note also follows from
symmetry and the matrix row-sum bound.

For a nonnegative multiplier of value at most `K eta^2/2`, Taylor's upper
bound along the negative gradient gives `||grad lambda||^2<=2K lambda`.
This argument requires a two-sided ball. The saved half-interval example
shows why one cannot use it in an unfixed original-core normal direction.
The optimization composition must first soundly fix active core bounds
and apply the lemma in the remaining face coordinates.

After eliminating the original free residual coordinates, residual Schur
curvature remains at least `mu`. The cross columns for released active
coordinates are the signed multiplier gradients. Choosing

```
theta <= min{K eta^2/2, mu*g/(4rK)}
```

therefore bounds their total squared operator norm by `mu*g/2`.
Young's inequality gives the reduced joint Hessian lower bound
`diag(g I,mu I/2)`. The argument releases the entire small-multiplier
subset simultaneously; it does not incorrectly sum bounds from different
sequential eliminations.

Restoring the previously eliminated free variables is also quantitative.
Completing the square and using `||H_ff^-1 H_f,outer||<=M/mu` give

```
nu=min{mu/2, min(g,mu/2)/(1+2(M/mu)^2)}.
```

This is a valid full principal-Hessian modulus. Additional sound bound
fixings preserve it as principal restrictions. Thus an algorithm need
not identify the small-multiplier subset explicitly: fixing all large
multipliers and possibly some additional coordinates is sufficient.

The tube lemma deliberately gives stable bound status, not a lower bound
on every multiplier. The two lemmas fit at exactly this interface. Weak
or identically zero multipliers can remain free; positive curvature is
proved without asserting strict complementarity.

## Remaining composition checks

The main algorithm must still choose its stable-ball radius and all
precision thresholds before sampling. It must count residual faces as
well as core faces in the active-core-gradient tail, preserve every global
optimizer through excluded-region tests, and use the smaller of the global
growth and local Hessian margins in its cutoff. The supporting lemmas
introduce no need to enumerate strata, represent the selector explicitly,
or perturb a residual coefficient.

This review did not rerun the authors' symbolic diagnostics. An inline
`python3` check passed for this file's local links, code fences, and
trailing whitespace. No root indices, external services, project-wide
tests, or CI logs were touched.
