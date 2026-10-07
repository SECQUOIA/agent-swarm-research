# Significance of the sparse smoothed polynomial theorem

Date: 2026-10-02. This is an independent significance assessment of the
actual [polynomial theorem](smoothed-sparse-polynomial.md), its
[quadratic predecessor](sparse-bag-cell-smoothed-miqp.md), the
[deterministic polynomial extension](polynomial-pruned-grid-extension.md),
and the [focused primary-source audit](../prior-art/sparse-smoothed-polynomial-prior.md).
It does not replace the separate mathematical reviews or establish
publication priority. The main theorem's final interface reviews were
being completed when this assessment was written.

## Assessment

This is a meaningful extension beyond sparse mixed-integer QP. It gives
global discovery for explicit fixed-degree nonlinear objectives with
continuous variables, without an input growth or boundary-Hessian
assumption, under a specified finite law of independent linear noise.
The result is exact for the sampled problem on every draw. Its usual
output identifies a globally valid strongly convex subproblem, whose
optimizer and value can subsequently be evaluated to arbitrary precision
in polynomial bit time.

The strongest defensible claim is therefore **expected exact implicit
optimization for fixed-degree sparse mixed polynomial box problems**,
with the stated width/noise dependence. It is not an exact algorithm for
unperturbed general MINLP, an FPT theorem in treewidth, or an improved
worst-case approximation scheme.

## What changes relative to the existing results

| Comparison | Material gain | What is inherited or remains weaker |
|---|---|---|
| Sparse smoothed MIQP | Allows nonlinear polynomial interactions of fixed degree, with irrational continuous optima and nonconstant Hessians. Replaces rational quadratic recovery by certified local convex-patch closure and an algebraic fallback. | The bag-cell count, sparse DP, arbitrary integer dimension, finite-law policy, and every-draw exactness principle already occur in the quadratic result. Its rational expanded output is replaced by implicit output on usual draws. |
| Deterministic polynomial pruning | Removes the point-growth input condition from the sampled-instance theorem and supplies exact continuous output with a useful evaluation contract. | The deterministic result has the stronger parameterized form `f_d(p,L/g) poly(I+q)` on its promised inputs. The smoothed bound is fixed-width polynomial, with an `n^p`-type factor. Neither dominates the other on all inputs. |
| Earlier deterministic convex-patch theorem | Does not require the full continuous Hessian at a boundary optimizer to be positive. Active continuous bounds are first certified and fixed; only the remaining interior block must be positive. | Strongly convex implicit descriptions and their evaluation are established tools. The new task is discovering and globally certifying a suitable patch with the expected sparse search bound. |

The polynomial rounding extension itself is modest: sequential
coordinate semiconcavity was already the mechanism behind the earlier
polynomial pruning result. The consequential work lies in closing the
search exactly despite nonlinear algebraic optima, controlling rare
finite-grid degeneracies, and keeping sampling precision out of the
fallback's exponential parameter.

The number of integer coordinates is unrestricted, but that alone is
not the new advance over the MIQP predecessor. For a pure integer box
with polynomially bounded domain sizes, ordinary exact finite-state DP
already works at fixed width. The most informative new scope combines
nonlinear continuous variables with native integer choices and sparse
interactions.

## Why the output is more than an argmin label

Writing `argmin_X F_gamma` for the original instance would be a short
but computationally empty representation. The theorem returns more:

1. Integer values and original continuous bounds that every optimizer
   must satisfy, justified by the retained global pruning record.
2. A rational box containing every remaining optimizer and a checked
   positive Hessian modulus throughout that box.
3. A polynomial-bit evaluation procedure producing feasible rational
   approximations and certified objective intervals at any requested
   precision, including at constrained boundary minima.

Strong convexity makes the specified primal point unique and removes
the global-search difficulty from later evaluation. This is a meaningful
exact implicit output convention. It does not provide expanded algebraic
coordinates, a minimal polynomial, or a finite rational exact value on
usual continuous draws. Those should not be advertised as outputs.
The reviewed [quartic path example](../geometric-dp/algebraic-output.md)
already has exponentially large expanded minimal polynomials at fixed
width and uniform conditioning, so this output distinction has a concrete
mathematical basis.

The compact descriptor and its global proof have different sizes. The
descriptor has polynomial length on the patch branch; the pruning proof
has the theorem's expected size and verification cost. Merely receiving
the compact box and Hessian test would not independently establish that
the original global optimum lies there. On exceptional draws, the
algebraic fallback may have exponentially large output. Its expected
cost is controlled, not its worst-case output size.

## The noise regime is substantive, but restrictive

The expected bound is

```
C^p [4+(1+n/2)L w_max/(2 sigma)]^p poly_d(I).
```

It is polynomial for each fixed bag size when the numerical ratio is
polynomially bounded. Small negative curvature does not replace `L`.
Large native-integer widths enter numerically, and a tiny binary-encoded
noise scale can make the bound exponential. The verified curvature bound
actually supplied is charged; an excessively loose monomial bound can
make the guarantee weak even if the true curvature is moderate.

This is not merely a large-noise regime in which the linear term
dominates the objective. For example, consider bounded-degree local
polynomial factors of bounded coefficient magnitude on `[-1,1]^n`,
with bounded coordinate occurrence and fixed bag size. A constant valid
`L` is available. Taking `sigma=n^-2` gives a polynomial expected bound
of order `C^p O(n^3)^p poly_d(I)`, while the entire perturbation changes
objective comparisons by at most `sigma sum_i w_i=2/n`. Thus vanishing
total perturbations are compatible with the stated polynomial regime.
This observation concerns scaling, not hardness of that example class.

The law nevertheless solves a different optimization problem. It gives
no exact recovery of the original optimizer, its active set, or its
integer labels. The original-objective gap consequence is at most
`sigma sum_i w_i` before evaluation error. Setting
`sigma=epsilon/(2 sum_i w_i)` yields an approximation algorithm with an
inverse-accuracy exponent proportional to `p`; this is not better than
the basic uniform-grid approximation bound and can be worse. The
interesting guarantee is exact completion of the sampled problem with
subsequent logarithmic-precision evaluation.

The finite law has an input-dependent resolution `M`, selected once
before sampling. Its description and random-bit count are polynomial,
although its support can be exponentially large. This is stronger than
a law retuned for each requested evaluation tolerance. It is narrower
than a claim for arbitrary machine-precision noise or every finite grid
of half-width `sigma`. Atoms that leave ties or degenerate optima are
handled on the same draw; resampling until a favorable instance appears
would be a different guarantee.

## Relation to established methods

The [primary-source audit](../prior-art/sparse-smoothed-polynomial-prior.md)
documents qualitative generic uniqueness and growth under linear tilts,
real quantifier elimination, exact algebraic global optimization, convex
weak optimization, sparse polynomial approximation, and sparse SOS
relaxations. None of these ingredients should be introduced as new.
In particular, qualitative genericity under an absolutely continuous
law does not pay for finite-grid atoms or supply the quantitative tail
needed here.

The meaningful candidate contribution is their composition with the
expected sparse bag-cell count: a base-chosen finite law, sparse global
pruning, exact patch discovery, and a same-draw fallback with the
required separation between base complexity and added coefficient bits.
The scoped source search did not identify a theorem with that full
combination. That is a reason for further comparison, not proof of
priority.

## What remains before a solver claim

The current diagnostics exercise the sparse DP, nonlinear rounding,
integer identification, active-bound fixing, and a local Hessian test.
They do not implement the complete sampler-budget construction,
algebraic fallback, or certified ellipsoid evaluator, and do not measure
the expected runtime on a distribution of instances.

The effective elimination constants can make the theoretical sampling
precision and cutoff conservative. Exact rational table storage, proof
record size, a practical curvature bound, and a numerical convex-patch
solver with a reliable certificate all need engineering. A successful
implementation should first measure retained-row counts and patch
closure on small coupled nonlinear mixed instances, then account for
certified arithmetic and fallback events separately. No practical
speedup follows from the theorem alone.

The product-box domain and explicit fixed-degree encoding are essential
scope limits. Arbitrary local nonlinear constraints, general arithmetic
circuits, or binary-encoded unbounded polynomial degree are not covered.
Within those limits, the theorem adds a genuine nonlinear exact-search
capability; its most useful presentation is as a theoretical discovery
and certification result, not a general-purpose MINLP solver claim.

## Assessment checks

This assessment read the actual theorem, the two predecessor results,
the earlier implicit-patch theorem, the composition review, and the
focused prior-art audit. It independently checked the scaling example
and the output/noise distinctions above. It did not rerun optimization
diagnostics, inspect CI, perform external source searches, or edit root
indices. This is a significance assessment rather than a new proof audit.
Targeted Python checks of whitespace, paired fenced blocks, and local
links passed, as did `git diff --check` scoped to this note and the two
current strict-copositivity notes.
