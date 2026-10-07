# Automatic joint convexification of small nonlinear blocks

This continuation develops a solver implementation and a coherent set of
results for joint convexification. The central operation is to propose a
linear inequality involving several nonlinear expressions, then certify a
lower bound on its support value over their common domain. Automatic discovery, proof of the
inequality, and the decision to spend solver time on it are separate tasks.

Read the integrated [report](document/main.pdf) and its
[claim-to-evidence map](document/COVERAGE.md) for the mathematical statements,
proofs, implementation boundaries, and computational evidence.

The [development program](PROGRAM.md) records the authorized scope. Earlier
univariate envelopes, curve-hull separation, and row-hull results are the
starting point; they are not claimed as new results of this continuation.

The controlled experiment supports keeping the new separator experimental
and leaving native SCIP as the default. Baseline and reformulation control
solved 19 of 24 selected application models; both cut modes solved 18.
Twenty models reached the solver, three failed the common domain admission
check, and one used unsupported variable exponents. All 1,082 recorded cuts
passed replay, and all 270 returned incumbents passed numerical residual
checks. These checks establish neither a general runtime benefit nor a
certificate for SCIP's complete solve. See the
[results](experiments/campaign-v1/results.md),
[raw comparisons](experiments/campaign-v1/summary.json), and
[replay record](experiments/campaign-v1/replay.json).

## Results and implementation

- **Rigorous exported cuts.** The [support kernel](solver/certified.py) proves
  bounds for supported polynomial and univariate elementary expressions.
  It certifies the actual binary64 direction, rounds the right-hand side
  outward, retains the complete proof domain, and provides a model-bound
  replay interface. The [numerical contract](numerics/contract.md) states the
  precise supported language and trusted arithmetic.
- **Coupled quadratic blocks.** The [theory and exact oracles](theory/README.md)
  cover arbitrary rational polygons in two variables, including line and
  point domains. A constrained-star extension permits any number of leaves
  sharing a center, with affine rows involving the center and at most one
  leaf. Conditional minimization produces a finite rational partition and
  an exact support value in polynomial time.
- **A reason to merge overlapping blocks.** The
  [overlap analysis](theory/overlap-review.md) gives an explicit unit-box
  example whose exact pair hulls permit value zero while the joint minimum
  is `1/128`, even with matching shared first and second moments. It also
  characterizes the gain from merging specified pair directions. This is a
  comparison with exact pair hulls; it does not imply dominance over dense
  semidefinite relaxations with additional lifted variables.
- **Automatic solver integration.** The [SCIP integration](solver/integration.py)
  discovers supported blocks, caches samples, bounds separation work, and
  retains native nonlinear enforcement. A
  [convex-combination certificate](implementation/screening.md) can safely
  skip separation at the current point when every normalized cut violation
  is at most the chosen tolerance. Floating-point searches only propose cuts.
- **An optional native sampling kernel.** The
  [C implementation and measurements](implementation/native-kernel.md)
  accelerate selected repeated polynomial evaluations. This is candidate
  generation, not a native SCIP constraint handler or a claim of faster
  complete solves.

Exact support does not make the bounded normal search complete. A failed or
budget-exhausted search means no cut was produced; it is not a proof of hull
membership. Cut certificates also do not certify SCIP's final global bound.

The importer has a deliberately narrow correctness contract. It checks the
whole source row against the assembled native expression, checks auxiliary
definitions and rewritten rows, and requires source domain restrictions to
hold throughout the declared box. It refuses models that fail these checks,
including some expressions whose domain constraints would otherwise narrow
the feasible set. Refusals are part of the measured applicability, not omitted
instances. The full solver still uses numerical feasibility and presolve.

## Evidence and attribution

The [frozen experiment protocol](experiments/protocol.md) specifies native
SCIP, matched auxiliary reformulation, unconditional activation, and automatic
activation controls. It separates synthetic mechanisms, a deterministically
selected application slice, and historical diagnostics. Original-model
residuals, proof replay, timing, and rejected blocks are separate evidence.

The [literature assessment](literature/README.md) and
[source manifest](literature/sources/MANIFEST.md) document the relevant primary
texts and versions. Simultaneous vector convexification, low-dimensional
quadratic hulls, rigorous Bernstein bounds, and box-star optimization all have
direct predecessors. The constrained-star construction, certificate contract,
and measured implementation are assessed against those predecessors; an
unsuccessful literature search would not establish publication priority.

Independent research agents reviewed the arithmetic, integration, and proofs.
These are internal reviews, not journal peer review or formal verification.
The [verification record](VERIFICATION.md) gives the actual targeted commands
and results. Project-wide verification and CI inspection are excluded by the
repository instructions.

## Running the implementation

Run commands from the repository root. The experiment environment uses Python
3.13.11 and the versions in [requirements.txt](requirements.txt). A separate
environment can be installed explicitly:

```sh
uv venv --python 3.13 /tmp/joint-convexification-env
uv pip install --python /tmp/joint-convexification-env/bin/python \
  -r research-20261002-convexification/requirements.txt
```

For an OSiL model, replace `path/to/model.osil` with its path:

```sh
/tmp/joint-convexification-env/bin/python \
  research-20261002-convexification/solver/run.py \
  path/to/model.osil auto --time-limit 30 --output /tmp/joint-cuts.json
```

The other modes are `baseline`, `control`, and `all`. Use `--no-star-merge`
or `--no-sample-cache` for the implemented ablations. The optional
`--build-native-sampler` requires a C compiler and explicitly builds the
sampling library; importing the module does not compile anything.

## Scope beyond this continuation

The implementation uses global cuts at the root node and explicitly bounded
discovery and separation. It does not implement arbitrary overlapping graph
hulls, multivariate elementary blocks, general nonlinear block domains, or a
complete exact MINLP solver. Extending the mathematics to broader classes and
establishing a broad end-to-end runtime advantage remain separate research
questions. The current deliverables make the supported classes, costs,
failure modes, and reusable components concrete and reviewable.
