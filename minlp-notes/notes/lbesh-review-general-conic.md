# Independent review of the general cone reference

The explicit cone reference is correct for the original five families of the
bounded controlled instance suite. The later trigonometric extension is outside
this reviewed cone formulation's scope. Its continuous formulation represents the intersection of the individual
disjunction hulls and the original global constraints. It does not claim the
convex hull of the complete GDP. Independent fractional-root comparisons passed
for all five small pilot families, as did scalar perspective checks at zero,
small, and ordinary positive weights. No correctness blocker was found.

This reviewer had already implemented and run a separate original-model
CVXPY enumeration before reading `conic_reference.py`. For this review, a
second independent hull formulation was written using CVXPY's perspective
atom, without the author's explicit cone maps. It appears in
`code/minlp_solver_lab/lbesh_research/test_conic_reference_independent.py`.
Only small pilot instances and scalar analytic cases were solved in this review.

## Closed perspectives and bounded hull

For positive weight y, the exponential cone means
`y exp(a/y) <= b`; at zero weight its closed slice is `a <= 0, b >= 0`.
Direct substitution into the four implemented maps gives:

- Exponential: `q >= y (exp(3z/y)-1)/(exp(1.5)-1)`.
- Negative log: `q >= -y log(1-z/y)/log(2)`.
- Reciprocal: `(q+y)(y-z) >= y^2`, with nonnegative factors, giving
  `q >= y (1/(1-z/y)-1)`.
- Quadratic: `q y >= 4 z^2`, giving `q >= 4z^2/y`.

The ordinary SOC conversion `norm((2c,a-b)) <= a+b` is equivalent to
`ab >= c^2` with nonnegative a and b. Its factors and the factor four in
the quadratic norm are correct. The constraint `q >= 0` is valid because all
four original laws are nonnegative on the declared production domain.

The scaled coordinate bounds force copied coordinates to zero at y=0.
Copied cost bounds `0 <= v <= upper*y`, together with positive cost weights,
then force every allocation epigraph q to zero as well. The zero-weight copies
therefore introduce neither a missing limit point nor spurious nonzero cost
or production. At positive weights, `z <= (10/11)y` keeps the log and
reciprocal arguments away from their singularities. Separate epigraph variables
for positive sums of convex costs are exact: feasible original values can
choose every epigraph at equality, and any larger choices only tighten the
upper cost budget.

The region cone rows use the correctly shifted copied argument
`scale*(u-center*y)`. Their four nonnegative right sides sum to at most
`radius*y`. At y=0 the copied box gives u=0 and their sum bound makes every
right side zero. At positive weights the original region follows by division.

Every allocation disjunction disaggregates both production coordinates and its
cost variable, including the off alternative. Each copied bound matches the
corresponding original common variable bound. The independently recomputed
cost upper bound is algebraically the same box maximum used by the generator;
ordinary floating-point evaluation may differ by rounding in the last bits.
Geometry disjunctions copy the two coordinates that occur in their region rows;
their global epigraph t is correctly retained outside the disjunctions.
All original demand, capacity, resource, congestion, variation, and objective
expressions match the generator.

With fixed modes, inactive alternatives are omitted and selected copies have
weight one. That is the original convex continuous subproblem and avoids
unnecessary zero-weight exponential cones. Input mode count and membership are
checked. As a suite-specific reference, this module has a deliberately much
narrower scope than a generic GDP translator.

## Independent fractional comparisons

The separate hull formulation uses CVXPY's `perspective` atom on the original
cost or region expression. It independently imposes common scaled boxes,
individual disjunction equations, and global constraints. This checks
fractional behavior, beyond the earlier integer-assignment comparison.

| Small pilot family | Independent perspective root | Explicit cone root |
| --- | ---: | ---: |
| exp | 2.29785515258 | 2.29785515256 |
| log | 2.57866163110 | 2.57866163030 |
| reciprocal | 2.32842730218 | 2.32842730234 |
| quadratic | 1.89737943602 | 1.89737943620 |
| logsumexp | 0.0788769337448 | 0.0788769333719 |

All five pairs agreed within 8.1e-10; all statuses were `optimal` at 1e-9
tolerances. The explicitly returned primal and numerical dual objectives also
agreed within 2e-7. This comparison shares CVXPY and Clarabel as numerical
infrastructure but not the formulation code or explicit perspective maps. The
analytic derivation above supplies the separate mathematical check.

Forty-eight scalar tests cover four laws, weights 0, 1e-5, 0.35, and 1, and
normalized inputs 0.1, 0.5, and 0.85. Their minima matched the known perspective
values within 2e-8. An initial run at unusually strict 1e-10 tolerances returned
`optimal_inaccurate` for the reciprocal case with weight one and input 0.85.
The final tests use the reference's ordinary 1e-9 tolerances and all return
`optimal`. The initial status is recorded here rather than treated as a model
error or silently erased.

## Numerical bounds and provenance

The raw Clarabel dual objective is a numerical estimate. At fixed assignments,
the exact analytic fixed-charge constant must be added because canonicalization
removes it. The initial implementation inferred that constant by subtracting
two numerical primal objectives. The author adopted this reviewer's
recommendation to compute the known fixed-charge sum directly. Root objectives
have zero such constant.

`bound_certified` is always false and `bound_kind` explicitly identifies a
floating-point conic dual estimate. This is appropriate. Canonical primal and
dual residuals measure the solver's conic system, not original Pyomo constraint
feasibility or exact dual feasibility. A fractional root witness is not an
integer GDP witness. Small residuals and close primal and dual objectives do
not turn these outputs into rigorous certificates.

`solve` retains `optimal_inaccurate` as a distinct status while returning the
available approximate primal and dual values; it does not rename that status
as optimal. `enumerate_small` treats such an assignment as unresolved and
withholds an enumeration lower estimate when any assignment is unresolved.
CVXPY warnings are not suppressed. Solver-limit statuses likewise do not
produce a claimed solved reference. Even an enumeration with only `optimal`
and `infeasible` statuses remains a numerical reference: infeasibility and
dual feasibility have not been independently certified.

The output records source hashes, the intended environment lock hash, and
actual runtime versions. The lock hash identifies the recorded environment
specification; it is not by itself proof that a caller used that environment.
Actual version fields retain that distinction. At review completion, before
the trigonometric generator extension and its unsupported-family guard:

| File | SHA-256 |
| --- | --- |
| `conic_reference.py` | `f56726090abbff0f126eeb003a204d01aa018a4efc4f5e88c22ac2db3a94efff` |
| `instances.py` | `171c50da9a23ba947c28e2d26ec941170b1551316596eb7065970282f7267fba` |
| `conic_reference_env/uv.lock` | `031d9c4c1b9947571870367c54c9254e3f9da21382eecb446072d1d7e60558f0` |

## Protocol deviation and reproduction

The coordinator and author reported that an ambiguous coordination instruction
led to solving all 42 continuous roots before the protocol freeze, including
the designated held-out seeds. This review did not inspect those held-out
objectives or use them to change model or algorithm settings. The author's
development note preserves the preliminary pass and states what was inspected.
The held-out set can be described as predeclared and untuned; it cannot be
described as completely unexamined before the freeze. A subsequent frozen
reference pass must retain a distinct artifact and its source hashes. The
independent checks in this review remain confined to pilot and analytic cases.

From `code/minlp_solver_lab`, these two targeted commands passed two tests each
(five root pairs and 48 scalar cases):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /tmp/lbesh-independent-instances-env/bin/python -m unittest lbesh_research.test_conic_reference_independent -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 lbesh_research/conic_reference_env/.venv/bin/python -m unittest lbesh_research.test_conic_reference_independent -v
```

The first environment was separately created for the prior independent
enumeration: Python 3.12.3 and CVXPY 1.9.3. Its pinned version list is retained
in `results/lbesh_development/independent_instances_requirements.txt`. The second
uses the author's lock with Python 3.13 and CVXPY 1.7.3. Both use Clarabel
0.11.1; results agreed at the printed precision. All solves used one thread and
a 30-second limit. `sha256sum` on the three files above recorded the reviewed
versions. No project-wide checks or CI inspection were performed.
