# Independent review of the controlled GDP instances

The initial review below covers the original 42 instances. The final section
independently reviews the subsequent nine-instance trigonometric extension and
updates the reviewed total to 51.

The instance generator is sound for its stated purpose: controlled tests of
bounded convex XOR GDPs. All 42 explicit witnesses and structural counts passed
independent checks against the original Pyomo models. Independent conic
enumeration of all 27 assignments in each of the five small pilot families also
produced feasible solutions with matching original-model objective values.
This review found no correctness blocker in the generator or its accompanying
model note. The suite alone does not establish application relevance, difficulty,
or practical superiority of LB-ESH.

The review was performed by a fresh subagent that did not author the generator,
its witness checker, or its model note. It read `instances.py`,
`lbesh-development-instances.md`, and the model assumptions of `conic.py`.
The independent tests and enumeration are in
`code/minlp_solver_lab/lbesh_research/test_instances_independent.py`.
They do not call `lbesh_research.validation` or the generator's `witness()`.

## Mathematical checks

For allocation models, every normalized coordinate and averaged coordinate is
between zero and 10/11 on the whole variable box. Logarithms and reciprocals
therefore have a positive domain margin, including at points that violate the
global sum-capacity row. The second derivatives printed in the model note are
correct and positive. Positive weighted sums after affine substitution are
convex; subtracting the epigraph variable preserves convexity. The upper
epigraph bounds use a coordinatewise maximum of increasing functions and do not
exclude the minimum epigraph value anywhere in that box.

All other nonlinear rows are sums of squares of affine expressions or positive
sums of exponentials of affine expressions. They are convex on the declared
domains. The region formulation is a sum-of-exponentials inequality equivalent
to a log-sum-exp sublevel set; its family name does not imply that the implemented
expression contains a logarithm. Region epigraph bounds are valid because each
congestion difference has absolute value at most three.

Each choice is a one-level XOR with three alternatives. XOR means exactly one
indicator is selected; it does not require the alternatives' continuous feasible
sets to be disjoint. The allocation alternatives overlap by design. Their
different fixed costs, operating costs, and capacities make this legitimate.

The analytical witness arguments in the model note hold for all draws in the
declared parameter intervals. In particular, standard capacity exceeds half
the unit capacity, each selected region center has exponential-row value four,
and the region witness's variation is at most 0.0512n, below the 0.55n limit.
The direct numerical checks additionally evaluated every global and selected
disjunct row, every bound, integer value, and XOR sum for all 42 instances with
a maximum allowed violation of 1e-10.

The nonlinear congestion expressions contain variables from all units, with
neighboring-unit interactions. The four allocation laws share the same genuine
coupling structure. This confirms a property of the formulations; it does not
prove that those constraints bind at optima or make any instance difficult.

## Independent numerical cross-check

CVXPY formulations were written independently of LB-ESH extraction, its master,
its cut generation, and the exact-hull builder. They use the generator's numeric
parameter data and variable upper bounds. Each small pilot instance was solved
for all 27 fixed choices with Clarabel. All returned optimal candidates were
mapped into the original Pyomo model and checked directly for bounds, active-row
feasibility, and objective agreement.

| Small pilot family | Best numerical objective | Selected modes | Original maximum violation |
| --- | ---: | --- | ---: |
| exp | 2.2988982512571163 | (0,2,2) | 3.60e-12 |
| log | 2.623680887970512 | (0,2,2) | 7.75e-11 |
| reciprocal | 2.3284312623657657 | (0,2,2) | 5.86e-12 |
| quadratic | 1.9062495933553476 | (1,2,2) | 2.46e-12 |
| logsumexp | 0.12390703718756486 | (1,2,0) | 0 |

Each allocation family had 16 assignments reported infeasible and 11 reported
optimal. The region family had 11 reported infeasible and 16 reported optimal.
One log assignment initially returned `optimal_inaccurate` at 1e-9 tolerances;
a retry at 1e-8 returned `optimal`. The artifact retains that initial status.
There were no unresolved assignments after the declared retry.

The exact quadratic hull baseline independently returned objective and bound
1.9062496233936121 on the small quadratic pilot, within 3.1e-8 of enumeration.
Its Gurobi run used one thread, a 30-second limit, and the baseline's default
gap tolerances. This confirms one model comparison, not the complete conic
translator implementation.

These are numerical cross-checks, not exact arithmetic certificates. Clarabel
optimality and infeasibility statuses were not independently certified by a
dual-residual checker. Accordingly, the table should not be promoted to exact
known optima or used to overstate the reliability of solver statuses. The
generator correctly leaves `known_optimum` unset.

## Design limitations and comparison requirements

The pilot and held-out seeds are disjoint. Repeated construction produced
identical parameter data, expressions, variable bounds, and initial values.
The four allocation families share their data, and sizes share unit-data
prefixes within each seed. They are paired mechanism tests, not 42 independent
draws from 42 application classes. Only two generator mechanisms and few seeds
are represented. The model note accurately reports these limitations.

The functions are nonquadratic, but they are conic-representable. Exponential
and negative-log epigraphs and the exponential regions admit exponential-cone
representations; reciprocal epigraphs on positive domains admit rotated
second-order-cone representations. Their quadratic global rows also admit
second-order cones. Thus the suite can test nonquadratic support and avoidance
of epsilon-perspective formulas. It cannot support a claim that these functions
fundamentally require a nonconic method. Any broad comparison against conic GDP
methods must acknowledge or test the applicable cones, rather than treating
the quadratic-only baseline's scope as a mathematical limitation of conic GDP.

No held-out optimization was run in this review. All solvers used one thread;
each continuous enumeration solve had a 30-second limit. No runtime comparison
is inferred from this correctness exercise. Difficulty and useful performance
separation still require the predeclared experiment and external instances.

## Reproduction and commands

The two original-model tests passed:

```sh
cd /workspace/minlp-notes/code/minlp_solver_lab
.venv/bin/python -m unittest lbesh_research.test_instances_independent -v
```

The independent enumeration used an isolated environment, without changing the
project dependencies. Python was 3.12.3, CVXPY 1.9.3, Clarabel 0.11.1, Pyomo
6.10.1, NumPy 2.5.3, and SciPy 1.18.1. The complete installed version list is
`code/minlp_solver_lab/results/lbesh_development/independent_instances_requirements.txt`.
The original installation and successful enumeration commands were:

```sh
uv venv /tmp/lbesh-independent-instances-env --python 3.12
uv pip install --python /tmp/lbesh-independent-instances-env/bin/python cvxpy pyomo
cd /workspace/minlp-notes/code/minlp_solver_lab
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /tmp/lbesh-independent-instances-env/bin/python -m lbesh_research.test_instances_independent --enumerate > /tmp/lbesh-independent-instances-enumeration.json
```

The retained output is
`code/minlp_solver_lab/results/lbesh_development/independent_instances_enumeration.json`.
Reproduction should install the retained requirements file in place of the
unpinned installation command above. The enumeration is optional; the ordinary
unit tests require only the existing project dependencies. A targeted
`.venv/bin/python -` script additionally called
`conic.solve(build('lbesh.quadratic.small.s104729'), time_limit=30, threads=1)`
and printed its status, objective, bound, and elapsed time. No project-wide
verification or CI inspection was performed.

## Independent review of the trigonometric extension

The additional law

    phi(z) = (1-cos(1.5z))/(1-cos(0.75))

is smooth, increasing, and strictly convex throughout the full argument box
`0 <= z <= 10/11`. Its derivative is
`1.5 sin(1.5z)/(1-cos(0.75))`, which is nonnegative on this interval. Its second
derivative is `2.25 cos(1.5z)/(1-cos(0.75))`, whose minimum is strictly positive
because `15/11 < pi/2`. These statements hold on the whole variable box, not
only on points satisfying the global sum-capacity row. The law is zero at zero
and one at one half. Positive sums after affine substitution preserve
convexity. Monotonicity validates the same box-based epigraph upper-bound
construction, and the unchanged standard-mode witness remains feasible.

The independent tests now check all 51 original Pyomo witnesses and structural
counts, as well as deterministic builds and disjoint pilot/held-out seeds.
The split is exactly 18 pilot and 33 held-out instances. A separate direct
comparison against the pre-extension manifest found all original 42 metadata
entries, including parameter hashes and generator versions, unchanged; the
only nine additions are the three existing sizes crossed with the three
existing seeds for `trig`. That manifest snapshot is retained in
`results/lbesh_development/independent_original42_manifest.json`.

There is also a direct source check: removing only the new family-tuple member
and scalar-law branch from the new file reproduces the previously reviewed
source hash
`171c50da9a23ba947c28e2d26ec941170b1551316596eb7065970282f7267fba`.
The extension's source hash is
`6e2ec1cae9b886297a1f641c7e4364a4ffa6634906fcb587d50a8768ebecb3de`.
This confirms that the original model-generation expressions were unchanged,
in addition to metadata agreement.

The extension is sound. It exercises a smooth convex law for which this work
supplies no standard-cone representation; this is not a claim that no conic
representation exists. It adds a cost law within the same allocation mechanism,
not another application domain. Its structural motivation and later addition
must remain visible in the experimental protocol. No trigonometric optimum,
runtime, or practical advantage has been established by these checks.

The optional independent cone enumeration was restricted explicitly to its
original five supported families. Its scalar dispatch now rejects unknown laws
instead of falling through to a quadratic expression. This prevents the new
family from being silently misrepresented by a reproduction command. The
general cone reference author was also asked to narrow its documented scope
and explicitly reject the unsupported trigonometric law.

The targeted command
`.venv/bin/python -m unittest lbesh_research.test_instances_independent -v`
passed three tests, including the new analytical curvature/normalization check.
Two `.venv/bin/python -` scripts independently compared the saved manifest and
reconstructed the prior source hash as described above. These extension checks
performed no optimization runs, held-out performance inspection, project-wide
verification, or CI inspection.
