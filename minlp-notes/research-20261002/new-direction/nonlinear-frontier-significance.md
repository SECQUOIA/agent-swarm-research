# Significance and assumptions of the nonlinear frontier

Date: 2026-10-02. This assessment reads the four current statements, their
completed mathematical reviews, and the local prior-art audits. It is
separate from those proof reviews and makes no priority claim. No index or
literature-KB files were edited.

**Status update, 2026-10-02.** The subsequently reviewed
[sparse smoothed polynomial theorem](smoothed-sparse-polynomial.md)
now establishes the main next target identified below. Its three stated
obligations are handled: conditional semiconcavity gives the expected bag
counts; fixed-block elimination and nonsingular stationary-root counts give
the finite-noise growth and gradient bounds; and a scalar lexicographic
elimination fallback has a base-only exponential budget. Exact implicit
patch output also has a polynomial-bit evaluator, with the GLS weak-output
feasibility repair checked explicitly. The
[combined review](smoothed-sparse-polynomial-independent-review.md) records
the proof and output qualifications. The assessment below is preserved as
the historical motivation for that result. Its deterministic question about
correlated boundary certificates under point growth alone remains open.

The strongest broad solver capability is **discovery**: certified mixed-box
polynomial approximation and exact native-integer optimization. The most
useful new output construction is the **verified convex patch**, which
identifies an unknown, possibly irrational optimizer without expanding its
coordinates. The nonlinear shell theorem adds direct verification of a
supplied rational candidate. These should not be combined into an
unrestricted exact nonlinear optimization claim.

## What the results actually provide

Here `p` is supplied maximum bag size, `I` is explicit input length, and
`kappa=max{1,L/g}` uses verified curvature and global point growth. Degree
is fixed.

| Result | Strongest capability | Main boundary |
|---|---|---|
| [Polynomial pruned grids](polynomial-pruned-grid-extension.md) | Finds a point and original-domain gap certificate in `f_d(p,kappa) poly(I+q)`; finds an exact native-integer optimum in `f_d(p,kappa) poly(I)` | Positive point growth controls the rate; continuous uniqueness alone is insufficient. |
| [Nonlinear shells](nonlinear-shell-certificate.md) | Certifies a supplied rational point and physical margin with `L/sigma<=max{32,20L/g}` | Does not find the candidate or certify a merely approximate numerical point as exact. |
| [Implicit convex patch](implicit-convex-patch-certificate.md) | Finds the exact integers and a verified strongly convex subproblem defining the exact optimizer, with certified arbitrary-precision evaluation | Requires `H_CC(a)>=g I`; expanded algebraic coordinates and values are excluded. |
| [Precision obstruction](implicit-optimum-precision-obstruction.md) | Forces exponentially long rational endpoints for specified enclosure/sign formats at constant width and conditioning | A format limitation, not optimization hardness or a barrier to all implicit output. |

The pruned-grid predecessor already states its arithmetic generality for
coordinate-semiconcave factors. The polynomial extension supplies the
verifiable curvature model, higher-degree denominator bound, and integer
value-spacing argument. It is a useful nonlinear consequence of that core
mechanism, not a second filtering algorithm. The exact-integer test remains
sound with ties; the point-growth FPT rate does not cover that case.

The shell theorem adds an essential exact-verification step: a Taylor
remainder transfers a quadratic certificate to the polynomial near its
zero, where ordinary additive grid error would not suffice. Its ingredients
have established precedents; the [source audit](../prior-art/nonlinear-shell-certificate-prior.md)
does not establish priority for the combined bound.

Convex-patch closure uses the standard implication that a positive Hessian
persists in a radius controlled by third derivatives. Its useful composition
with the search is discovering that patch, fixing integers, and proving
original global containment without knowing the optimizer or its growth.
It is an exact-output construction, not a new global-search mechanism.

## Assumptions and possible overclaims

- **Global growth carries separation from competitors.** A point at distance
  `R` with objective gap `Delta` forces `g<=Delta/R^2`. Local curvature,
  bounded degree, or uniqueness does not prevent distant near ties. Large
  binary-encoded integer ranges are allowed but do not ensure moderate
  conditioning.
- **The accepted curvature is the parameter.** Monomial interval bounds are
  easy to verify but can lose cancellations. A sharper `L` requires a
  counted proof, and curvature must hold between lattice labels. No bound
  in terms of an unsupported sharp curvature follows.
- **The patch hypothesis is local, not global convexity.** It neither reveals
  the winning integer assignment nor identifies its basin, so the theorem
  is not ordinary convex optimization in disguise. At continuous interior
  optima the hypothesis follows from point growth. At boundaries it is
  genuinely stronger: positive linear growth may coexist with a zero or
  indefinite Hessian. Replacing `H_CC(a)>=g I` by mere positive definiteness
  would introduce the missing ratio `L/mu`, where `mu` is the local minimum
  Hessian eigenvalue.
- **Encoding and domain restrictions matter.** Explicit bounded-degree
  monomials control exact value heights. Arbitrary circuits and binary
  exponents do not inherit the bit bound. Factor scopes must fit bags;
  Hessian sparsity at one point is insufficient. Product-box rounding does
  not preserve general coupling constraints. Rational-lattice shell
  verification is established, while physical-metric discovery currently
  has the separately audited native-integer statement.
- **Parameterized polynomial is not input-only polynomial.** Patch endpoints
  and proof length are `f(p,kappa) poly(I)`. Third-derivative and Taylor
  bounds affect stage counts through their bit lengths, which is useful,
  but the conditioning-dependent prefactor remains. No practical performance
  conclusion follows from the asymptotic statement.

The patch note's `G=F+y+x_n y^2` example makes the Hessian qualification
concrete: original growth and upper curvature stay bounded while the added
positive eigenvalue is doubly exponentially small. It also has the easy
global elimination `partial_y G>=1`. Thus it limits a full-coordinate
convex-patch contract rather than every exact algorithm.

## Exact implicit output and the precision obstruction

“The minimizer of the input” alone would add little. The returned patch is
more specific: integers are fixed, uniform strong convexity is verified,
and a pruning trace proves original global optimality. Its constrained
minimizer is unique independently of the growth premise. The proved
arbitrary-precision evaluation procedure makes this an effective exact
representation. The KKT system need not preserve the original graph width;
the evaluation proof correctly uses the sparse primal problem instead of
assuming a cheap generic KKT oracle.

The precision examples are globally strongly convex and have short
recurrences or symbolic proofs. They are not hard optimization benchmarks.
They show that even exact range evaluation over one independent-coordinate
rectangle can force huge endpoint encodings when the entire rectangle must
certify an active-gradient sign. The [prior-art comparison](../prior-art/implicit-optimum-precision-prior.md)
correctly separates this from limits of interval methods as a whole. The
convex-patch theorem responds by allowing boundary-touching boxes and leaving
active-set selection inside the certified convex problem.

## Highest-potential next target

Prioritize **sparse smoothed polynomial optimization with exact implicit
output**. This could remove the rational-candidate input and explain useful
conditioning without planting an optimizer. It is not yet established.

The route has three concrete obligations:

1. Extend the [sparse bag-cell expectation bound](sparse-bag-cell-smoothed-miqp.md)
   using polynomial conditional semiconcavity. This part appears direct.
2. Bound bad growth and active-gradient events for one polynomial-bit
   rational noise law. Nonsingular free stationary roots on a fixed face
   do not depend on an active coordinate's own linear noise; a uniform
   isolated-root count can support the margin bound. Finite-grid growth
   transfer also needs a proved `exp(poly(I))` bound on one-coefficient
   bad-event complexity.
3. Obtain a same-draw exact fallback with cost
   `B_base poly(I+log N_noise)`, where `B_base=exp(poly(I))` is determined
   before sampling. A generic doubly exponential elimination bound is too
   large. Even an undifferentiated `exp(poly(I+log N_noise))` bound risks a
   sampling-precision circle, so coefficient-height cost must be separated.

On a good draw, integer singleton filtering and active-bound elimination
should expose a continuous free block with Hessian at least `2g I`, enabling
convex-patch closure. Exceptional draws may have tied or flat optima, so the
every-draw output must permit an exact algebraic fallback rather than demand
a unique strongly convex patch on every sample. A successful analysis would
likely give fixed-width expected polynomial work with explicit numerical
width/curvature/noise factors, not automatically FPT in width. The required
root counts, finite-law transfer, and fallback need primary-source and
mathematical verification before promoting this target.

Efficient evaluation of that output is another separate obligation. The
good-event growth threshold can be exponentially small, so applying a
`kappa`-parameterized evaluator to the returned patch need not give
polynomial expected evaluation work. A general convex bit algorithm with
polynomial dependence on `log(1/tau)` could avoid that problem; otherwise
state only the construction and output-size guarantee initially.

A second, harder target is exact implicit output for boundary optima under
point growth alone. It needs a correlated local certificate that can use
implicit equations when checking boundary conditions. Adding tiny-gradient
or strict-interior-slack parameters would merely reintroduce the scales
exposed by the precision examples. This target remains important but has a
less concrete positive route at present.

A sharper benchmark for that target is available from the same residual
chain: set `h=(x_n+r_n)/2` and `G=F+y^2+3yh`. The identity
`G=(F+y^2)/4+3(F-r_n^2)/4+3(r_n+y)^2/4+3yx_n/2` gives growth
`9/64`, while upper curvature remains `35/16`. The terminal Hessian
block is `[[2,3],[3,2]]`, so a convex patch cannot retain both those
coordinates nondegenerately. Its active derivative is still doubly
exponentially small, and the rectangular-sign obstruction persists.
The short displayed identity explains why correlated boundary certificates,
rather than more Hessian refinement, are the relevant missing mechanism.
This is a benchmark, not a hardness or priority claim.

## Evidence and presentation

The polynomial discovery extension has a mathematical audit, not a separate
implementation of its full optimizer. The nonlinear shell checker tests
actual polynomial OR-DP tables. The patch checks test closure and integer
filtering rather than an end-to-end solver. Present one core conditioned
search method, its nonlinear consequences, and complementary exact proof
objects; do not count each formal extension as an unrelated major algorithm.

This assessment used local reads and an independent assumption challenge.
It did not rerun optimization tests or inspect CI. A scoped document check
covers formatting and local links only.
