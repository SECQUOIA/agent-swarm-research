# Certified polynomial ODE support prototype

Status, 12 September 2026: implemented research prototype; formal structure,
compiler and rational propagation have passed fresh independent review. Novelty and
practical solver improvements remain unestablished. The closest-source audit in
[the theory draft](../results/extended-rpd-supporting-flow.md) credits existing
comparison, subgradient, affine-relaxation and extended-McCormick results.

## Capability and certificate boundary

`code/research_20260912/extended_rpd.py` compiles affine minorants of a specified
polynomial extended-RPD vector field. It uses fixed rational interval parts,
the sign-selected multiplication rule of Ye and Scott (2023), a signed upper
state channel, and optional finite affine-invariant propagation. Coefficients
are exact fractions. Floating-point reference values choose among valid affine
pieces; a wrong choice can weaken a support without invalidating it. The
compiled state coefficient matrix is checked to be Metzler.

A coupled-invariant penalty dual is also implemented. Its feasible multipliers
lie in boxes. Approximate LP multipliers are rationalized and clamped to those
boxes, and the affine intercept is recomputed exactly. A fixed collection of
these tuples defines a finite convex, monotone refinement. No claim about the
quality of these bundles has yet been established. A four-variable check
recovers the exact coupled upper bounds `(1/2, 3/4, 3/4, 1/2)` from the theory
example.

`rational_affine_flow.py` propagates held affine supports using exact rational
Taylor polynomials with a rigorous remainder estimate and controlled rounding.
It shifts final affine constants by a certified coefficient-error allowance
over the parameter box. It does not certify that its input fields are valid
supports. That separate obligation is supplied by the mathematical construction,
the exact compiler and the physical state-tube proof. See the
[propagation proof](research-20260912-rational-flow.md),
[propagation review](research-20260912-rational-flow-independent-review.md), and
[compiler review](research-20260912-ode-theory-independent-review.md). Independent
checks include 8,640 exact support inequalities and 109 exact rational
matrix-exponential reference enclosures. Each review states its coverage.

The numerical reference trajectory is not part of the certificate. It selects
supports only. The nonlinear ODE solutions used below are diagnostics and do
not establish continuous-time validity by sampling.

## Initial reproducible cases

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/ode_support_experiment.py --output code/research_20260912/results/ode_initial_certificate.json --models dimerization shift_methanation --steps 10 30 --sweeps 0 1 2
```

The saved JSON contains all exact slab coefficients, initial coefficients,
parameter/state boxes, final cuts, error allowances and source hashes. Both
models use a half-unit horizon. Rate constants are illustrative; these are not
calibrated process models or industrial benchmarks.

| Model | Parameters and physical tube proof | Initial result |
|---|---|---|
| Closed `2A ⇌ B` | Forward rate in `[0.3,1.5]`; nonnegativity and `A+2B=1` give `A∈[0,1]`, `B∈[0,1/2]`. | Thirty slabs with one invariant sweep compile and certify in about 0.21 seconds; maximum nominal deficit from the numerical RPD reference is `7.40e-6`. |
| Water-gas shift and methanation | Two initial feed amounts in `[1/2,3/2]`; nonnegativity and carbon, oxygen and hydrogen inventories prove all five state intervals. | Thirty slabs and two sweeps compile and certify in about 2.60 seconds; maximum nominal deficit is `1.57e-4`. |

Across the twelve initial cases, certified numerical error allowances are at
most `1.155e-10`. Numerical physical-state comparisons at 9 or 81 parameter
grid points show no violation. This is a functionality check, with no comparison
against a competing implementation and no demonstrated global-MINLP speedup.
Nominal support deficits are numerical diagnostics, not certified error bounds
relative to the RPD solution. Their variation need not be monotone across
different sampled support sequences.

## Correction found by independent review

The first compiler draft accepted integer invariant metadata without coercion,
so Python division could introduce a floating approximation. For the equation
`3*x1=1`, this created an invalid signed upper derivative by exactly
`1/54043195528445952`. Model metadata now undergoes exact rational conversion
before any arithmetic, and implicit floating model constants are rejected.
The reviewer also found that a constant-only RHS was not lifted to an arithmetic
object; that case is corrected. The factory models already used fractions,
but the general interface required these fixes.

## Prior work and limitation that matter for global optimization

Validated convex/concave ODE relaxations are established. Sahlodin and Chachuat's
[Taylor-model method](https://doi.org/10.1016/j.compchemeng.2011.01.031) and
[discretize-then-relax method](https://doi.org/10.1016/j.apnum.2011.01.009) are
necessary competitors. Houska, Villanueva and Chachuat's
[stable set-valued integration method](https://doi.org/10.1137/140976807) also
addresses enclosure stability and wrapping, using a predictor-validation
approach with affine set parameterizations. Their abstracts/bibliographic
records were inspected and the sources were queued for full-text retrieval;
a detailed algorithm comparison is outstanding. The present prototype does
not establish novelty merely by producing mathematically validated ODE cuts.

Fixed broad state intervals need not give exact relaxation trajectories even
when the parameter box shrinks to a singleton. For the dimerization model with
rate fixed to one, one invariant sweep still leaves numerical half-horizon
state widths about `0.188603` and `0.0943015`. Consequently parameter branching
alone cannot be asserted to converge for this prototype.

To use it in a convergent global optimizer, state intervals must also tighten.
The held-support comparison remains valid with prescribed time-dependent
interval parts that enclose physical states. This route is now implemented,
as described next. Comparisons against stronger existing ODE relaxations and
useful optimization improvements remain outstanding.

## Validated time-dependent tubes and controlled coefficient rounding

`polynomial_tubes.py` implements exact interval arithmetic and a strict Picard
inclusion check for each raw time-slab box. Only after this check succeeds does
it intersect with the proved physical box and propagate conservation rows.
The endpoint interval follows from integrating the interval RHS over the slab.
See the [proof and convergence note](research-20260912-validated-polynomial-tubes.md)
and [independent review](research-20260912-polynomial-tube-independent-review.md).

`compile_slabs` uses the corresponding proved state box on each time interval.
It rejects mismatched time grids and model metadata. The same RHS is still a
caller obligation; metadata comparison cannot authenticate a supplied Python
callable. Direct comparison with the signed physical state proves validity
across tube switches. One should retain the interval objective bound alongside
affine cuts: interval-width convergence then supplies a safeguard independent
of the quality of support choices. Fixed endpoint rounding precision does not
give asymptotic convergence; its accumulated rounding error must also tend to
zero. The proof note retains an exact counterexample.

The singleton dimerization runs in
`results/ode_singleton_tubes.json` give the following first-state widths at
the nominal parameter (horizon `1/2`, one invariant sweep):

| Slabs | Interval endpoint width | Certified affine-cut width |
|---:|---:|---:|
| 10 | 0.370274 | 0.0257966 |
| 30 | 0.135870 | 0.00337640 |
| 100 | 0.0421501 | 0.000322392 |

The last run spends about 1.10 seconds on tube construction, support
compilation and certification. These exact affine cuts enclose the physical
state, conditional on the reviewed physical metadata and arithmetic, while
the tabulated decimal widths are rounded display values.

With varying interval coefficients, exact rational denominators made the
five-species matrix propagation expensive. `round_physical_supports` addresses
this without assuming inaccurate coefficients are exact supports. It rounds
the parameter/state slopes to a fixed rational grid, computes the exact
largest rounding error over `p∈P` and `z=(x,-x), x∈X`, subtracts that error from
the affine constant, then rounds the constant downward. State slope pairs are
combined using the exact physical relation between lower and signed upper
channels. Nonnegative off-diagonal coefficients remain nonnegative.

The resulting affine field bounds signed physical derivatives on the proved
tube. It need not minorize the full extended-RPD field away from physical
states. Direct cooperative linear comparison is sufficient, so this distinction
does not weaken the physical certificate. The independent reviewer checked
the rounding lemma and its implementation.

For quarter-width parameter boxes, compare
`results/ode_quarter_tubes.json` with `results/ode_rounded_tubes.json`:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/ode_support_experiment.py --output code/research_20260912/results/ode_rounded_tubes.json --models dimerization shift_methanation --steps 30 100 --sweeps 1 --parameter-factor 1/4 --validated-tubes --support-denominator 1000000
```

Omit `--support-denominator` for the unrounded comparison. In the 100-slab
five-species case, certification decreases from about 80.3 to 6.62 seconds;
combined tube/compilation/certification time decreases from 84.5 to 11.1
seconds. Every nominal state-width change is below `7.5e-7`. These are single
bounded runs of this implementation, not a benchmark against competing
validated ODE methods. The choice of a millionth grid is an experiment setting,
not an optimal precision policy.
