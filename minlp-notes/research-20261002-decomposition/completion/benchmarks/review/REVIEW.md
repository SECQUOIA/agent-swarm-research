# Independent benchmark review

The review covers the phase-two corpus, exact reference algorithms, runner,
resource accounting, and public-input fidelity. It does not constitute a
project-wide check or a solver performance claim.

## Input and reference checks

`check_inputs.py` compares every polynomial coefficient parsed from each retained
QPLIB file with its separate GAMS representation. Both complete models pass:
3852 has 231 variables and 440 quadratic terms; 5881 has 120 variables and 2,123
quadratic terms. The binary domains and objective sign conversion agree. The
retained `.qplib`, `.gms`, and `.sol` bytes match the archived phase-one inputs.
The input hashes and results are saved in `input-audit.json`.

The metadata hash matches `continuous_input_audit.json`. The metadata contains
exactly the three screened continuous bound-only cases. These are screening
refusals, not benchmark failures or solver executions.

The small-box reference oracle is mathematically sound on its stated compact
box domain: a quadratic minimum in a singular stationary face can move in a
null direction at constant objective to a smaller face. Thus some minimizing
face has a nonsingular free Hessian, or is a vertex. Enumerating all faces and
integer assignments therefore includes a minimizer. The review directly checked
all 15 saved box-reference witnesses for rational feasibility and exact objective
value.

The constrained reference oracle uses the corresponding KKT argument for each
integer assignment. A minimum-dimensional minimizing face has a nonsingular KKT
system after independent active rows are chosen. The corpus equality rows are
independent, and enumeration includes all independent completions by active
inequalities. All seven references regenerated unchanged. The narrow oracle now
explicitly rejects dependent equality rows, following a review finding; it does
not report such inputs as infeasible.

## Findings resolved during implementation

- The protocol originally described a five-second solver budget and proof replay
  inside the solving worker. It now describes the actual two-second cooperative
  solver budget and separate five-second solver and checker subprocess limits.
- The runner originally passed optimal-set result wrappers directly to a verifier
  expecting their inner certificate. It now unwraps certified results and retains
  inconclusive outcomes without inventing a proof. Exact rational verifier outputs
  are serialized explicitly as strings.
- Optimal-set minimum values now receive the same independent objective and exact
  reference comparison as lower/upper-bound certificates. Membership examples
  additionally exercise the set description.
- Per-run source watches now include the shared archived corpus module, original
  QPLIB inputs, and reference JSON files, as well as the lane-specific code.

The baseline run predates these harness fixes. Its actual contemporaneous runner
and corpus snapshots are retained separately; its solver/checker code is unchanged.
All 16 baseline certificate models were independently compared with the original
corpus and archived minimum-degree decomposition; all match. The contemporaneous
harness snapshots also match the original run-manifest hashes.

## Saved artifact checks

`check_artifacts.py` checks final aggregate rows against their individual result
files, compressed certificate sizes, exact input-model coefficients and domains,
attaining points, reference enclosures, time sums, and the actual source snapshots.
It reads retained proof-replay outcomes and keeps partial-bound replays separate
from successful solves. It does not rerun experiments or count archived pilots.

At this review stage, the baseline, completed-grid, exact-output, and optimal-set
lanes contain 46 configurations and 46 valid retained replays. Of these, 38 finish
the requested solve; eight retain a checked enclosure at a time or table limit.
All 32 available exact-reference enclosures pass. All nine exact-output requests
finish with zero gap, and all five optimal-set requests produce checked set
descriptions. Source hashes match the snapshots that actually ran, including
the reference snapshots retained before later corpus extensions.

The completed constrained lane adds 16 configurations: seven meet the requested
additive gap, five prove an exact value, one proves infeasibility, two retain
checked partial bounds, and one rejects an invalid TU input. Every returned
point was also checked directly against the original linear rows and native
labels. This brings the audited total to 62 configurations, 61 valid replays,
51 completed solves, and 46 exact-reference enclosures. The new disconnected-set
reference and both piecewise recourse references were regenerated independently.

The final recourse lane adds 11 configurations, all with valid replays: six exact
values, four certified approximations, and one QPLIB table-limit enclosure. The
earlier recourse snapshot was retained in its archive and excluded after a
reviewed preprocessing improvement.

**The final main suite contains 73 configurations, 72 valid proof replays,
61 completed solves, 54 exact-reference enclosures, and 29 certified exact
values.** One configuration correctly rejects invalid TU input. Every reported
approximation reaches gap at most `1/1024`; resource-limit enclosures are counted
separately. All reported totals match an independent recount of the raw rows.
The complete machine-readable audit is in `artifact-audit.json`.

The piecewise convex recourse examples at scales 1 and 100 both use 17 table
states, six completed levels, and seven local QP queries, with certified gap
`27/65536`. Their local QP face counts are seven and twelve respectively; the
evidence establishes the stated equal grid/query counts, not identical total
oracle work. The two independent optimum references are `-17/32` and `-809/1616`.

`reproduce.py` and `summarize.py` were also inspected: they restore
the lane's actual archived inputs and sources, exclude archived pilots, and
derive missing constrained gap fields from the exact bounds.

Measured runtime dependencies agree with the current implementation for the
completed lanes. The sole difference inspected was a later `solve_exact`
docstring expansion; it changed no executable statements.

No unresolved correctness or reporting finding remains in this main-suite
review. The separate `extensions/` suite has its own independent audit and is
excluded from the 73-run totals above.

## Targeted commands run

```
python research-20261002-decomposition/completion/benchmarks/review/check_inputs.py
python research-20261002-decomposition/completion/benchmarks/review/check_artifacts.py
```

Passed. A separate narrow Python check validated the 15 box-reference witnesses,
regenerated the seven constrained references, and confirmed rejection of a
duplicated equality row. No project-wide checks or CI inspection were performed.
