# Independent closed-cone reference for the controlled LB-ESH suite

This baseline gives exact mathematical cone formulations for five supported
controlled families: exponential, logarithmic, reciprocal, quadratic, and
log-sum-exp. These cover 42 of the current 51 controlled instances. The nine
trigonometric instances added later are explicitly unsupported: the Python API
raises `UnsupportedConicReference`, and the command-line interface records
`status: unsupported`. No verified cone mapping for that family is implemented;
this makes no claim that such a representation is mathematically impossible. Clarabel solves those formulations in floating point. Neither a
reported optimal status nor a numerical dual objective is a rigorous certificate.
The baseline currently provides continuous hull roots and exhaustive small-instance
references; it is not a competitive mixed-integer exponential-cone solver.

Implementation: `code/minlp_solver_lab/lbesh_research/conic_reference.py`.
It reads only the named instance metadata and coefficient generator. It does not
read Pyomo expression trees, invoke LB-ESH extraction, or reuse its cuts.
An independent reviewer separately implemented the original fixed-assignment
models using CVXPY's ordinary exp, log, inverse and square atoms before inspecting
this explicit cone implementation.

## Exact formulation

Write the closed exponential cone as

\[
K_{\exp}=\operatorname{cl}\{(a,b,c):b>0,\ b\exp(a/b)\le c\}.
\]

Its zero-scale slice is `b=0, a<=0, c>=0`. The
[CVXPY exponential-cone definition](https://www.cvxpy.org/api_reference/cvxpy.constraints.html#cvxpy.constraints.exponential.ExpCone)
and [implementation](https://www.cvxpy.org/version/1.5/_modules/cvxpy/constraints/exponential.html)
use this convention. For a disjunct weight `y`, normalized copied argument `z`,
and epigraph copy `q`, the implemented perspectives are:

| Original law | Cone epigraph |
|---|---|
| `(exp(3z)-1)/(exp(1.5)-1)` | `(3z,y,(exp(1.5)-1)q+y) in K_exp` |
| `-log(1-z)/log(2)` | `(-log(2)q,y,y-z) in K_exp` |
| `1/(1-z)-1` | `(q+y)(y-z)>=y²`, both factors nonnegative |
| `4z²` | `q*y>=4z²`, both factors nonnegative |

The product inequalities use ordinary second-order cones:
`a*b>=c², a,b>=0` iff `norm((2c,a-b))<=a+b`.
All allocation laws are nonnegative on the copied nonnegative input domain, so
`q>=0` is valid. Their coefficients in the cost constraint are positive.
Consequently separate epigraph variables introduce no relaxation: the sum of
epigraph values can meet the budget exactly whenever the original sum can.
For positive `y`, division by `y` recovers the original constraint. Copied box
bounds imply `z=0` at `y=0`; nonnegative epigraph variables can be set to zero
there. The log and reciprocal input box gives `z<=y/1.1`, keeping normalized
arguments uniformly away from their singularity when `y>0`.

For each geometry disjunct, four cone rows are

\[
(s\alpha_p(u_p-c_p y),y,r_{p,s})\in K_{\exp},\qquad
\sum_{p,s}r_{p,s}\le R y,
\]

where `s` ranges over `-1,+1`, with `-2y<=u_p<=2y`. At `y=0`, the copied
coordinates and all `r` are zero. Positive `y` recovers the original sum of
exponentials constraint.

Within each allocation disjunction both coordinates and the epigraph `t` are
disaggregated for every mode, including the off mode. Each copy receives the
original common finite box scaled by its mode weight. The copied mode-capacity
constraint, cost constraint, and off-mode `t=0` are imposed, and copies sum to
the original variables. Geometry disjunctions analogously disaggregate both
coordinates. The weights sum to one. Since each bounded disjunct is closed and
convex, this is its standard exact convex combination formulation. Global
coupling constraints remain on the original variables. Thus the resulting root
is the intersection of individual-disjunction convex hulls and global constraints;
it is not claimed to be the convex hull of the complete feasible GDP.

Fixed assignments use direct cones at `y=1` for the selected mode; inactive
modes are omitted. This avoids unnecessary zero-scale cones in enumeration.
The dual objective has the exact analytic fixed-charge constant added back.

## Reproduction and numerical evidence

The isolated environment is `lbesh_research/conic_reference_env/` with its own
`pyproject.toml` and `uv.lock`. Direct dependencies are Python 3.13,
Pyomo 6.10.1, CVXPY 1.7.3 and Clarabel 0.11.1. The lock records all transitive
versions. The actual resolved numerical versions are NumPy 2.5.3 and SciPy 1.18.1.
The main solver-lab environment also received CVXPY/Clarabel through an initial
`uv pip install`; its project manifest and lock were not changed. The isolated
environment is used for recorded reference runs.

From `code/minlp_solver_lab`:

```sh
uv sync --frozen --directory lbesh_research/conic_reference_env
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 lbesh_research/conic_reference_env/.venv/bin/python -m unittest lbesh_research.test_conic_reference
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 lbesh_research/conic_reference_env/.venv/bin/python -m lbesh_research.conic_reference --name lbesh.exp.small.s104729 --out results/lbesh_development/conic_exp_pilot.json
```

Add `--enumerate` only for the small instances; larger enumeration is rejected.
Each solve records source/lock hashes, solver and package versions, solver status,
canonical primal/dual residuals, numerical gap, setup-inclusive elapsed time and
Clarabel-only runtime. Clarabel's linear solver reports one thread; the
[solver settings](https://clarabel.org/stable/api_settings/) document these controls.
The result's flat `witness` mapping can be checked with
`validate_witness(build(name), {"variables": result["witness"]}, reported_objective=result["obj"])`
for integer assignments. A continuous root witness is generally fractional and
must not be classified as GDP feasible by that validator.

The four targeted unit tests passed on 2026-09-19: explicit unsupported-family
rejection, positive and zero perspective
scales for four laws, finite-epigraph rejection of singular log/reciprocal inputs,
and agreement of all five independent best pilot assignments with the original
Pyomo feasibility validator. All-mode-one fixed witnesses also passed for all five
small pilots; their largest original row residual was `8.36e-11`. No project-wide
verification or CI inspection was run.

An initial singular-log test allowed `q<=100`; the exponential cone then involved
a value below `1e-30` and Clarabel returned `user_limit`. The final test uses
`q<=2` so infeasibility has a numerically resolvable separation. This is a reminder
that cone reformulations avoid epsilon-model bias but do not remove numerical
conditioning limits. The controlled log family has a uniform positive denominator
margin from its finite box.

### Reference-only pass before the protocol freeze

A coordination misunderstanding caused all 42 continuous roots, including
held-out seeds, to be solved before the code review and protocol freeze.
`results/lbesh_development/general_conic_roots.json` preserves this preliminary
pass. No held-out objective was inspected to tune the method or the instances;
only aggregate status, residual and timing statistics were inspected. The pass
had both `optimal` and `optimal_inaccurate` statuses, maximum canonical primal
residual `5.83e-10`, maximum canonical dual residual `2.64e-9`, and total
setup-inclusive time about 6.6 seconds. These residuals are not certificates of
original GDP feasibility or exact dual feasibility. This pass predates the
addition of source hashes and exact analytic objective offsets (root offsets are
zero, so the latter does not alter these roots).

The held-out set must therefore be described as predeclared and untuned, not as
completely unexamined before freezing. A fresh reference pass after independent
review should be retained separately with frozen fingerprints. This preliminary
file must not be silently relabeled as that frozen run.

## Frozen reference batch

`code/minlp_solver_lab/lbesh_reference_batch.py` schedules the 42 supported roots
and all 14 supported small instances (27 assignments each), sequentially at one
thread after the main and supplemental solver queues finish. It uses the frozen
reference module unchanged, checks its source and environment hashes against
`source_v1_manifest.json`, and verifies the pinned interpreter and direct package
versions. There are no numerical retries or tolerance changes. Solver exceptions
are retained per assignment as explicit unresolved records; other assignments
continue. Every original solver status and result remains in the output.

From `code/minlp_solver_lab`, run:

```sh
lbesh_research/conic_reference_env/.venv/bin/python lbesh_reference_batch.py --roots-out results/lbesh_development/general_conic_roots_frozen_v1.jsonl --enumeration-out results/lbesh_development/general_conic_enumeration_frozen_v1.jsonl
```

The driver sets BLAS/OpenMP thread limits before importing numerical libraries.
Both outputs are created exclusively; existing files cause refusal before any
solve. Add `--dry-run` to check the environment and print the schedule without
solving or creating outputs. The dry run verified 42 roots and 14 enumerations.
A mocked numerical-failure check verified that all 27 assignment failures remain
visible with no retries; this check ran no optimization.

The frozen JSONL files are directly readable by
`lbesh_study_analysis.py --references`. Once the complete frozen rerun exists,
it supersedes the preliminary `general_conic_roots.json` for reported root
comparisons. The preliminary artifact remains as evidence of the disclosed
pre-freeze pass; it must not be relabeled or supplied as a frozen reference.
