The [quadratic aggregation package](topics/27-quadratic-aggregation/README.md)
verifies the main certificate equivalence under asymptotic hyperplane
convexity, its HHC specialization, and three supporting lemmas. All 12
obligations are complete in 11 modules, with independent statement reviews,
targeted axiom checks, and kernel replays. The related source note and paper
record the simplified compactness proof and the unverified ancillary scope.

[Topic 28](topics/28-quadratic-aggregation-consequences/README.md) completes
the recommended closed-system, Shor, exact SDP, and boundary-example
extension. Its 10 new modules have independent reviews, a 158-declaration
axiom audit, and successful kernel replays.
[Topic 29](topics/29-infinite-aggregation/README.md) completes the
infinite-aggregation construction: actual HHC for every `r≥2`, exact
spectral goodness, uncountably many indispensable strict rays, and the
finite closed-hull obstruction. Its 18 modules passed the 248-declaration
axiom audit and all kernel replays. Both packages in the
[extension sequence](QUADRATIC-AGGREGATION-EXTENSIONS.md) are complete.

The [recommended-topic sequence](RECOMMENDED-TOPICS-PLAN.md) tracks the new
sequential verification campaign. Its first topic, the
[sharp marginal-floor theorem](topics/12-marginal-floor/README.md), is complete
and verified. [Certified MINLP](topics/14-certified-minlp/README.md) is also
complete, as are [many-leaf reciprocal hulls](topics/13-many-leaf-reciprocal/README.md).
[Flat-chain network–simplex thresholds](topics/15-flat-chain-threshold/README.md)
are complete and independently reviewed, as are
[deterministic potential-flow certificates](topics/16-potential-flow-certificates/README.md),
[arbitrary-grid switching control](topics/17-grid-switching/README.md), and
[positive-box multilinear gaps](topics/18-positive-box/README.md).
[Structural multilinear gaps](topics/19-structural-multilinear/README.md) are
also complete: feedback, frequency-two and incidence-treewidth-two bounds,
including their stated sharpness and box extensions.
[Scalar quadratic precision](topics/20-scalar-quadratic/README.md) is complete,
including sharp constants, rank/inertia laws and explicit finite linear lifts.
[DAG spectral approximation sets](topics/21-dag-spectral/README.md) are complete,
including all 33 frozen claims, independent reviews and targeted checks.
[Represented-matroid spectral approximation sets](topics/22-represented-matroid-spectral/README.md)
are complete: all 37 claims, original-input construction and polynomial
bit work, exact singular ranges, criterion selectors, and explicit subclasses
in 65 modules passed independent reviews and targeted checks.
Topics 00–22 are complete within their listed scopes; topics 23–26 remain
queued. Each verification record separates targeted checks from project-wide CI.

During local work, run targeted checks only. CI handles project-wide
verification; do not run it locally or inspect CI status or logs. Historical
full-project logs below record earlier work, not a current local requirement.

The [focused cubic completion](topics/11-cubic-completion/README.md) adds
thirteen proof modules for the universal `31/12` bound, fixed-mixture
optimality, and the analytic lower bound `1610000/743033`. The
[standalone cubic paper](../paper-cubic-gap/README.md) includes its source map
and exported proofs. That completion brought the canonical project to 160 proof modules.
Its final check status is recorded in the [topic verification record](topics/11-cubic-completion/VERIFICATION.md).

The [topic index](topics/README.md) lists the verification packages and their status.
The [multilinear completion package](topics/10-multilinear-completion/README.md)
adds general envelope attainment and interpretation, exact individual envelopes,
original-box gap comparisons, construction counts, actual family asymptotics,
and kernel-checked printed examples. Its
[coverage guide](topics/10-multilinear-completion/COVERAGE.md) and
[verification record](topics/10-multilinear-completion/VERIFICATION.md) describe
the seven new modules and the updated standalone distribution: 147 canonical
proof modules at this stage and 48 in the standalone dependency closure.

The [standalone multilinear bundle](../paper-multilinear-gap/README.md)
contains a focused paper and a dependency-complete export of the conjecture
disproof, exact dyadic gap, and sharp leading asymptotics. Its
[verification record](../paper-multilinear-gap/formal/VERIFICATION.md)
documents the fresh isolated checks after moving the generic `hullGap`
definition into `CubicGap/Envelope.lean`. The earlier topic manifests identify
their original verification snapshots; they are not regenerated to describe
this later source layout. The proof sources in this directory remain canonical.

The packages use the pinned toolchain and the same allowed-axiom policy;
each verification record identifies the checks actually performed at that stage.
Certified MINLP has a separate [formal project](../paper-certified-minlp/formal/README.md).
The six additional topics were completed sequentially: switching control, FBBT,
potential-flow certificates, cubic gaps, reciprocal-anchor hulls, and
network–simplex hulls. Each numbered topic folder contains an explanation,
claim-to-theorem coverage table, verification log, and source fingerprints.
The [project verification record](VERIFICATION.md) records the original 106
proof modules and the subsequent nine-module
[positive multilinear disproof](topics/07-multilinear-disproof/README.md).
That extension proves unbounded term-by-term/convex-hull gap ratios, beyond
the finite cubic witnesses. Its coverage does not include the sharp
degree/dimension asymptotics or the exact dyadic hull-gap formula.

The subsequent [exact multilinear package](topics/08-exact-multilinear/README.md)
proves the finite hull-gap formula with an attaining law. The
[sharp multilinear package](topics/09-sharp-multilinear/README.md) proves
both degree and dimension asymptotics with leading constant one, over all
finite nonnegative boxes. These added 25 proof modules, for 140 at that stage.

The original package formalizes the exact convex box-count theorem from
[the manuscript](../paper-integer-dimension/sections/04-vector.tex)
(`thm:exact-box-gap`) and its
[supporting proof](../results/convex-polynomial-box-error-exact-integer-gap.md).

For the map on `[0,1]^n`

```
F_n(x) = ((7/4)(1-x_i)^32, (7/4)x_i^32) for i = 1,...,n,
```

with unit componentwise vertical error, the minimum number of general
integer coordinates is `n`, and the minimum number of binary coordinates is
`ceil(n log_2 3)`. Both minima are attained by finite rational linear
formulations. The proofs hold for every natural dimension, including zero.

The main declaration is
[`ExactCounts.exact_box_counts`](Formal/ExactBoxCounts.lean).
It combines the two lower bounds, rational upper constructions, the exact
logarithmic formula, and a general-integer formulation with `3n` continuous
auxiliaries and `13n` inequalities. The polynomial components have rational
coefficients, exact degree 32, and are convex on the unit interval. Requiring
the lifted convex sets to be closed leaves both minima unchanged.

**Representation and scope.**

[`Model.lean`](Formal/Model.lean) defines the visible coordinates, original
graph, unit-error condition, and integer/binary lift models. A lift may use
any finite number of continuous auxiliary coordinates and any convex set;
general integer coordinates are unbounded. Admissibility requires both that
every original graph point has a witness and that every admitted integer
slice stays inside the input cube and the prescribed error tube.

`HasBinaryLift` permits arbitrary convex binary lifts, matching the broader
definition in the supporting note. The manuscript reserves its binary
minimum for polyhedral lifts. Our lower bound applies to the larger class,
and our upper construction is a rational polyhedron, so both conventions
give the stated count. Minima are expressed by `IsLeast`, which proves
attainment as well as optimality.

[`RationalPolyhedron.lean`](Formal/RationalPolyhedron.lean) uses a finite
syntax of rational constants, coordinates, addition, and rational scaling.
Its feasible sets are finite systems of affine inequalities. This makes the
rational MILP claim explicit, without assuming a polyhedral representation
theorem or trusting an external optimization solver.

Our upper construction retains three weights per input coordinate and bounds
the visible coordinates by weighted box endpoints. It proves graph coverage
and validity directly. This is a smaller formulation than the proof note's
vertex-weight construction. The verified size is a count of variables and
inequalities, not a bound on serialized bit length. The binary construction
has `3^n` continuous weights and `3^n + 6n + 2p + 2` inequalities for any
binary budget `p` with `3^n ≤ 2^p`; its continuous size can be exponential.

The [coverage record](COVERAGE.md) maps each obligation to its Lean proof.
This project covers the exact-count theorem and listed supporting claims.
The [exact-count completion](topics/00-exact-counts/README.md) also verifies the
monotone affine shear, strict slice errors, fixed numerical data, and the
quantitative linear gap. It does not formalize the entire integer-dimension
manuscript or claims of novelty and publication priority. No external solver or finite sample check is used as
evidence for a universally quantified conclusion.

**Reproduce verification.**

Install Elan, Git, and Python 3, then run from this directory:

```bash
lake exe cache get
bash scripts/verify.sh
```

Elan reads the pinned Lean version from `lean-toolchain`. Mathlib is pinned
to release `v4.33.1`, with exact dependency revisions in
`lake-manifest.json`. Keep these files in version control; updating them is
a deliberate dependency change. Downloaded dependencies and build artifacts
are excluded by `.gitignore`.

The verification script checks that every proof module is imported, builds
with warnings treated as failures, audits every declaration owned by a
project module, including private declarations and every topic namespace, and replays the compiled project declarations
through Lean's kernel with the bundled `leanchecker`. It uses one replay
worker to bound memory consumption when importing mathlib. The replay uses
the installed Lean kernel; it is a second checking pass, not a separately
implemented proof assistant. It treats imported mathlib declarations as the
dependency base rather than replaying all of mathlib from scratch.

The axiom audit permits only `propext`, `Classical.choice`, and `Quot.sound`.
It rejects unfinished proofs, custom assumptions, and native-computation
axioms transitively, including dependencies imported by project theorems.
Private auxiliaries are audited directly, as well as through their users.
Mathematical meaning still rests on the documented definitions and the
review connecting them to the manuscript.

The [GitHub workflow](../.github/workflows/lean.yml) runs the same build,
axiom, import-coverage, and kernel-replay checks on relevant changes. It
requires only read access and does not publish documents.

**Work on the proofs.**

Open this directory in VS Code through WSL and use the official Lean 4
extension. The Lean Infoview shows the remaining goals. For a single file,
use `lake env lean Formal/Scalar.lean`; for the complete project use the
verification script. Add each new proof module to `Formal.lean` so the
coverage check includes it.

`noncomputable` definitions use ordinary real-number mathematics and
classical choices. Their logical proofs are kernel-checked; the keyword
does not admit a theorem or add an axiom. The Mathlib lint set is enabled
except for its repository-specific copyright/license-header requirement.

See [VERIFICATION.md](VERIFICATION.md) for the recorded local verification.

[Topic 30](topics/30-infinite-aggregation-hull/README.md) verifies the exact
ordinary and closed hulls of the infinite-aggregation example, actual
PD/PSD lifts, and equality with the hull of its weak system. A direct
two-point proof includes `r=2`; ten new modules and 93 audited declarations
passed all targeted checks. [Topic 31](topics/31-aggregation-accuracy/README.md)
also completes the accuracy bounds, exact rational construction and
coefficient-size results: fifteen modules, 232 audited declarations, and
all kernel replays passed.
