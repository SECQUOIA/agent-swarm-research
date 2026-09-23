# Independent review of the actual-oracle diagnostic

Date: 2026-09-19. Reviewer: `/root/publication_challenge`, which did not
author the diagnostic, LB-ESH oracle, or theoretical example. Reviewed
artifacts are `code/minlp_solver_lab/lbesh_oracle_diagnostic.py` and
`code/minlp_solver_lab/results/lbesh_development/oracle_diagnostic.json`,
along with the completed [author note](lbesh-oracle-diagnostic.md).

**Verdict:** the diagnostic correctly measures the stated representation
effect using the actual frozen cut-generation routine. Its arithmetic,
function/gradient accounting, geometric stopping, support comparisons, and
non-dominance witnesses passed independent checks. It strengthens the case
for a modest computational paper by connecting the theoretical explanation
to executable oracle behavior. It does not establish full GDP performance,
general runtime superiority, or a new ESH principle.

## Independent source and mathematical checks

The diagnostic constructs an `LBESH` object without solver initialization
and invokes its existing `_esh_cuts` method through actual `NLRow` objects.
The wrapper supplies analytical values and gradients and counts calls. No
known boundary point is substituted into the ESH implementation. It asserts
that every requested ESH cut uses a distinct boundary point, excluding an
unreported ECP fallback in these trials. The manufactured rows isolate this
oracle; they do not exercise symbolic differentiation, hull transformation,
master optimization, NLP initialization, or callback integration.

For the scalar row, `q(x)=x-1`, and for two-dimensional rows,
`q(x)=x'Qx-1`, with `Q=I` or `diag(1,4)`. All base rows are convex. For
positive `a`, `exp(a*q)-1` is convex because exponential is convex and
increasing. Its sublevel set is exactly the base row's sublevel set. The
fixed zero anchors are strictly feasible for every tested representation.
Thus neither the feasible set nor anchor changes when comparing scales.

The largest transformed argument evaluated on the centered two-dimensional
rays is `32*(1.75^2-1)=66`; the smallest anchor argument is `-32`. Every
bisection point lies on the anchor-to-candidate segment, so these bounds
cover its evaluations too. Scalar arguments lie between `-32` and `32`.
All are safely finite in the tested arithmetic. The results do not license
extrapolation to arbitrarily large scales, where overflow and conditioning
become separate issues.

The scalar procedure simulates exact optimization of the retained affine
cuts over `[0,2]` by taking the new upper endpoint. Each new endpoint is
strictly smaller than its predecessor and at least one up to the declared
roundoff allowance, so it is the tightest retained bound. Every policy starts
with the same box-only master endpoint 2 and stops on `x-1 <= 1e-8`.
The prior endpoint is checked to exceed that tolerance. This is common
geometric accuracy; changing nonlinear row values cannot change the stopping
criterion.

I independently checked every stored ECP update against

```
p_next = p - (1-exp(-a*(p-1)))/a.
```

For transformed rows the total cut count exceeds `a*(1-1e-8)`, as required
by the strict per-step decrease bound. The untransformed affine row is a
separate control. ECP cut counts at the base row and scales
`1,2,4,8,16,32` are respectively `1,5,6,8,12,20,36`; each ESH run uses
one cut. Maximum stored-versus-analytical recurrence error is
`2.23e-16` after rounding upward. The affine base and scalar example should
not be portrayed as difficult GDP instances.

For each two-dimensional trial, the candidate is `radius*b`, where
`b'Qb=1`. The expected normal is parallel to `Qb`. The code divides both
the normal and constant by the same positive Euclidean norm, so comparisons
use the same original-coordinate halfspace scale. I independently checked
the full-ellipsoid validity condition

```
sqrt(n'Q^(-1)n) + c <= 0
```

with its numerical allowance, along with strict separation of the candidate.
This tests the maximum over the entire feasible ellipsoid, rather than
only a boundary sample. All 896 trials passed. ESH normalized constants
match the exact support constants within `4.45e-16`; this is agreement to
floating-point precision, not an exact arithmetic certificate. Bisection
boundary points are only approximate, even though their resulting tangent
constants agree that closely on these rows.

Centered anchors and radial candidates make the ESH and ECP normals
parallel here, and ESH yields the tighter halfspace. That deliberately
controlled geometry does not imply general dominance. The separate
off-center disk example uses candidate `(2,0)`, anchor `(0,0.9)`, and
witnesses `(1.2,1)` and `(1.3,-2)`. Independent substitution gives ECP
cut values `-0.05,+0.05`, and ESH cut values approximately
`+0.543346,-0.912852`. Their opposite signs demonstrate both failed
inclusions. The witnesses need not be disk-feasible: they compare the
two outer halfspaces. Each cut's disk validity is checked separately.

## Evaluation accounting and reproducibility

The stored counts are calls to the row's value and gradient interfaces.
A gradient evaluation may itself evaluate exponential internally; the
separate gradient count accounts for that operation. These counts are not
counts of elementary floating-point instructions.

I independently instrumented the counted wrapper's value calls for one
ellipsoid trial, then reconstructed every bisection midpoint and bracket
update from the recorded arguments. The call order is one candidate value,
one anchor value, 34 bisection midpoint values, and one value used with the
final tangent gradient. Thus an ESH cut uses 37 values and one gradient;
its root-search count is one and its root value count is 34. ECP uses two
values and one gradient per cut. The diagnostic's subtraction of three
non-root values per ESH cut is correct for this frozen routine and the
asserted absence of fallback. A changed oracle would require rechecking
that accounting rule.

The nine timing samples per trial are descriptive microtimings. They
exclude model construction, interior-point search, optimization, imports,
and solver startup, and are collected in a fixed policy order. They should
not be interpreted as a full-algorithm speed comparison or an independent
statistical performance study. Operation counts and geometric checks carry
the diagnostic's principal evidence.

An independent full replay produced the same 14 scalar and 896
two-dimensional records. Every non-timing field matched the saved artifact
exactly. Saved SHA-256 values matched the current diagnostic, solver, and
structure files. The reviewed diagnostic source hash is
`56cc9f2b532dfb1a2f2de3f36fa2039995d8d4c3359f57ea8e48d4965a664f4b`.

Targeted commands, from `code/minlp_solver_lab`:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  .venv/bin/python lbesh_oracle_diagnostic.py \
  --output /tmp/lbesh-oracle-independent-replay.json
```

Two additional `.venv/bin/python -` inline scripts performed the independent
artifact/trace audit described above and checked the author's numerical
table, final scalar error, and timing ranges against the saved JSON. All
checks passed. The final author note accurately states the finite-arithmetic,
analytic-wrapper, fixed-anchor, centered-geometry, and timing limitations;
I found no wording correction necessary. These checks used the existing
Python 3.13.11 environment with
NumPy 2.5.3, Pyomo 6.10.1, and gurobipy 13.0.3. No solver optimization,
license request, new dependency, project-wide verification, or CI inspection
was performed.

## Implication for publication scope

The diagnostic establishes a useful mechanism: fixed-anchor radial cuts
remain nearly invariant across these equivalent smooth representations,
whereas point tangents weaken and require more sequential scalar master
updates. It also measures the price: every radial cut spends 34 root value
evaluations before its final tangent, including on the affine control where
point separation already finishes in one cut. The off-center example
prevents a false universal dominance inference.

Together these observations support an interpretable computational study
even if its main GDP results are mixed or negative. They explain why radial
separation can save master steps while still failing to improve total time.
They do not prove that representation sensitivity causes any particular
main-benchmark outcome; that link still depends on the completed study's
measured cuts, times, and formulation/tree comparisons. The independent
publication challenge's requirement for a bounded actual-oracle mechanism
diagnostic is satisfied.
