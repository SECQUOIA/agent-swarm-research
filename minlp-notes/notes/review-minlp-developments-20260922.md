# Corrective audit of recent MINLP developments

Date: 2026-09-22. Scope: the quadratic aggregation certificate, monomial wedge
envelopes, constrained clustering and reduced-space extension, row hulls, and
shared-variable convexification. The user requested ten subagents to search
for mistakes and apply justified corrections. Ten reviewers were assigned
separate tasks; the coordinating agent checked findings and reviewed edits.
This audit began at commit `481e01a2` with a clean working tree.

## Assessment

No error was found in the main quadratic aggregation theorem or the six
principal wedge regimes with nonzero exponents and nonzero exponent sum.
The main clustering bound and conditional reduced-space transfer also
survived, with proof and scope corrections. These are human-readable proof
audits, not formal certification or a guarantee that no errors remain.

The audit found substantive false ancillary statements, an invalid
counterexample, an incomplete exponent classification, and an implementation
bug capable of producing an invalid row-hull cut. Earlier positive review
verdicts therefore needed qualification. The corrected conclusions, rather
than the historical verdicts, govern the current results.

## Review assignments

| Reviewer | Scope | Outcome |
|---|---|---|
| `aggregation_proof` | Main theorem and cone-separation argument | No main-proof error found; independently disproved the stronger relaxation claim; rechecked its correction. |
| `aggregation_corollaries` | Corollaries, closed-system example, SDP interpretation | Corrected scope and stability example; exact witness checks. |
| `wedge_main` | Six regimes, zero individual exponents, numerical checker | Main regimes retained; missing cases and checker behavior corrected. |
| `wedge_boundary` | Degree zero, ordinary versus closed hull | Derived and independently checked the replacement hull description. |
| `cluster_proof` | Local lower-bound proof and assumptions | Corrected final infimum passage; reviewed the repaired example and domain-reduction qualifications. |
| `cluster_counts` | Counting, reduced space, illustration | Repaired the counterexample and removed unsupported automatic width guarantees. |
| `novelty_audit` | Primary sources and relevance claims | Distinguished exact published questions from related results and qualified novelty. |
| `row_hull_audit` | Theory, pricing implementation, experiments | Repaired pricing/proof claims and the endpoint-rounding bug. |
| `shared_variable_audit` | Links, moment hulls, residuals, literature | Corrected epigraph and projection claims; reproduced the saved point's exact residual. |
| `status_consistency` | README, logs, review records | Reconciled current scope, historical claims, timings, and verification labels. |

## Applied corrections

### Quadratic aggregation

The theorem guarantees existence of a nontrivial globally convex aggregation
when the hull is proper under its assumptions. It does **not** say that such
aggregations imply every valid linear inequality or describe the hull.
The corrected note exhibits an HHC system with feasible strip
`-2 < x_1 < -1` whose globally convex aggregations and Shor relaxation admit
zero. BDS's good aggregations must not be conflated with globally convex
quadratic functions.

The claim separating HHC from stable convexity now has explicit arbitrarily
small perturbations and a midpoint contradiction. A stale Shor-equality
statement was corrected. Near-zero numerical SDP values are not certificates
of exact zero; the SDP result is a mathematical characterization rather than
an implemented certified classifier. The main theorem and corollary
statements were retained.

### Monomial wedges

The former degree-zero product formula confused the convex hull with its
closure. For `f=x_2/x_1` and ratios in `[1,2]`, the claimed product contained
`(1,1,2)`, while every graph combination with `x_2=x_1` has height one.
The replacement treats empty domains, a single ray, effective value bounds,
boundary fibers, and constant functions. A separate univariate case covers
one zero exponent, which the six-regime table omitted.

The numerical checker now distinguishes signed validity discrepancies from
finite-sample approximation error, rejects unsuccessful LP solves, and exits
unsuccessfully when an inconsistency is detected. Numerical sampling remains
a sanity check, not a proof of envelope validity or exactness.

### Clustering and domain reduction

The local proof now takes an infimum of the pointwise lower bound correctly.
The Taylor continuity-modulus repair and the sign `eps-eta` for incumbent
error were already present before this audit; they are not new fixes here.
The equality case `eta=eps` is now distinguished from `eta>eps`.

The former neighborhood counterexample used the wrong side of a constraint
surface. Its feasible set was not a singleton, and the original objective
could also improve at first order. The box orientation is corrected, with
an explicit relaxed-feasible witness proving a first-order gap. The old
numerical gap limits are withdrawn. This disproves automatic neighborhood
second-order convergence for that scheme, not the possibility of designing
a different scheme with that property.

Counts are local and scale-wise for disjoint boxes with comparable side
lengths. They are not total-tree or runtime bounds. Quartic and first-order
scaling claims were corrected; finite numerical observations are not
asymptotic proofs. The conditional width-tight domain-reduction theorem is
retained. Unsupported claims that interval Newton, affine fibers, FBBT, or
OBBT automatically meet it were replaced by a certified local-branch
construction and explicit limitations.

The illustration also omitted the initial unfathomed root from its maximum
open-box count when both children fathomed immediately. Its initialization
now counts that root; the historical examples had larger maxima and do not
depend on this edge case.

### Row hulls

A floating-point inverse coordinate map can send an exact normalized
endpoint just inside a discontinuous concave item. Its mathematical chord
gap is zero at the endpoint, but evaluating the nearby interior point can
give a positive jump and invalidate a pricing bound. The implementation
now enforces the exact endpoint values, with an independent regression.

The no-gain criterion now includes nonaffine concave functions, rather than
only strictly concave ones. The merged-pricing approximation proof now
repairs a near-feasible box point globally instead of assuming the retained
maximum-profit subset remains feasible after clipping. Its guarantee is
explicitly ideal-arithmetic pricing for a fixed dual vector, not an
approximate separation algorithm or a floating-point certificate. Mixed-row
pricing now includes the omitted full-item profits. A false restriction of
possible gains to faces with a linear item at its bound was removed.

### Shared-variable terms

The joint epigraph hull need not equal the intersection of individual
epigraph hulls. The new example `x^2, sqrt(x)` on `[0,1]` disproves the
blanket claim and the resulting exclusion of one-sided mixed-curvature uses.
The note distinguishes a nonlinear relation from its convex hull and lists
all nonnegative factors needed in the displayed moment cones; the cone code
already imposed them. Literature comparisons now account for changes of sign
in lifted coordinates before claiming that mixed curvature is outside prior
theory.

The saved water-network point has positive exact violation
`32325/2^49`, approximately `5.742e-11`. It meets the stated tolerance but is
not an exactly feasible point or a certified upper bound on the exact
problem. The rounded upper bound is `5.8e-11`. Solver-reported solve counts
and dual bounds remain uncertified. Stale BARON and SCIP descriptions were
corrected.

## Verification and limits

Only topic-specific checks were run. No project-wide verification, CI
inspection, expensive benchmark reruns, or Lean formalization was performed.
The historical solver tables were not regenerated with the endpoint fix;
their code hashes refer to the historical benchmark revision. Exact witness
checks test the corrected examples, not the universal theorems.

The following commands were run from the repository root unless a different
working directory is stated. Python environments were the existing project
environment or Conda `minlp-notes`; no packages were installed for this audit.

| Command | Outcome |
|---|---|
| `python3 code/quadratic_aggregation/check_scope_counterexamples.py` | Exact aggregation and stability witnesses passed; independently rerun by the main-proof reviewer and coordinator. |
| `python code/cluster_problem/check_counterexample.py` | Exact symbolic identities, relaxation convexity, and critical-space curvature passed (SymPy 1.14.0). |
| `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python code/monomial_wedge/check_envelopes.py` | All 26 nonzero-degree cases and exact rational degree-zero examples passed (NumPy 2.5.1, SciPy 1.18.0). Maximum reported signed LP discrepancy `1.0e-15/u`, finite-sample discrepancy `4.2e-4/u`, no sampled outside point found LP-feasible. |
| `python code/row_hull/review_code/check_audit_scope.py` | Three exact rational checks passed. |
| `code/minlp_solver_lab/.venv/bin/python code/shared_variable_terms/exact_check_point.py waterno2_18 code/shared_variable_terms/point_waterno2_18.json` | Saved objective and positive residual reproduced exactly. |
| `code/minlp_solver_lab/.venv/bin/python code/shared_variable_terms/review/exact_scope_audit.py` | Exact-decimal coefficient check and epigraph/cone counterexamples passed; reuses the existing XML parser. |
| `git diff --check` | No whitespace errors in the final changes. |

From `code/row_hull`:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
../minlp_solver_lab/.venv/bin/python -m pytest -q -p no:cacheprovider test_rowhull.py
```

Result after the endpoint correction: **217 passed**. The following additional
comparison used the existing review script's fixed RNG seed 1 and checked
300 nine-item rows against brute-force pricing, including forced compression
and one-/two-decimal widths. No invalid lower bound was found.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
../minlp_solver_lab/.venv/bin/python - <<'PY'
from review_code.check_pricing import main
for decimals in [1, 2, None]:
    for kmax in [8, 4000]:
        main(decimals, 50, 9, kmax)
PY
```

The root-counter correction was also checked without solving any optimization
problem:

```bash
conda run -n minlp-notes python - <<'PY'
import runpy
m = runpy.run_path("code/cluster_problem/count_boxes.py")
bb = m["branch_and_bound"]
root = ((0.0, 1.0),)
lb = lambda box: -1.0 if box[0][1] - box[0][0] > 0.75 else 0.0
assert bb(lb, root, 0.0, 0.1) == (1, 1)
assert bb(lambda box: 0.0, root, 0.0, 0.1) == (1, 0)
PY
```

The coordinating agent ran the equivalent `python -c` command; both checks
passed. Reviewers also independently re-read the corrected aggregation,
wedge-boundary, and clustering arguments. These rechecks found no further
necessary mathematical correction within their assigned scopes.
